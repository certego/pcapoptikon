#!/usr/bin/env python
#
# models.py
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA  02111-1307  USA
#
# Author:   Pietro Delsante <p.delsante@certego.net>
#           www.certego.net
#
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
    user                    = models.ForeignKey(User, null=True, blank=True, default=None)
    status                  = models.IntegerField('Task status', default=STATUS_NEW, null=False, blank=True, choices=STATUS_CHOICES)
    results_dir             = models.CharField('Temporary results dir', max_length=512, blank=True, null=True, default=None)
    results                 = jsonfield.JSONField('Results', null=True, blank=True, default=None)
