import requests

url2 = "http://127.0.0.1:8000/items"

data_logowanie = {
    "login_or_email": "John12",
    "password": "ZaQ1@wSx"
}

response2 = requests.post(url2, json=data_logowanie)


if response2.status_code == 200:
    print("Response:", response2.json())
else:
    print("POST request 2 failed! Status code:", response2.status_code)
    print("Response content:", response2.text)