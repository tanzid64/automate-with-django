from django.shortcuts import redirect, render
from data_entry.utils import check_csv_errors, get_all_custom_models
from uploads.models import Upload
from django.conf import settings
from django.contrib import messages
from .tasks import export_data_task, import_data_task
from django.core.management import call_command

# Create your views here.
def import_data(request):
  if request.method == 'POST':
    file_path = request.FILES.get('file_path')
    model_name = request.POST.get('model_name')

    # store this file inside upload model
    upload = Upload.objects.create(file=file_path, model_name=model_name)

    # construct the full path of the file to be imported
    relative_path = str(upload.file.url)
    base_url = str(settings.BASE_DIR)
    file_path = base_url + relative_path

    # check for the csv errors
    try:
      check_csv_errors(file_path, model_name)
    except Exception as e:
      messages.error(request, str(e))
      return redirect('importdata')
    
    # handle the import data task here
    import_data_task.delay(file_path, model_name, request.user.email)

    messages.success(request, 'Your data is being imported. You will be notified once it is completed.')
    return redirect('importdata')
  else:
    all_models = get_all_custom_models()
    context = {
      'all_models': all_models
    }
  return render(request, 'data_entry/importdata.html', context)

def export_data(request):
  if request.method == 'POST':
    model_name = request.POST.get('model_name')
    # call the export data task here
    export_data_task.delay(model_name, request.user.email)
    messages.success(request, 'Your data is being exported. You will be notified once it is completed.')
    return redirect('exportdata')
  else:
    all_models = get_all_custom_models()
    context = {
      'all_models': all_models
    }
  return render(request, 'data_entry/exportdata.html', context)