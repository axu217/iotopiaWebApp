from django.contrib.auth.models import User
from django import forms

class SubmitForm(forms.Form):
	CHOICES = (('1', 'Electricity'), ('2', 'Water'))

	recipient = forms.IntegerField()
	amount = forms.IntegerField()
	energyType = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
	