from django.urls import path
from . import views

urlpatterns = [
  path('import-data/', views.import_data, name='importdata'),
  path('export-data/', views.export_data, name='exportdata'),
]