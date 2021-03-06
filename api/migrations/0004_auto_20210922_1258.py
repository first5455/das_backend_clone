# Generated by Django 3.2.6 on 2021-09-22 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_kubernetespod_node'),
    ]

    operations = [
        migrations.RenameField(
            model_name='kubernetespod',
            old_name='clusterip',
            new_name='podip',
        ),
        migrations.AddField(
            model_name='kubernetesservice',
            name='clusterip',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AddField(
            model_name='kubernetesservice',
            name='externalip',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AddField(
            model_name='kubernetesservice',
            name='protocol',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AddField(
            model_name='kubernetesservice',
            name='type',
            field=models.CharField(default='', max_length='500'),
        ),
        migrations.AlterField(
            model_name='kubernetesservice',
            name='port',
            field=models.CharField(default='', max_length=500),
        ),
    ]
