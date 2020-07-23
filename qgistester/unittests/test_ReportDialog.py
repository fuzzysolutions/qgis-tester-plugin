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

from qgis.PyQt.QtWidgets import QMenu, QAction
from qgis.PyQt.QtCore import Qt, QPoint
from qgis.PyQt.QtGui import QColor

import utilities
from qgistesting import start_app
from qgistesting.mocked import get_iface
from qgistester.reportdialog import ReportDialog
from qgistester.report import Report, TestResult
from qgistester.unittests.data.plugin1 import functionalTests, unitTests
from qgistester.test import UnitTestWrapper


class ReportDialogTests(unittest.TestCase):
    """Tests for the ReportDialog class"""

    @classmethod
    def setUpClass(cls):
        cls.QGIS_APP = start_app()
        assert cls.QGIS_APP is not None
        cls.IFACE_Mock = get_iface()
        assert cls.IFACE_Mock is not None

        # load sample tests
        cls.functionalTests = functionalTests()
        cls.unitTests = [UnitTestWrapper(unit) for unit in unitTests()]
        cls.allTests = cls.functionalTests + cls.unitTests

    def testInit(self):
        """Check if __init__ is correctly executed"""
        r = Report()  # r.results is empty
        dlg = ReportDialog(r)
        expectedColorList = [Qt.green, Qt.red, Qt.gray, Qt.magenta, QColor(237, 189, 129)]
        self.assertEqual(dlg.resultColor, expectedColorList)
        self.assertEqual(dlg.resultsTree.topLevelItemCount(), 0)
        self.assertEqual(dlg.resultsTree.receivers(dlg.resultsTree.itemClicked), 1)
        self.assertEqual(dlg.resultsTree.receivers(dlg.resultsTree.customContextMenuRequested), 1)
        self.assertEqual(dlg.buttonBox.receivers(dlg.buttonBox.rejected), 1)

        r = Report()
        for test in self.allTests:
            tr = TestResult(test)
            r.addTestResult(tr)
        dlg = ReportDialog(r)
        self.assertEqual(dlg.resultsTree.topLevelItemCount(), 1)
        self.assertTrue(dlg.resultsTree.topLevelItem(0).isExpanded())
        self.assertEqual(dlg.resultsTree.topLevelItem(0).childCount(), 3)
        self.assertEqual(dlg.resultsTree.topLevelItem(0).child(0).text(0), 'Functional test')
        self.assertEqual(dlg.resultsTree.topLevelItem(0).child(1).text(0), 'Test that fails')
        self.assertEqual(dlg.resultsTree.topLevelItem(0).child(2).text(0), 'Test that passes')

    def testShowPopupMenu(self):
        """Check if a context menu is opened when issue url is present"""
        # check with 'Test that fails' item which does NOT have an url
        r = Report()
        for test in self.allTests:
            tr = TestResult(test)
            r.addTestResult(tr)
        dlg = ReportDialog(r)
        dlg.resultsTree.topLevelItem(0).child(1).setSelected(True)
        point = QPoint(0, 0)
        qmenuMock = mock.Mock(spec=QMenu)
        qactionMock = mock.Mock(spec=QAction)
        with mock.patch('PyQt5.QtWidgets.QMenu', qmenuMock):
            with mock.patch('PyQt5.QtWidgets.QAction', qactionMock):
                dlg.showPopupMenu(point)

        self.assertEqual(qmenuMock.mock_calls, [])
        self.assertEqual(qactionMock.mock_calls, [])

        # check with 'Functional tests' that does have an url
        r = Report()
        for test in self.allTests:
            tr = TestResult(test)
            r.addTestResult(tr)
        dlg = ReportDialog(r)
        dlg.resultsTree.topLevelItem(0).child(0).setSelected(True)
        point = QPoint(0, 0)
        qmenuMock = mock.Mock(spec=QMenu)
        qactionMock = mock.Mock(spec=QAction)
        with mock.patch('qgistester.reportdialog.QMenu', qmenuMock):
            with mock.patch('qgistester.reportdialog.QAction', qactionMock):
                self.assertEqual(dlg.resultsTree.selectedItems()[0].result.test.issueUrl, 'http://www.example.com')
                dlg.showPopupMenu(point)
        self.assertIn('call()', str(qmenuMock.mock_calls[0]))
        self.assertIn('call().addAction', str(qmenuMock.mock_calls[1]))
        self.assertIn('call().exec_(PyQt5.QtCore.QPoint())', str(qmenuMock.mock_calls[2]))
        self.assertIn("call('Open issue page', None)", str(qactionMock.mock_calls[0]))
        self.assertIn("call().triggered.connect", str(qactionMock.mock_calls[1]))

    def testItemClicked(self):
        """Test that result is set to the clicked value"""
        r = Report()
        for test in self.allTests:
            tr = TestResult(test)
            r.addTestResult(tr)
        dlg = ReportDialog(r)
        self.assertEqual(dlg.resultText.toPlainText(), '')
        dlg.itemClicked()
        self.assertEqual(dlg.resultText.toPlainText(), '')

        currentItem = dlg.resultsTree.topLevelItem(0).child(0)
        dlg.resultsTree.setCurrentItem(currentItem)
        dlg.itemClicked()
        self.assertIn('Test name: -Functional test', dlg.resultText.toPlainText())
        self.assertIn('Test result:Test skipped', dlg.resultText.toPlainText())

    def testOkPressed(self):
        """Check that the widget is closed when OK clicked"""
        r = Report()
        dlg = ReportDialog(r)
        dlg.show()
        self.assertTrue(dlg.isVisible())
        dlg.close()
        self.assertFalse(dlg.isVisible())


def suiteSubset():
    tests = ['testInit']
    suite = unittest.TestSuite(list(map(ReportDialogTests, tests)))
    return suite


def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(ReportDialogTests, 'test'))
    return suite


def run_all():
    unittest.TextTestRunner(verbosity=3, stream=sys.stdout).run(suite())


def run_subset():
    unittest.TextTestRunner(verbosity=3, stream=sys.stdout).run(suiteSubset())


if __name__ == '__main__':
    run_all()
