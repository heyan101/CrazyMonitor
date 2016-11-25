# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-25 10:06
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('interval', models.IntegerField(default=300, verbose_name='\u544a\u8b66\u95f4\u9694(s)')),
                ('recover_notice', models.BooleanField(default=True, verbose_name='\u6545\u969c\u6062\u590d\u540e\u53d1\u9001\u901a\u77e5\u6d88\u606f')),
                ('recover_subject', models.CharField(blank=True, max_length=128, null=True, verbose_name='\u6807\u9898')),
                ('recover_message', models.TextField(blank=True, null=True, verbose_name='\u6b63\u6587')),
                ('enabled', models.BooleanField(default=True, verbose_name='\u542f\u7528\u62a5\u8b66')),
            ],
        ),
        migrations.CreateModel(
            name='ActionOperation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('step', models.SmallIntegerField(default=1, verbose_name='\u7b2cn\u6b21\u544a\u8b66')),
                ('action_type', models.CharField(choices=[(b'email', b'Email'), (b'sms', b'SMS'), (b'script', b'RunScript')], default=b'email', max_length=64, verbose_name='\u52a8\u4f5c\u7c7b\u578b')),
                ('msg_format', models.TextField(default=b'Host({hostname},{ip}) service({service_name}) has issue,msg:{msg}', verbose_name='\u6d88\u606f\u683c\u5f0f')),
            ],
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('ip_addr', models.GenericIPAddressField(unique=True)),
                ('monitored_by', models.CharField(choices=[(b'agent', b'Agent'), (b'snmp', b'SNMP'), (b'wget', b'WGET')], max_length=64, verbose_name='\u76d1\u63a7\u65b9\u5f0f')),
                ('host_alive_check_interval', models.IntegerField(default=30, verbose_name='\u4e3b\u673a\u5b58\u6d3b\u72b6\u6001\u76d1\u6d4b\u95f4\u9694')),
                ('status', models.IntegerField(choices=[(1, b'Onlice'), (2, b'Down'), (3, b'Unreachable'), (4, b'Offline'), (5, b'Problem')], default=1, verbose_name='\u72b6\u6001')),
                ('memo', models.TextField(blank=True, null=True, verbose_name='\u5907\u6ce8')),
            ],
        ),
        migrations.CreateModel(
            name='HostGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('memo', models.TextField(blank=True, null=True, verbose_name='\u5907\u6ce8')),
            ],
        ),
        migrations.CreateModel(
            name='Maintenance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('content', models.TextField(verbose_name='\u7ef4\u62a4\u5185\u5bb9')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('host_groups', models.ManyToManyField(blank=True, to='monitor.HostGroup')),
                ('hosts', models.ManyToManyField(blank=True, to='monitor.Host')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='\u670d\u52a1\u540d\u79f0')),
                ('interval', models.IntegerField(default=60, verbose_name='\u76d1\u63a7\u95f4\u9694')),
                ('plugin_name', models.CharField(default=b'n/a', max_length=64, verbose_name='\u63d2\u4ef6\u540d')),
                ('has_sub_service', models.BooleanField(default=False, help_text='\u5982\u679c\u4e00\u4e2a\u670d\u52a1\u8fd8\u6709\u72ec\u7acb\u7684\u5b50\u670d\u52a1 ,\u9009\u62e9\u8fd9\u4e2a,\u6bd4\u5982 \u7f51\u5361\u670d\u52a1\u6709\u591a\u4e2a\u72ec\u7acb\u7684\u5b50\u7f51\u5361')),
                ('memo', models.CharField(blank=True, max_length=128, null=True, verbose_name='\u5907\u6ce8')),
            ],
        ),
        migrations.CreateModel(
            name='ServiceIndex',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('key', models.CharField(max_length=64)),
                ('data_type', models.CharField(choices=[(b'int', b'int'), (b'float', b'float'), (b'str', b'string')], default=b'int', max_length=32, verbose_name='\u6307\u6807\u6570\u636e\u7c7b\u578b')),
                ('memo', models.CharField(blank=True, max_length=128, null=True, verbose_name='\u5907\u6ce8')),
            ],
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='\u6a21\u7248\u540d\u79f0')),
                ('services', models.ManyToManyField(blank=True, to='monitor.Service', verbose_name='\u670d\u52a1\u5217\u8868')),
            ],
        ),
        migrations.CreateModel(
            name='Trigger',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='\u89e6\u53d1\u5668\u540d\u79f0')),
                ('severity', models.IntegerField(choices=[(1, b'Information'), (2, b'Warning'), (3, b'Average'), (4, b'High'), (5, b'Diaster')], verbose_name='\u544a\u8b66\u7ea7\u522b')),
                ('enabled', models.BooleanField(default=True)),
                ('memo', models.TextField(blank=True, null=True, verbose_name='\u5907\u6ce8')),
            ],
        ),
        migrations.CreateModel(
            name='TriggerExpression',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('specified_index_key', models.CharField(blank=True, max_length=64, null=True, verbose_name='\u53ea\u76d1\u63a7\u4e13\u95e8\u6307\u5b9a\u7684\u6307\u6807key')),
                ('operator_type', models.CharField(choices=[(b'eq', b'='), (b'lt', b'<'), (b'gt', b'>')], max_length=32, verbose_name='\u8fd0\u7b97\u7b26')),
                ('data_calc_func', models.CharField(choices=[(b'avg', b'Average'), (b'max', b'Max'), (b'hit', b'Hit'), (b'last', b'Last')], max_length=64, verbose_name='\u6570\u636e\u5904\u7406\u65b9\u5f0f')),
                ('data_calc_args', models.CharField(help_text='\u82e5\u662f\u591a\u4e2a\u53c2\u6570,\u5219\u7528,\u53f7\u5206\u5f00,\u7b2c\u4e00\u4e2a\u503c\u662f\u65f6\u95f4', max_length=64, verbose_name='\u51fd\u6570\u4f20\u5165\u53c2\u6570')),
                ('threshold', models.IntegerField(verbose_name='\u9608\u503c')),
                ('logic_type', models.CharField(blank=True, choices=[(b'or', b'OR'), (b'and', b'AND')], max_length=32, null=True, verbose_name='\u4e0e\u4e00\u4e2a\u6761\u4ef6\u7684\u903b\u8f91\u5173\u7cfb')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitor.Service', verbose_name='\u5173\u8054\u670d\u52a1')),
                ('service_index', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitor.ServiceIndex', verbose_name='\u5173\u8054\u670d\u52a1\u6307\u6807')),
                ('trigger', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitor.Trigger', verbose_name='\u6240\u5c5e\u89e6\u53d1\u5668')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('phone', models.BigIntegerField(blank=True, null=True)),
                ('weixin', models.CharField(blank=True, max_length=64, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='template',
            name='triggers',
            field=models.ManyToManyField(blank=True, to='monitor.Trigger', verbose_name='\u89e6\u53d1\u5668\u5217\u8868'),
        ),
        migrations.AddField(
            model_name='service',
            name='items',
            field=models.ManyToManyField(blank=True, to='monitor.ServiceIndex', verbose_name='\u6307\u6807\u5217\u8868'),
        ),
        migrations.AddField(
            model_name='hostgroup',
            name='templates',
            field=models.ManyToManyField(blank=True, to='monitor.Template'),
        ),
        migrations.AddField(
            model_name='host',
            name='host_groups',
            field=models.ManyToManyField(blank=True, to='monitor.HostGroup'),
        ),
        migrations.AddField(
            model_name='host',
            name='templates',
            field=models.ManyToManyField(blank=True, to='monitor.Template'),
        ),
        migrations.AddField(
            model_name='actionoperation',
            name='notifiers',
            field=models.ManyToManyField(blank=True, to='monitor.UserProfile', verbose_name='\u901a\u77e5\u5bf9\u8c61'),
        ),
        migrations.AddField(
            model_name='action',
            name='host_groups',
            field=models.ManyToManyField(blank=True, to='monitor.HostGroup'),
        ),
        migrations.AddField(
            model_name='action',
            name='hosts',
            field=models.ManyToManyField(blank=True, to='monitor.Host'),
        ),
        migrations.AddField(
            model_name='action',
            name='operations',
            field=models.ManyToManyField(to='monitor.ActionOperation'),
        ),
        migrations.AddField(
            model_name='action',
            name='triggers',
            field=models.ManyToManyField(blank=True, help_text='\u60f3\u8ba9\u54ea\u4e9btrigger\u89e6\u53d1\u5f53\u524d\u62a5\u8b66\u52a8\u4f5c', to='monitor.Trigger'),
        ),
    ]
