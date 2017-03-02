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
		electricity = float(tup[0])
		water = float(tup[1])
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

		passIn['lighting1'] = min(lighting1, 100)
		passIn['lighting2'] = lighting2
		passIn['lighting3'] = lighting3
		passIn['lighting4'] = lighting4
		passIn['lighting5'] = lighting5
		passIn['lighting6'] = lighting6
		passIn['lighting7'] = lighting7
		passIn['lighting8'] = lighting8

		userList = services.getUsers(request)

		passIn['userList'] = userList

		data = bacnet.getHVACHistory("north", "temp", "1d", "-7d", "*");

		data = data['Items']
		data = [(x["Value"], x["Timestamp"][5:10]) for x in data]
		labels = [str(x[1]) for x in data]
		vals = [x[0] for x in data]
		
		passIn['HVAClabels'] = labels
		passIn['HVACvals'] = vals

		data = bacnet.getBlinds();
		passIn['Blindvals'] = data

		return render(request, self.template_name, passIn)

	def post(self, request):

		if('submitHVAC' in request.POST):
			return postHelper("HVAC", self, request)
		elif('submitSendCredit' in request.POST):
			return postHelper("trade", self, request)
		elif('submitLighting' in request.POST):
			return postHelper("lighting", self, request)
		elif('submitBlinds' in request.POST):
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

		elif(submitType == "lighting"):
			zoneNum = 1
			brightness = form.cleaned_data['brightness']

			result = bacnet.setLighting(zoneNum, brightness)

			return redirect('main:index')
		else:
			print("\n \n YOLOBBY \n \n ")
			percentage = form.cleaned_data['height']
			result = bacnet.setBlinds(percentage)

			return redirect('main:index')




	return render(request, self.template_name)

class GraphsView(View):
	template_name = 'main/graphs.html'

	def get(self, request):

		data = bacnet.getHVACHistory("north", "temp", "1d", "-7d", "*");

		data = data['Items']
		data = [(x["Value"], x["Timestamp"][5:10]) for x in data]
		labels = [str(x[1]) for x in data]
		vals = [x[0] for x in data]

		passIn = {}
		passIn['HVAClabels'] = labels
		passIn['HVACvals'] = vals

		data = bacnet.getLightingHistory(1, "1d", "-7d", "*");

		data = data['Items']
		data = [(x["Value"], x["Timestamp"][5:10]) for x in data]
		labels = [str(x[1]) for x in data]
		vals = [x[0] for x in data]

		passIn['Lightinglabels'] = labels
		passIn['Lightingvals'] = vals


		return render(request, self.template_name, passIn)








