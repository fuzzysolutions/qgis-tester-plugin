# -*- coding: utf-8 -*-

#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#

import os
import sys
import glob
import importlib
import pkgutil
import unittest
from qgistester.test import Test, UnitTestWrapper


def findTests(path=None, prefix=None):
    """Search for tests in the given path and prefix

    :param path: list of paths.
    :param prefix: string e.g. "module." attached to the beginning of found modules
    :return: list of tests extracted from the module(s)
    """
    _tests = []
    if prefix is None:
        prefix = __name__ + '.'
    if path is None:
        path = __path__

    # skip if itself
    if 'qgistester.tests' in prefix:
        return _tests

    # parse tests of the module to look for unit and functional tests
    for importer, modname, ispkg in pkgutil.iter_modules(path, prefix):
        modtests = []
        group = modname.split('.')[-1]
        try:
            module = __import__(modname, fromlist='dummy')
        except ImportError:
            # add path in python search path and try again
            for p in path:
                sys.path.append(p)
            module = __import__(modname, fromlist="dummy")

        if 'functionalTests' in dir(module):
            modtests.extend(module.functionalTests())
        if 'unitTests' in dir(module):
            modtests.extend([UnitTestWrapper(unit) for unit in module.unitTests()])
        for t in modtests:
            t.group = group
        _tests.extend(modtests)
    return  _tests

tests = findTests()

def _testsFromModule(module, category='General'):
    modtests = []
    if 'functionalTests' in dir(module):
        modtests.extend(module.functionalTests())
    if 'unitTests' in dir(module):
        modtests.extend([UnitTestWrapper(unit, category) for unit in module.unitTests()])
    if 'settings' in dir(module):
        for test in modtests:
            test.settings = module.settings()
    return modtests

def addTestModule(module, group=None):
    modtests = _testsFromModule(module)
    for t in modtests:
        t.group = group
        if t not in tests:
            tests.append(t)

def removeTestModule(module, group=None):
    modtests = _testsFromModule(module)
    for t in modtests:
        t.group = group
        if t in tests:
            tests.remove(t)
