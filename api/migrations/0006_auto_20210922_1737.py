# Generated by Django 3.2.6 on 2021-09-22 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_kubernetesservice_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='kubernetesnode',
            name='cpu_capacity',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AddField(
            model_name='kubernetesnode',
            name='memory_capacity',
            field=models.CharField(default='', max_length=500),
        ),
    ]