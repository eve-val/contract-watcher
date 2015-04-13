#!/usr/bin/env python

from setuptools import setup

setup(
    name='contract-watcher',
    version='0.1',
    install_requires=[
        'evelink',
        'jinja2',
        'paste',
        'webapp2',
        'webob',  # shame on webapp2 for not declaring the dependency.
    ],
)
