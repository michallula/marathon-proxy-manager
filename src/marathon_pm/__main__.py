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
   NGINX: {CREATE: CreateNginxConfCommand(), UPDATE: UpdateNginxConfCommand()},
   HAPROXY: {CREATE: CreateHAProxyConfCommand(), UPDATE: UpdateHAProxyConfCommand()}
}


def main():
    parser = argparse.ArgumentParser(description='Manage nginx and haproxy configuration for marathon mesos.')
    parser.add_argument(u'server_type', choices=[NGINX, HAPROXY])
    parser.add_argument(u'action', choices=[CREATE, UPDATE])
    parser.add_argument(u'output-dir', nargs='?', default=u"dupa")
    args = parser.parse_args()
    kwargs = dict(args._get_kwargs())
    server_type = kwargs.pop(u'server_type')
    action_name = kwargs.pop(u'action')
    action = ACTIONS_DICT.get(server_type).get(action_name)
    return action(**kwargs)

main()
