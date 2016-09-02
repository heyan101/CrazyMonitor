# coding:utf8

from django.contrib.auth.models import User
from django.db import models


class Host(models.Model):
    """
    主机
    """
    name = models.CharField(max_length=64, unique=True)
    ip_addr = models.GenericIPAddressField(unique=True)
    host_groups = models.ManyToManyField('HostGroup', blank=True)
    templates = models.ManyToManyField('Template', blank=True)
    monitored_by_choices = (
        ('agent', 'Agent'),
        ('snmp', 'SNMP'),
        ('wget', 'WGET'),
    )
    monitored_by = models.CharField(u'监控方式', max_length=64, choices=monitored_by_choices)
    host_alive_check_interval = models.IntegerField(u'主机存活状态监测间隔', default=30)
    status_choices = (
        (1, 'Onlice'),
        (2, 'Down'),
        (3, 'Unreachable'),
        (4, 'Offline'),
        (5, 'Problem'),
    )
    status = models.IntegerField(u'状态', choices=status_choices, default=1)
    memo = models.TextField(u"备注", blank=True, null=True)

    def __unicode__(self):
        return self.name


class HostGroup(models.Model):
    """
    主机群
    """
    name = models.CharField(max_length=64, unique=True)
    templates = models.ManyToManyField('Template', blank=True)
    memo = models.TextField(u'备注', blank=True, null=True)

    def __unicode__(self):
        return self.name


class Service(models.Model):
    """
    服务
    """
    name = models.CharField(u'服务名称', max_length=64, unique=True)
    interval = models.IntegerField(u'监控间隔', default=60)
    plugin_name = models.CharField(u'插件名', max_length=64, default='n/a')
    items = models.ManyToManyField('ServiceIndex', verbose_name=u'指标列表', blank=True)
    # 如果一个服务还有独立的子服务 ,选择这个,比如 网卡服务有多个独立的子网卡
    has_sub_service = models.BooleanField(default=False, help_text=u'如果一个服务还有独立的子服务 ,选择这个,比如'
                                                                   u' 网卡服务有多个独立的子网卡')
    memo = models.CharField(u'备注', max_length=128, blank=True, null=True)

    def __unicode__(self):
        return self.name
        # def get_service_items(obj):
        #    return ",".join([i.name for i in obj.items.all()])


class ServiceIndex(models.Model):
    """
    服务指标
    """
    name = models.CharField(max_length=64)
    key = models.CharField(max_length=64)
    data_type_choices = (
        ('int', "int"),
        ('float', "float"),
        ('str', "string")
    )
    data_type = models.CharField(u'指标数据类型', max_length=32, choices=data_type_choices, default='int')
    memo = models.CharField(u'备注', max_length=128, blank=True, null=True)

    def __unicode__(self):
        return "%s.%s" % (self.name, self.key)


class Template(models.Model):
    """
    模板
    """
    name = models.CharField(u'模版名称', max_length=64, unique=True)
    services = models.ManyToManyField('Service', verbose_name=u'服务列表', blank=True)
    triggers = models.ManyToManyField('Trigger', verbose_name=u'触发器列表', blank=True)

    def __unicode__(self):
        return self.name


class Trigger(models.Model):
    """
    触发器
    触发器和触发器的触发条件做了一个反向关联，一般的思路应该是一个触发器有多个触发条件，但是如果这样的话，当有多个触发器共用一
    个触发器条件，修改触发器触发条件，会产生不确定性结果，所以我们采用反向关联，一个触发器条件对应一个触发器
    """
    name = models.CharField(u'触发器名称', max_length=64)
    severity_choices = (
        (1, 'Information'),
        (2, 'Warning'),
        (3, 'Average'),
        (4, 'High'),
        (5, 'Diaster'),
    )
    # expressions = models.ManyToManyField(TriggerExpression,verbose_name=u"条件表达式")
    severity = models.IntegerField(u'告警级别', choices=severity_choices)
    enabled = models.BooleanField(default=True)
    memo = models.TextField(u"备注", blank=True, null=True)

    def __unicode__(self):
        return '<service:%s, severity:%s>' % (self.name, self.get_severity_display())


