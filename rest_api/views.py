import logging
import json

from rest_framework.authentication import TokenAuthentication

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

import datetime

from django.db import transaction
from django.db.models import Q
from . import bacnet



# At end of session call with valid token and the token will be destroyed.
class ChartView(APIView):

	def get(self, request):
		passIn = {}
		chartType = request.GET.get('typeOfCredit')
		xinterval = request.GET.get('xinterval')
		duration = request.GET.get('duration')
		data = {}

		if(chartType == "1"):
			data = bacnet.getHVACHistory("north", "temp", xinterval, duration, "*");
		else:
			data = bacnet.getLightingHistory(1, xinterval, duration, "*");

		data = data['Items']

		if(xinterval == "1h"):
			data = [(x["Value"], x["Timestamp"][11:16]) for x in data]
		else:
			data = [(x["Value"], x["Timestamp"][5:10]) for x in data]

		labels = [str(x[1]) for x in data]
		vals = [x[0] for x in data]
		passIn['labels'] = labels
		passIn['vals'] = vals

		return Response(passIn)





