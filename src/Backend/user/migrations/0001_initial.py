# Generated by Django 3.1.3 on 2023-01-17 11:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(blank=True, error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, null=True, unique=True, verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('gender', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], max_length=1, null=True)),
                ('usr_email', models.EmailField(blank=True, max_length=254, null=True, unique=True, verbose_name='email address')),
                ('usr_profile_pic', models.ImageField(blank=True, null=True, upload_to='uploads/user/images/')),
                ('user_type', models.IntegerField(choices=[(0, 'SUPER_USER'), (1, 'NORMAL_USER'), (2, 'ADMIN')], default=1, verbose_name='user type')),
                ('is_deleted', models.BooleanField(default=False, help_text='Designates whether this user is deleted', verbose_name='deleted')),
                ('is_verify', models.BooleanField(default=True, help_text='Designates whether this user is verified', verbose_name='verify')),
                ('is_notification', models.BooleanField(default=False, help_text='User get Notification using Apps', verbose_name='notification')),
                ('is_message', models.BooleanField(default=False, help_text='User get mobile SMS', verbose_name='message')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(auto_now=True, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'db_table': 'auth_user',
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(blank=True, max_length=200, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_company', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserCompanyManager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_primary_phone', models.BooleanField(default=True, help_text='User get phone number', verbose_name='is primary number')),
                ('phn_cell', models.CharField(blank=True, max_length=50, null=True, unique=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_manager', to='user.company')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_manager', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
