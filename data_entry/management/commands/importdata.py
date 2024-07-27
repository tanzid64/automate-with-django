import csv
from django.apps import apps
from django.core.management.base import BaseCommand, CommandError
from data_entry.models import Student

# proposed command - python manage.py importdata file_path model_name

class Command(BaseCommand):
  help = "Import data from csv file"

  def add_arguments(self, parser):
    parser.add_argument('file_path', type=str, help="The path of the csv file to import")
    parser.add_argument('model_name', type=str, help="The name of the model to import data to")

  def handle(self, *args, **options) :
    # Logics to import data from csv file
    file_Path = options['file_path']
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

    with open(file_Path, 'r') as file:
      reader = csv.DictReader(file)
      for row in reader:
        model.objects.create(**row)
    self.stdout.write(self.style.SUCCESS('Data imported successfully'))