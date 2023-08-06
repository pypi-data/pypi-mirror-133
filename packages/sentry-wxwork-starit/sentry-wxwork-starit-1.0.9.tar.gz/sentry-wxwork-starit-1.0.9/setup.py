#!/usr/bin/env python
"""
sentry-wxwork-starit
==============

A `Sentry <https://getsentry.com>`_ plugin which posts notifications
to `WxWork <https://work.weixin.qq.com/>`_.

:license: MIT, see LICENSE for more details.
"""

from setuptools import setup, find_packages
from sentry_wxwork import __version__
import os

cwd = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
readme_text = open(os.path.join(cwd, 'README.md')).read()

setup(
    name='sentry-wxwork-starit',
    version=__version__,
    author='Sokos Lee',
    author_email='sokos@staritgp.com',
    url='http://gitlab.oa.com/sokos/sentry_wxwork_notification/',
    long_description=readme_text,
    long_description_content_type="text/markdown",
    license='MIT',
    description='A Sentry plugin which posts notifications to WxWork.',
    packages=find_packages(),
    install_requires=[
      'sentry',
    ],
    include_package_data=True,
    entry_points={
        'sentry.apps': [
            'sentry_wxwork = sentry_wxwork',
        ],
        'sentry.plugins': [
            'sentry_wxwork = sentry_wxwork.plugin:WxWorkPlugin',
        ]
    },
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development',
        'Topic :: System :: Monitoring'
    ],
)