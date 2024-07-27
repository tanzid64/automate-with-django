from django.core.management.base import BaseCommand
from data_entry.models import Student

# I want to add some data into the database using custom command.

class Command(BaseCommand):
  help = "Insert data into the database"

  def handle(self, *args, **options):
    # Code to insert data into the database
    data_set = [
      {
        "roll": "1",
        "name": "John",
        "age": 20
      },
      {
        "roll": "2",
        "name": "Jane",
        "age": 21
      },
      {
        "roll": "3",
        "name": "Jack",
        "age": 22
      },
      {
        "roll": "4",
        "name": "Jill",
        "age": 23
      },
      {
        "roll": "5",
        "name": "Jenny",
        "age": 24
      },
      {
        "roll": "6",
        "name": "Jen",
        "age": 25
      }
    ]
    for data in data_set:
      # based on roll number duplicate validation
      roll = data['roll']
      existing_record = Student.objects.filter(roll=roll).exists()
      if not existing_record:
        Student.objects.create(**data)
      else:
        self.stdout.write(self.style.WARNING(f"Record with roll number {roll} already exists"))
    self.stdout.write(self.style.SUCCESS("Data inserted successfully"))
