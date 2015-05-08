#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  Copyright (c) 2015 Lingaro

import argparse

from .nginx import MarathonProxyManagerCommand as Cmd


def main():
    parser = argparse.ArgumentParser(description=u'Manages nginx configuration for marathon mesos.')

    parser.add_argument(u'--conf-dir',
                        nargs=u'?',
                        default=Cmd.DEFAULT_CONF_DIR,
                        help=u"Nginx config directory path")
    parser.add_argument(u'--output-dir',
                        nargs=u'?',
                        default=Cmd.DEFAULT_OUT_DIR,
                        help=u"script output dir path where the generated configuration will be written to")
    parser.add_argument(u'--template-dir',
                        nargs=u'?',
                        default=Cmd.DEFAULT_TEMPLATE_PATH,
                        help=u"template directory where nginx.tmpl file is stored"
                        )
    parser.add_argument(u'--template-name',
                        nargs=u'?',
                        default=Cmd.DEFAULT_TEMPLATE_NAME,
                        help=u"name of template file, default is nginx.tmpl"
                        )
    parser.add_argument(u'--marathon-url',
                        nargs=u'?',
                        default=Cmd.DEFAULT_MARATHON_URL,
                        help=u"full url to marathon instance (with scheme)")
    parser.add_argument(u'--domain',
                        nargs=u'?',
                        default=Cmd.DEFAULT_DOMAIN,
                        help=u"domain name from witch requests will be accepted")
    parser.add_argument(u'--delete-unused',
                        action=u'store_true',
                        default=Cmd.DEFAULT_DELETE_UNUSED,
                        help=u"indicates that other server definitions not related to current marathon tasks should be"
                             u" deleted")
    parser.add_argument(u'--override',
                        action=u'store_true',
                        default=Cmd.DEFAULT_OVERRIDE,
                        help=u"indicates that existing configuration should be overridden")
    parser.add_argument(u'--reload',
                        action=u'store_true',
                        default=Cmd.DEFAULT_RELOAD,
                        help=u"indicates that nginx configuration should be reloaded if was changed")
    parser.add_argument(u'--apps',
                        nargs=u'*',
                        type=str,
                        default=Cmd.DEFAULT_APPS,
                        help=u"application names list for which configuration should be generated")
    parser.add_argument(u'--exclude',
                        nargs=u'*',
                        type=str,
                        default=Cmd.DEFAULT_EXCLUDE,
                        help=u"application names list for which configuration shouldn't be generated")
    parser.add_argument(u'--generate-for-suspended',
                        action=u'store_true',
                        default=Cmd.DEFAULT_GENERATE_FOR_SUSPENDED,
                        help=u'indicates that configuration should be generated for suspended apps')

    ns, _ = parser.parse_known_args()

    kwargs = dict(
        conf_dir=ns.conf_dir,
        output_dir=ns.output_dir,
        template_dir=ns.template_dir,
        template_name=ns.template_name,
        marathon_url=ns.marathon_url,
        domain=ns.domain,
        delete_unused=ns.delete_unused,
        override=ns.override,
        reload=ns.reload,
        apps=ns.apps,
        exclude=ns.exclude,
        generate_for_suspended=ns.generate_for_suspended
    )

    action = Cmd(**kwargs)
    return action(**kwargs)

main()
