#!/usr/bin/env python

import pkgutil
import sys


def autoload(dirname):
    """ Autoload all modules in a directory """
    
    for importer, package_name, _ in pkgutil.iter_modules([dirname]):
        if package_name not in sys.modules:
            module = importer.find_module(package_name).load_module(package_name)
