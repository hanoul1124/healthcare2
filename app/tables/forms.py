from django import forms
from django.contrib.admin.widgets import AdminDateWidget


class XLSXImportForm(forms.Form):
    xlsx_file = forms.FileField()
    date_input = forms.DateField(widget=forms.SelectDateWidget)
