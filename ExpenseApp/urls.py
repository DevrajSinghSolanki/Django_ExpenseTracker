from django.urls import path
from . import views
urlpatterns = [
    path('',views.openIndex),
    path('signup-form',views.openSignupform),
    path('save-user',views.saveUser),
    path('dashboard',views.OpenDashboard),
    path('login',views.LoginUser),
    path('logout',views.LogoutUser),
    path('income-form',views.openIncomeForm),
    path('expense-form',views.openExpenseForm),
    path('save-income',views.saveIncome),
    path('save-expense',views.saveExpense),
    path('delete-income/<int:id>',views.deleteIncome),
    path('delete-expense/<int:id>',views.deleteExpense),
    path('open-update-income/<int:id>',views.openupdateIncome),
    path('open-update-expense/<int:id>',views.openupdateExpense),
    path('update-income/<int:id>',views.updateIncome),
    path('update-expense/<int:id>',views.updateExpense),
    path('all-incomes',views.getAllIncomes),
    path('all-expenses',views.getAllExpenses),
    path('all-transactions',views.getAllTransactions),
    path('income-analysis',views.getIncomeAnalysis),
    path('expense-analysis',views.getExpenseAnalysis)
]
