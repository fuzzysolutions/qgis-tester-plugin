# coding=utf-8

"""Safe Translations Test.

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

__author__ = 'ismailsunni@yahoo.co.id'
__date__ = '12/10/2011'
__copyright__ = ('Copyright 2012, Australia Indonesia Facility for '
                 'Disaster Reduction')

"""

import os
import sys
import unittest

from qgis.PyQt.QtCore import QCoreApplication, QTranslator


class SafeTranslationsTest(unittest.TestCase):
    """Test that translations work."""

    def setUp(self):
        if 'LANG' in iter(list(os.environ.keys())):
            os.environ.__delitem__('LANG')

    def tearDown(self):
        if 'LANG' in iter(list(os.environ.keys())):
            os.environ.__delitem__('LANG')

    @unittest.skip('Skip until locale translation will be set')
    def test_qgis_translations(self):
        """Test that translations work."""
        parent_path = os.path.join(__file__, os.path.pardir, os.path.pardir)
        dir_path = os.path.abspath(parent_path)
        file_path = os.path.join(dir_path, 'i18n', 'af.qm')
        translator = QTranslator()
        translator.load(file_path)
        QCoreApplication.installTranslator(translator)

        expected_message = 'Goeie more'
        real_message = QCoreApplication.translate('@default', 'Good morning')
        self.assertEqual(real_message, expected_message)


def suiteSubset():
    tests = ['test_qgis_translations']
    suite = unittest.TestSuite(list(map(SafeTranslationsTest, tests)))
    return suite


def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(SafeTranslationsTest, 'test'))
    return suite


def run_all():
    unittest.TextTestRunner(verbosity=3, stream=sys.stdout).run(suite())


def run_subset():
    unittest.TextTestRunner(verbosity=3, stream=sys.stdout).run(suiteSubset())


if __name__ == '__main__':
    run_all()
