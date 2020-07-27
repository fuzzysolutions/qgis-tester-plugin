# -*- coding: utf-8 -*-

#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#

import os
import configparser

from qgis.PyQt.QtCore import Qt, QUrl
from qgis.PyQt.QtGui import QIcon, QDesktopServices
from qgis.PyQt.QtWidgets import QAction, QMessageBox

from qgis.core import QgsApplication, QgsMessageOutput

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
        cfg = configparser.ConfigParser()
        cfg.read(os.path.join(pluginPath, 'metadata.txt'))
        info = cfg['general']

        html = '<style>body, table {padding:0px; margin:0px; font-family:verdana; font-size: 1.1em;}</style>'
        html += '<body>'
        html += '<table cellspacing="4" width="100%"><tr><td>'
        html += '<h1>{}</h1>'.format(info['name'])
        html += '<h3>{}</h3>'.format(info['description'])
        if info['about'] != '':
            html += info['about'].replace('\n', '<br/>')
        html += '<br/><br/>'

        if info['category'] != '':
            html += '{}: {} <br/>'.format('Category', info['category'])

        if info['tags'] != '':
            html += '{}: {} <br/>'.format('Tags', info['tags'])

        if info['homepage'] != '' or info['tracker'] != '' or info['code_repository'] != '':
            html += 'More info:'
            if info['homepage'] != '':
                html += '<a href="{}">{}</a> &nbsp;'.format(info['homepage'], 'Homepage')

            if info['tracker'] != '':
                html += '<a href="{}">{}</a> &nbsp;'.format(info['tracker'], 'Bug tracker')

            if info['repository'] != '':
                html += '<a href="{}">{}</a> &nbsp;'.format(info['repository'], 'Code repository')

            html += '<br/>'

        html += '<br/>'
        if info['email'] != '':
            html += '{}: <a href="mailto:{}">{}</a>'.format('Author', info['email'], info['author'])
            html += '<br/><br/>'
        elif info['author'] != '':
            html += '{}: {}'.format('Author', info['author'])
            html += '<br/><br/>'

        if info['version'] != '':
            html += 'Installed version: {}<br/>'.format(info['version'])

        if 'changelog' in info and info['changelog'] != '':
            html += '<br/>'
            changelog = 'Changelog:<br/>{} <br/>'.format(info['changelog'])
            html += changelog.replace('\n', '<br/>')

        html += '</td></tr></table>'
        html += '</body>'

        dlg = QgsMessageOutput.createMessageOutput()
        dlg.setTitle('Plugin info')
        dlg.setMessage(html, QgsMessageOutput.MessageHtml)
        dlg.showMessage()

