from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
# Create your models here.
from user.managers import UserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from .generate_number import generate_number

is_gender = (
    ('M', 'Male'),
    ('F', 'Female'),
)


class User(AbstractBaseUser, PermissionsMixin):

    class UserType(models.IntegerChoices):
        SUPER_USER = '0', _('SUPER_USER')
        NORMAL_USER = '1', _('NORMAL_USER')
        ADMIN = '2', _('ADMIN')

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_(
            'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        error_messages={
            'unique': _("A user with that username already exists."),
        }, blank=True, null=True
    )
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    gender = models.CharField(
        max_length=1, choices=is_gender, null=True, blank=True)
    usr_email = models.EmailField(
        _('email address'), null=True, blank=True, unique=True)
    usr_profile_pic = models.ImageField(
        upload_to='uploads/user/images/', blank=True, null=True)
    user_type = models.IntegerField(
        _('user type'), choices=UserType.choices, default=UserType.NORMAL_USER)
    is_deleted = models.BooleanField(_('deleted'), default=False, help_text=_(
        'Designates whether this user is deleted'))
    is_verify = models.BooleanField(_('verify'), default=True, help_text=_(
        'Designates whether this user is verified'))
    is_notification = models.BooleanField(
        _('notification'), default=False, help_text=_('User get Notification using Apps'))
    is_message = models.BooleanField(
        _('message'), default=False, help_text=_('User get mobile SMS'))
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'auth_user'
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.username


class Company(models.Model):
    user = models.ForeignKey(
        'user.User', related_name='user_company', on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.company_name


class UserCompanyManager(models.Model):
    user = models.ForeignKey(
        'user.User', related_name='user_manager', on_delete=models.CASCADE)
    company = models.ForeignKey(
        'user.Company', related_name='company_manager', on_delete=models.CASCADE)
    is_primary_phone = models.BooleanField(
        _('is primary number'), default=True, help_text=_('User get phone number'))
    phn_cell = models.CharField(
        max_length=50, blank=True, null=True, unique=True)
