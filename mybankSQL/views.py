from .models import Deposit, Withdrawal, Transfer
from django.shortcuts import render, HttpResponse
from django.db.models import Q

from mybankSQL.models import Account, Deposit, Withdrawal, Transfer, TransactionID, AccountID, Demo
from datetime import date

# Create your views here.


def get_acc_no(acc_no):
    while type(acc_no) != int:
        acc_no = acc_no.acc_no
    return acc_no


def index(Request):
    return render(Request, "index.html")


def create_acc(Request):
    if Request.method == "POST":
        main_name = Request.POST.get("main_name")
        f_name = Request.POST.get("f_name")
        m_name = Request.POST.get("m_name")
        dob = Request.POST.get("dob")
        amount = int(Request.POST.get("amount"))
        acc_no = AccountID.generate_account_id()

        account = Account(acc_no=acc_no, name=main_name,
                          father_name=f_name, mother_name=m_name, dob=dob, balance=amount)
        account.save()

        context = {
            "acc_no": acc_no,
            "name": main_name,
            "balance": amount
        }

        return render(Request, "Create account redirect.html", context)

    return render(Request, "Create account.html")


def deposit(Request):
    if Request.method == "POST":
        try:
            ab = Request.POST
            acc_no = Request.POST.get("acc_no")
            name = Request.POST.get("name")
            amount = int(Request.POST.get("amount"))

            account = Account.objects.get(acc_no=acc_no, name=name)
            account.balance += amount
            balance = account.balance
            print(type(account.balance), type(amount))
            account.save()

            # print(account["acc_no"])
            transaction_id = TransactionID.generate_transaction_id()

            deposit = Deposit(acc_no=account,
                              name=name,
                              date=date.today(),
                              amount=amount,
                              transaction_id=transaction_id
                              )

            deposit.save()

            context = {
                "acc_no": acc_no,
                "transaction_no": transaction_id,
                "deposited_amt": amount,
                "balance": account.balance
            }

            return render(Request, "Deposit redirect.html", context)

        except Account.DoesNotExist:
            # Add a template for displaying an account not found message
            return HttpResponse("Invalid")

    return render(Request, "Deposit.html")


def withdraw(Request):
    if Request.method == "POST":
        try:

            ab = Request.POST
            name = Request.POST.get("name")
            acc_no = Request.POST.get("acc_no")
            amount = int(Request.POST.get("amount"))

            # # Retrieve balance from the Account model
            account = Account.objects.get(acc_no=acc_no, name=name)

            balance = account.balance

            if balance >= amount:

                transaction_id = TransactionID.generate_transaction_id()

                # Insert into Withdrawal model
                deposit = Withdrawal(acc_no=account,
                                     name=name,
                                     date=date.today(),
                                     amount=amount,
                                     transaction_id=transaction_id
                                     )

                # Update balance in the Account model
                account.balance -= amount
                account.save()
                context = {
                    "acc_no": acc_no,
                    "transaction_no": transaction_id,
                    "withdrawl_amt": amount,
                    "balance": account.balance
                }
                deposit.save()

                return render(Request, "Withdraw redirect.html", context)

            else:
                return HttpResponse('Your account has insufficient balance.')

        except Account.DoesNotExist:
            # Add a template for displaying an account not found message
            return HttpResponse("Invalid")

    return render(Request, "Withdraw.html")


def transfer(Request):
    if Request.method == "POST":
        # try:

        reciever_acc_no = Request.POST.get("reciever_acc_no")
        reciever_name = Request.POST.get("reciever_name")
        sender_acc_no = Request.POST.get("sender_acc_no")
        sender_name = Request.POST.get("sender_name")
        amount = int(Request.POST.get("amount"))

        #
        # Retrieve balance from the sender's account
        sender_account = Account.objects.get(
            acc_no=sender_acc_no, name=sender_name)

        sender_balance = sender_account.balance

        if sender_balance >= amount:

            receiver_account = Account.objects.get(
                acc_no=reciever_acc_no, name=reciever_name)

            transaction_id = TransactionID.generate_transaction_id()

            # Insert into Transfer model
            transfer = Transfer.objects.create(
                acc_no_receiver=receiver_account,
                receiver_name=reciever_name,
                acc_no_sender=sender_account,
                sender_name=sender_name,
                amount=amount,
                date=date.today(),
                transaction_id=transaction_id
            )

            transfer.save()

            # Update balance in the sender's account
            sender_account.balance -= amount
            balance = sender_account.balance
            sender_account.save()

            # Update balance in the receiver's account
            receiver_account.balance += amount
            receiver_account.save()

            context = {
                "acc_no": get_acc_no(sender_account),
                "transaction_no": transaction_id,
                "transfered_amt": amount,
                "balance": balance
            }

            return render(Request, "Transfer redirect.html", context)

            # return HttpResponse(f'Sender Account No.:{sender_account} Your current balance is: {sender_balance - amount}\nTransaction ID: {transfer.transaction_id}')

        else:
            return HttpResponse('Your account has insufficient balance.')

        # except Account.DoesNotExist:
        #     # Add a template for displaying an account not found message
        #     return HttpResponse("Invalid")

    return render(Request, "Transfer.html")


