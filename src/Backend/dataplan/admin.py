from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from django.contrib import admin

from user.forms import UserChangeForm, UserCreationForm
from dataplan.models import *
# Register your models here.


class DataPlanAdmin(admin.ModelAdmin):
    list_display = [
        'plan_name',
        'duration_in_month',
        'plan_amt',
        'is_cancel_able',
    ]


admin.site.register(DataPlan, DataPlanAdmin)


class PurchesAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'company',
        'data_plan',
        'data_plan_started',
        'data_plan_ended',
        'active_plan',
    ]


admin.site.register(Purches, PurchesAdmin)
