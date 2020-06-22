import requests
from werkzeug.security import check_password_hash

from base import BASE_URL

def get_all_employees():
    return requests.get(BASE_URL + "/employees").json()

def try_register_no_user():
    data = {
        "password": "123456",
        "departmentId": None,
        "bossId": 1,
        "firstName": "Pepito",
        "lastName": "Pruebas",
        "salary": 1337.00,
    }
    emps_before = get_all_employees()
    r = requests.post(BASE_URL + "/register", json=data)
    assert r.status_code == 400
    emps_after = get_all_employees()
    assert emps_after == emps_before

def try_register_no_password():
    data = {
        "email": "pepito@company.com",
        "departmentId": None,
        "bossId": 1,
        "firstName": "Pepito",
        "lastName": "Pruebas",
        "salary": 1337.00,
    }
    emps_before = get_all_employees()
    r = requests.post(BASE_URL + "/register", json=data)
    assert r.status_code == 400
    emps_after = get_all_employees()
    assert emps_after == emps_before

def try_register_repeated_email():
    emps_before = get_all_employees()
    data = {
        "email": emps_before[0]["email"],
        "password": "123456",
        "departmentId": None,
        "bossId": 1,
        "firstName": "Pepito",
        "lastName": "Pruebas",
        "salary": 1337.00,
    }
    r = requests.post(BASE_URL + "/register", json=data)
    assert r.status_code == 400
    emps_after = get_all_employees()
    assert emps_after == emps_before

def try_register_ok():
    data = {
        "email": "pruebas@company.com",
        "password": "pruebas",
        "departmentId": None,
        "bossId": 1,
        "firstName": "Pepito",
        "lastName": "Pruebas",
        "salary": 1337.00,
    }
    emps_before = get_all_employees()
    r = requests.post(BASE_URL + "/register", json=data)
    assert r.status_code == 200
    resp_data = r.json()

    emps_after = get_all_employees()
    assert len(emps_after) == len(emps_before) + 1

    assert "sessionToken" in resp_data
    assert "user" in resp_data

    resp_user = resp_data["user"]
    for k in data:
        if k != "password":
            assert data[k] == resp_user[k]

def run():
    try_register_no_user()
    try_register_no_password()
    try_register_repeated_email()
    try_register_ok()