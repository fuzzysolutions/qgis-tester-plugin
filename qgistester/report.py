# -*- coding: utf-8 -*-

"""
***************************************************************************
    report.py
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


class Report:

    def __init__(self):
        self.results = []

    def addTestResult(self, result):
        self.results.append(result)


class TestResult:

    PASSED, FAILED, SKIPPED, CONTAINS_ERROR, FAILED_AT_SETUP = list(range(5))

    def __init__(self, test):
        self.test = test
        self.status = self.SKIPPED
        self.errorStep = None
        self.errorMessage = None

    def failed(self, step, message):
        self.status = self.FAILED
        self.errorStep = step
        self.errorMessage = message

    def containsError(self, step, message):
        self.status = self.CONTAINS_ERROR
        self.errorStep = step
        self.errorMessage = message

    def setupFailed(self, step, message):
        self.status = self.FAILED_AT_SETUP
        self.errorStep = step
        self.errorMessage = message

    def passed(self):
        self.status = self.PASSED

    def skipped(self):
        self.status = self.SKIPPED

    def __str__(self):
        s = 'Test name: {}-{}\nTest result:'.format(self.test.group, self.test.name)
        if self.status == self.SKIPPED:
            s+= 'Test skipped'
        elif self.status == self.PASSED:
            s+= 'Test passed correctly'
        elif self.status == self.CONTAINS_ERROR:
            s+= 'Test contains an error at step "{}":\n{}'.format(self.errorStep, self.errorMessage)
        elif self.status == self.FAILED_AT_SETUP:
            s+= 'Test step "{}" failed at setup:\n{}'.format(self.errorStep, self.errorMessage)
        else:
            s+= 'Test failed at step "{}" with message:\n{}'.format(self.errorStep, self.errorMessage)
        return s
