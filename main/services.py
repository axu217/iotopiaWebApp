import requests

BaseURL = "https://cory406.eecs.berkeley.edu/rest_api/"
Token = ""


def getBalances(request):
	temp = request
	token = temp.session['token']
	headers = {'Authorization': "Token " + token}
	r = requests.get(BaseURL + "get_credit_balances/", headers=headers, verify=False)
	results = r.json()
	
	electricity = results[0]['balance']
	water = results[1]['balance']

	return(electricity, water)

def sendCredit(request, recipient, amount, creditType):
	temp = request
	token = temp.session['token']
	headers = {'Authorization': "Token " + token}
	params = {'to_user_id': recipient, 'credit_type_id': creditType, 'quantity': amount}

	r = requests.post(BaseURL + "gift_credit/", headers=headers, params=params, verify=False)
	results = r.json()

	print("yey")
	print("yey")
	print("yey")

	print(results)

	print("yey")
	print("yey")
	print("yey")

	return "bruh"

	

