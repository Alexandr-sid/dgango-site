from django import forms
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile

def validate_upload_file(file: InMemoryUploadedFile) -> None:
    if file.name and 'virus' in file.name:
        raise ValidationError("File name should not contain word 'virus'")


class UserBioForm(forms.Form):
    name = forms.CharField(label="Full name")
    age = forms.IntegerField(label="Your age")
    bio = forms.CharField(label="Biography", widget=forms.Textarea)


class UploadFileForm(forms.Form):
    filename = forms.FileField(validators=[validate_upload_file])

