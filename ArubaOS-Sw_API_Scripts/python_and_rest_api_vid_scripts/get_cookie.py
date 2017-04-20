import requests

url = "http://192.168.1.29/rest/v1/login-sessions"

payload = "{\"userName\": \"joe\", \"password\": \"x\"}"

response = requests.request("POST", url, data=payload)

print(response.text)
print(response.headers)



