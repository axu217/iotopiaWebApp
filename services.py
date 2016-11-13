import requests

BaseURL = "https://cory406.eecs.berkeley.edu/rest_api/"
Token = ""


def login(username, password):
	params = {'username': username, 'password': password}
	r = requests.post(BaseURL + "api-token-auth/", params, verify=False)
	results = r.json()
	print(results)

	if("token" in results.keys()):
		Token = results["token"]
		return "success"
	else:
		return "failed"
