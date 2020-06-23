import requests

BASE_URL = "http://localhost:8080/api"

def get_token():
    # We assume that the testing user exists, as created by the register test
    data = {"email": "pruebas@company.com", "password": "pruebas"}
    r = requests.post(f"{BASE_URL}/login", data=data)
    assert r.status_code == 200
    resp = r.json()
    assert "sessionToken" in resp
    return resp["sessionToken"]
