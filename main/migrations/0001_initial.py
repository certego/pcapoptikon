# -*- coding: utf-8 -*-
#
# 0001_initial.py
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
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import main.models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pcap_file', models.FileField(upload_to=b'extracted_files', max_length=512, verbose_name=b'PCAP File')),
                ('submitted_on', models.DateTimeField(default=main.models.add_now, verbose_name=b'Added on', blank=True)),
                ('status', models.IntegerField(default=0, blank=True, verbose_name=b'Task status', choices=[(-1, b'Failed'), (0, b'In queue'), (1, b'Processing'), (2, b'Queued'), (3, b'No further action required (completed or discarded)')])),
                ('results_dir', models.CharField(default=None, max_length=512, null=True, verbose_name=b'Temporary results dir', blank=True)),
                ('results', jsonfield.fields.JSONField(default=None, null=True, verbose_name=b'Results', blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
