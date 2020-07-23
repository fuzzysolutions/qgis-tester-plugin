# -*- coding: utf-8 -*-
"""Test TestSelector.py."""
from __future__ import absolute_import
from builtins import map
#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#
import unittest
import sys
import os
try:
    import mock
except ImportError:
    import unittest.mock as mock
import utilities
from qgis.PyQt.QtCore import Qt
from qgistesting import start_app, stop_app
from qgistesting.mocked import get_iface
from qgistester.unittests.data.plugin1 import unitTests
from qgistester.tests import findTests
from qgistester.testselector import TestSelector

class TestSelectorTests(unittest.TestCase):
    """Tests for the TestSelector widget that select the list of tests to
    execute."""

    @classmethod
    def setUpClass(cls):
        """Test setUp method."""
        utilities.setUpEnv()
        cls.QGIS_APP = start_app()
        assert cls.QGIS_APP is not None
        cls.IFACE_Mock = get_iface()
        assert cls.IFACE_Mock is not None
        # get test data
        testPluginPath = os.path.abspath('data')
        cls.tests = findTests(path=[testPluginPath], prefix='')

    @classmethod
    def tearDownClass(cls):
        """Test tearDown method."""
        utilities.cleanUpEnv()

    def testInit(self):
        """check if __init__ is correctly executed."""
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
        """check if all tests are checked/unchecked dependin on previous
        state."""
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
        """check the widget is closed."""
        with mock.patch('qgistester.tests.tests', self.tests):
            ts = TestSelector()
            ts.show()  # dlg.resultsTree is a QTreeWidget
            # do test
            self.assertTrue(ts.isVisible())
            ts.cancelPressed()
            self.assertFalse(ts.isVisible())

    def testOkPressed(self):
        """check the list of checked tests ar added to test suite."""
        with mock.patch('qgistester.tests.tests', self.tests):
            ts = TestSelector()
            ts.show()  # dlg.resultsTree is a QTreeWidget
            self.assertTrue(ts.isVisible())
            ts.okPressed()
            self.assertEqual(len(ts.tests), 0)
            self.assertFalse(ts.isVisible())

            # do test 1: all selected
            ts = TestSelector()
            ts.show()  # dlg.resultsTree is a QTreeWidget
            self.assertTrue(ts.isVisible())
            ts.checkTests(lambda t: Qt.Checked)
            ts.okPressed()
            self.assertEqual(ts.tests[0], self.tests[0])
            self.assertEqual(ts.tests[1], self.tests[1])
            self.assertEqual(ts.tests[2], self.tests[2])
            self.assertFalse(ts.isVisible())

            # do test 1: uncheck the middle test
            ts = TestSelector()
            ts.show()  # dlg.resultsTree is a QTreeWidget
            self.assertTrue(ts.isVisible())
            ts.checkTests(lambda t: Qt.Checked)
            ts.testsTree.topLevelItem(0).child(1).child(0).child(0).setCheckState(0, False)
            ts.okPressed()
            self.assertEqual(ts.tests[0], self.tests[0])
            self.assertEqual(ts.tests[1], self.tests[2])
            self.assertFalse(ts.isVisible())


###############################################################################

def suiteSubset():
    """Setup a test suit for a subset of tests."""
    tests = ['testInit']
    suite = unittest.TestSuite(list(map(TestSelectorTests, tests)))
    return suite


def suite():
    """Return test suite for all tests."""
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(TestSelectorTests, 'test'))
    return suite


def run_all():
    """run all tests using unittest => no nose or testplugin."""
    # demo_test = unittest.TestLoader().loadTestsFromTestCase(CatalogTests)
    unittest.TextTestRunner(verbosity=3, stream=sys.stdout).run(suite())


def run_subset():
    """run a subset of tests using unittest > no nose or testplugin."""
    unittest.TextTestRunner(verbosity=3, stream=sys.stdout).run(suiteSubset())

if __name__ == "__main__":
    run_all()
