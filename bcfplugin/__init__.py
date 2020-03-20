"""
Copyright (C) 2019 PODEST Patrick

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
"""

"""
Author: Patrick Podest
Date: 2019-08-16
Github: @podestplatz

**** Description ****
This file initializes the plugin global variables and imports everything from
the programmaticInterface into the plugin global namespace. It further is
responsible for checking whether all dependency requirements are met by the
system.
It further initializes the logging system of python and provides
`createLogger()` which is intended to be called by every submodule to attain a
separate instance of logging.Logger.
"""

import os
import sys
import logging
import importlib
from enum import Enum

import bcfplugin.util as util
from bcfplugin.loghandlers.stdoutfilter import StdoutFilter

excPath = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, excPath)

__all__ = ["programmaticInterface", "ui"]

LOGFORMAT = "[%(levelname)s]%(module)s.%(funcName)s(): %(message)s"
""" Format of all logged messages """

PREFIX = "bcfplugin_"

LOGFILE = "{}log.txt".format(PREFIX)


def printErr(msg):

    """ Print an error using stderr. """

    print(msg, file=sys.stderr)


def printInfo(msg):

    """ Print an informational message using stdout. """

    print(msg)


def getStdoutHandler():

    """ Returns a handler for the logging facility of python, writing the
    messages to stdout """

    handler = logging.StreamHandler(stream = sys.stdout)
    handler.setLevel(logging.DEBUG)

    filter = StdoutFilter()
    format = logging.Formatter(LOGFORMAT)
    handler.setFormatter(format)
    handler.addFilter(filter)

    return handler


def getFileHandler(fpath):

    """ Returns a handler for the logging facility of python, writing the
    messages to file `fpath` """

    handler = logging.FileHandler(fpath)
    handler.setLevel(logging.DEBUG)

    format = logging.Formatter(LOGFORMAT)
    handler.setFormatter(format)

    return handler


def createLogger(name):

    """ Creates a new logger instance with module name = `name`.

    The new instance is then returned.
    """

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    return logger


frontend = None

# delete temporary artifacts
import util
util.deleteTmp()

# create working directory
path = util.getSystemTmp()
logfile = os.path.join(path, LOGFILE)

# generate config for root logger
logHandlers = [getFileHandler(logfile)]
logHandlers.append(getStdoutHandler())
logging.basicConfig(level=logging.INFO, handlers=logHandlers)

from programmaticInterface import *
