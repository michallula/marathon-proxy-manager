import argparse

from .nginx import MarathonProxyManagerCommand as Cmd


def main():
    parser = argparse.ArgumentParser(description=u'Manages nginx configuration for marathon mesos.')

    parser.add_argument(u'--conf-dir', nargs=u'?', default=Cmd.DEFAULT_CONF_DIR)
    parser.add_argument(u'--output-dir', nargs=u'?', default=Cmd.DEFAULT_OUT_DIR)
    parser.add_argument(u'--template-name', nargs=u'?', default=Cmd.DEFAULT_TEMPLATE_PATH)
    parser.add_argument(u'--marathon-url', nargs=u'?', default=Cmd.DEFAULT_MARATHON_URL)
    parser.add_argument(u'--domain', nargs=u'?', default=Cmd.DEFAULT_DOMAIN)
    parser.add_argument(u'--delete-unused', action=u'store_true', default=Cmd.DEFAULT_DELETE_UNUSED)
    parser.add_argument(u'--override', action=u'store_true', default=Cmd.DEFAULT_OVERRIDE)
    parser.add_argument(u'--reload', action=u'store_true', default=Cmd.DEFAULT_RELOAD)
    parser.add_argument(u'--apps', nargs=u'*', type=str, default=Cmd.DEFAULT_APPS)
    parser.add_argument(u'--exclude', nargs=u'*', type=str, default=Cmd.DEFAULT_EXCLUDE)

    ns, _ = parser.parse_known_args()

    kwargs = dict(
        conf_dir=ns.conf_dir,
        output_dir=ns.output_dir,
        marathon_url=ns.marathon_url,
        domain=ns.domain,
        delete_unused=ns.delete_unused,
        override=ns.override,
        reload=ns.reload,
        apps=ns.apps,
        exclude=ns.exclude
    )

    action = Cmd(**kwargs)
    return action(**kwargs)

main()
