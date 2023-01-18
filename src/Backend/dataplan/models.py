from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
# Create your models here.
from user.managers import UserManager
from django.db.models.signals import post_save
from django.dispatch import receiver


class DataPlan(models.Model):
    plan_name = models.CharField(max_length=100, blank=True, null=True, unique=True)
    duration_in_month = models.IntegerField(default=0, blank=True, null=True)
    plan_amt = models.DecimalField(
        max_digits=50, decimal_places=2, blank=True, null=True)
    is_cancel_able = models.BooleanField(
        _('is cancleable data plan'), default=False, help_text=_('Is the data plan cancleable'))

    def __str__(self):
        return self.plan_name


class Purches(models.Model):
    user = models.ForeignKey(
        'user.User', related_name='user_data', on_delete=models.CASCADE)
    company = models.ForeignKey(
        'user.Company', related_name='company_data', on_delete=models.CASCADE)
    data_plan = models.ForeignKey(
        'dataplan.DataPlan', related_name='data_plan', on_delete=models.CASCADE)
    data_plan_started = models.DateTimeField(auto_now_add=True)
    data_plan_ended = models.DateTimeField(blank=True, null=True)
    active_plan = models.BooleanField(
        _('active plan'), default=False, help_text=_('active plan')
    )
