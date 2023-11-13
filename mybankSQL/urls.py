from django.contrib import admin
from django.urls import path
from mybankSQL import views

urlpatterns = [
    # path('', include('example.urls')),

    path("", views.index, name="index"),
    path("acc_create", views.create_acc, name="create_acc"),
    path("deposit", views.deposit, name="deposit"),
    path("withdraw", views.withdraw, name="withdraw"),
    path("transfer", views.transfer, name="transfer"),
    path("statement", views.statement, name="statement"),
    path("history", views.history, name="history"),

    # path("create_acc_redirect", views.create_acc_redirect,
    #      name="create_acc_redirect"),
    path("deposit_redirect", views.deposit_redirect, name="deposit_redirect"),
    path("withdraw_redirect", views.withdraw_redirect, name="withdraw_redirect"),
    path("transfer_redirect", views.transfer_redirect, name="transfer_redirect"),
    path("statement_redirect", views.statement_redirect, name="statement_redirect"),
    path("history_redirect", views.history_redirect, name="history_redirect"),
]
