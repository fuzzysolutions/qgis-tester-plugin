# -*- coding: utf-8 -*-

#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#

__author__ = 'Alessandro Pasotti'
__date__ = 'April 2016'
__copyright__ = '(C) 2016 Boundless, http://boundlessgeo.com'

import os
import sys
import unittest

import utilities
from qgistester.tests import findTests, addTestModule


class StepTests(unittest.TestCase):
    """Tests for the Step class"""

    def testFindTests(self):
        """Check findTests method"""
        tests = findTests(path=[os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')], prefix='data.')
        test_names = [utw.name for utw in tests]
        self.assertIn('Test that fails', test_names)
        self.assertIn('Test that passes', test_names)
        self.assertIn('Functional test', test_names)

    def testAddTestModule(self):
        """Check addTestModule method"""
        from qgistester import tests
        if tests.tests is None:
            tests.tests = []

        from qgistester.unittests.data import plugin1
        addTestModule(plugin1, 'Plugin1')
        test_names = [utw.name for utw in tests.tests]
        self.assertIn('Test that fails', test_names)
        self.assertIn('Test that passes', test_names)
        self.assertIn('Functional test', test_names)


def suiteSubset():
    tests = ['testInit']
    suite = unittest.TestSuite(list(map(StepTests, tests)))
    return suite


def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(StepTests, 'test'))
    return suite


def run_all():
    unittest.TextTestRunner(verbosity=3, stream=sys.stdout).run(suite())


def run_subset():
    unittest.TextTestRunner(verbosity=3, stream=sys.stdout).run(suiteSubset())


if __name__ == '__main__':
    run_all()
