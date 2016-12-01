from django.shortcuts import render, redirect
from django.views.generic import View
from . import services
from . import bacnet
from .forms import SubmitForm, HVACForm, LightingForm

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
	form_class1 = HVACForm
	form_class2 = LightingForm
	template_name = 'main/control.html'
	
	def get(self, request):

		passIn = {}
	
		northTemp = bacnet.getHVAC("north", "default")
		northLow = bacnet.getHVAC("north", "low")
		northHigh = bacnet.getHVAC("north", "high")

		westTemp = bacnet.getHVAC("west", "default")
		westLow = bacnet.getHVAC("west", "low")
		westHigh = bacnet.getHVAC("west", "high")

		passIn['northTemp'] = northTemp
		passIn['westTemp'] = westTemp

		passIn['northLow'] = northLow
		passIn['westLow'] = westLow

		passIn['northHigh'] = northHigh
		passIn['westHigh'] = westHigh

		lighting1 = bacnet.getLighting(1)
		lighting2 = bacnet.getLighting(2)
		lighting3 = bacnet.getLighting(3)
		lighting4 = bacnet.getLighting(4)
		lighting5 = bacnet.getLighting(5)
		lighting6 = bacnet.getLighting(6)
		lighting7 = bacnet.getLighting(7)
		lighting8 = bacnet.getLighting(8)

		passIn['lighting1'] = lighting1
		passIn['lighting2'] = lighting2
		passIn['lighting3'] = lighting3
		passIn['lighting4'] = lighting4
		passIn['lighting5'] = lighting5
		passIn['lighting6'] = lighting6
		passIn['lighting7'] = lighting7
		passIn['lighting8'] = lighting8

		return render(request, self.template_name, passIn)

	def post(self, request):

		form = ""

		if('submitHVAC' in request.POST):
			form = self.form_class1(request.POST)
			
			if form.is_valid():
				loc = form.cleaned_data['hvacLoc']
				lowHigh = form.cleaned_data['lowHigh']
				temp = form.cleaned_data['temperature']

				result = bacnet.setHVAC(loc, lowHigh, temp)

				return redirect('main:index')

		if('submitLighting' in request.POST):
			form = self.form_class2(request.POST)
			
			if form.is_valid():
				zoneNum = form.cleaned_data['lightingZoneNumber']
				brightness = form.cleaned_data['brightness']

				result = bacnet.setLighting(zoneNum, brightness)

				return redirect('main:index')

		return render(request, self.template_name)


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
		return render(request, self.template_name)
	





