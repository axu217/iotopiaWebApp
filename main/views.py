from django.shortcuts import render, redirect
from django.views.generic import View
from . import services
from . import bacnet
from .forms import SubmitForm, HVACForm, LightingForm, BlindsForm

# Create your views here.
class MainView(View):
	template_name = 'main/home.html'
	
	def get(self, request):
		tup = services.getBalances(request)
		electricity = int(tup[0])
		water = int(tup[1])
		ePercent = electricity / 50
		wPercent = water/ 50

		passIn = {'electricity': electricity, 'water': water, 'electricityPercentage' : ePercent, 'waterPercentage': wPercent}
	
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

		userList = services.getUsers(request)

		passIn['userList'] = userList

		return render(request, self.template_name, passIn)

	def post(self, request):

		if('submitHVAC' in request.POST):
			return postHelper("HVAC", self, request)
		elif('submitSendCredit' in request.POST):
			return postHelper("trade", self, request)
		elif('submitLighting' in request.POST):
			return postHelper("lighting", self, request)
		elif('submitLighting' in request.POST):
			return postHelper("blinds", self, request)  
		else:
			return 0

def postHelper(submitType, passView, request):

	if(submitType == "HVAC"):
		passView.form_class = HVACForm
	elif(submitType == "trade"):
		passView.form_class = SubmitForm
	elif(submitType == "lighting"):
		passView.form_class = LightingForm
	else:
		passView.form_class = BlindsForm

	form = passView.form_class(request.POST)

	if form.is_valid():
		if(submitType == "HVAC"):
			low = form.cleaned_data['low']
			high = form.cleaned_data['high']

			bacnet.setHVAC(1, "Low", low)
			bacnet.setHVAC(1, "High", high)

			return redirect('main:index')
			
		elif(submitType == "trade"):

			recipient = form.cleaned_data['recipient']
			amount = form.cleaned_data['amount']
			energyType = form.cleaned_data['energyType']
			result = services.sendCredit(request, int(recipient), int(amount), int(energyType))

			return redirect('main:index')

		else:
			zoneNum = 1
			brightness = form.cleaned_data['brightness']

			result = bacnet.setLighting(zoneNum, brightness)

			return redirect('main:index')

	return render(request, self.template_name)

class GraphsView(View):
	template_name = 'main/graphs.html'

	def get(self, request):

		data = bacnet.getHVACHistory("north", "temp", "1d", "-7d", "8");
		

		return render(request, self.template_name)
