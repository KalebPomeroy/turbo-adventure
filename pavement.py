#!/usr/bin/env python

import sys
from os.path import dirname

import paver.doctools
from paver.easy import options
from paver.setuputils import setup, find_packages

# make sure the current directory is in the python import path
sys.path.append(dirname(__file__))

# # import our tasks
from tasks.deployment import *

#
# default task options
#
options(
    root_dir = dirname(__file__)
)

#
# project dependencies
#
install_requires = [
    'setuptools',
    'cerberus',
    'coverage',
    'python-daemon',
    'pyyaml',
    'tornado',
    'tornadio2'
]

#
# Setuptools configuration, used to create python .eggs and such.
# See: http://bashelton.com/2009/04/setuptools-tutorial/ for a nice
# setuptools tutorial.
#
setup(
    name="turbo-adventure",
    version="0.1",
    
    # packaging infos
    package_data={'': ['*.yaml', '*.html']},
    packages=find_packages(exclude=['test', 'test.*']),
    
    # dependency infos
    install_requires=install_requires,
    
    entry_points={
        'console_scripts': [
            'turbo-adventure = application.server:serve'
        ]
    },
    
    zip_safe=False
)
