from django.shortcuts import render, redirect

from django.contrib.auth import login
import datetime
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from .models import Expense, Category, Budget
from django.db.models import Sum



# Create your views here.
def home(request):
    return render(request, 'home.html')

def expenses_index(request):
  expenses = Expense.objects.filter(user=request.user)
  categories = Category.objects.all()
  category_expenses = Category.objects.filter(expense__user = request.user).annotate(total_expenses = Sum('expense__amount'))
  budgets = Budget.objects.filter(user=request.user)
  budget = budgets[0]
  sum = 0
  for expense in expenses:
    if expense.date >= budget.start_date and expense.date <= budget.end_date:
      sum += expense.amount
  percent_left = int(((budget.amount - sum) / budget.amount) * 100)
  amount_left = budget.amount - sum
  return render(request, 'expenses/index.html', {
    'expenses': expenses,
    'categories': categories,
    'category_expenses': category_expenses,
    'budget': budget,
    'sum': sum,
    'amount_left': amount_left,
    'percent_left': percent_left
  })

def expenses_detail(request, expense_id):
  expense = Expense.objects.get(id=expense_id)
  return render(request, 'expenses/detail.html', { 'expense': expense })

def categories_detail(request, category_id):
  category = Category.objects.get(id=category_id)
  expenses = Expense.objects.filter(category=category)
  return render(request, 'main_app/category_detail.html', { 'category': category, 'expenses': expenses})

def budget_detail(request):
  budgets = Budget.objects.filter(user=request.user)
  budget = budgets[0]
  expenses = Expense.objects.filter(user=request.user)
  sum = 0
  for expense in expenses:
    if expense.date >= budget.start_date and expense.date <= budget.end_date:
      sum += expense.amount
  percent_left = int(((budget.amount - sum) / budget.amount) * 100)
  amount_left = budget.amount - sum
  return render(request, 'main_app/budget_detail.html', { 
    'budget': budget,
    'sum': sum,
    'amount_left': amount_left,
    'percent_left': percent_left
      })

class ExpenseCreate(CreateView):
  model = Expense
  fields = ['title', 'amount', 'date', 'category']

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)  

class ExpenseUpdate(UpdateView):
  model = Expense
  fields = ['title', 'amount', 'date', 'category']

class ExpenseDelete(DeleteView):
  model = Expense
  success_url = '/expenses'

class CategoryCreate(CreateView):
  model = Category
  fields = ['title']

class CategoryUpdate(UpdateView):
  model = Category
  fields = ['title']

class CategoryDelete(DeleteView):
  model = Category
  success_url = '/categories'

class CategoryList(ListView):
  model = Category

class BudgetCreate(CreateView):
  model = Budget
  fields = ['amount', 'start_date', 'end_date']

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form) 
  
class BudgetUpdate(UpdateView):
  model = Budget
  fields = ['amount', 'start_date', 'end_date']

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('budget_create')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

