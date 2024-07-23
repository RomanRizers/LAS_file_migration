from django import forms

class LasFileUploadForm(forms.Form):
    las_file = forms.FileField(label='Выберите файл LAS')
