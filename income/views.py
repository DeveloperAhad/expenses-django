from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Category, Income
from authentication.models import UserPreference
from django.http import JsonResponse

import json

# Create your views here.
def search_income(request):
    if request.method == "POST":
        search_str = json.loads(request.body).get('searchText')
        expenses = Income.objects.filter(amount__istartswith=search_str, owner=request.user) | Income.objects.filter(date__istartswith=search_str, owner=request.user) | Income.objects.filter(description__icontains=search_str, owner=request.user) |  Income.objects.filter(category__icontains=search_str, owner=request.user)
        
        data = expenses.values()
        # print(data)

        return JsonResponse(list(data), safe=False)


@login_required(login_url='login')   
def index(request):
    user_info = UserPreference.objects.filter(user=request.user).exists()
    currency = 'USD'
    if user_info:
        currency = UserPreference.objects.get(user=request.user).currency.split('-')[0]

    context = {
        'Incomes': Income.objects.filter(owner=request.user).all(),
        'currency': currency
    }
    return render(request, 'income/index.html', context)

@login_required(login_url='login')
def add_income(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'value': request.POST
    }
    if request.method == "GET":
        pass

    if request.method == "POST":
        amount = request.POST.get("amount")
        description = request.POST.get("description")
        category = request.POST.get("category")
        date = request.POST.get("date")

        if not amount:
            messages.error(request, "Amount is required!")
            return render(request, 'expenses/add-new-expenses.html', context);

        if not description:
            messages.error(request, "Description is required!")
            return render(request, 'expenses/add-new-expenses.html', context);   
        
        Income.objects.create(amount=amount, description=description, category=category, date=date, owner=request.user)
        messages.success(request, "Income save successfully")
        return redirect('expenses')
         

    return render(request, 'income/add-new-income.html', context);

@login_required(login_url='login')
def edit_income(request, id):
    is_income = Income.objects.filter(pk=id,owner=request.user).exists()
    if not is_income:
        return redirect('income')

    income = Income.objects.get(pk=id, owner=request.user)
    categories = Category.objects.all()
    context = {
        'income': income,
        'categories': categories
    }

    if request.method == "POST":
        amount = request.POST.get("amount")
        description = request.POST.get("description")
        category = request.POST.get("category")
        date = request.POST.get("date")

        if not amount:
            messages.error(request, "Amount is required!")
            return render(request, 'income/edit-expenses.html', context);

        if not description:
            messages.error(request, "Description is required!")
            return render(request, 'income/edit-expenses.html', context); 
        
        income.owner = request.user
        income.amount = amount
        income.category = category
        income.description = description
        income.date = date
        income.save()
        messages.success(request, "Income edit successfully")
        return redirect('income')

    return render(request, 'income/edit-income.html', context);

@login_required(login_url='login')
def delete_income(request):
    is_expenses = Income.objects.filter(pk=id, owner=request.user).exists()
    if is_expenses:
        Income.objects.get(pk=id).delete()
        messages.success(request, "Delete successfully")
    return redirect('income')