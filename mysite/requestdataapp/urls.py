from django.urls import path
from .views import process_get_view, user_form, upload_file_form

app_name = 'requestdataapp'

urlpatterns = [
    path("get/", process_get_view, name="get-view"),
    path("bio/", user_form, name="user-form"),
    path("upload/", upload_file_form, name="upload-file"),
]
