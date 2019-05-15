from django import forms


class XLSXImportForm(forms.Form):
    xlsx_file = forms.FileField()