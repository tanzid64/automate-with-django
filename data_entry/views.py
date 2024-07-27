from django.shortcuts import redirect, render
from data_entry.utils import get_all_custom_models
from uploads.models import Upload
from django.conf import settings
from django.core.management import call_command
from django.contrib import messages

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

    # triggered importdata command
    try:
      call_command('importdata', file_path, model_name)
      messages.success(request, 'Data imported successfully')
    except Exception as e:
      messages.error(request, str(e))
    return redirect('importdata')
  else:
    all_models = get_all_custom_models()
    context = {
      'all_models': all_models
    }
  return render(request, 'data_entry/importdata.html', context)