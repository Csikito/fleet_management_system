import configparser

ini = configparser.ConfigParser()
ini.read(".fleet.ini")


def get_uri(uri_dict):
    uri = f"{uri_dict['dialect']}://{uri_dict['username']}:{uri_dict['password']}@{uri_dict['host']}:{uri_dict['port']}/{uri_dict['database']}"
    return uri


class DatabaseConfig(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    def __init__(self, flask_app):
        self.__class__.SECRET_KEY = ini[flask_app]["secret_key"].encode()

class Config(DatabaseConfig):
    SQLALCHEMY_DATABASE_URI = get_uri(ini["SQLALCHEMY_DATABASE_URI"])


class TestConfig(DatabaseConfig):
    SQLALCHEMY_DATABASE_URI = get_uri(ini["SQLALCHEMY_TEST_DATABASE_URI"])
