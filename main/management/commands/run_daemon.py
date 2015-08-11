import glob
import logging
import os
import simplejson as json
import threading
import tempfile
import time

from datetime import datetime
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from main.models import *
from suricatasc import *

from idstools.unified2 import FileEventReader
from idstools import maps

log = logging.getLogger(__name__)

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('socket', metavar='socket', nargs='?', help='socket file to connnect to', default=None)

    def handle(self, *args, **options):
        log.info("Starting up pcapoptikon daemon")

        if options.get("socket", None):
            SOCKET_PATH = options["socket"]
        else:
            SOCKET_PATH = "/var/run/suricata/suricata-command.socket"

        # Start the task submitter thread
        ts = TasksSubmitter(SOCKET_PATH)
        ts.start()

        # Start the result retriever thread
        rr = ResultsRetriever(SOCKET_PATH)
        rr.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            log.info("Shutting down on user's request")
            ts.terminate()
            rr.terminate()
            # Join both the children
            ts.join()
            rr.join()

class BaseWorker(threading.Thread):

    def __init__(self, socket_path, group=None, target=None, name=None, args=(), kwargs={}):
        self.running = True
        self.SOCKET_PATH = socket_path
        super(BaseWorker, self).__init__(group=group, target=target, name=name, args=args, kwargs=kwargs)

    def _fetch_new_tasks(self):
        return Task.objects.filter(status__exact=Task.STATUS_NEW).order_by('submitted_on')

    def _fetch_queued_tasks(self):
        return Task.objects.filter(status__exact=Task.STATUS_QUEUED).order_by('submitted_on')

    def _mark_as_new(self, task):
        log.debug("[{}] Marking task as new".format(task.id))
        task.status = Task.STATUS_NEW
        task.save()

    def _mark_as_processing(self, task):
        log.debug("[{}] Marking task as processing".format(task.id))
        task.status = Task.STATUS_PROCESSING
        task.save()

    def _mark_as_queued(self, task):
        log.debug("[{}] Marking task as queued".format(task.id))
        task.status = Task.STATUS_QUEUED
        task.save()

    def _mark_as_failed(self, task):
        log.debug("[{}] Marking task as failed".format(task.id))
        task.status = Task.STATUS_FAILED
        task.save()

    def _mark_as_completed(self, task):
        log.debug("[{}] Marking task as completed".format(task.id))
        task.status = Task.STATUS_DONE
        task.save()

    def _connect(self, sc):
        while self.running:
            log.debug("Attempting connection to socket {}".format(self.SOCKET_PATH))
            try:
                sc.connect()
                return sc
            except SuricataNetException as err:
                log.debug("Unable to connect to socket {}: {}".format(self.SOCKET_PATH, err))
                time.sleep(1)
            except SuricataReturnException as err:
                log.debug("Unable to negotiate version with server: {}".format(err))
                time.sleep(1)
            except Exception as err:
                log.debug("Got error: {}".format(err))
                time.sleep(1)

    def terminate(self):
        self.running = False

class ResultsRetriever(BaseWorker):

    def __init__(self, socket_path, group=None, target=None, name=None, args=(), kwargs={}):
        log.info("Initializing new ResultsRetriever thread")
        super(ResultsRetriever, self).__init__(socket_path, group=group, target=target, name=name, args=args, kwargs=kwargs)

    def run(self):
        while self.running:
            log.debug("Fetching queued tasks")
            tasks = self._fetch_queued_tasks()
            log.debug("Got {} queued tasks".format(len(tasks)))

            for task in tasks:
                try:
                    self.retrieve_results(task)
                except Exception as err:
                    log.exception("[{}] Got exception while retrieving results: {}".format(task.id, err))
                    self._mark_as_failed(task)

            # Sleep when no pending tasks
            log.info("Sleeping for {} seconds waiting for new tasks".format(10))
            time.sleep(10)

    def retrieve_results(self, task):
        if not task.results_dir:
            log.error("[{}] Task was marked as processing but had no results dir")
            self._mark_as_failed(task)

        sc = SuricataSC(self.SOCKET_PATH)
        sc = self._connect(sc)

        res = sc.send_command('pcap-file-list', None)
        sc.close()

        if task.pcap_file.name in res["files"]:
            log.info("[{}] File {} is still queued".format(task.id, task.pcap_file.name))
            return
        else:
            try:
                log_file_pattern = os.path.join(task.results_dir, 'snort.unified2.*')
                log_file = glob.glob(log_file_pattern)[0]
            except IndexError as err:
                log.exception("[{}] Unable to find a log file in {}".format(task.id, log_file_pattern))
                self._mark_as_failed(task)
                return
            except Exception as err:
                log.exception("[{}] Got exception while retrieving results: {}".format(task.id, err))
                self._mark_as_failed(task)
                return

            reader = FileEventReader(log_file)
            events = []
            for event in reader:
                events.append(event)

            task.results = json.dumps(events)
            self._mark_as_completed(task)

class TasksSubmitter(BaseWorker):
    def __init__(self, socket_path, group=None, target=None, name=None, args=(), kwargs={}):
        log.info("Initializing new TasksSubmitter thread")
        super(TasksSubmitter, self).__init__(socket_path, group=group, target=target, name=name, args=args, kwargs=kwargs)

    def run(self):
        while self.running:
            log.debug("Fetching new tasks")
            tasks = self._fetch_new_tasks()
            log.debug("Got {} new tasks".format(len(tasks)))

            for task in tasks:
                self._mark_as_processing(task)
                try:
                    self.submit_task(task)
                except Exception as e:
                    log.exception("[{}] Got CalledProcessError exception: {}".format(task.id, e))
                    self._mark_as_failed(task)

            # Sleep when no pending tasks
            log.info("Sleeping for {} seconds waiting for new tasks".format(10))
            time.sleep(10)

    def submit_task(self, task):
        sc = SuricataSC(self.SOCKET_PATH)
        sc = self._connect(sc)

        file_path = os.path.join(settings.MEDIA_ROOT, task.pcap_file.name)
        output_dir = tempfile.mkdtemp()

        res = sc.send_command('pcap-file', {'filename': file_path, 'output-dir': output_dir})

        if res['return'] == 'OK':
            task.results_dir = output_dir
            self._mark_as_queued(task)
        else:
            self._mark_as_failed(task)
            log.error("Error running task {}: {}".format(task.id, json.dumps(res['message'])))

        sc.close()
