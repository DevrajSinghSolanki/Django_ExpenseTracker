# Generated by Django 4.0.6 on 2022-08-31 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ExpenseApp', '0002_income_expense'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='type',
            field=models.CharField(default='e', max_length=1),
        ),
        migrations.AddField(
            model_name='income',
            name='type',
            field=models.CharField(default='i', max_length=1),
        ),
    ]
