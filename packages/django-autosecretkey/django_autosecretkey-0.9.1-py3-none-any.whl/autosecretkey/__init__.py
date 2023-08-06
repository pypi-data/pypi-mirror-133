import configparser

from django.core.management.utils import get_random_secret_key

class AutoSecretKey:
    @staticmethod
    def write_config_file(path, config):
        with open(path, "w") as outfile:
            config.write(outfile)

    @classmethod
    def read_config_file(cls, path, template=None, create=False):
        config = configparser.ConfigParser(interpolation=None)

        try:
            config.read(path)
                
        except FileNotFoundError:
            if not create:
                raise

            if template:
                config.read(template)
            
            cls.write_config_file(path, config)

        return config

    def write(self):
        self.__class__.write_config_file(self.path, self.config)

    def update(self, template=None, create=False):
        self.config = self.__class__.read_config_file(self.path, template, create)

    @property
    def secret_key(self):
        try:
            return self.config[self.section][self.config_key]
        except (KeyError, TypeError):
            new_key = get_random_secret_key()

            self.config[self.section] = { self.config_key: new_key }
            self.write()
            
            return new_key

    def __init__(self, path, section="AutoSecretKey", config_key="SecretKey", template=None, create=True):
        self.path = path
        self.section = section
        self.config_key = config_key
        self.update(template, create)
