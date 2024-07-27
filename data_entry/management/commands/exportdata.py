import csv
from django.core.management.base import BaseCommand, CommandError
from django.apps import apps
import datetime
# proposed command - python manage.py exportdata model_name
class Command(BaseCommand):
  help = "Export data to csv file"
  def add_arguments(self, parser):
    parser.add_argument('model_name', type=str, help="The name of the model to export data from")
  def handle(self, *args, **options):
    # fetch the data from database
    model_name = options['model_name'].capitalize()
    model = None
    # search for the model across all installed apps
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
    data = model.objects.all()
    # generate timestapm
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    # define the csv file path
    file_path = f"exported_{model_name}_data_{timestamp}.csv"
    # open the csv file
    with open(file_path, "w", newline="") as file:
      writer = csv.writer(file)
      # write the header row
      # List comprehension method for creating the header row from the model fields
      writer.writerow([field.name for field in model._meta.fields])
      # write the data rows
      for dt in data:
        writer.writerow([getattr(dt, field.name) for field in model._meta.fields])
    self.stdout.write(self.style.SUCCESS(f"Data exported to {file_path}"))