class TriggerExpression(models.Model):
    """
    触发条件
    """
    trigger = models.ForeignKey('Trigger', verbose_name=u"所属触发器")
    service = models.ForeignKey('Service', verbose_name=u"关联服务")
    service_index = models.ForeignKey(ServiceIndex, verbose_name=u"关联服务指标")
    specified_index_key = models.CharField(verbose_name=u"只监控专门指定的指标key", max_length=64, blank=True, null=True)
    operator_type_choices = (('eq', '='), ('lt', '<'), ('gt', '>'))
    operator_type = models.CharField(u"运算符", choices=operator_type_choices, max_length=32)
    data_calc_type_choices = (
        ('avg', 'Average'),
        ('max', 'Max'),
        ('hit', 'Hit'),
        ('last', 'Last'),
    )
    data_calc_func = models.CharField(u"数据处理方式", choices=data_calc_type_choices, max_length=64)
    data_calc_args = models.CharField(u"函数传入参数", help_text=u"若是多个参数,则用,号分开,第一个值是时间", max_length=64)
    threshold = models.IntegerField(u"阈值")
    logic_type_choices = (('or', 'OR'), ('and', 'AND'))
    logic_type = models.CharField(u"与一个条件的逻辑关系", choices=logic_type_choices, max_length=32, blank=True, null=True)

    def __unicode__(self):
        return "%s %s(%s(%s))" % (self.service_index, self.operator_type, self.data_calc_func, self.data_calc_args)

    # 将一个普通类转为抽象类的方法，这里暂时没有使用
    class Meta:
        pass
        # unique_together = ('trigger_id','service')


class Action(models.Model):
    """
    报警开关
    """
    name = models.CharField(max_length=64, unique=True)
    host_groups = models.ManyToManyField('HostGroup', blank=True)
    hosts = models.ManyToManyField('Host', blank=True)
    triggers = models.ManyToManyField('Trigger', blank=True, help_text=u"想让哪些trigger触发当前报警动作")
    interval = models.IntegerField(u'告警间隔(s)', default=300)
    operations = models.ManyToManyField('ActionOperation')

    recover_notice = models.BooleanField(u'故障恢复后发送通知消息', default=True)
    recover_subject = models.CharField(u'标题', max_length=128, blank=True, null=True)
    recover_message = models.TextField(u'正文', blank=True, null=True)

    enabled = models.BooleanField(u'启用报警', default=True)

    def __unicode__(self):
        return self.name


class ActionOperation(models.Model):
    """
    报警设置
    """
    name = models.CharField(max_length=64)
    step = models.SmallIntegerField(u"第n次告警", default=1)
    action_type_choices = (
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('script', 'RunScript'),
    )
    action_type = models.CharField(u"动作类型", choices=action_type_choices, default='email', max_length=64)
    notifiers = models.ManyToManyField('UserProfile', verbose_name=u"通知对象", blank=True)
    _msg_format = '''Host({hostname},{ip}) service({service_name}) has issue,msg:{msg}'''

    msg_format = models.TextField(u"消息格式", default=_msg_format)

    def __unicode__(self):
        return self.name


class Maintenance(models.Model):
    """
    维护计划，维护的时候可以让它不报警
    """
    name = models.CharField(max_length=64, unique=True)
    hosts = models.ManyToManyField('Host', blank=True)
    host_groups = models.ManyToManyField('HostGroup', blank=True)
    content = models.TextField(u"维护内容")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __unicode__(self):
        return self.name


class UserProfile(models.Model):
    """
    用户信息
    """
    user = models.OneToOneField(User)
    name = models.CharField(max_length=32)
    phone = models.BigIntegerField(blank=True, null=True)
    weixin = models.CharField(max_length=64, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __unicode__(self):
        return self.name


''''
CPU
    idle 80
    usage  90
    system  30
    user
    iowait  50

memory :
    usage
    free
    swap
    cache
    buffer

load:
    load1
    load 5
    load 15
'''
