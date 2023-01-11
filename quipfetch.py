import requests

url = 'https://quip.bmi.stonybrook.edu/user/login?_format=json'
headers = { 'Content-Type': 'application/json' }
body = { 'name': 'jbalsamo', 'pass': 'H8tha1dr' }

resp = requests.post(url, json=body,headers=headers)
out = resp.json()

print(out.get('csrf_token'))

get_url = 'https://quip.bmi.stonybrook.edu/jwt/token'

#token = requests.get(get_url)

#rint(token)

