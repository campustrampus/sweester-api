"""
Manages configuration values.
"""
import os
from base64 import b64decode
import yaml
import boto3

from sweester.utils.logger import get_logger

LOGGER = get_logger(__name__)

CONFIG_DEFAULT = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.yaml')


class Singleton(type):
    """
    A metaclass that creates a Singleton base class when called.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """overriding __call__"""
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

    @classmethod
    def reset(mcs):
        """tear down class instances"""
        mcs._instances = {}


# pylint: disable=too-few-public-methods
class Config(metaclass=Singleton):
    """
    Config class derived from Singleton
    """
    def __init__(self, config_file=CONFIG_DEFAULT):
        super(Config, self).__init__()
        self.config_file = config_file
        if not os.path.isfile(self.config_file):
            self.settings = {}
            return
        with open(self.config_file, "r") as conf:
            LOGGER.info("reading %s", self.config_file)
            data = yaml.safe_load(conf)
            self.settings = flatten_object(data)


def is_kms_encrypted(val):
    """
    Check if a value is kms encrypted.
    :param val: The value that might be KMS encrypted.
    :return: A boolean that indicates whether or not the value was KMS encrypted.
    """
    result = False
    text = str(val)
    if len(text) > 128 and ' ' not in text:
        try:
            b64decode(text)
            result = True
        except TypeError:
            pass
    return result


def flatten_object(obj, result=None):
    """
    Convert an object to a flatten dictionary
    example: { "db": { "user": "bar" }} becomes {"db.user": "bar" }
    """
    if not result:
        result = {}

    def _flatten(key_obj, name=''):
        if isinstance(key_obj, dict):
            for item in key_obj:
                arg = str(name) + str(item).replace('_', '.') + '.'
                _flatten(key_obj[item], arg)
        elif isinstance(key_obj, list):
            index = 0
            for item in key_obj:
                arg = str(name) + str(index) + '.'
                _flatten(item, arg)
                index += 1
        else:
            result[name[:-1]] = key_obj

    _flatten(obj)
    return result


def get_boolean(key_name, default_value=False):
    """
    Get boolean value for a key; otherwise, return default value.
    """
    if not key_name:
        return default_value

    key_val = str(settings(str(key_name))).lower()
    if key_val in ["1", "on", "true", "yes"]:
        return True
    return False if key_val else default_value


def get_uint(key_name, default_value=0):
    """
    Get unsigned integer value for a key; otherwise, return default value.
    """
    result = default_value
    if key_name:
        key_val = settings(str(key_name))
        key_int = int(key_val) if key_val.isdigit() else 0
        result = key_int if key_int > 0 else default_value
    return result


def settings(setting_key=None, default_value=''):
    """
    Get the instance by a key in application settings (config.yaml file)
    example: print(settings('mysql.database'))
    """
    config = Config().settings
    result = ''

    if not setting_key:
        return config

    env_var = str.replace(setting_key, ".", "_").upper()
    key_val = os.environ.get(env_var, '')

    if not key_val:
        key_val = config.get(setting_key, default_value)

    if ('password' or 'key' in setting_key) and is_kms_encrypted(key_val):
        result = boto3.client('kms').decrypt(CiphertextBlob=b64decode(key_val))['Plaintext']
    elif key_val:
        result = key_val

    return result