def statement(Request):
    if Request.method == "POST":
        try:
            acc_no = Request.POST.get("acc_no")

            account = Account.objects.get(acc_no=acc_no)
            # return HttpResponse(f'Account Number: {acc_no} Name: {account.name} \nBalance: {account.balance}')

            context = {
                "acc_no": acc_no,
                "name": account.name,
                "balance": account.balance
            }

            return render(Request, "Statement redirect.html", context)

        except Account.DoesNotExist:
            return HttpResponse('This account is invalid \nPlease check the details you have entered.')

    return render(Request, "Statement.html")


def history(Request):

    if Request.method == "POST":
        # try:
        acc_no = Request.POST.get("acc_no")
        start_date = Request.POST.get("start_date")
        end_date = Request.POST.get("end_date")
        limit = int(Request.POST.get("limit"))

        print(acc_no)

        deposits = Deposit.objects.filter(
            acc_no=acc_no, date__range=(start_date, end_date))
        withdrawals = Withdrawal.objects.filter(
            acc_no=acc_no, date__range=(start_date, end_date))
        transfers = Transfer.objects.filter(Q(acc_no_receiver=acc_no) | Q(
            acc_no_sender=acc_no), date__range=(start_date, end_date))

        # transactions = list(deposits) + list(withdrawals) + list(transfers)
        # print(list(deposits))

        # print(list(withdrawals))

        # print(list(transfers))
        # transactions.sort(key=lambda x: x.date, reverse=True)

        for i in withdrawals:
            print(i.acc_no)
            demo = Demo.objects.create(
                # acc_no_reciever=receiver_account,
                # reciever_name=reciever_name,
                acc_no_sender=get_acc_no(i),
                sender_name=i.name,
                Balance=i.amount,
                Date=i.date,
                TID=i.transaction_id,
                transaction_category="Debit"

            )

            demo.save()

        for i in deposits:
            print(i.acc_no)
            demo = Demo.objects.create(
                acc_no_reciever=get_acc_no(i),
                reciever_name=i.name,
                # acc_no_sender=i.acc_no,
                # sender_name=i.name,
                Date=i.date,
                Balance=i.amount,
                TID=i.transaction_id,
                transaction_category="Credit"

            )
            demo.save()

        for i in transfers:
            # print(i.acc_no)
            demo = Demo.objects.create(
                acc_no_reciever=get_acc_no(i.acc_no_receiver),
                reciever_name=i.receiver_name,
                acc_no_sender=get_acc_no(i.acc_no_sender),
                sender_name=i.sender_name,
                Date=i.date,
                Balance=i.amount,
                TID=i.transaction_id,
                transaction_category="Transfer"

            )
            demo.save()

        # Retrieve all instances of Demo sorted by Date in descending order
        sorted_demo = Demo.objects.all().order_by('-Date')

        if len(sorted_demo) == 0:
            HttpResponse(
                'This account is invalid \nPlease check the details you have entered')

        elif limit >= len(sorted_demo):
            print('ANO(R)', 'NO(R)', 'acc_no_sender', 'sender_name', 'Balacnce',
                  'Date', 'TID', 'DCT', sep='     ')
            # Print the sorted instances
            for instance in sorted_demo:
                print(instance.acc_no_reciever, instance.reciever_name, instance.acc_no_sender, instance.sender_name,
                      instance.Balance, instance.Date, instance.TID, instance.transaction_category)

            context = {
                "details_list": sorted_demo
            }
            Demo.objects.all().delete()

            return render(Request, "History redirect.html", context)

        else:
            print('ANO(R)', 'NO(R)', 'acc_no_sender', 'sender_name', 'Balacnce',
                  'Date', 'TID', 'DCT', sep='     ')

            for instance in sorted_demo[:limit]:
                print(instance.acc_no_reciever, instance.reciever_name, instance.acc_no_sender, instance.sender_name,
                      instance.Balance, instance.Date, instance.TID, instance.transaction_category)

            context = {
                "details_list": sorted_demo[:limit]
            }

            Demo.objects.all().delete()

            return render(Request, "History redirect.html", context)

        # return HttpResponse("Hello")

        # except Exception as e:
        #     # Add a template for displaying an account not found message
        #     print(Exception, "hello")
        #     return HttpResponse(f"{Exception}")

    return render(Request, "History.html")


def deposit_redirect(Request):

    return render(Request, "Deposit redirect.html")


def withdraw_redirect(Request):

    return render(Request, "History redirect.html")


def transfer_redirect(Request):

    return render(Request, "Transfer redirect.html")


def statement_redirect(Request):

    return render(Request, "Statement redirect.html")


def history_redirect(Request):

    return render(Request, "History redirect.html")
