#-*- coding: utf8 -*
#
# Max E. Kuznecov ~syhpoon <mek@mek.uz.ua> 2008-2009
#
# This file is part of XYZCommander.
# XYZCommander is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# XYZCommander is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser Public License for more details.
# You should have received a copy of the GNU Lesser Public License
# along with XYZCommander. If not, see <http://www.gnu.org/licenses/>.

# Core tests

import __builtin__
import locale
import tempfile
import os

import libxyz.core as core

from nose.tools import raises
from libxyz.exceptions import *

# Global data
xyz = None
files = {}

def setup():
    global xyz, filesw
    
    xyz = core.XYZData()
    __builtin__._ = lambda x: x
    __builtin__.xyzenc = locale.getpreferredencoding()

    # Setup files
    files["actions_good"], files["actions_bad"] = setup_actions()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def setup_actions():
    fd_good, path_good = tempfile.mkstemp(text=True)
    fd_bad, path_bad = tempfile.mkstemp(text=True)
    os.write(fd_good, """action(r'iname{".*\.pdf$"}', lambda obj: obj)""")
    os.write(fd_bad, ":(")

    return path_good, path_bad

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
def teardown():
    global files
    
    for k in files:
        os.unlink(files[k])

#### Tests

@raises(XYZValueError)
def test_queue_input_arg():
    core.Queue("wrong")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def test_func():
    size = 5
    
    q = core.Queue(size)

    for i in range(size):
        q.push(i)

    _res = []

    for i in range(size):
        _res.append(q.pop())

    assert _res == list(range(size))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
@raises(IndexError)
def test_queue_pop():
    core.Queue(1).pop()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def test_queue_tail1():
    assert core.Queue(1).tail() is None

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def test_queue_tail2():
    q = core.Queue(1)
    q.push("abc")
    assert q.tail() == "abc"

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TestActionManager(object):
    def setUp(self):
        self.xyz = core.XYZData()
        self.am = core.ActionManager(xyz, [])

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @raises(XYZRuntimeError)
    def testRegisterIncorrectRule(self):
        self.am.register("WRONG", lambda: None)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testRegisterCorrectRule(self):
        assert self.am.register("size{100}", lambda: None) is None

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @raises(XYZRuntimeError)
    def testParseConfigIncorrect(self):
        global files

        xyz = core.XYZData()
        dsl = core.dsl.XYZ(xyz)

        am = core.ActionManager(xyz, [files["actions_bad"], "none"])
        xyz.am = am

        am.parse_configs()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def testParseConfigCorrect(self):
        global files

        xyz = core.XYZData()
        dsl = core.dsl.XYZ(xyz)
        am = core.ActionManager(xyz, [files["actions_good"], "none"])
        xyz.am = am

        assert am.parse_configs() is None
