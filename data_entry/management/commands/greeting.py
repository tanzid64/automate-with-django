from django.core.management.base import BaseCommand, CommandParser

class Command(BaseCommand):
  help = "Greet the user"
  def add_arguments(self, parser):
    parser.add_argument('name', type=str, help="The name of the person to greet")

  def handle(self, *args, **options):
    name = options['name']
    self.stdout.write(f'Hello {name}, Good morning..')