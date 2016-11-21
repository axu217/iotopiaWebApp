from django.shortcuts import render, redirect
from django.views.generic import View
from . import services
from . import bacnet
from .forms import SubmitForm, ControlForm

# Create your views here.
class MainView(View):
	template_name = 'main/home.html'
	
	def get(self, request):
		tup = services.getBalances(request)
		electricity = int(tup[0])
		water = int(tup[1])
		ePercent = electricity / 50
		wPercent = water/ 50

		return render(request, self.template_name, {'electricity': electricity, 'water': water, 'electricityPercentage' : ePercent, 'waterPercentage': wPercent})

class ControlFormView(View):
	form_class = ControlForm
	template_name = 'main/control.html'
	
	def get(self, request):
		form = self.form_class(None)
		return render(request, self.template_name)

	def post(self, request):
		form = self.form_class(request.POST)

		if form.is_valid():
			temperature = form.cleaned_data['temperature']
			result = bacnet.set_pi_bacnet(bacnet.zone_west_high, temperature)

			return redirect('main:index')
		return render(request, self.template_name, {'form': form})


class SendFormView(View):
	form_class = SubmitForm
	template_name = 'main/send.html'

	def get(self, request):
		form = self.form_class(None)
		userList = services.getUsers(request)
		return render(request, self.template_name, {'form': form, 'userList': userList})

	def post(self, request):
		form = self.form_class(request.POST)

		if form.is_valid():
			recipient = form.cleaned_data['recipient']
			amount = form.cleaned_data['amount']
			energyType = form.cleaned_data['energyType']
			result = services.sendCredit(request, int(recipient), int(amount), int(energyType))

			return redirect('main:index')
		return render(request, self.template_name, {'form': form})
	





