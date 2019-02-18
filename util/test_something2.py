import requests

base_url = "https://dt-dev.arctron.cn/api"

url = base_url + "/user/login"
data = {
    "email": "demo",
    "password": "123456"
}


resp = requests.post(url,data)

req_header = resp.request.headers
print(req_header)