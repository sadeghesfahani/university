# Generated by Django 3.2.6 on 2021-08-28 08:46

import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import university.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth.user')),
                ('personal_id', models.SmallIntegerField(default=university.models.generateStaffPersonalId, unique=True)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth.user')),
                ('student_id', models.SmallIntegerField(default=university.models.generateStudentPersonalId, unique=True)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth.user')),
                ('personal_id', models.SmallIntegerField(default=university.models.generateTeacherPersonalId, unique=True)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='University',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('staff', models.ManyToManyField(to='university.Staff')),
                ('students', models.ManyToManyField(to='university.Student')),
                ('teachers', models.ManyToManyField(to='university.Teacher')),
            ],
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('staff', models.ManyToManyField(to='university.Staff')),
                ('students', models.ManyToManyField(to='university.Student')),
                ('teachers', models.ManyToManyField(to='university.Teacher')),
                ('university', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='faculty', to='university.university')),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course', to='university.faculty')),
                ('students', models.ManyToManyField(to='university.Student')),
                ('teachers', models.ManyToManyField(to='university.Staff')),
            ],
        ),
    ]
