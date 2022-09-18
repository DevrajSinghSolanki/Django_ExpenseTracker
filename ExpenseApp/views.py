from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from . models import User,Income,Expense
from django.db.models import Sum
from django.contrib.auth.hashers import check_password,make_password
import random

# Create your views here.
def openIndex(request):
    if 'user_id' in request.session:
        return redirect('/dashboard')
    else:
        return render(request,'Index.html')

def openSignupform(request):
    return render(request,'signup-form.html')

def saveUser(request):
    u=User()
    tname=u.name=request.POST['name']
    tphone=u.phone=request.POST['phone']
    temail=u.email=request.POST['email']
    tpass=make_password(request.POST['password'])
    u.password=tpass
    result=User.objects.filter(email=temail)
    result1=User.objects.filter(phone=tphone)
    if result or result1:
        return render(request,'signup-form.html',{'error':'Email Or Phone Already Exists!!!','name':tname,'phone':tphone,'email':temail})
    u.save()
    return render(request,'Index.html',{'result':'Your Account Created Sucessfully !'})

def OpenDashboard(request):
    if 'user_id' in request.session:
        id=request.session['user_id']
        user=User.objects.get(id=id)
        incomes=user.income_set.aggregate(Sum('amount'))
        expenses=user.expense_set.aggregate(Sum('amount'))
        totalIncome=0 if incomes['amount__sum'] is None else incomes['amount__sum']
        totalExpense=0 if expenses['amount__sum'] is None else expenses['amount__sum']
        currentBalance=totalIncome-totalExpense
        return render(request,'dashboard.html',{'user':user,'Incomes':totalIncome,'Expenses':totalExpense,'Balance':currentBalance})
    return redirect('/')

def LoginUser(request):
    email=request.POST['email']
    password=request.POST['password']
    result=User.objects.filter(email=email)
    if result:
        passw=result[0].password
        check=check_password(password,passw)        
        if check:
            request.session['user_id']=result[0].id
            return redirect('/dashboard')
        return render(request,'Index.html',{'error':'Wrong Password!'})
    return render(request,'Index.html',{'error':'Wrong Email'})

def LogoutUser(request):
    del request.session['user_id']
    return redirect('/')

def openIncomeForm(request):
    if 'user_id' in request.session:
        id=request.session['user_id']
        user=User.objects.get(id=id)
        return render(request,'income-form.html',{'user':user})
    return redirect('/')

def openExpenseForm(request):
    if 'user_id' in request.session:
        id=request.session['user_id']
        user=User.objects.get(id=id)
        return render(request,'expense-form.html',{'user':user})
    return redirect('/')

def saveIncome(request):
    if 'user_id' in request.session:
        id=request.session['user_id']
        user=User.objects.get(id=id)
        income=Income()
        income.amount=request.POST['amount']
        income.category=request.POST['category']
        income.remark=request.POST['remark']
        income.date=request.POST['date']
        income.time=request.POST['time']
        income.user=user
        income.save()
        return redirect('/all-incomes')
    return redirect('/')

def saveExpense(request):
    if 'user_id' in request.session:
        id=request.session['user_id']
        user=User.objects.get(id=id)
        expense=Expense()
        expense.amount=request.POST['amount']
        expense.category=request.POST['category']
        expense.remark=request.POST['remark']
        expense.date=request.POST['date']
        expense.time=request.POST['time']
        expense.user=user
        expense.save()
        return redirect('/all-expenses')
    return redirect('/')

def deleteIncome(request,id):
    if 'user_id' in request.session:
        uid=request.session['user_id']
        user=User.objects.get(id=uid)
        inc=Income.objects.get(id=id)
        inc.delete()
        return redirect('/all-incomes')
    return redirect('/')

def deleteExpense(request,id):
    if 'user_id' in request.session:
        uid=request.session['user_id']
        user=User.objects.get(id=uid)
        exp=Expense.objects.get(id=id)
        exp.delete()
        return redirect('/all-expenses')
    return redirect('/')

