# Generated by Django 5.0.7 on 2024-07-29 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_entry_creator_month_entry_month'),
    ]

    operations = [
        migrations.CreateModel(
            name='fileModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='uploads/')),
            ],
        ),
        migrations.AlterModelOptions(
            name='month',
            options={'ordering': ['-created']},
        ),
        migrations.AddField(
            model_name='entry',
            name='saldo',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
