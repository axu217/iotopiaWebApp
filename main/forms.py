from django.contrib.auth.models import User
from django import forms

class SubmitForm(forms.Form):
	CHOICES = (('1', 'Electricity'), ('2', 'Water'))

	recipient = forms.IntegerField()
	amount = forms.IntegerField()
	energyType = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)

class HVACForm(forms.Form):
	CHOICES = (('1', 'Low'), ('2', 'High'))

	hvacLoc = forms.IntegerField()
	lowHigh = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
	temperature = forms.IntegerField()

class LightingForm(forms.Form):

	lightingZoneNumber = forms.IntegerField()
	brightness = forms.IntegerField()
	