import requests
from decouple import config
import time

######

localhost8000uvicorn = "http://127.0.0.1:8000"
URL: str = str(config("TEST_API_URL", default=localhost8000uvicorn))

defaultapikey = "thisisanapikey"
api_key: str = str(config("TEST_API_KEY", default=defaultapikey))

######

auth_headers = {
    'Content-Type': 'application/json',
    'api_token': api_key
}

print("### -- TESTING API -- ###")
print("get root:")
print(requests.get(URL).json())
print("get bep:")
print(requests.get(URL+"/bep/").json())
print("get door:")
print(requests.get(URL+"/door/").json())
print("get local:")
print(requests.get(URL+"/local/").json())

time_unix = int(time.time())
print("time_unix = " + str(time_unix))
print("PUT local with api_key:")
time_unix = int(time.time())
print(
    requests.put(
        URL+"/local/",
        json={
            "door_state": 1,
            "info": "testing api with api key",
            "update_time": "2021-01-01 00:00:00",
            "update_time_unix": time_unix,
            "temperature": 21,
            "humidity": 50
        },
        headers=auth_headers
    ).json()
)

print("get local:")
print(requests.get(URL+"/local/").json())
print("get door:")
print(requests.get(URL+"/door/").json())

print("PUT local without api_key:")
print(
    requests.put(
        URL+"/local/",
        json={
            "door_state": 0,
            "info": "testing api",
            "update_time": "2023-01-01 00:30:00",
            "update_time_unix": time_unix,
            "temperature": 31,
            "humidity": 99
        }
    ).json()
)

print("get local:")
print(requests.get(URL+"/local/").json())
print("get door:")
print(requests.get(URL+"/door/").json())

print("get temp:")
print(requests.get(URL+"/temp/").json())
print("post test:")
print(requests.post(URL+"/test/").json())

print("## -- END TESTING API -- ##")

