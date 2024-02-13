import re

#FOR production
RE_USER = re.compile(r"MYSQL_USER:\s*(\w+)", re.I)
RE_PWD = re.compile(r"MYSQL_PASSWORD:\s*(\w+)", re.I)
RE_DB = re.compile(r"MYSQL_DATABASE:\s*(\w+)", re.I)

# for local testing add the .github folder at the same level as the CI project, then swap these lines.
# ci_yml = open("./.github/workflows/ci_test.yml", "r", encoding="utf-8").read() 
ci_yml = open("../.github/workflows/ci_test.yml", "r", encoding="utf-8").read()


dbuser = RE_USER.search(ci_yml).group(1)
dbpwd = RE_PWD.search(ci_yml).group(1)
dbname = RE_DB.search(ci_yml).group(1)

###############################################################################
# Project-specific settings
###############################################################################

# Shows debug messages while Silence is running
DEBUG_ENABLED = False

# Database connection details
DB_CONN = {
    "host": "127.0.0.1",
    "port": 3306,
    "username": dbuser,
    "password": dbpwd,
    "database": dbname,
}

# The sequence of SQL scripts located in the sql/ folder that must
# be ran when the 'silence createdb' command is issued
SQL_SCRIPTS = [
    "create_tables.sql",
    "create_views.sql",
    "populate_database.sql",
]

# The port in which the API and the web server will be deployed
HTTP_PORT = 8080

# The URL prefix for all API endpoints
API_PREFIX = "/api"

# Table and fields that are used for both login and register
USER_AUTH_DATA = {
    "table": "Employees",
    "identifier": "email",
    "password": "password",
    "role": "position",
    "active_status": "isActive"
}

# for local testing add a secret key here.

