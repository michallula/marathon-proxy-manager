#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  Copyright (c) 2015 Lingaro


from setuptools import setup

version = u'0.1'

setup(
    name=u'marathon-proxy-manager',
    version=version,
    description=u'Reverse proxy and load balancing configuration for marathon mesos environment',
    author=u'Michał Lula',
    author_email=u'michal.lula@lingaro.com',
    url=u'https://github.com/michallula/marathon-proxy-manager',
    download_url=u'https://github.com/michallula/marathon-proxy-manager/tarball/{version}'.format(version=version),
    keywords=['marathon', 'mesos', 'haproxy', 'nginx'],
    package_dir={u'': 'src'},
    packages=['marathon_pm'],
    install_requires=[
        u'argparse',
        u'marathon',
        u'jinja2'
    ]
)