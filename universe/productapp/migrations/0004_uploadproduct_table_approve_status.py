# Generated by Django 4.1 on 2022-09-15 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("productapp", "0003_alter_uploadproduct_table_price_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="uploadproduct_table",
            name="approve_status",
            field=models.CharField(default="Unapproved", max_length=100),
        ),
    ]