__author__ = 'michal'

import abc

from marathon import MarathonClient
from jinja2 import Environment, ChoiceLoader, FileSystemLoader, PackageLoader


class MarathonPMCommand(object):

    __metaclass__ = abc.ABCMeta

    DEFAULT_TEMPLATE_LOADER = PackageLoader(u'marathon_pm', u'templates')
    DEFAULT_MARATHON_URL = u'http://localhost:8080'
    DEFAULT_CONF_DIR = u''

    _template_env = None
    _marathon_cli = None

    @classmethod
    def create_marathon_client(cls, marathon_url):
        return MarathonClient(marathon_url)

    @classmethod
    def create_template_loader(cls, template_path=None):
        if template_path is not None:
            return ChoiceLoader([
                FileSystemLoader(template_path),
                cls.DEFAULT_TEMPLATE_LOADER
            ])
        else:
            return cls.DEFAULT_TEMPLATE_LOADER

    @classmethod
    def create_template_env(cls, loader):
        return Environment(loader=loader)

    @property
    def template_env(self):
        if self._template_env is None:
            self._template_env = self.create_template_env(
                loader=self.create_template_loader(
                    template_path=self._template_path
                )
            )
        return self._template_env

    @property
    def marathon_cli(self):
        if self._marathon_cli is None:
            self._marathon_cli = self.create_marathon_client(self._marathon_url)
        return self._marathon_cli

    def __init__(self, *args, **kwargs):
        self._template_path = kwargs.get(u'template_path', None)
        self._marathon_url = kwargs.get(u'marathon_url', self.DEFAULT_MARATHON_URL)
        self._conf_dir = kwargs.get(u'conf_dir', self.DEFAULT_CONF_DIR) or self.DEFAULT_CONF_DIR
        self._out_dir = kwargs.get(u'output_dir', self._conf_dir) or self._conf_dir

    @abc.abstractmethod
    def __call__(self, *args, **kwargs):
        pass

