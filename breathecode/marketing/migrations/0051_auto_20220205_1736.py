# Generated by Django 3.2.9 on 2022-02-05 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketing', '0050_alter_tag_tag_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='disputed_at',
            field=models.DateTimeField(
                blank=True,
                default=None,
                help_text=
                'Disputed tags get deleted after 10 days unless its used in 1+ automations or has 1+ subscriber',
                null=True),
        ),
        migrations.AddField(
            model_name='tag',
            name='disputed_reason',
            field=models.TextField(blank=True,
                                   default=None,
                                   help_text='Explain why you think the tag should be deleted',
                                   null=True),
        ),
    ]