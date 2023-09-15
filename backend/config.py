import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

database_password_local = os.environ.get("DB_PASSWORD_LOCAL")
database_password_unit_test = os.environ.get("DB_PASSWORD_UNIT_TEST")