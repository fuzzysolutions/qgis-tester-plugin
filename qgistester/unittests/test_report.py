# -*- coding: utf-8 -*-

"""
***************************************************************************
    test_Report.py
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


import sys
import unittest
import unittest.mock as mock

import utilities
from qgistester.report import Report, TestResult
from qgistester.test import Test, UnitTestWrapper


class ReportTests(unittest.TestCase):
    """Tests for the Report class"""

    def testInit(self):
        """Check if __init__ is correctly executed"""
        r = Report()
        self.assertIsInstance(r.results, list)
        self.assertEqual(len(r.results), 0)

    def testAddTestResult(self):
        """Test if a test is added to the results array"""
        r = Report()
        test = mock.Mock()
        tr = TestResult(test)
        r.addTestResult(tr)
        self.assertEqual(r.results[0], tr)
        self.assertEqual(len(r.results), 1)


class TestResultTests(unittest.TestCase):
    """Tests for the TestResult class"""

    def testInit(self):
        """Check if __init__ is correctly executed"""
        tr = TestResult('fake_test')
        self.assertEqual(tr.test, 'fake_test')
        self.assertEqual(tr.status, tr.SKIPPED)
        self.assertEqual(tr.errorStep, None)
        self.assertEqual(tr.errorMessage, None)

    def testFailed(self):
        """Check if the fail flag is correctly set"""
        t = Test('Test that has fails')
        t.addStep('Fail', lambda: False)
        tr = TestResult(t)
        tr.failed('fake_step', 'FAILED')
        self.assertEqual(tr.status, tr.FAILED)
        self.assertEqual(tr.errorStep, 'fake_step')
        self.assertEqual(tr.errorMessage, 'FAILED')

    def testPassed(self):
        """Check if the passed flag is correctly set"""
        t = Test('Test that passed')
        t.addStep('Passed', lambda: False)
        tr = TestResult(t)
        tr.passed()
        self.assertEqual(tr.status, tr.PASSED)
        self.assertIsNone(tr.errorStep)
        self.assertIsNone(tr.errorMessage)

    def testSkipped(self):
        """Check if the skipped flag is correctly set"""
        t = Test('Test that was skipped')
        t.addStep('Skipped', lambda: False)
        tr = TestResult(t)
        tr.skipped()
        self.assertEqual(tr.status, tr.SKIPPED)
        self.assertIsNone(tr.errorStep)
        self.assertIsNone(tr.errorMessage)

    def test__str___(self):
        """Test __str__ method"""
        t = Test('Test that was skipped')
        t.addStep('Skipped', lambda: False)
        tr = TestResult(t)
        self.assertEqual('{}'.format(tr), 'Test name: -Test that was skipped\nTest result:Test skipped')


class TestRealRunner(unittest.TestCase):
    """Tests that TestResult is correctly populated after a real test run"""

    @classmethod
    def runner(cls, suite):
        test = list(suite)[0]
        utw = UnitTestWrapper(test)
        report = Report()
        result = TestResult(test)
        step = utw.steps[0]
        try:
            step.function()
            result.passed()
        except Exception as e:
            result.failed(test, str(e))
        report.addTestResult(result)
        return report.results[0]

    def testPassed(self):
        """Tests if a passed test correctly set PASSED in TestResult"""

        class TestPassed(unittest.TestCase):
            def testPassed(self):
                self.assertTrue(True)

        # Mimick the behaviour in testerwidget.py
        suite = unittest.makeSuite(TestPassed, 'test')
        result = self.runner(suite)
        self.assertEqual(result.status, result.PASSED)

    def testFailed(self):
        """Tests if a passed test correctly set FAILED in TestResult"""

        class TestFailed(unittest.TestCase):
            def testFailed(self):
                self.assertTrue(False)

        # Mimick the behaviour in testerwidget.py
        suite = unittest.makeSuite(TestFailed, 'test')
        result = self.runner(suite)
        self.assertEqual(result.status, result.FAILED)


def suiteSubset():
    tests = ['testInit']
    suite = unittest.TestSuite(list(map(ReportTests, tests)))
    return suite


def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(ReportTests, 'test'))
    suite.addTests(unittest.makeSuite(TestResultTests, 'test'))
    suite.addTests(unittest.makeSuite(TestRealRunner, 'test'))
    return suite


def run_all():
    unittest.TextTestRunner(verbosity=3, stream=sys.stdout).run(suite())


def run_subset():
    unittest.TextTestRunner(verbosity=3, stream=sys.stdout).run(suiteSubset())


if __name__ == '__main__':
    run_all()
