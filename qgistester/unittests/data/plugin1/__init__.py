# -*- coding: utf-8 -*-
#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#

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
