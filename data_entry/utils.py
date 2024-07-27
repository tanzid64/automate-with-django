import os
from django.apps import apps
from django.conf import settings
from django.core.management.base import CommandError
from django.db import DataError
import csv
import datetime
from django.core.mail import EmailMessage

def get_all_custom_models():
  default_models = ['ContentType', 'Session', 'LogEntry', 'Group', 'Permission', 'Upload']
  custom_models = []
  for model in apps.get_models():
    if model.__name__ not in default_models:
      custom_models.append(model.__name__)
  return custom_models

def check_csv_errors(file_path, model_name):
  # search for the model across all installed apps
  model = None
  for app_config in apps.get_app_configs():
    # get_app_configs() returns a list of metadata of all installed apps
    # Try to search for the model inside the app
    try:
      model = app_config.get_model(model_name)
      break # stop searching once the model is found
    except LookupError:
      continue # continue searching if the model is not found

  if not model:
    raise CommandError(f"Model '{model_name}' not found in any app.")
  # compare csv header with model's field names
  model_fields = [field.name for field in model._meta.fields if field.name != 'id']

  try:
    with open(file_path, 'r') as file:
      reader = csv.DictReader(file)
      header = reader.fieldnames

      # compare header with model's field names
      if header != model_fields:
        raise DataError(f"CSV header does not match model fields '{model_fields}'.")
  except Exception as e:
    raise e
  
  return model

def send_email_notification(subject, body, to_email, attachment=None):
  from_email = settings.DEFAULT_FROM_EMAIL
  try:
    mail = EmailMessage(body=body, subject=subject, from_email=from_email, to=to_email)
    if attachment:
      mail.attach_file(attachment)
    mail.send()
  except Exception as e:
    raise e
  

def generate_csv_file(model_name):
  # generate timestapm
  timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
  # define the csv file path
  export_dir = 'exported_data'
  file_name = f"exported_{model_name}_data_{timestamp}.csv"
  file_path = os.path.join(settings.MEDIA_ROOT, export_dir, file_name)
  return file_path