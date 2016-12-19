import requests
import json

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
	headers = {'Authorization': "Token " + token, 'content-type': 'application/json'}
	params = {'to_user_id': recipient, 'credit_type_id': creditType, 'quantity': amount}

	r = requests.post(BaseURL + "gift_credit/", data=json.dumps(params), headers=headers, verify=False)
	results = r.json()

	return "success"

def getUsers(request):
	temp = request
	token = temp.session['token']
	headers = {'Authorization': "Token " + token}
	r = requests.get(BaseURL + "get_users/", headers=headers, verify=False)
	
	userList = []
	results = r.json()

	for user in results:
		userID = user["id"]
		name = user["owner"]
		tempUser = User(userID, name)
		userList.append(tempUser)

	return userList

class User:
	def __init__(self, idInput, name):
		self.id= idInput
		self.name = name







