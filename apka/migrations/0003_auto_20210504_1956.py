# Generated by Django 3.1.7 on 2021-05-04 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apka', '0002_auto_20210504_0921'),
    ]

    operations = [
        migrations.AddField(
            model_name='statusdata',
            name='prover',
            field=models.CharField(blank=True, default=None, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='directory',
            name='last_updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='file',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='file',
            name='last_updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='filesection',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='filesection',
            name='last_updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='sectioncategory',
            name='last_updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='status',
            name='last_updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='statusdata',
            name='last_updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
