from django.db import models

import random
import string

# Create your models here.


class Account(models.Model):
    acc_no = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=25)
    father_name = models.CharField(max_length=25)
    mother_name = models.CharField(max_length=25)
    dob = models.DateField()
    balance = models.IntegerField()


class Deposit(models.Model):
    acc_no = models.ForeignKey(Account, on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
    date = models.DateField()
    amount = models.IntegerField()
    transaction_id = models.CharField(max_length=30)


class Withdrawal(models.Model):
    acc_no = models.ForeignKey(Account, on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
    date = models.DateField()
    amount = models.IntegerField()
    transaction_id = models.CharField(max_length=30)


class Transfer(models.Model):
    acc_no_receiver = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='receiver')
    receiver_name = models.CharField(max_length=25)
    acc_no_sender = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='sender')
    sender_name = models.CharField(max_length=25)
    amount = models.IntegerField()
    date = models.DateField()
    transaction_id = models.CharField(max_length=30)


class TransactionID(models.Model):
    transaction_id = models.CharField(
        max_length=30, unique=True, primary_key=True)

    @classmethod
    def generate_transaction_id(cls):
        while True:
            transaction_id = ''.join(random.choices(
                string.ascii_uppercase + string.digits, k=30))
            if not cls.objects.filter(transaction_id=transaction_id).exists():
                return transaction_id


class AccountID(models.Model):
    acc_no = models.CharField(max_length=9, unique=True, primary_key=True)

    @classmethod
    def generate_account_id(cls):
        while True:
            acc_no = ''.join(random.choices(string.digits, k=9))
            if not cls.objects.filter(acc_no=acc_no).exists():
                return acc_no


class Demo(models.Model):
    acc_no_reciever = models.IntegerField(null=True, blank=True)
    reciever_name = models.CharField(max_length=20, null=True, blank=True)
    acc_no_sender = models.IntegerField(null=True, blank=True)
    sender_name = models.CharField(max_length=20, null=True, blank=True)
    Balance = models.IntegerField()
    Date = models.DateField()
    TID = models.CharField(max_length=30)
    transaction_category = models.CharField(max_length=20)
