import requests

BaseURL = "https://cory406.eecs.berkeley.edu/rest_api/"
Token = ""


def login(username, password, request):
	params = {'username': username, 'password': password}
	r = requests.post(BaseURL + "api-token-auth/", params, verify=False)
	results = r.json()
	print(results)

	if("token" in results.keys()):
		Token = results["token"]
		request.session['token'] = Token
		return "success"
	else:
		return "failed"
