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

from nose.tools import raises
from libxyz.exceptions import XYZValueError
from libxyz.core import Queue

def setup():
    import __builtin__
    __builtin__._ = lambda x: x

def teardown():
    pass

#### Tests

@raises(XYZValueError)
def test_queue_input_arg():
    Queue("wrong")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def test_func():
    size = 5
    
    q = Queue(size)

    for i in range(size):
        q.push(i)

    _res = []

    for i in range(size):
        _res.append(q.pop())

    assert _res == list(range(size))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
@raises(IndexError)
def test_queue_pop():
    Queue(1).pop()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def test_queue_tail1():
    assert Queue(1).tail() is None

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def test_queue_tail2():
    q = Queue(1)
    q.push("abc")
    assert q.tail() == "abc"

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
