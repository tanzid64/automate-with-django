from django.http import HttpResponse
from django.shortcuts import redirect, render
from data_entry.tasks import celery_test_task
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate

def home(request):
  return render(request, 'home.html')

def celery_test(request):
  # I want to execute a time consuming task here
  celery_test_task.delay()
  return HttpResponse('Function executed successfully')


def register(request):
  if request.method == 'POST':
    form = RegisterForm(request.POST)
    if form.is_valid():
      form.save()
      messages.success(request, 'Your account has been created! You are now able to log in')
      return redirect('home')
    else:
      context = {
        'form': form,
        "register": True
      }
      return render(request, 'register.html', context)
  else:
    form = RegisterForm()
    context = {
      'form': form,
      "register": True
    }
  return render(request, 'register.html', context)

def login(request):
  if request.method == 'POST':
    form = AuthenticationForm(data=request.POST)
    if form.is_valid():
      username = form.cleaned_data.get('username')
      password = form.cleaned_data.get('password')
      user = authenticate(username=username, password=password)
      if user:
        login(request, user)
        return redirect('home')
    else:
      messages.error(request, 'Invalid username or password')
      return redirect('login')
  else:
    form = AuthenticationForm()
  return render(request, 'register.html', {'form': form})

def logout(request):
  logout(request)
  return redirect('home')