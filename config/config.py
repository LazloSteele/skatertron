import json
from os import mkdir
from os.path import realpath, dirname, join, isdir, isfile


my_dir = dirname(realpath(__file__))
secret_dir = r'secret'
config_path = join(my_dir, 'config.json')
user_path = join(my_dir, secret_dir, 'postgres_user_data.json')

if not isfile(user_path):
    new_user_name = input('enter postgres username: ')
    new_password = input('enter postgres password: ')

    if not isdir(join(my_dir, secret_dir)):
        mkdir(join(my_dir, secret_dir))

    pg_data_dict = {
        "user": new_user_name,
        "pw": new_password
    }

    pg_data_json = json.dumps(pg_data_dict)

    with open(join(my_dir, secret_dir, "postgres_user_data.json"), "w") as outfile:
        outfile.write(pg_data_json)

class Config:

    @staticmethod
    def user():
        with open(user_path, "r") as pg_json:
            pg_data = json.load(pg_json)
            return pg_data["user"]

    @staticmethod
    def pw():
        with open(user_path, "r") as pg_json:
            pg_data = json.load(pg_json)
            return pg_data["pw"]
