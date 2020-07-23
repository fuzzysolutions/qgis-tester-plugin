# -*- coding: utf-8 -*-

#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#

__author__ = 'Alessandro Pasotti'
__date__ = 'April 2016'
__copyright__ = '(C) 2016 Boundless, http://boundlessgeo.com'

import sys
import unittest
import unittest.mock as mock

import utilities
from qgistesting import start_app
from qgistesting.mocked import get_iface
from qgistester.test import UnitTestWrapper
from qgistester.testerwidget import TesterWidget
from qgistester.unittests.data.plugin1 import functionalTests, unitTests
from qgistester.report import Report, TestResult


class TesterWidgetTests(unittest.TestCase):
    """Tests for the TesterWidget class"""

    @classmethod
    def setUpClass(cls):
        cls.QGIS_APP = start_app()
        assert cls.QGIS_APP is not None
        cls.IFACE_Mock = get_iface()
        assert cls.IFACE_Mock is not None

        cls.functionalTests = functionalTests()
        cls.unitTests = [UnitTestWrapper(unit) for unit in unitTests()]
        cls.allTests = cls.functionalTests + cls.unitTests

    def __testInit(self):
        """Check if __init__ is correctly executed"""
        self.assertTrue(False)

    def testSetTests(self):
        """Check if tests list is set"""
        widget = TesterWidget()
        widget.setTests(self.allTests)
        self.assertEqual(widget.tests, self.allTests)

    def testStartTesting_UnitTests(self):
        """Test the run of the first unit tests setting up the result"""
        widget = TesterWidget()
        widget.setTests(self.unitTests)
        with mock.patch('qgis.utils.iface', self.IFACE_Mock):
            widget.startTesting()
        self.assertIsInstance(widget.report, Report)
        self.assertEqual(len(widget.report.results), 2)
        self.assertEqual(widget.report.results[0].status, TestResult.FAILED)
        self.assertEqual(widget.report.results[1].status, TestResult.PASSED)

    def testStartTesting_FunctionalTests(self):
        """Test the run of the first functional tests setting up the result"""
        widget = TesterWidget()
        widget.setTests(self.functionalTests)
        widget.startTesting()
        for t in widget.tests:
            for s in t.steps:
                widget.testPasses()
        self.assertIsInstance(widget.report, Report)
        self.assertGreater(len(widget.report.results), 0)
        for r in widget.report.results:
            self.assertEqual(r.status, TestResult.PASSED)

    def testSkipTest(self):
        """Test if test is skipped pressing stop test + relative cleanup"""
        widget = TesterWidget()
        widget.setTests(self.functionalTests)
        widget.startTesting()
        for t in widget.tests:
            widget.skipTest()
        self.assertIsInstance(widget.report, Report)
        self.assertGreater(len(widget.report.results), 0)
        for r in widget.report.results:
            self.assertEqual(r.status, TestResult.SKIPPED)

    def testCancelTesting(self):
        """Test if a test set invisible"""
        widget = TesterWidget()
        widget.setVisible = mock.Mock()
        widget.cancelTesting()
        self.assertEqual(widget.setVisible.call_count, 1)


def suiteSubset():
    tests = ['testInit']
    suite = unittest.TestSuite(list(map(TesterWidgetTests, tests)))
    return suite


def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(TesterWidgetTests, 'test'))
    return suite


def run_all():
    unittest.TextTestRunner(verbosity=3, stream=sys.stdout).run(suite())


def run_subset():
    unittest.TextTestRunner(verbosity=3, stream=sys.stdout).run(suiteSubset())


if __name__ == '__main__':
    run_all()
