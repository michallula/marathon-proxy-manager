
__author__ = 'michal'

import os
import subprocess

from ..command import MarathonPMCommand


class NginxMarathonPMCommand(MarathonPMCommand):

    DEFAULT_TEMPLATE_NAME = u'nginx.tmpl'
    DEFAULT_CONF_DIR = u'/etc/nginx'
    DELETE_UNUSED = False

    _template = None

    def __init__(self, *args, **kwargs):
        super(NginxMarathonPMCommand, self).__init__(*args, **kwargs)
        self._template_name = kwargs.get(u'template_name', self.DEFAULT_TEMPLATE_NAME)
        self._delete_unused = kwargs.get(u'delete_unused', self.DELETE_UNUSED)


    @property
    def template(self):
        if self._template is None:
            self._template = self.template_env.get_template(self._template_name)
        return self._template

    def get_tasks(self):
        return self.marathon_cli.list_tasks()

    def group_tasks(self, tasks):
        result = {}
        for task in tasks:
            app_name = task.app_id[1:]
            if app_name not in result:
                result[app_name] = []
            result[app_name].append(task)
        return result

    def render_conf(self, app_name, tasks, *args, **kwargs):
        return self.template.render(app_name=app_name, tasks=tasks, **dict(*args, **kwargs))

    def read_conf(self, app_name):
        file_path = os.path.join(self._conf_dir, 'sites-enabled', app_name)
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                return file.read()

    def write_conf(self, app_name, conf):
        avail_file_path = os.path.join(self._out_dir, 'sites-available', app_name)
        enabled_file_path = os.path.join(self._out_dir, 'sites-enabled', app_name)
        if os.path.isfile(enabled_file_path):
            os.remove(enabled_file_path)
        with open(avail_file_path, u'w+') as file:
            file.write(conf)
        os.symlink(avail_file_path, enabled_file_path)

    def reload_nginx_config(self):
        subprocess.call(["service", "nginx", "reload"])

    def delete_unused_confs(self, skip=None):
        skip = skip or ()
        modified = False
        for dir_name in ('sites-available', 'sites-enabled'):
            dir_path = os.path.join(self._out_dir, dir_name)
            for file_name in os.listdir(os.path.join(dir_path)):
                if not file_name in skip:
                    path = os.path.join(dir_path, file_name)
                    if os.path.isfile(path):
                        modified = True
                        os.remove(path)
        return modified
