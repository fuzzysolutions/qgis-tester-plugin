# -*- coding: utf-8 -*-

"""
***************************************************************************
    __init__.py
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

__author__ = 'Alessandro Pasotti'
__date__ = 'April 2016'
__copyright__ = '(C) 2016 Boundless, http://boundlessgeo.com'


"""Dummy plugin with tests which can be used by Tester plugin"""

import unittest
from qgistester.test import Test

def functionalTests():
    test = Test('Functional test')
    test.addStep('Step 1', prestep=lambda: True, isVerifyStep=True)
    test.addStep('Step 1', prestep=lambda: True, isVerifyStep=True)
    test.setIssueUrl('http://www.example.com')
    return [test]


class Plugin1Tests(unittest.TestCase):
    """Provides two tests for fail/pass cases"""
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def testPassed(self):
        """Test that passes"""
        self.assertTrue(True)

    def testFailed(self):
        """Test that fails"""
        self.assertTrue(False)


def unitTests():
    suite = unittest.makeSuite(Plugin1Tests, 'test')
    _tests = []
    _tests.extend(suite)
    return _tests
