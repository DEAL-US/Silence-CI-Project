import requests

from utils import BASE_URL

def try_login_empty():
    data = {}
    r = requests.post(BASE_URL + "/login", json=data)
    assert r.status_code == 400
    assert "sessionToken" not in r.json()

def try_login_no_password():
    data = {
        "email": "pruebas@company.com",
    }
    r = requests.post(BASE_URL + "/login", json=data)
    assert r.status_code == 400
    assert "sessionToken" not in r.json()

def try_login_no_id():
    data = {
        "password": "pruebas",
    }
    r = requests.post(BASE_URL + "/login", json=data)
    assert r.status_code == 400
    assert "sessionToken" not in r.json()

def try_login_incorrect_email():
    data = {
        "email": "notexists@null.com",
        "password": "pruebas",
    }
    r = requests.post(BASE_URL + "/login", json=data)
    assert r.status_code == 400
    assert "sessionToken" not in r.json()

def try_login_incorrect_password():
    data = {
        "email": "pruebas@company.com",
        "password": "djgnhasfkjghnahslfkjfgjkl",
    }
    r = requests.post(BASE_URL + "/login", json=data)
    assert r.status_code == 400
    assert "sessionToken" not in r.json()

def try_login_ok():
    data = {
        "email": "pruebas@company.com",
        "password": "pruebas",
    }
    r = requests.post(BASE_URL + "/login", json=data)
    assert r.status_code == 200
    assert "sessionToken" in r.json()

def run():
    print("Testing /login...")
    try_login_empty()
    try_login_no_password()
    try_login_no_id()
    try_login_incorrect_email()
    try_login_incorrect_password()
    try_login_ok()