# Generated by Django 4.2.7 on 2023-11-23 17:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        (
            "mybankSQL",
            "0006_alter_demo_acc_no_reciever_alter_demo_acc_no_sender_and_more",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="account",
            name="dob",
        ),
        migrations.RemoveField(
            model_name="demo",
            name="Date",
        ),
        migrations.RemoveField(
            model_name="deposit",
            name="date",
        ),
        migrations.RemoveField(
            model_name="transfer",
            name="date",
        ),
        migrations.RemoveField(
            model_name="withdrawal",
            name="date",
        ),
    ]
