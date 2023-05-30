from django.forms import ModelForm
from django import forms
from .models import Work,Member,Organization,Types
from Customer.models import Measurement,Customers
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError

from dal import autocomplete
import djhacker
class WorkFoam(ModelForm):
    customer = forms.ModelChoiceField(
        queryset=Customers.objects.all(),
        widget=autocomplete.ModelSelect2(url='test-autocomplete')
    )
    cost = forms.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(9999999999)]
    )
    billno = forms.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(9999999999999)]
    )
    class Meta:
        model = Work
        fields = ("customer","type","billno","date", "astar", "piku", "cost", "worker")
        widgets = {
            'customer': autocomplete.ModelSelect2(url='test-autocomplete'),
            'date': forms.widgets.DateInput(attrs={'type': 'date'}),
            'cost': forms.NumberInput(attrs={'min': 0, 'max': 9999999999}),
            'billno': forms.NumberInput(attrs={'min': 0, 'max': 9999999999999}),
        }
        labels = {
            'cost': 'Cost',
        }
        help_texts = {
            'cost': 'Enter valid value',
            'billno': 'Enter valid value',
        }
    def __init__(self, organization, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.org = organization
        self.fields['astar'].choices = [
            choice for choice in self.fields['astar'].choices if choice[0] != Work.MaterialChoices.STAGE3
        ]
        self.fields['piku'].choices = [
            choice for choice in self.fields['piku'].choices if choice[0] != Work.MaterialChoices.STAGE3
        ]
        self.fields['worker'].queryset = Member.objects.filter(organization=self.org).distinct()
        self.fields['type'].queryset = Types.objects.filter(organization=self.org).distinct()
djhacker.formfield(
    Work.customer,
    forms.ModelChoiceField,
    widget=autocomplete.ModelSelect2(url='test-autocomplete')
)
class CustomerFoam(ModelForm):
  class Meta:
    model = Customers
    fields = ("mobileno","name","address","email")
class MeasurementFoam(ModelForm):
  class Meta:
    model = Measurement
    fields = ("legs","west","hand")
class OrganizationFoam(ModelForm):
  class Meta:
    model = Organization
    fields = ("name",)
class TypeFoam(ModelForm):
  class Meta:
    model = Types
    fields = ("name",)