from django.core.management import call_command
from awd_main.celery import app
import time

from data_entry.utils import generate_csv_file, send_email_notification

@app.task
def celery_test_task():
  time.sleep(5) # simulation of any task that's going to take 10 seconds
  # send email
  body="test email body"
  subject = "test email"
  to_email = ["tanzid3@gmail.com"]
  send_email_notification(subject, body, to_email)
  return 'celery test task & email executed successfully'

@app.task
def import_data_task(file_path, model_name):
  try:
    call_command('importdata', file_path, model_name)
  except Exception as e:
    raise e
  
  # notify the user by email
  body="import data task executed successfully"
  subject = "import data task"
  to_email = ["tanzid3@gmail.com"]
  send_email_notification(subject, body, to_email)
  return 'import data task executed successfully'


@app.task
def export_data_task(model_name):
  try:
    call_command('exportdata', model_name)
  except Exception as e:
    raise e
  file_path = generate_csv_file(model_name)
  # notify the user by email
  body="export data task executed successfully. Check the attachment."
  subject = "export data task"
  to_email = ["tanzid3@gmail.com"]
  send_email_notification(subject, body, to_email, attachment=file_path)
  return 'export data task executed successfully'