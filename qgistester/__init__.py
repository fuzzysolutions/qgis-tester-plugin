# -*- coding: utf-8 -*-

#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#

import os

def classFactory(iface):
    from qgistester.plugin import TesterPlugin
    return TesterPlugin(iface)

