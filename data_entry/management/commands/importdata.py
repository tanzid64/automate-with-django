import csv
from django.apps import apps
from django.core.management.base import BaseCommand, CommandError
from django.db import DataError
from data_entry.models import Student
from data_entry.utils import check_csv_errors

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
    model = check_csv_errors(file_Path, model_name)

    with open(file_Path, 'r') as file:
      reader = csv.DictReader(file)
      for row in reader:
        model.objects.create(**row)
    self.stdout.write(self.style.SUCCESS('Data imported successfully'))