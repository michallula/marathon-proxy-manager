#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  Copyright (c) 2015 Lingaro

import os
import subprocess

from marathon import MarathonClient
from jinja2 import Environment, ChoiceLoader, FileSystemLoader, PackageLoader


class MarathonProxyManagerCommand(object):

    DEFAULT_TEMPLATE_LOADER = PackageLoader(u'marathon_proxy_manager', u'templates')
    DEFAULT_MARATHON_URL = u'http://localhost:8080'
    DEFAULT_DOMAIN = u'localhost'
    DEFAULT_TEMPLATE_PATH = None
    DEFAULT_TEMPLATE_NAME = u'nginx.tmpl'
    DEFAULT_CONF_DIR = u'/etc/nginx'
    DEFAULT_OUT_DIR = None
    DEFAULT_DELETE_UNUSED = False
    DEFAULT_OVERRIDE = False
    DEFAULT_RELOAD = False
    DEFAULT_GENERATE_FOR_SUSPENDED = False
    DEFAULT_APPS = ()
    DEFAULT_EXCLUDE = ()

    _template = None

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

    @classmethod
    def reload_nginx_conf(cls):
        subprocess.call([u"service", u"nginx", u"reload"])

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

    @property
    def template(self):
        if self._template is None:
            self._template = self.template_env.get_template(self._template_name)
        return self._template

    def __init__(self, *args, **kwargs):
        self._marathon_url = kwargs.get(u'marathon_url', self.DEFAULT_MARATHON_URL)
        self._conf_dir = kwargs.get(u'conf_dir', self.DEFAULT_CONF_DIR) or self.DEFAULT_CONF_DIR
        self._out_dir = kwargs.get(u'output_dir', self.DEFAULT_OUT_DIR) or self._conf_dir
        self._template_path = kwargs.get(u'template_dir', self.DEFAULT_TEMPLATE_PATH)
        self._template_name = kwargs.get(u'template_name', self.DEFAULT_TEMPLATE_NAME)
        self._delete_unused = kwargs.get(u'delete_unused', self.DEFAULT_DELETE_UNUSED)
        self._reload = kwargs.get(u'reload', self.DEFAULT_RELOAD)
        self._override = kwargs.get(u'override', self.DEFAULT_OVERRIDE)
        self._apps = tuple(kwargs.get(u'apps', self.DEFAULT_APPS))
        self._exclude = tuple(kwargs.get(u'exclude', self.DEFAULT_EXCLUDE))
        self._generate_for_suspended = kwargs.get(u'generate_for_suspended', self.DEFAULT_GENERATE_FOR_SUSPENDED)

    def get_tasks(self):
        return self.marathon_cli.list_tasks()

    def get_apps(self):
        return self.marathon_cli.list_apps()

    def group_tasks(self, apps, tasks):
        return dict((app, [task for task in tasks if task.app_id == app.id]) for app in apps)

    def should_process(self, app, tasks):
        app_name = app.id[1:]
        if not self._generate_for_suspended and not bool(tasks):
            return False
        if self._apps:
            return app_name in (set(self._apps) - set(self._exclude))
        elif self._exclude:
            return app_name not in self._exclude
        return True

    def apps_generator(self):
        all_apps = self.get_apps()
        all_tasks = self.get_tasks()
        grouped_tasks = self.group_tasks(all_apps, all_tasks)
        for app, tasks in grouped_tasks.iteritems():
            if self.should_process(app, tasks):
                yield (app, tasks)

    def render_conf(self, app, tasks, *args, **kwargs):
        return self.template.render(app=app, tasks=tasks, **dict(*args, **kwargs))

    def read_conf(self, app_name):
        file_path = os.path.join(self._conf_dir, u'sites-enabled', app_name)
        if os.path.isfile(file_path):
            with open(file_path, u'r') as file:
                return file.read()

    def write_conf(self, app_name, conf):
        avail_file_path = os.path.join(self._out_dir, u'sites-available', app_name)
        with open(avail_file_path, u'w+') as file:
            file.write(conf)
        enabled_file_path = os.path.join(self._out_dir, u'sites-enabled', app_name)
        if self._override and os.path.isfile(enabled_file_path):
            os.remove(enabled_file_path)
        if not os.path.isfile(enabled_file_path):
            os.symlink(avail_file_path, enabled_file_path)

    def delete_unused_conf(self, apps=None, excluded=None):
        apps = apps or ()
        excluded = excluded or ()
        modified = ()
        for dir_name in (u'sites-available', u'sites-enabled'):
            dir_path = os.path.join(self._out_dir, dir_name)
            for file_name in os.listdir(os.path.join(dir_path)):
                if (not apps or file_name in apps) and (file_name not in excluded):
                    path = os.path.join(dir_path, file_name)
                    if os.path.isfile(path):
                        modified += (file_name,)
                        os.remove(path)
        return modified

    def should_override(self, app_name, conf, old_conf=None):
        return old_conf is None or (self._override and conf != old_conf)

    def __call__(self, *args, **kwargs):
        apps = ()
        modified = False
        for app, tasks in self.apps_generator():
            app_name = app.id[1:]
            conf = self.render_conf(app, tasks, *args, **kwargs)
            old_conf = self.read_conf(app_name)
            apps += (app_name,)
            if self.should_override(app_name, conf, old_conf):
                self.write_conf(app_name, conf)
                modified = True
        if self._delete_unused:
            if self.delete_unused_conf(apps=self._apps, excluded=self._exclude + apps):
                modified = True
        if self._reload and modified:
            self.reload_nginx_conf()
