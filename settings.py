import re

RE_DB = re.compile(r"create database (?:if not exists)?\s+(.*);", re.I)
RE_USER = re.compile(r"create user (?:if not exists)?\s*'(.*?)'.*identified by '(.*?)';", re.I)

travis_yml = open("../.travis.yml", "r", encoding="utf-8").read()

dbname = RE_DB.search(travis_yml).group(1)
user_m = RE_USER.search(travis_yml)
dbuser = user_m.group(1)
dbpwd = user_m.group(2)

###############################################################################
# Project-specific settings
###############################################################################

# Shows debug messages while Silence is running
DEBUG_ENABLED = False

# Database connection details
DB_CONN = {
    "host": "localhost",
    "port": 3306,
    "username": dbuser,
    "password": dbpwd,
    "database": dbname,
}

# The sequence of SQL scripts located in the sql/ folder that must
# be ran when the 'silence createdb' command is issued
SQL_SCRIPTS = [
    "create_tables.sql",
    "populate_database.sql"
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
}
