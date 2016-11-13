from django.shortcuts import render, redirect
from django.views.generic import View
from . import services
from .forms import SubmitForm

# Create your views here.
class MainView(View):
	template_name = 'main/home.html'
	
	def get(self, request):
		tup = services.getBalances(request)
		electricity = tup[0]
		water = tup[1]
		return render(request, self.template_name, {'electricity': int(electricity), 'water': int(water)})

class SendFormView(View):
	form_class = SubmitForm
	template_name = 'main/send.html'

	def get(self, request):
		form = self.form_class(None)
		return render(request, self.template_name, {'form': form})

	def post(self, request):
		form = self.form_class(request.POST)

		if form.is_valid():
			recipient = form.cleaned_data['recipient']
			amount = form.cleaned_data['amount']
			energyType = form.cleaned_data['energyType']
			result = services.sendCredit(request, int(recipient), int(amount), int(energyType))

			return redirect('main:index')
		return render(request, self.template_name, {'form': form})
	





