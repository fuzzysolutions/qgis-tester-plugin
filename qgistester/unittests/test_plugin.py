# -*- coding: utf-8 -*-

"""
***************************************************************************
    test_plugin.py
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
from unittest.mock import call

from qgis.PyQt.QtWidgets import QWidget, QAction, QMessageBox

import utilities
from qgistesting import start_app
from qgistesting.mocked import get_iface

import qgistester
from qgistester.plugin import TesterPlugin
from qgistester.test import Test


class TesterTests(unittest.TestCase):
    """Tests for the TesterPlugin class"""

    @classmethod
    def setUpClass(cls):
        cls.QGIS_APP = start_app(cleanup=False)
        assert cls.QGIS_APP is not None
        cls.IFACE_Mock = get_iface()
        assert cls.IFACE_Mock is not None

    def testInit(self):
        """Check that the plugin is loaded correctly"""
        self.IFACE_Mock.reset_mock()
        self.testerPlugin = TesterPlugin(self.IFACE_Mock)
        self.assertEqual(len(self.IFACE_Mock.mock_calls), 1)
        stringToFind = 'call.initializationCompleted.connect(<bound method TesterPlugin.hideWidget of <qgistester.plugin.TesterPlugin'
        self.assertIn(stringToFind, str(self.IFACE_Mock.mock_calls[-1]))

        self.assertEqual(self.IFACE_Mock, self.testerPlugin.iface)
        self.assertIsNone(self.testerPlugin.widget)

    def testHideWidget(self):
        """Check that the test widget is hidden by default"""
        testerPlugin = TesterPlugin(self.IFACE_Mock)
        testerPlugin.widget = mock.Mock(spec=QWidget)
        self.assertEqual(len(testerPlugin.widget.mock_calls), 0)
        testerPlugin.hideWidget()
        self.assertEqual(len(testerPlugin.widget.mock_calls), 1)
        self.assertEqual('call.hide()', str(testerPlugin.widget.mock_calls[-1]))

    def testUnload(self):
        """Check that the plugin unloaded correctly"""
        testerPlugin = TesterPlugin(self.IFACE_Mock)
        action = QAction('Start testing', self.IFACE_Mock.mainWindow())
        actionHelp = QAction('Help', self.IFACE_Mock.mainWindow())
        actionAbout = QAction('About…', self.IFACE_Mock.mainWindow())
        testerPlugin.action = action
        testerPlugin.actionHelp = actionHelp
        testerPlugin.actionAbout = actionAbout
        testerPlugin.widget = mock.MagicMock(QWidget)

        self.IFACE_Mock.reset_mock()
        testerPlugin.unload()
        self.assertEqual(len(self.IFACE_Mock.mock_calls), 3)
        self.assertNotIn('widget', testerPlugin.__dict__)

    def testInitGui(self):
        """Check that the plugin UI initialised correctly"""
        testerPlugin = TesterPlugin(self.IFACE_Mock)
        self.assertNotIn('action', testerPlugin.__dict__)

        testerPlugin.iface.reset_mock()
        testerPlugin.initGui()
        self.assertIsNotNone(testerPlugin.action)
        self.assertTrue(isinstance(testerPlugin.action, QAction))
        self.assertEqual(testerPlugin.action.receivers(testerPlugin.action.triggered), 1)
        # number of calls to addPluginToMenu should be equal to the number of actions in the plugin menu
        self.assertEqual(sum(map(lambda x : 'addPluginToMenu' in x, testerPlugin.iface.mock_calls)), 3)

    def testTest(self):
        """Check test method"""

        """
        1) test if messageBox.warning is called
        2) open test selector widget
            2.1) cancel => do nothing
            2.2) ok =>
                2.2.1) Create TesterWidget and dock it
                2.2.2) load tests in it
                2.2.3) start running test
        """
        qwidget = mock.Mock(spec=QWidget)
        qwidget.isVisible.return_value = True
        testerPlugin = TesterPlugin(self.IFACE_Mock)
        testerPlugin.widget = qwidget
        qmessageboxMock = mock.Mock(spec=QMessageBox.warning)
        with mock.patch('PyQt5.QtWidgets.QMessageBox.warning', qmessageboxMock):
            testerPlugin.test()
        self.assertEqual('Tester plugin', str(qmessageboxMock.call_args[0][1]))
        self.assertEqual('A test cycle is currently being run', str(qmessageboxMock.call_args[0][2]))

        # test 2.1
        dlgMock = mock.Mock()
        dlgMock.tests = None
        testselectorMock = mock.Mock(spec=qgistester.testselector.TestSelector, return_value=dlgMock)
        testerPlugin = TesterPlugin(self.IFACE_Mock)
        # needed to go through the first tested if condition
        testerPlugin.widget = None
        with mock.patch('qgistester.plugin.TestSelector', testselectorMock):
            testerPlugin.test()
        self.assertIsNone(testerPlugin.widget)

        # test 2.2 and 2.3
        self.IFACE_Mock.reset_mock
        testselectorMock.reset_mock
        dlgMock.reset_mock
        mytest = Test('some tests')
        mytest.settings = {}
        dlgMock.tests = [mytest]
        testerwidgetMock = mock.Mock(spec=qgistester.testerwidget.TesterWidget, return_value=dlgMock)
        testerPlugin = TesterPlugin(self.IFACE_Mock)
        # needed to go through the first tested if condition
        testerPlugin.widget = None
        with mock.patch('qgistester.plugin.TestSelector', testselectorMock):
            with mock.patch('qgistester.plugin.TesterWidget', testerwidgetMock):
                testerPlugin.test()
        self.assertIsNotNone(testerPlugin.widget)
        self.assertIn('call.addDockWidget', str(testerPlugin.iface.mock_calls[-1]))
        expected = [call.exec_(), call.exec_(), call.testingFinished.connect(testerPlugin.testingFinished),
                    call.show(), call.setTests([mytest]), call.startTesting()]
        self.assertEqual(dlgMock.mock_calls, expected)


def suiteSubset():
    tests = ['testInit']
    suite = unittest.TestSuite(list(map(TesterTests, tests)))
    return suite


def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(TesterTests, 'test'))
    return suite


def run_all():
    unittest.TextTestRunner(verbosity=3, stream=sys.stdout).run(suite())


def run_subset():
    unittest.TextTestRunner(verbosity=3, stream=sys.stdout).run(suiteSubset())


if __name__ == '__main__':
    run_all()
