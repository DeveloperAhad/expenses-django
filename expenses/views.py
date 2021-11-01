from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Category, Expense
from authentication.models import UserPreference
from django.http import JsonResponse
import json

# Create your views here.
def search_expenses(request):
    if request.method == "POST":
        search_str = json.loads(request.body).get('searchText')
        expenses = Expense.objects.filter(amount__istartswith=search_str, owner=request.user) | Expense.objects.filter(date__istartswith=search_str, owner=request.user) | Expense.objects.filter(description__icontains=search_str, owner=request.user) |  Expense.objects.filter(category__icontains=search_str, owner=request.user)
        
        data = expenses.values()
        # print(data)

        return JsonResponse(list(data), safe=False)


@login_required(login_url='login')
def index(request):
    user_info = UserPreference.objects.filter(user=request.user).exists()
    currency = 'USD'
    if user_info:
        currency = UserPreference.objects.get(user=request.user).currency.split('-')[0]

    expenses = Expense.objects.filter(owner=request.user)
    
    context = {
        'expenses': expenses,
        'currency': currency
    }

    # print(expenses.get_total())

    return render(request, 'expenses/index.html', context)
    
@login_required(login_url='login')
def add_expenses_view(request):
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
        
        Expense.objects.create(amount=amount, description=description, category=category, date=date, owner=request.user)
        messages.success(request, "Expense save successfully")
        return redirect('expenses')
         

    return render(request, 'expenses/add-new-expenses.html', context);

    
@login_required(login_url='login')
def edit_expenses_view(request, id):
    is_expenses = Expense.objects.filter(pk=id,owner=request.user).exists()
    if not is_expenses:
        return redirect('expenses')

    expenses = Expense.objects.get(pk=id, owner=request.user)
    categories = Category.objects.all()
    context = {
        'expenses': expenses,
        'categories': categories
    }

    if request.method == "POST":
        amount = request.POST.get("amount")
        description = request.POST.get("description")
        category = request.POST.get("category")
        date = request.POST.get("date")

        if not amount:
            messages.error(request, "Amount is required!")
            return render(request, 'expenses/edit-expenses.html', context);

        if not description:
            messages.error(request, "Description is required!")
            return render(request, 'expenses/edit-expenses.html', context); 
        
        expenses.owner = request.user
        expenses.amount = amount
        expenses.category = category
        expenses.description = description
        expenses.date = date
        expenses.save()
        messages.success(request, "Expense edit successfully")
        return redirect('expenses')
         

    return render(request, 'expenses/edit-expenses.html', context);

@login_required(login_url='login')
def delete_expenses_view(request, id):
    is_expenses = Expense.objects.filter(pk=id, owner=request.user).exists()
    if is_expenses:
        Expense.objects.get(pk=id).delete()
        messages.success(request, "Delete successfully")
    return redirect('expenses')