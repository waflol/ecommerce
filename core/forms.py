from tkinter import Widget
from django import forms
from core.models import *

class ProductForms(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'category': forms.Select(attrs={'class':'form-control'})
        }