# -*- coding: utf-8 -*-

"""
***************************************************************************
    manualtests.py
    ---------------------
    Date                 : July 2017
    Copyright            : (C) 2017 by Boundless, http://boundlessgeo.com
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
__date__ = 'July 2017'
__copyright__ = '(C) 2017 Boundless, http://boundlessgeo.com'


def functionalTests():
    try:
        from qgistester.test import Test
    except:
        return []

    passingTest = Test('This test should pass')
    passingTest.addStep('Click on "Test passes"')

    skippedTest = Test('This test should be skiped')
    skippedTest.addStep('Click on "Skip test"')

    def failingFunction():
        assert False

    failingTest = Test('This test should fail')
    failingTest.addStep("Failing step", function=failingFunction)

    failingSetupTest = Test('This test should fail in the step setup')
    failingSetupTest.addStep("Failing prestep", prestep=failingFunction)

    def errorFunction():
        raise Exception ("Error in test")

    errorTest = Test('This test should error')
    errorTest.addStep("Error step", function=errorFunction)

    return [passingTest, skippedTest, failingTest, failingSetupTest, errorTest]
