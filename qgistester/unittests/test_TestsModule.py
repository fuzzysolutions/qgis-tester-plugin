# -*- coding: utf-8 -*-

"""
***************************************************************************
    test_TestsModule.py
    ---------------------
    Date                 : April 2016
    Copyright            : (C) 2016 by Boundless, http://boundlessgeo.com
                         : (C) 2020 by QCooperative, https://www.qcooperative.net
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

__author__ = 'Luigi Pirelli'
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
