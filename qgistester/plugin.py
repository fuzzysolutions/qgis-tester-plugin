# -*- coding: utf-8 -*-

#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#

import os

from qgis.PyQt.QtCore import Qt, QUrl
from qgis.PyQt.QtGui import QIcon, QDesktopServices
from qgis.PyQt.QtWidgets import QAction, QMessageBox

from qgis.core import QgsApplication

from qgistester.testerwidget import TesterWidget
from qgistester.testselector import TestSelector
from qgistester.settingswindow import SettingsWindow
from qgistester.tests import addTestModule
from qgistester.manualtests import manualtests

pluginPath = os.path.dirname(__file__)


class TesterPlugin:

    def __init__(self, iface):
        self.iface = iface
        self.lastSettings = {}
        self.widget = None
        self.iface.initializationCompleted.connect(self.hideWidget)

        addTestModule(manualtests, 'Tester Plugin')

    def initGui(self):
        self.action = QAction('Start testing', self.iface.mainWindow())
        self.action.setIcon(QIcon(os.path.join(pluginPath, 'plugin.svg')))
        self.action.setObjectName('testerStart')
        self.action.triggered.connect(self.test)
        self.iface.addPluginToMenu('Tester', self.action)

        self.actionHelp = QAction('Help', self.iface.mainWindow())
        self.actionHelp.setIcon(QgsApplication.getThemeIcon('/mActionHelpContents.svg'))
        self.actionHelp.setObjectName('testerHelp')
        self.actionHelp.triggered.connect(self.openHelp)
        self.iface.addPluginToMenu('Tester', self.actionHelp)

        self.actionAbout = QAction('About…', self.iface.mainWindow())
        self.actionAbout.setIcon(QIcon(os.path.join(pluginPath, 'about.svg')))
        self.actionAbout.setObjectName('testerAbout')
        self.actionAbout.triggered.connect(self.about)
        self.iface.addPluginToMenu('Tester', self.actionAbout)

    def unload(self):
        self.iface.removePluginMenu('Tester', self.action)
        self.iface.removePluginMenu('Tester', self.actionHelp)
        self.iface.removePluginMenu('Tester', self.actionAbout)

        if self.widget:
            self.widget.hide()
            del self.widget

    def hideWidget(self):
        if self.widget:
            self.widget.hide()

    def test(self):
        if self.widget is not None and self.widget.isVisible():
            QMessageBox.warning(self.iface.mainWindow(), 'Tester plugin', 'A test cycle is currently being run')
            return

        dlg = TestSelector()
        dlg.exec_()
        if dlg.tests:
            settings = {}
            for test in dlg.tests:
                settings.update(test.settings)
            settings.update(self.lastSettings)
            if settings:
                settingsDlg = SettingsWindow(settings)
                settingsDlg.exec_()
                if not settingsDlg.settings:
                    return
                self.lastSettings = settingsDlg.settings
                for key, value in list(settingsDlg.settings.items()):
                    os.environ[key] = value
            self.widget = TesterWidget()
            self.widget.testingFinished.connect(self.testingFinished)
            self.iface.addDockWidget(Qt.TopDockWidgetArea, self.widget)
            self.widget.show()
            self.widget.setTests(dlg.tests)
            self.widget.startTesting()

    def testingFinished(self):
        dlg = self.widget.getReportDialog()
        dlg.exec_()
        reopen = dlg.reopen
        self.widget = None
        if reopen:
            self.test()

    def openHelp(self):
        url = QUrl('file://{}'.format(os.path.join(pluginPath, 'docs',  'html', 'index.html')))
        QDesktopServices.openUrl(url)

    def about(self):
        pass
