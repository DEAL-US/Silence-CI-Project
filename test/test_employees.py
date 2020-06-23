import requests

from utils import BASE_URL, get_token

def get_all():
    r = requests.get(BASE_URL + "/employees")
    assert r.status_code == 200
    return r.json()

###############################################################################

def try_get_all_sorted():
    emps = get_all()
    for attr in emps[0]:
        for order in ("asc", "desc"):
            r = requests.get(f"{BASE_URL}/employees?_sort={attr}&_order={order}")
            assert r.status_code == 200
            sorted_api = r.json()
            for e1, e2 in zip(sorted_api, sorted_api[1:]):
                if order == "asc":
                    assert str(e1[attr]) <= str(e2[attr])
                else:
                    assert str(e1[attr]) >= str(e2[attr])

def try_get_all_filtered():
    filtered_pairs = []

    emps = get_all()
    for emp in emps:
        for attr in emp:
            val = emp[attr]
            pair = (attr, val)
            if pair in filtered_pairs: continue
            filtered_pairs.append(pair)

            r = requests.get(f"{BASE_URL}/employees?{attr}={val}")
            assert r.status_code == 200
            filtered_emps = list(filter(lambda x: x[attr] == val, emps))
            api_res = r.json()
            assert len(filtered_emps) == len(api_res)
            assert all(x in api_res for x in filtered_emps)

def try_get_all_paginated():
    emps = get_all()
    n_emps = len(emps)

    for limit in range(1, n_emps + 1):
        page = 0
        while limit * page < n_emps:
            r = requests.get(f"{BASE_URL}/employees?_limit={limit}&_page={page}")
            assert r.status_code == 200
            api_res = r.json()
            paginated = emps[limit * page:limit * (page + 1)]
            assert len(api_res) == len(paginated)
            assert all(x in api_res for x in paginated)
            page += 1

def try_get_one_ok():
    dpmts = get_all()

    for dpmt in dpmts:
        dpmt_id = dpmt["departmentId"]
        r = requests.get(f"{BASE_URL}/employees/{dpmt_id}")
        assert r.status_code == 200
        resp = r.json()
        assert len(resp) == 1
        assert r.json()[0] == dpmt

def try_get_one_not_exists():
    r = requests.get(f"{BASE_URL}/employees/2522461635631")
    assert r.status_code == 404

def try_create_unauthorized():
    dpmts_before = get_all()
    data = {"name": "Department of testing", "city": "Testingville"}
    r = requests.post(f"{BASE_URL}/employees", data=data)
    dpmts_after = get_all()
    assert r.status_code == 401
    assert dpmts_before == dpmts_after

def try_create_ok():
    dpmts_before = get_all()
    token = get_token()
    headers = {"Token": token}
    data = {"name": "Department of testing", "city": "Testingville"}
    r = requests.post(f"{BASE_URL}/employees", data=data, headers=headers)
    dpmts_after = get_all()
    assert r.status_code == 200
    assert len(dpmts_before) + 1 == len(dpmts_after)
    createdId = r.json()["lastId"]

    created = requests.get(f"{BASE_URL}/employees/{createdId}").json()[0]
    for field in data:
        assert data[field] == created[field]

def try_create_repeated():
    dpmts_before = get_all()
    token = get_token()
    headers = {"Token": token}
    data = {"name": "Department of testing", "city": "Testingville"}
    r = requests.post(f"{BASE_URL}/employees", data=data, headers=headers)
    dpmts_after = get_all()
    assert r.status_code == 400
    assert len(dpmts_before) == len(dpmts_after)

def try_edit_unauthorized():
    dpmt = get_all()[0]
    dpmt_id = dpmt["departmentId"]

    data = {"name": "Tests Department", "city": "Land of Testing"}
    r = requests.put(f"{BASE_URL}/employees/{dpmt_id}", data=data)
    
    assert r.status_code == 401
    dpmt_after = requests.get(f"{BASE_URL}/employees/{dpmt_id}").json()[0]
    assert dpmt == dpmt_after

def try_edit_ok():
    dpmt = get_all()[0]
    dpmt_id = dpmt["departmentId"]

    token = get_token()
    headers = {"Token": token}
    data = {"name": "Tests Department", "city": "Land of Testing"}
    r = requests.put(f"{BASE_URL}/employees/{dpmt_id}", data=data, headers=headers)
    
    assert r.status_code == 200
    dpmt_after = requests.get(f"{BASE_URL}/employees/{dpmt_id}").json()[0]
    for field in data:
        assert data[field] == dpmt_after[field]

def try_delete_unauthorized():
    dpmts_before = get_all()
    dpmt = dpmts_before[0]
    dpmt_id = dpmt["departmentId"]

    r = requests.delete(f"{BASE_URL}/employees/{dpmt_id}")
    dpmts_after = get_all()
    
    assert r.status_code == 401
    assert dpmts_after == dpmts_before

def try_delete_ok():
    dpmts_first = get_all()
    token = get_token()
    headers = {"Token": token}
    data = {"name": "Department to be deleted", "city": "Nowhere"}

    r = requests.post(f"{BASE_URL}/employees", data=data, headers=headers)
    assert r.status_code == 200
    insertedId = r.json()["lastId"]
    dpmts_after_insert = get_all()
    assert len(dpmts_after_insert) == len(dpmts_first) + 1
    r = requests.get(f"{BASE_URL}/employees/{insertedId}")
    assert r.status_code == 200

    r = requests.delete(f"{BASE_URL}/employees/{insertedId}", headers=headers)
    assert r.status_code == 200
    dpmts_after_delete = get_all()
    assert dpmts_after_delete == dpmts_first
    r = requests.get(f"{BASE_URL}/employees/{insertedId}")

def run():
    print("Testing /employees...")
    try_get_all_sorted()
    try_get_all_filtered()
    try_get_all_paginated()
    #try_get_one_ok()
    #try_get_one_not_exists()
    #try_create_unauthorized()
    #try_create_ok()
    #try_create_repeated()
    #try_edit_unauthorized()
    #try_edit_ok()
    #try_delete_unauthorized()
    #try_delete_ok()
