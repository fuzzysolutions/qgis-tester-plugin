# -*- coding: utf-8 -*-

"""
***************************************************************************
    utilities.py
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

import os
import sys

# add current module to PYTHONPATH
path = os.path.join(os.path.abspath(os.path.dirname(__file__)), os.path.pardir, os.path.pardir)
sys.path.insert(1, path)

