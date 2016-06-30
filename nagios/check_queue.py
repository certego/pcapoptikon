#!/usr/bin/env python

import argparse
import os
import sys

RET_OK = 0
RET_WARN = 1
RET_CRIT = 2
RET_UNK = 3

sys.path.append(os.path.realpath(os.path.join(
    os.path.dirname(__file__),
    '..'
)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pcapoptikon.settings")

from main.models import Task


help_all = (
    "Check status of PCAPOptikon queues (new, processing and queued)"
)

help_crit = (
    "Critical threshold. If you specify a single integer, it will be applied "
    "to all three queues; else, just specify three comma-separated integers "
    "in this order: -c new,processing,queued"
)

help_warn = (
    "Warning threshold. If you specify a single integer, it will be applied "
    "to all three queues; else, just specify three comma-separated integers "
    "in this order: -w new,processing,queued"
)


def parse_thresholds(val):
    try:
        if "," not in val:
            t = int(val)
            return (t, t, t)
        else:
            toks = val.split(',', 2)
            return (int(toks[0]), int(toks[1]), int(toks[2]))
    except:
        print(
            "Wrong argument: thresholds should be either a single integer "
            "or three comma-separated integers"
        )
        sys.exit(RET_UNK)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(help_all)
    parser.add_argument(
        '-c',
        type=str,
        required=True,
        help=help_crit
    )
    parser.add_argument(
        '-w',
        type=str,
        required=True,
        help=help_warn
    )

    args = parser.parse_args()

    crit_thresholds = parse_thresholds(args.c)
    warn_thresholds = parse_thresholds(args.w)

    new = Task.objects.filter(status=Task.STATUS_NEW).count()
    queued = Task.objects.filter(status=Task.STATUS_QUEUED).count()
    processing = Task.objects.filter(status=Task.STATUS_PROCESSING).count()

    ret = RET_OK
    ret_msg = "OK"
    if (
        new >= crit_thresholds[0] or
        queued >= crit_thresholds[1] or
        processing >= crit_thresholds[2]
    ):
        ret = RET_CRIT
        ret_msg = "CRITICAL"
    elif (
        new >= warn_thresholds[0] or
        queued >= warn_thresholds[1] or
        processing >= warn_thresholds[2]
    ):
        ret = RET_WARN
        ret_msg = "WARNING"

    print(
        "{msg}: {new} new, {queued} queued and {processing} processing | "
        "new={new} queued={queued} processing={processing}".format(
            msg=ret_msg,
            new=new,
            queued=queued,
            processing=processing,
        )
    )
    sys.exit(ret)
