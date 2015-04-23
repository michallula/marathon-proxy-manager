
__author__ = 'michal'

from .common import NginxMarathonPMCommand


class CreateNginxConfCommand(NginxMarathonPMCommand):

    def __call__(self, *args, **kwargs):
        tasks = self.get_tasks()
        grouped_tasks = self.group_tasks(tasks)
        conf_modified = False
        for app_name, tasks in grouped_tasks.iteritems():
            conf = self.render_conf(app_name, tasks, *args, **kwargs)
            old_conf = self.read_conf(app_name)
            if not old_conf or conf != old_conf:
                self.write_conf(app_name, conf)
                conf_modified = True
        if self._delete_unused:
            if self.delete_unused_confs(skip=grouped_tasks.keys()):
                conf_modified = True
        if conf_modified:
            self.reload_nginx_config()
