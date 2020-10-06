# Generated by Django 3.1.1 on 2020-10-05 22:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admissions', '0011_auto_20201005_2253'),
        ('events', '0004_auto_20200806_0042'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('feedback', '0003_auto_20200806_0417'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='entity_id',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='entity_slug',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='entity_type',
        ),
        migrations.AddField(
            model_name='answer',
            name='academy',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='admissions.academy'),
        ),
        migrations.AddField(
            model_name='answer',
            name='cohort',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='admissions.cohort'),
        ),
        migrations.AddField(
            model_name='answer',
            name='event',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='events.event'),
        ),
        migrations.AddField(
            model_name='answer',
            name='mentor',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mentor_set', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='answer',
            name='user',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
