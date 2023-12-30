# Generated by Django 4.2.7 on 2023-12-30 08:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('BillSoftwareapp', '0002_parties_itemmodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='FirstBill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bill_number', models.PositiveIntegerField()),
                ('bill_date', models.DateField(null=True)),
                ('supply_source', models.CharField(max_length=150, null=True)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='BillSoftwareapp.parties')),
            ],
        ),
    ]