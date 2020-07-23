# -*- coding: utf-8 -*-

#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#

__author__ = 'Luigi Pirelli'
__date__ = 'April 2016'
__copyright__ = '(C) 2016 Boundless, http://boundlessgeo.com'

import sys
import unittest
import unittest.mock as mock

import utilities
from qgistester.test import Step
from qgistester.test import Test
from qgistester.test import UnitTestWrapper
from qgistester.test import _TestRunner
from qgistester.test import _TestResult
from qgistester.unittests.data.plugin1 import unitTests


class StepTests(unittest.TestCase):
    """Tests for the Step class"""

    def testInit(self):
        """Check if __init__ is correctly executed"""
        def testFunction1():
            pass

        def testFunction2():
            pass

        description1 = 'this is a step description'
        description2 = 'this is a step description'
        preStep = Step(description1, testFunction1)

        s2 = Step(description2, testFunction2, preStep, True)
        self.assertEqual(s2.description, description2)
        self.assertEqual(s2.function, testFunction2)
        self.assertEqual(s2.prestep, preStep)
        self.assertTrue(s2.isVerifyStep)


class TestTests(unittest.TestCase):
    """Tests for the Test class"""

    def testInit(self):
        """Check if __init__ is correctly executed"""
        name = 'this is the test name'
        t = Test(name)
        self.assertEqual(len(t.steps), 0)
        self.assertEqual(t.name, name)
        self.assertEqual(t.group, '')
        self.assertIn('<lambda> at ', str(t.cleanup))
        self.assertIsNone(t.cleanup())
        self.assertIsNone(t.issueUrl)

    def testAddStep(self):
        """Check if a test is correclty added"""

        def testFunction1():
            pass

        def testFunction2():
            pass

        description1 = 'this is a step description'
        description2 = 'this is a step description'
        preStep = Step(description1, testFunction1)
        t = Test('this is the test name')

        t.addStep(description2, testFunction2, preStep, True)
        self.assertEqual(len(t.steps), 1)
        s = t.steps[0]
        self.assertEqual(s.description, description2)
        self.assertEqual(s.function, testFunction2)
        self.assertEqual(s.prestep, preStep)
        self.assertTrue(s.isVerifyStep)

    def testSetCleanup(self):
        """Test if cleanup function is set"""

        def testFunction1():
            pass

        name = 'this is the test name'
        t = Test(name)

        t.setCleanup(testFunction1)
        self.assertEqual(t.cleanup, testFunction1)

    def testSetIssueUrl(self):
        """Test is issue url is set"""
        issueUrl = 'http://www.example.com'
        name = 'this is the test name'
        t = Test(name)
        t.setIssueUrl(issueUrl)
        self.assertEqual(t.issueUrl, issueUrl)


class UnitTestWrapperTests(unittest.TestCase):
    """Tests for the UnitTestWrapper class"""

    def testInit(self):
        """Check if __init__ is correctly executed"""
        unitTest = unitTests()[0]

        utw = UnitTestWrapper(unitTest)
        self.assertIsInstance(utw, Test)
        self.assertEqual(utw.test, unitTest)
        self.assertEqual(len(utw.steps), 1)
        step = utw.steps[0]
        self.assertEqual(step.description, 'Run unit test')
        self.assertEqual(step.function, utw._runTest)

    def testSetCleanup(self):
        """Check if cleanup is set"""
        pass

    def test_runTest(self):
        """Check if _runTest is set"""
        unitTest = unitTests()[0]
        utw = UnitTestWrapper(unitTest)

        resultMock = mock.Mock(spect=_TestResult)
        resultMock.err = None
        _TestRunnerMock = mock.Mock(spect=_TestRunner)
        _TestRunnerMock.run.return_value = resultMock
        with mock.patch('qgistester.test._TestRunner', mock.Mock(return_value=_TestRunnerMock)):
            try:
                utw._runTest()
            except:
                # if exception raise then error
                self.assertTrue(False)

            self.assertIn('call.run', str(_TestRunnerMock.mock_calls[0]))

        unitTest = unitTests()[0]
        utw = UnitTestWrapper(unitTest)
        err = []
        uknownContent = "I don't know the type of the first element"
        attrs = {'message': 'this is the error message'}
        errMessage = type('errMessage', (object,), attrs)
        exc_type, exc_value, exc_traceback = sys.exc_info()

        err.append(uknownContent)
        err.append(errMessage)
        err.append(exc_traceback)

        resultMock = mock.Mock(spect=_TestResult)
        resultMock.err = err
        _TestRunnerMock = mock.Mock(spect=_TestRunner)
        _TestRunnerMock.run.return_value = resultMock
        with mock.patch('qgistester.test._TestRunner', mock.Mock(return_value=_TestRunnerMock)):
            try:
                utw._runTest()
            except:
                pass
            else:
                # if there is NO exception then error
                self.assertTrue(False)

            self.assertIn('call.run', str(_TestRunnerMock.mock_calls[0]))


class _TestRunnerTests(unittest.TestCase):
    """Tests for the _TestRunner class"""

    def testInit(self):
        """Check if __init__ is correctly executed"""
        runner = _TestRunner()
        self.assertIsInstance(runner, unittest.runner.TextTestRunner)

    def testRun(self):
        """Check if test sets result after run"""
        unitTestMock = mock.Mock(spec=unittest.TestCase)
        runner = _TestRunner()
        result = runner.run(unitTestMock)
        self.assertIsInstance(result, _TestResult)
        self.assertIn('call(<qgistester.test._TestResult run=0 errors=0 failures=0>)', str(unitTestMock.mock_calls[0]))


class _TestResultTests(unittest.TestCase):
    """Tests for the _TestResult"""

    def testInit(self):
        """Check if __init__ is correctly executed"""
        runner = _TestResult()
        self.assertIsInstance(runner, unittest.result.TestResult)
        self.assertIsNone(runner.err)

    def testAddSuccess(self):
        """Check if success state is added"""
        pass

    def testAddError(self):
        """Check if error state is added"""
        unitTestMock = mock.Mock(spec=unittest.TestCase)
        errMock = mock.Mock()
        tr = _TestResult()
        tr.addError(unitTestMock, errMock)
        self.assertEqual(len(unitTestMock.mock_calls), 0)
        self.assertEqual(tr.err, errMock)

    def testAddFailure(self):
        """Check if failure state is added"""

        unitTestMock = mock.Mock(spec=unittest.TestCase)
        errMock = mock.Mock()
        tr = _TestResult()
        tr.addError(unitTestMock, errMock)
        self.assertEqual(len(unitTestMock.mock_calls), 0)
        self.assertEqual(tr.err, errMock)


def suiteSubset():
    tests = ['testInit']
    suite = unittest.TestSuite(list(map(StepTests, tests)))
    return suite


def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(StepTests, 'test'))
    suite.addTests(unittest.makeSuite(TestTests, 'test'))
    suite.addTests(unittest.makeSuite(UnitTestWrapperTests, 'test'))
    suite.addTests(unittest.makeSuite(_TestRunnerTests, 'test'))
    suite.addTests(unittest.makeSuite(_TestResultTests, 'test'))
    return suite


def run_all():
    unittest.TextTestRunner(verbosity=3, stream=sys.stdout).run(suite())


def run_subset():
    unittest.TextTestRunner(verbosity=3, stream=sys.stdout).run(suiteSubset())


if __name__ == '__main__':
    run_all()
