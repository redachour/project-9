from django import forms
from django.utils import timezone

from .models import *


class MenuForm(forms.ModelForm):
    '''This form is for creating or editing a menu'''
    class Meta:
        model = Menu
        fields = ['season',
                  'items',
                  'expiration_date']

    def clean_expiration_date(self):
        expiration_date = self.cleaned_data['expiration_date']
        if expiration_date and expiration_date <= timezone.now():
            raise forms.ValidationError("Expiration date should be in future")
        return expiration_date
