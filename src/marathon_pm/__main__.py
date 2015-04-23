import argparse

from .haproxy.create import CreateHAProxyConfCommand
from .haproxy.update import UpdateHAProxyConfCommand
from .nginx.create import CreateNginxConfCommand
from .nginx.update import UpdateNginxConfCommand

NGINX = u'nginx'
HAPROXY = u'haproxy'

CREATE = u'create'
UPDATE = u'update'

ACTIONS_DICT = {
   NGINX: {CREATE: CreateNginxConfCommand, UPDATE: UpdateNginxConfCommand},
   HAPROXY: {CREATE: CreateHAProxyConfCommand, UPDATE: UpdateHAProxyConfCommand}
}


def main():
    parser = argparse.ArgumentParser(description='Manage nginx and haproxy configuration for marathon mesos.')
    parser.add_argument(u'server_type', choices=[NGINX, HAPROXY])
    parser.add_argument(u'action', choices=[CREATE, UPDATE])
    parser.add_argument(u'--conf-dir', nargs='?', default=None)
    parser.add_argument(u'--output-dir', nargs='?', default=None)
    parser.add_argument(u'--marathon-url', nargs='?', default=u'http://localhost:8080')
    parser.add_argument(u'--domain', nargs='?', default=u'localhost')
    parser.add_argument(u'--delete-unused', action='store_true', default=False)
    ns, _ = parser.parse_known_args()
    action_cls = ACTIONS_DICT.get(ns.server_type).get(ns.action)
    kwargs = dict(
        conf_dir=ns.conf_dir,
        output_dir=ns.output_dir,
        marathon_url=ns.marathon_url,
        domain=ns.domain,
        delete_unused=ns.delete_unused,
    )
    action = action_cls(**kwargs)
    return action(**kwargs)

main()
