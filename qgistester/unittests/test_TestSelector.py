# -*- coding: utf-8 -*-

"""
***************************************************************************
    test_TestSelector.py
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
import unittest.mock as mock

from qgis.PyQt.QtCore import Qt

import utilities
from qgistesting import start_app, stop_app
from qgistesting.mocked import get_iface
from qgistester.unittests.data.plugin1 import unitTests
from qgistester.tests import findTests
from qgistester.testselector import TestSelector


class TestSelectorTests(unittest.TestCase):
    """Tests for the TestSelector class"""

    @classmethod
    def setUpClass(cls):
        cls.QGIS_APP = start_app(cleanup=False)
        assert cls.QGIS_APP is not None
        cls.IFACE_Mock = get_iface()
        assert cls.IFACE_Mock is not None

        testPluginPath = os.path.abspath('data')
        cls.tests = findTests(path=[testPluginPath], prefix='')

    def testInit(self):
        """Check if __init__ is correctly executed"""
        with mock.patch('qgistester.tests.tests', self.tests):
            ts = TestSelector()
            self.assertEqual(ts.testsTree.topLevelItemCount(), 1)

            # Tree in the test selector looks like
            #
            # Manual and semi-automated tests
            # +-General
            #   +-Functional test
            # Fully automated tests
            # +-General
            #   +-Test that fails
            #   +-Test that passes
            rootItem = ts.testsTree.topLevelItem(0)
            self.assertEqual(rootItem.childCount(), 2)
            self.assertEqual(rootItem.child(0).text(0), 'Manual and semi-automated tests')
            self.assertEqual(rootItem.child(0).child(0).text(0), 'General')
            self.assertEqual(rootItem.child(0).child(0).child(0).text(0), 'Functional test')
            self.assertEqual(rootItem.child(1).text(0), 'Fully automated tests')
            self.assertEqual(rootItem.child(1).child(0).text(0), 'General')
            self.assertEqual(rootItem.child(1).child(0).child(0).text(0), 'Test that fails')
            self.assertEqual(rootItem.child(1).child(0).child(1).text(0), 'Test that passes')

            self.assertEqual(rootItem.child(0).checkState(0), Qt.Unchecked)
            self.assertEqual(rootItem.child(1).checkState(0), Qt.Unchecked)
            self.assertTrue(rootItem.isExpanded())
            self.assertFalse(rootItem.child(0).isExpanded())
            self.assertFalse(rootItem.child(1).isExpanded())

            self.assertEqual(ts.selectAllLabel.receivers(ts.selectAllLabel.linkActivated), 1)
            self.assertEqual(ts.unselectAllLabel.receivers(ts.unselectAllLabel.linkActivated), 1)
            self.assertEqual(ts.buttonBox.receivers(ts.buttonBox.accepted), 1)
            self.assertEqual(ts.buttonBox.receivers(ts.buttonBox.rejected), 1)

    def testCheckTests(self):
        """Check selecting/deselecting tests"""
        with mock.patch('qgistester.tests.tests', self.tests):
            ts = TestSelector()
            rootItem = ts.testsTree.topLevelItem(0)
            self.assertTrue(rootItem.child(0).checkState(0) == Qt.Unchecked)
            self.assertTrue(rootItem.child(1).checkState(0) == Qt.Unchecked)

            ts.checkTests(lambda t: Qt.Checked)
            self.assertTrue(rootItem.child(0).checkState(0) == Qt.Checked)
            self.assertTrue(rootItem.child(1).checkState(0) == Qt.Checked)
            self.assertTrue(rootItem.child(0).child(0).checkState(0) == Qt.Checked)
            self.assertTrue(rootItem.child(0).child(0).child(0).checkState(0) == Qt.Checked)
            self.assertTrue(rootItem.child(1).child(0).checkState(0) == Qt.Checked)
            self.assertTrue(rootItem.child(1).child(0).child(0).checkState(0) == Qt.Checked)
            self.assertTrue(rootItem.child(1).child(0).child(1).checkState(0) == Qt.Checked)

    def testCancelPressed(self):
        """Check that the widget is closed"""
        with mock.patch('qgistester.tests.tests', self.tests):
            ts = TestSelector()
            ts.show()
            self.assertTrue(ts.isVisible())
            ts.cancelPressed()
            self.assertFalse(ts.isVisible())

    def testOkPressed(self):
        """Check that selected tests are added to the suite"""
        with mock.patch('qgistester.tests.tests', self.tests):
            ts = TestSelector()
            ts.show()
            self.assertTrue(ts.isVisible())
            ts.okPressed()
            # no tests selected by default
            self.assertEqual(len(ts.tests), 0)
            self.assertFalse(ts.isVisible())

            # select all tests
            ts = TestSelector()
            ts.show()
            self.assertTrue(ts.isVisible())
            ts.checkTests(lambda t: Qt.Checked)
            ts.okPressed()
            self.assertEqual(ts.tests[0], self.tests[0])
            self.assertEqual(ts.tests[1], self.tests[1])
            self.assertEqual(ts.tests[2], self.tests[2])
            self.assertFalse(ts.isVisible())

            # select 2 tests out of 3 available
            ts = TestSelector()
            ts.show()
            self.assertTrue(ts.isVisible())
            ts.checkTests(lambda t: Qt.Checked)
            ts.testsTree.topLevelItem(0).child(1).child(0).child(0).setCheckState(0, False)
            ts.okPressed()
            self.assertEqual(ts.tests[0], self.tests[0])
            self.assertEqual(ts.tests[1], self.tests[2])
            self.assertFalse(ts.isVisible())


def suiteSubset():
    tests = ['testInit']
    suite = unittest.TestSuite(list(map(TestSelectorTests, tests)))
    return suite


def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(TestSelectorTests, 'test'))
    return suite


def run_all():
    unittest.TextTestRunner(verbosity=3, stream=sys.stdout).run(suite())


def run_subset():
    unittest.TextTestRunner(verbosity=3, stream=sys.stdout).run(suiteSubset())


if __name__ == '__main__':
    run_all()
