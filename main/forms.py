from django.contrib.auth.models import User
from django import forms

class SubmitForm(forms.Form):
	CHOICES = (('1', 'Electricity'), ('2', 'Water'))

	recipient = forms.IntegerField()
	amount = forms.IntegerField()
	energyType = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)

class HVACForm(forms.Form):

	low = forms.IntegerField()
	high = forms.IntegerField()

class LightingForm(forms.Form):

	brightness = forms.IntegerField()
class BlindsForm(forms.Form):

	height = forms.IntegerField()