def openupdateIncome(request,id):
    if 'user_id' in request.session:
        uid=request.session['user_id']
        user=User.objects.get(id=uid)
        inc=Income.objects.get(id=id)
        return render(request,'income-form.html',{'user':user,'income':inc})
    return redirect('/')

def updateIncome(request,id):
    if 'user_id' in request.session:
        uid=request.session['user_id']
        user=User.objects.get(id=uid)
        income=Income.objects.get(id=id)
        income.amount=request.POST['amount']
        income.category=request.POST['category']
        income.remark=request.POST['remark']
        income.date=request.POST['date']
        income.time=request.POST['time']
        income.user=user
        income.save()
        return redirect('/all-incomes')
    return redirect('/')

def openupdateExpense(request,id):
    if 'user_id' in request.session:
        uid=request.session['user_id']
        user=User.objects.get(id=uid)
        exp=Expense.objects.get(id=id)
        return render(request,'expense-form.html',{'user':user,'expense':exp})
    return redirect('/')

def updateExpense(request,id):
    if 'user_id' in request.session:
        uid=request.session['user_id']
        user=User.objects.get(id=uid)
        expense=Expense.objects.get(id=id)
        expense.amount=request.POST['amount']
        expense.category=request.POST['category']
        expense.remark=request.POST['remark']
        expense.date=request.POST['date']
        expense.time=request.POST['time']
        expense.user=user
        expense.save()
        return redirect('/all-expenses')
    return redirect('/')

def getAllIncomes(request):
    if 'user_id' in request.session:
        id=request.session['user_id']
        user=User.objects.get(id=id)
        incomes=user.income_set.all().order_by('-date')
        return render(request,'all-incomes.html',{'user':user,'Incomes':incomes})
    return redirect('/')

def getAllExpenses(request):
    if 'user_id' in request.session:
        id=request.session['user_id']
        user=User.objects.get(id=id)
        expenses=user.expense_set.all().order_by('-date')
        return render(request,'all-expenses.html',{'user':user,'Expenses':expenses})
    return redirect('/')

def getAllTransactions(request):
    if 'user_id' in request.session:
        id=request.session['user_id']
        user=User.objects.get(id=id)
        incomes=user.income_set.all()
        expenses=user.expense_set.all()
        transactions=list(incomes)+list(expenses)
        for i in range(0, len(transactions)):    
            for j in range(i+1, len(transactions)):    
                if(transactions[i].date < transactions[j].date):    
                    temp = transactions[i]    
                    transactions[i] = transactions[j]
                    transactions[j] = temp
        return render(request,'all-transactions.html',{'user':user,'Transactions':transactions})
    return redirect('/')

def getIncomeAnalysis(request):
    if 'user_id' in request.session:
        id=request.session['user_id']
        user=User.objects.get(id=id)
        incomes=user.income_set.values('category').order_by('category').annotate(total=Sum('amount'))
        cate=[]
        tot=[]
        colors=[]
        result={'category':cate,'total':tot,'colors':colors}
        for income in incomes:
            result['category'].append(income['category'])
            result['total'].append(income['total'])
            result['colors'].append('rgb('+str(random.randint(0,255))+', '+str(random.randint(0,255))+', '+str(random.randint(0,255))+')')
        print(result)
        return JsonResponse(result)

def getExpenseAnalysis(request):
    if 'user_id' in request.session:
        id=request.session['user_id']
        user=User.objects.get(id=id)
        expenses=user.expense_set.values('category').order_by('category').annotate(total=Sum('amount'))
        cate=[]
        tot=[]
        colors=[]
        result={'category':cate,'total':tot,'colors':colors}
        for expense in expenses:
            result['category'].append(expense['category'])
            result['total'].append(expense['total'])
            result['colors'].append('rgb('+str(random.randint(0,255))+', '+str(random.randint(0,255))+', '+str(random.randint(0,255))+')')
        print(result)
        return JsonResponse(result)
    