# -*- coding: utf-8 -*-

"""
***************************************************************************
    test.py
    ---------------------
    Date                 : October 2015
    Copyright            : (C) 2015 by Boundless, http://boundlessgeo.com
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

__author__ = 'Victor Olaya'
__date__ = 'October 2015'
__copyright__ = '(C) 2015 Boundless, http://boundlessgeo.com'


import traceback

from unittest.suite import TestSuite
from unittest.result import TestResult
from unittest.runner import TextTestRunner


class Step:

    def __init__(self, description, function=None, prestep=None, isVerifyStep=False, busyCursor=True):
        self.description = description
        self.function = function
        self.prestep = prestep
        self.isVerifyStep = isVerifyStep
        self.busyCursor = busyCursor


class Test:

    def __init__(self, name, category='General'):
        self.steps = []
        self.name = name
        self.group = ''
        self.category = category
        self.cleanup = lambda: None
        self.issueUrl = None
        self.settings = {}

    def __eq__(self, o):
        return o.name == self.name and o.group == self.group

    def addStep(self, description, function=None, prestep=None, isVerifyStep=False):
        self.steps.append(Step(description, function, prestep, isVerifyStep))

    def setCleanup(self, function):
        self.cleanup = function

    def setIssueUrl(self, url):
        self.issueUrl = url


class UnitTestWrapper(Test):

    def __init__(self, test, category='General'):
        Test.__init__(self, test.shortDescription() or str(test), category)
        self.test = test
        self.steps.append(Step('Run unit test', self._runTest))

    def setCleanup(self):
        pass

    def _runTest(self):
        """Method used to run a test"""
        suite = TestSuite()
        suite.addTest(self.test)
        runner = _TestRunner()
        result = runner.run(suite)
        if result.err is not None:
            desc = str(result.err) + '\n' + ''.join(traceback.format_tb(result.err[2]))
            if isinstance(result.err[1], AssertionError):
                raise AssertionError(desc)
            else:
                raise Exception(desc)


class _TestRunner(TextTestRunner):

    def __init__(self):
        pass

    def run(self, test):
        result = _TestResult()
        test(result)

        return result


class _TestResult(TestResult):

    def __init__(self):
        TestResult.__init__(self)
        self.err = None

    def addSuccess(self, test):
        pass

    def addError(self, test, err):
        self.err = err

    def addFailure(self, test, err):
        self.err = err
