# -*- coding: utf-8 -*-

#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#

import os
import json
from collections import defaultdict

from qgis.PyQt import uic
from qgis.PyQt.QtCore import Qt, QSettings
from qgis.PyQt.QtWidgets import (QTreeWidgetItem,
                                 QTreeWidgetItemIterator,
                                 QDialog,
                                 QDialogButtonBox,
                                 QSizePolicy,
                                 QApplication)

from qgis.core import QgsApplication, Qgis
from qgis.gui import QgsMessageBar

import qgistester.tests as tests
from qgistester.test import UnitTestWrapper

WIDGET, BASE = uic.loadUiType(os.path.join(os.path.dirname(__file__), 'testselector.ui'))


class TestSelector(BASE, WIDGET):

    def __init__(self):
        super(TestSelector, self).__init__()
        self.setupUi(self)

        self.tests = None

        self.bar = QgsMessageBar()
        self.bar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.layout().insertWidget(1, self.bar)

        allTests = defaultdict(list)
        for test in tests.tests:
            allTests[test.group].append(test)

        for group, groupTests in allTests.items():
            groupItem = QTreeWidgetItem()
            groupItem.setText(0, group)
            groupItem.setFlags(groupItem.flags() | Qt.ItemIsTristate);
            unitItem = QTreeWidgetItem()
            unitItem.setText(0, 'Fully automated tests')
            unitItem.setFlags(unitItem.flags() | Qt.ItemIsTristate);
            manualItem = QTreeWidgetItem()
            manualItem.setText(0, 'Manual and semi-automated tests')
            manualItem.setFlags(manualItem.flags() | Qt.ItemIsTristate);
            unitTestsByCategories = defaultdict(list)
            manualTestsByCategories = defaultdict(list)
            for test in groupTests:
                if isinstance(test, UnitTestWrapper):
                    unitTestsByCategories[test.category].append(test)
                else:
                    manualTestsByCategories[test.category].append(test)
            for testsList, parentItem in [(unitTestsByCategories, unitItem), (manualTestsByCategories, manualItem)]:
                for cat, catTests in testsList.items():
                    categoryItem = QTreeWidgetItem()
                    categoryItem.setText(0, cat)
                    categoryItem.setFlags(manualItem.flags() | Qt.ItemIsTristate);
                    for test in catTests:
                        testItem = QTreeWidgetItem()
                        testItem.setFlags(testItem.flags() | Qt.ItemIsUserCheckable);
                        testItem.setCheckState(0, Qt.Unchecked);
                        testItem.test = test
                        testItem.setText(0, test.name)
                        categoryItem.addChild(testItem)
                    parentItem.addChild(categoryItem)
            if manualItem.childCount():
                groupItem.addChild(manualItem)
            if unitItem.childCount():
                groupItem.addChild(unitItem)
            self.testsTree.addTopLevelItem(groupItem)
            groupItem.setExpanded(True)

        self.testsTree.itemChanged.connect(self.toggleRunButton)
        self.buttonBox.button(QDialogButtonBox.Ok).setText('Run selected tests')
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
        self.buttonBox.accepted.connect(self.okPressed)
        self.buttonBox.rejected.connect(self.cancelPressed)

        self.selectAllLabel.linkActivated.connect(lambda: self.checkTests(lambda t: Qt.Checked))
        self.unselectAllLabel.linkActivated.connect(lambda: self.checkTests(lambda t: Qt.Unchecked))

        def _onlyManual(t):
            if isinstance(t, UnitTestWrapper):
                return Qt.Unchecked
            else:
                return Qt.Checked

        self.onlyManualLabel.linkActivated.connect(lambda: self.checkTests(_onlyManual))

        def _onlyUnit(t):
            if isinstance(t, UnitTestWrapper):
                return Qt.Checked
            else:
                return Qt.Unchecked

        self.onlyUnitLabel.linkActivated.connect(lambda: self.checkTests(_onlyUnit))

        filepath = os.path.expanduser('~/.testerplugin/failed.txt')
        if os.path.exists(filepath):
            with open(filepath) as f:
                failed = json.load(f)
        else:
            failed = []

        def _onlyLastFailures(t):
            if t.group in failed and t.name in failed[t.group]:
                return Qt.Checked
            else:
                return Qt.Unchecked

        self.onlyLastFailuresLabel.linkActivated.connect(lambda: self.checkTests(_onlyLastFailures))

        self.exportButton.clicked.connect(self.export)

    def export(self):
        allTests = defaultdict(list)
        for test in tests.tests:
            allTests[test.group].append(test)

        s = ''
        for group, groupTests in allTests.items():
            s += '- {}\n'.format(group)
            for t in groupTests:
                s += '\t- {}\n'.format(t.name)

        cb = QApplication.clipboard()
        cb.clear(mode=cb.Clipboard )
        cb.setText(s, mode=cb.Clipboard)
        self.bar.pushMessage('', 'Tests list has been copied to your clipboard', level=Qgis.Success, duration=5)

    def checkTests(self, condition):
        self.checkTest(self.testsTree.invisibleRootItem(), condition)

    def checkTest(self, item, condition):
        count = item.childCount()
        if count:
            for i in range(count):
                self.checkTest(item.child(i), condition)
        else:
            try:
                item.setCheckState(0, condition(item.test))
            except:
                pass

    def cancelPressed(self):
        self.close()

    def okPressed(self):
        self.close()

    def toggleRunButton(self):
        self.tests = []
        iterator = QTreeWidgetItemIterator(self.testsTree)
        item = iterator.value()
        while item:
            if item.checkState(0) == Qt.Checked and item.childCount() == 0:
                self.tests.append(item.test)
            iterator += 1
            item = iterator.value()

        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(len(self.tests) > 0)
