import requests

print("### -- TESTING API -- ###")
print("get root:")
print(requests.get("http://localhost:8000/").json())
print("get bep:")
print(requests.get("http://localhost:8000/bep/").json())
print("get door:")
print(requests.get("http://localhost:8000/door/").json())
print("get local:")
print(requests.get("http://localhost:8000/local/").json())

print("POST local:")
print(
    requests.post(
        "http://localhost:8000/local/",
        json={
            "door_state": 1,
            "info": "testing api",
            "upsate_time": "2021-01-01 00:00:00",
            "update_time_unix": 1610000000,
            "temperature": 21,
            "humidity": 50
        }
    ).json()
)
print("get local:")
print(requests.get("http://localhost:8000/local/").json())
print("get door:")
print(requests.get("http://localhost:8000/door/").json())

print("## -- END TESTING API -- ##")
