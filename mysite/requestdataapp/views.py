from django.core.files.storage import FileSystemStorage
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .forms import UserBioForm, UploadFileForm


# Create your views here.
def process_get_view(request: HttpRequest) -> HttpResponse:
    a = request.GET.get("a", "")
    b = request.GET.get("b", "")
    result = a + b
    context = {
        "a" : a,
        "b" : b,
        "result" : result,
    }
    return render(request, "requestdataapp/request-query-params.html", context=context)


def user_form(request: HttpRequest) -> HttpResponse:
    context = {
        "form": UserBioForm(),
    }
    return render(request, "requestdataapp/user-bio-form.html", context=context)


def upload_file_form(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        upload_form = UploadFileForm(request.POST, request.FILES)
        if upload_form.is_valid():
            # upload_file = request.FILES["upload-file"]
            upload_file = upload_form.cleaned_data["filename"]
            fs = FileSystemStorage()
            file_name = fs.save(upload_file.name, upload_file)
            file_size = fs.size(file_name)
            context_error = {
                "file_name": file_name,
            }
            if file_size > 1_048_576:
                print("Uploaded file is big:", file_name)
                fs.delete(file_name)
                return render(request, "requestdataapp/error-upload.html", context=context_error)
            else:
                print("saved file", file_name)
    else:
        upload_form = UploadFileForm()

    context = {
        "upload_form": upload_form,
    }
    return render(request, "requestdataapp/file-upload.html", context=context)
