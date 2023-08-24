# Generated by Django 4.2.3 on 2023-08-23 16:24

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_sale_counter_sale_installments1_sale_installments2_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='scheduleevent',
            name='sale',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.sale'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='due_date',
            field=models.DateField(default=datetime.date(2023, 8, 23)),
        ),
        migrations.AlterField(
            model_name='scheduleevent',
            name='status',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
