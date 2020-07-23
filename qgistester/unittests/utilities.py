# -*- coding: utf-8 -*-

#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#

__author__ = 'Luigi Pirelli'
__date__ = 'April 2016'
__copyright__ = '(C) 2016 Boundless, http://boundlessgeo.com'

import os
import sys

# add current module to PYTHONPATH
path = os.path.join(os.path.abspath(os.path.dirname(__file__)), os.path.pardir, os.path.pardir)
sys.path.insert(1, path)
