#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  Copyright (c) 2015 Lingaro


from setuptools import setup

version = u'0.1.5'

setup(
    name=u'marathon-proxy-manager',
    version=version,
    description=u'Reverse proxy and load balancing configuration for marathon mesos environment',
    author=u'Michał Lula',
    license=u'MIT',
    author_email=u'michal.lula@lingaro.com',
    url=u'https://github.com/michallula/marathon-proxy-manager',
    download_url=u'https://github.com/michallula/marathon-proxy-manager/tarball/{version}'.format(version=version),
    keywords=[u'marathon', u'mesos', u'nginx', u'load-balancing', u'reverse proxy'],
    package_dir={'': 'src'},
    packages=['marathon_proxy_manager'],
    package_data={'marathon_proxy_manager': ['marathon_proxy_manager/templates/*.tmpl']},
    include_package_data=True,
    install_requires=[
        u'argparse',
        u'marathon',
        u'jinja2'
    ]
)