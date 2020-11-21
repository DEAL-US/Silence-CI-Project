from silence.decorators import endpoint

@endpoint(
    route="/departments",
    method="GET",
    sql="SELECT * FROM Departments",
)
def get_all():
    pass

###############################################################################

@endpoint(
    route="/departments/$departmentId",
    method="GET",
    sql="SELECT * FROM Departments WHERE departmentId = $departmentId",
)
def get_by_id():
    pass

###############################################################################

@endpoint(
    route="/departments",
    method="POST",
    sql="INSERT INTO Departments (name, city) VALUES ($name, $city)",
    auth_required=True,
)
def add(name, city):
    pass

###############################################################################

@endpoint(
    route="/departments/$departmentId",
    method="PUT",
    sql="UPDATE Departments SET name = $name, city = $city WHERE departmentId = $departmentId",
    auth_required=True,
)
def update(name, city):
    pass

###############################################################################

@endpoint(
    route="/departments/$departmentId",
    method="DELETE",
    sql="DELETE FROM Departments WHERE departmentId = $departmentId",
    auth_required=True,
)
def delete():
    pass
