# Automate With Django

Automate the boring stuff with django

## Technology

- Framework: Django
- Database: SQLite, Redis
- Celery

# Features

- Custom commands for import data to database table.
- Custom commands for export data from database table.
- import data from frontend (csv file) to database table.
- export data from database as csv file and send through email.
- Handle long task with celery & redis

## Deployment

The first thing to do is to clone the repository:

```bash
  git clone https://github.com/tanzid64/automate-with-django.git
  cd automate-with-django/
```

Create a virtual environment to install dependencies in and activate it:
<br/>
For windows:

```bash
  python -m venv .venv
  .venv\Scripts\activate
```

For Ubuntu:

```bash
  virtualenv .venv
  source .venv/bin/activate
```

Then install the dependencies:

```bash
  pip install -r requirements.txt
```

Create a file name .env in root directory.

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`SECRET_KEY`
`DEBUG`
`EMAIL_HOST_USER`
`EMAIL_HOST_PASSWORD`
`EMAIL_HOST`
`EMAIL_PORT`
`CELERY_BROKER_URL`

Apply migrations:

```bash
  python manage.py migrate
```

Create an admin account:

```bash
  python manage.py createsuperuser
```

Start the django application:

```bash
  python manage.py runserver
```

Import data from csv to database:

```bash
  python manage.py importdata file_path model_name
```

Export data from database to csv:

```bash
  python manage.py exportdata model_name
```

That's it! You should now be able to see the demo application.
Browse:

- HomePage: localhost:8000/
- Admin Panel: localhost:8000/admin/
