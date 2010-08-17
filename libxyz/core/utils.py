#-*- coding: utf8 -*
#
# Max E. Kuznecov ~syhpoon <mek@mek.uz.ua> 2008
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

import sys
import os
import termios
import copy
import types

from libxyz.parser import Lexer
from libxyz.exceptions import XYZValueError

def ustring(string, enc=None):
    """
    Return unicode string
    """

    if isinstance(string, unicode):
        return string

    if enc is None:
        enc = xyzenc

    if not isinstance(string, str):
        return unicode(string)

    # String
    return string.decode(enc, 'replace')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def bstring(bstr, enc=None):
    """
    Return encoded byte string
    """

    if isinstance(bstr, str):
        return bstr
    
    if enc is None:
        enc = xyzenc

    if not isinstance(bstr, unicode):
        return str(bstr)

    return bstr.encode(enc, 'replace')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def term_settings():
    """
    Return current terminal settings
    """
    
    stdin = sys.stdin.fileno()

    # WTF?
    if not os.isatty(stdin):
        return None

    return termios.tcgetattr(stdin)
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def setup_term():
    """
    Terminal initialization
    @return: Old terminal settings
    """

    term = term_settings()
    stdin = sys.stdin.fileno()

    if term is None:
        return None
    
    try:
        vdisable = os.fpathconf(stdin, "PC_VDISABLE")
    except ValueError:
        return

    _saved_term = copy.deepcopy(term[-1])

    # Disable special symbols
    _todisable = [getattr(termios, x) for x in ("VQUIT",     # ^\
                                                "VINTR",     # ^C
                                                "VSUSP",     # ^Z
                                                "VLNEXT",    # ^V
                                                "VSTART",    # ^Q
                                                "VSTOP",     # ^S
                                                "VDISCARD",  # ^O
                                                )]

    for _key in _todisable:
        term[-1][_key] = vdisable

    termios.tcsetattr(stdin, termios.TCSANOW, term)

    return _saved_term

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def restore_term(term_data):
    """
    Restore terminal settings
    """
    
    stdin = sys.stdin.fileno()

    term = term_settings()

    if term is None:
        return None
    
    term[-1] = term_data

    if os.isatty(stdin):
        termios.tcsetattr(stdin, termios.TCSANOW, term)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def is_func(obj):
    """
    Check if object is of function type
    """
    
    return isinstance(obj, types.FunctionType) or \
           isinstance(obj, types.MethodType)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def intersect(s1, s2):
    """
    Find intersection between two strings
    """

    s1 = ustring(s1)
    s2 = ustring(s2)

    for index in range(len(s2) - 1, 0, -1):
        if s1.endswith(s2[:index]):
            return s2[index:]

    return s2

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def split_cmd(cmd):
    """
    Split command line
    """

    lexer = Lexer(ustring(cmd), [])
    lexer.escaping_on()

    data = []

    while True:
        res = lexer.lexer()

        if res is None:
            break
        else:
            __, val = res
            data.append(val)

    return data

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def typer(*types, **kw):
    msg = kw.get('msg', _(u"Invalid argument type %s"))
    error = kw.get('error', XYZValueError)

    def _wrap1(fun):
        def _wrap2(*args, **kwargs):
            for t, arg in zip(types, args):
                if t is not None:
                    if not isinstance(arg, t):
                        raise error(msg % str(type(arg)))

            return fun(*args, **kwargs)

        return _wrap2

    return _wrap1
