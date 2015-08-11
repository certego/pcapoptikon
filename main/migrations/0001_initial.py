# -*- coding: utf-8 -*-
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
