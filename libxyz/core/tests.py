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
from libxyz.vfs import VFSDispatcher

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

class TestQueue(object):
    """
    libxyz.core.Queue tests
    """
    
    def setUp(self):
        self.q = core.Queue(1)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @raises(XYZValueError)
    def test_queue_input_arg(self):
        core.Queue("wrong")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    @raises(IndexError)
    def test_queue_pop(self):
        self.q.pop()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def test_queue_tail1(self):
        assert self.q.tail() is None

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def test_queue_tail2(self):
        self.q.push("abc")
        assert self.q.tail() == "abc"

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def test_func(self):
        size = 5
    
        q = core.Queue(size)

        for i in range(size):
            q.push(i)

        _res = []

        for i in range(size):
            _res.append(q.pop())

        assert _res == list(range(size))

#++++++++++++++++++++++++++++++++++++++++++++++++

class TestActionManager(object):
    """
    libxyz.core.ActionManager tests
    """
    
    def setUp(self):
        self.xyz = core.XYZData()
        self.dsl = core.dsl.XYZ(self.xyz)
        self.am = core.ActionManager(xyz, [])
        self.xyz.vfs = VFSDispatcher(self.xyz)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def tearDown(self):
        core.dsl.XYZ._clear()
        
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
        am = core.ActionManager(self.xyz, [files["actions_bad"], "none"])
        self.xyz.am = am

        am.parse_configs()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def testParseConfigCorrect(self):
        am = core.ActionManager(self.xyz, [files["actions_good"], "none"])
        self.xyz.am = am

        assert am.parse_configs() is None

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testMatch(self):
        vfs_size = self.xyz.vfs.dispatch("/tmp/test_size")
        vfs_size.size = 100
        vfs_name = self.xyz.vfs.dispatch("/tmp/test_name")
        vfs_owner = self.xyz.vfs.dispatch("/tmp/test_owner")
        vfs_owner.uid = 500
        vfs_owner.gid = 501

        self.am.register("size{100}", lambda: "size")
        self.am.register("name{test_name}", lambda: "name")
        self.am.register("owner{500:501}", lambda: "owner")

        assert self.am.match(vfs_size)() == "size"
        assert self.am.match(vfs_name)() == "name"
        assert self.am.match(vfs_owner)() == "owner"

#++++++++++++++++++++++++++++++++++++++++++++++++

class TestDSL(object):
    def setUp(self):
        self.xyz = core.XYZData()
        self.xyz.conf = {"xyz": {}}
        self.xyz.conf["xyz"]["plugins"] = {":core:shell": "ENABLE"}
        self.xyz.km = core.KeyManager(self.xyz, [])
        self.xyz.pm = core.plugins.PluginManager(self.xyz, [])
        self.dsl = core.dsl.XYZ(self.xyz)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def tearDown(self):
        self.dsl._clear()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def setupValues(self):
        # Local section
        self.dsl.let("var1", "val1")
        # Test section
        self.dsl.let("var2", "val2", sect="test")
        # Dict value
        self.dsl.let("dictvar", {1: 2, 3: 4})
        self.dsl.let("dictvar", {3: 33, 5: 6})
        
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    @raises(DSLError)
    def testNotInstantiated(self):
        self.dsl._clear()
        self.dsl.let("a", "b")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testLetVal(self):
        self.setupValues()
        
        assert self.xyz.conf["local"]["var1"] == "val1"
        assert self.xyz.conf["test"]["var2"] == "val2"
        assert self.xyz.conf["local"]["dictvar"] == {1: 2, 3: 33, 5: 6}

        assert self.dsl.val("var1") == "val1"
        assert self.dsl.val("var2", "test") == "val2"
        assert self.dsl.val("dictvar") == {1: 2, 3: 33, 5: 6}

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testUnlet(self):
        self.setupValues()

        assert self.dsl.val("var1") == "val1"
        self.dsl.unlet("var1")
        assert self.dsl.val("var1") is None

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testLoad(self):
        self.dsl.load(":core:shell:execute")
