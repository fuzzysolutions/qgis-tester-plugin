# -*- coding: utf-8 -*-

"""
***************************************************************************
    run_all_tests.py
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

import utilities
from qgistester.unittests.test_Test import suite as testTestsSuite
from qgistester.unittests.test_plugin import suite as pluginTestsSuite
from qgistester.unittests.test_report import suite as reportTestsSuite
from qgistester.unittests.test_ReportDialog import suite as reportDialogTestsSuite
from qgistester.unittests.test_TesterWidget import suite as testerWidgetTestsSuite
from qgistester.unittests.test_TestSelector import suite as selectorTestsSuite
from qgistester.unittests.test_translations import suite as translationsTestsSuite


def unitTests():
    _tests = []
    _tests.extend(pluginTestsSuite())
    _tests.extend(reportTestsSuite())
    _tests.extend(reportDialogTestsSuite())
    _tests.extend(testTestsSuite())
    _tests.extend(testerWidgetTestsSuite())
    _tests.extend(selectorTestsSuite())
    _tests.extend(translationsTestsSuite())
    return _tests


def runAllUnitTests():
    _suite = unittest.TestSuite()
    _suite.addTest(pluginTestsSuite())
    _suite.addTest(reportTestsSuite())
    _suite.addTest(reportDialogTestsSuite())
    _suite.addTest(testTestsSuite())
    _suite.addTest(testerWidgetTestsSuite())
    _suite.addTest(selectorTestsSuite())
    _suite.addTest(translationsTestsSuite())
    unittest.TextTestRunner(verbosity=3, stream=sys.stdout).run(_suite)


if __name__ == '__main__':
    runAllUnitTests()
