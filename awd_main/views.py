from django.http import HttpResponse
from django.shortcuts import render
from data_entry.tasks import celery_test_task

def home(request):
  return render(request, 'home.html')

def celery_test(request):
  # I want to execute a time consuming task here
  celery_test_task.delay()
  return HttpResponse('Function executed successfully')