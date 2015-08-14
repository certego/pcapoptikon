import collections
import jsonfield
import pytz
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from tastypie.models import create_api_key


models.signals.post_save.connect(create_api_key, sender=User)

# add_now() is used to create auto datetime fields with the correct timezone
def add_now():
    return datetime.now(pytz.timezone(settings.TIME_ZONE))

class Task(models.Model):
    STATUS_FAILED       = -1    # Failed
    STATUS_NEW          =  0    # In queue
    STATUS_PROCESSING   =  1    # Processing
    STATUS_QUEUED       =  2    # Processing
    STATUS_DONE         =  3    # No further action required (completed or discarded)

    STATUS_CHOICES = (
        (STATUS_FAILED,     'Failed'),
        (STATUS_NEW,        'In queue'),
        (STATUS_PROCESSING, 'Processing'),
        (STATUS_QUEUED,     'Queued'),
        (STATUS_DONE,       'No further action required (completed or discarded)'),
    )

    pcap_file               = models.FileField('PCAP File', upload_to='extracted_files', max_length=512, blank=False, null=False)
    submitted_on            = models.DateTimeField('Added on', default=add_now, null=False, blank=True)
    user                    = models.ForeignKey(User)
    status                  = models.IntegerField('Task status', default=STATUS_NEW, null=False, blank=True, choices=STATUS_CHOICES)
    results_dir             = models.CharField('Temporary results dir', max_length=512, blank=True, null=True, default=None)
    results                 = jsonfield.JSONField('Results', null=True, blank=True, default=None)
