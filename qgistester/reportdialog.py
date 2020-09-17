# -*- coding: utf-8 -*-

"""
***************************************************************************
    reportdialog.py
    ---------------------
    Date                 : November 2015
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
__date__ = 'November 2015'
__copyright__ = '(C) 2015 Boundless, http://boundlessgeo.com'


import os
import json
import codecs
import webbrowser
from collections import defaultdict

from qgis.PyQt import uic
from qgis.PyQt.QtCore import Qt, QSettings, QFileInfo
from qgis.PyQt.QtWidgets import (QTreeWidgetItem,
                                 QMenu,
                                 QAction,
                                 QFileDialog,
                                 QPushButton,
                                 QDialogButtonBox,
                                 QMessageBox)
from qgis.PyQt.QtGui import QColor
from qgis.core import QgsApplication

WIDGET, BASE = uic.loadUiType(os.path.join(os.path.dirname(__file__), 'reportdialog.ui'))


class ReportDialog(BASE, WIDGET):

    resultColor = [Qt.green, Qt.red, Qt.gray, Qt.magenta, QColor(237, 189, 129)]
    resultTag = ['PASSED', 'FAILED', 'SKIPPED', 'CONTAINS_ERROR', 'FAILED_AT_SETUP']

    def __init__(self, report):
        super(ReportDialog, self).__init__()
        self.setupUi(self)

        self.actionSaveAll.setIcon(QgsApplication.getThemeIcon('/mActionFileSave.svg'))
        self.actionSaveSelected.setIcon(QgsApplication.getThemeIcon('/mActionFileSaveAs.svg'))
        self.actionOpenTracker.setIcon(QgsApplication.getThemeIcon('/mActionHelpAPI.png'))

        self.actionSaveAll.triggered.connect(lambda: self.saveResults(True))
        self.actionSaveSelected.triggered.connect(lambda: self.saveResults(False))

        self.resultsTree.clear()

        results = report.results

        self.saveFailed(results)

        self.reopen = False

        allResults = defaultdict(list)
        for result in results:
            test = result.test
            allResults[test.group].append(result)

        for group, groupResults in list(allResults.items()):
            groupItem = QTreeWidgetItem()
            groupItem.setText(0, group)
            for result in groupResults:
                resultItem = QTreeWidgetItem()
                resultItem.result = result
                resultItem.setText(0, result.test.name)
                resultItem.setForeground(0, self.resultColor[result.status])
                groupItem.addChild(resultItem)
            self.resultsTree.addTopLevelItem(groupItem)

        self.resultsTree.expandAll()
        self.resultsTree.itemClicked.connect(self.itemClicked)
        self.resultsTree.customContextMenuRequested.connect(self.showPopupMenu)

        button = QPushButton('Re-open test selector');
        def _reopen():
            self.reopen = True
            self.close()
        button.clicked.connect(_reopen)

        self.buttonBox.addButton(button, QDialogButtonBox.ActionRole);

        self.buttonBox.rejected.connect(self.close)

    def saveFailed(self, results):
        allFailed = {}
        allResults = defaultdict(list)
        for result in results:
            test = result.test
            allResults[test.group].append(result)
        for group, groupResults in list(allResults.items()):
            failed = []
            for result in groupResults:
                if result.status in [1, 3, 4]:
                    failed.append(result.test.name)
            allFailed[group] = failed
        folder = os.path.expanduser('~/.testerplugin')
        if not os.path.exists(folder):
            os.makedirs(folder)
        filepath = os.path.join(folder, 'failed.txt')
        with open(filepath, 'w') as f:
            json.dump(allFailed, f)

    def showPopupMenu(self, point):
        item = self.resultsTree.selectedItems()[0]
        if not hasattr(item, 'result'):
            return
        url = item.result.test.issueUrl
        if url:
            menu = QMenu()
            action = QAction('Open issue page', None)
            action.triggered.connect(lambda: webbrowser.open_new(url))
            menu.addAction(action)
            point = self.mapToGlobal(point)
            menu.exec_(point)

    def itemClicked(self):
        try:
            result= self.resultsTree.currentItem().result
        except:
            return
        self.resultText.setText(str(result))

    def saveResults(self, saveAll=False):
        currentItem = self.resultsTree.currentItem()
        if not saveAll and not hasattr(currentItem, 'result'):
            QMessageBox.warning(self, 'Save results', 'No test item selected')
            return

        settings = QSettings('Boundless', 'qgistester')
        lastDirectory = settings.value('lastDirectory', '.')
        fileName, _ = QFileDialog.getSaveFileName(self,
                                                  self.tr('Save file'),
                                                  lastDirectory,
                                                  self.tr('HTML files (*.html)'))

        if fileName == '':
            return

        if not fileName.lower().endswith('.html'):
            fileName += '.html'

        settings.setValue('lastDirectory', QFileInfo(fileName).absoluteDir().absolutePath())

        out = '<html><head>'
        out += '<meta http-equiv="Content-Type" content="text/html; charset=utf-8" /></head><body>'

        if saveAll:
            for i in range(self.resultsTree.topLevelItemCount()):
                groupItem = self.resultsTree.topLevelItem(i)
                out += '<h3>{}</h3>'.format(groupItem.text(0))
                out += '<ul>'
                for j in range(groupItem.childCount()):
                    results = groupItem.child(j).result
                    out += '<li>[{}] {}'.format(self.resultTag[results.status], results.test.name)
                    if results.status not in [results.SKIPPED, results.PASSED]:
                        out += '<p>Failed at step "{}" with message</p>'.format(results.errorStep)
                        out += '<code>{}</code>'.format(results.errorMessage)
                    out += '</li>'
                out += '</ul>'
        else:
            results = self.resultsTree.currentItem().result
            out += '<h3>{}</h3>'.format(results.test.group)
            out += '<ul>'
            out += '<li>[{}] {}'.format(self.resultTag[results.status], results.test.name)
            if results.status not in [results.SKIPPED, results.PASSED]:
                out += '<p>Failed at step "{}" with message</p>'.format(results.errorStep)
                out += '<code>{}</code>'.format(results.errorMessage)
            out += '</li></ul>'
        out += '</body></html>'

        with codecs.open(fileName, 'w', encoding='utf-8') as f:
            f.write(out)
