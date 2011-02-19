#-*- coding: utf8 -*
#
# Max E. Kuznecov <syhpoon@syhpoon.name> 2008
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

import stat
import pwd
import grp
import re

import libxyz.parser as parser

from libxyz.exceptions import XYZValueError
from libxyz.exceptions import LexerError
from libxyz.exceptions import FSRuleError
from libxyz.vfs.vfsobj import  VFSObject
from libxyz.vfs.types import *
from libxyz.core.utils import ustring, is_func

class FSRule(parser.BaseParser):
    """
    FS rule parser

    Rule syntax is following:

    rule            ::= expr $
                        | expr op rule
    expr            ::= expr_body
                        | NOT expr_body
                        | "(" rule ")"
    expr_body       ::= ftype "{" ARG "}"
    op              ::= AND | OR
    ftype           ::= TYPE | PERM | OWNER | NAME | SIZE
                        | LINK_TYPE | LINK_PERM | LINK_OWNER | LINK_NAME
                        | LINK_EXISTS | LINK_SIZE

    Examples:

    type{file} and perm{+0111}
    (owner{user} and not owner{:group}) or owner{root}
    """

    # Tokens
    TOKEN_TYPE = "type"
    TOKEN_PERM = "perm"
    TOKEN_OWNER = "owner"
    TOKEN_NAME = "name"
    TOKEN_INAME = "iname"
    TOKEN_SIZE = "size"
    TOKEN_LINK_TYPE = "link_type"
    TOKEN_LINK_PERM = "link_perm"
    TOKEN_LINK_OWNER = "link_owner"
    TOKEN_LINK_NAME = "link_name"
    TOKEN_LINK_INAME = "link_iname"
    TOKEN_LINK_EXISTS = "link_exists"
    TOKEN_LINK_SIZE = "link_size"
    TOKEN_AND = "and"
    TOKEN_OR = "or"
    TOKEN_NOT = "not"
    TOKEN_OPEN_BR = "{"
    TOKEN_CLOSE_BR = "}"
    TOKEN_OPEN_PAR = "("
    TOKEN_CLOSE_PAR = ")"
    TOKEN_DEFAULT = True
    TOKEN_ARG = False
    EOF = None

    TOKENS_EXTENDED = []
    TRANSFORM_EXTENDED = {}

    TOKENS = [TOKEN_TYPE, TOKEN_PERM, TOKEN_OWNER, TOKEN_NAME, TOKEN_INAME,
              TOKEN_LINK_TYPE, TOKEN_LINK_PERM, TOKEN_LINK_OWNER,
              TOKEN_LINK_NAME, TOKEN_LINK_INAME, TOKEN_LINK_EXISTS,
              TOKEN_AND, TOKEN_OR, TOKEN_NOT, TOKEN_OPEN_BR, TOKEN_CLOSE_BR,
              TOKEN_OPEN_PAR, TOKEN_CLOSE_PAR, TOKEN_DEFAULT,
              TOKEN_SIZE, TOKEN_LINK_SIZE, EOF]

    # Nonterminals
    NTOKEN_START = 100
    NTOKEN_RULE = 101
    NTOKEN_EXPR = 102
    NTOKEN_EXPR_BODY = 103
    NTOKEN_OP = 104
    NTOKEN_FTYPE = 105

    FTYPE = [TOKEN_TYPE,
             TOKEN_PERM,
             TOKEN_OWNER,
             TOKEN_NAME,
             TOKEN_INAME,
             TOKEN_SIZE,
             TOKEN_LINK_TYPE,
             TOKEN_LINK_PERM,
             TOKEN_LINK_OWNER,
             TOKEN_LINK_NAME,
             TOKEN_LINK_INAME,
             TOKEN_LINK_EXISTS,
             TOKEN_LINK_SIZE,
            ]

    INFIX_OP = (TOKEN_AND, TOKEN_OR)

    @classmethod
    def extend(cls, token, trans_func, match_func):
        """
        Extend FSRule parser with new expressions
        @param token: new token expression
        @param trans_func: Transformation function
        @param match_func: Match function
        """

        if token in cls.TOKENS_EXTENDED or token in cls.TOKENS or \
        token in cls.FTYPE:
            raise FSRuleError(_(u"Error extending FSRule: "\
                                u"token %s already registered") % token)

        if not callable(trans_func) or not callable(match_func):
            raise FSRuleError(_(u"Error extending FSRule: "\
                                u"trans_func and match_func arguments "\
                                u"must be functions."))

        # 1. Append token to lists
        cls.TOKENS_EXTENDED.append(token)
        cls.TOKENS.append(token)
        cls.FTYPE.append(token)

        # 2. Add transformation func
        cls.TRANSFORM_EXTENDED[token] = trans_func

        # 3. Add match func
        Expression.extend(token, match_func)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @classmethod
    def unextend(cls, token):
        """
        Remove extended expression from parser
        """

        if token not in cls.TOKENS_EXTENDED:
            return False

        try:
            cls.TOKENS_EXTENDED.remove(token)
        except ValueError:
            pass

        try:
            cls.TOKENS.remove(token)
        except ValueError:
            pass

        try:
            cls.FTYPE.remove(token)
        except ValueError:
            pass

        try:
            del(cls.TRANSFORM_EXTENDED[token])
        except KeyError:
            pass

        return Expression.unextend(token)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __init__(self, rule):
        """
        @param rule: String rule
        """

        super(FSRule, self).__init__()

        self.raw_rule = rule
        
        self._stack = []
        self._done = False
        self._cur_obj = None
        self._expressions = parser.lr.Tree()
        self._exp_pointer = self._expressions
        self._exp_stack = []

        # Action table
        self._action = parser.lr.ActionTable()

        _s = self._shift
        _r = self._reduce

        self._action.add(0, self.TOKEN_TYPE, (_s, 2))
        self._action.add(0, self.TOKEN_PERM, (_s, 3))
        self._action.add(0, self.TOKEN_OWNER, (_s, 4))
        self._action.add(0, self.TOKEN_NAME, (_s, 5))
        self._action.add(0, self.TOKEN_INAME, (_s, 5))
        self._action.add(0, self.TOKEN_SIZE, (_s, 27))
        self._action.add(0, self.TOKEN_LINK_TYPE, (_s, 27))
        self._action.add(0, self.TOKEN_LINK_PERM, (_s, 27))
        self._action.add(0, self.TOKEN_LINK_OWNER, (_s, 27))
        self._action.add(0, self.TOKEN_LINK_NAME, (_s, 27))
        self._action.add(0, self.TOKEN_LINK_INAME, (_s, 27))
        self._action.add(0, self.TOKEN_LINK_EXISTS, (_s, 27))
        self._action.add(0, self.TOKEN_LINK_SIZE, (_s, 27))
        self._action.add(0, self.TOKEN_NOT, (_s, 1))
        self._action.add(0, self.TOKEN_OPEN_PAR, (_s, 6))

        self._action.add(1, self.TOKEN_TYPE, (_s, 2))
        self._action.add(1, self.TOKEN_PERM, (_s, 3))
        self._action.add(1, self.TOKEN_OWNER, (_s, 4))
        self._action.add(1, self.TOKEN_NAME, (_s, 5))
        self._action.add(1, self.TOKEN_INAME, (_s, 5))
        self._action.add(1, self.TOKEN_SIZE, (_s, 27))
        self._action.add(1, self.TOKEN_LINK_TYPE, (_s, 27))
        self._action.add(1, self.TOKEN_LINK_PERM, (_s, 27))
        self._action.add(1, self.TOKEN_LINK_OWNER, (_s, 27))
        self._action.add(1, self.TOKEN_LINK_NAME, (_s, 27))
        self._action.add(1, self.TOKEN_LINK_INAME, (_s, 27))
        self._action.add(1, self.TOKEN_LINK_EXISTS, (_s, 27))
        self._action.add(1, self.TOKEN_LINK_SIZE, (_s, 27))

        self._action.add(2, self.TOKEN_DEFAULT, (_r, 10))
        self._action.add(3, self.TOKEN_DEFAULT, (_r, 11))
        self._action.add(4, self.TOKEN_DEFAULT, (_r, 12))
        self._action.add(5, self.TOKEN_DEFAULT, (_r, 13))

        self._action.add(6, self.TOKEN_TYPE, (_s, 2))
        self._action.add(6, self.TOKEN_PERM, (_s, 3))
        self._action.add(6, self.TOKEN_OWNER, (_s, 4))
        self._action.add(6, self.TOKEN_NAME, (_s, 5))
        self._action.add(6, self.TOKEN_INAME, (_s, 5))
        self._action.add(6, self.TOKEN_SIZE, (_s, 27))
        self._action.add(6, self.TOKEN_LINK_TYPE, (_s, 27))
        self._action.add(6, self.TOKEN_LINK_PERM, (_s, 27))
        self._action.add(6, self.TOKEN_LINK_OWNER, (_s, 27))
        self._action.add(6, self.TOKEN_LINK_NAME, (_s, 27))
        self._action.add(6, self.TOKEN_LINK_INAME, (_s, 27))
        self._action.add(6, self.TOKEN_LINK_EXISTS, (_s, 27))
        self._action.add(6, self.TOKEN_LINK_SIZE, (_s, 27))
        self._action.add(6, self.TOKEN_NOT, (_s, 1))
        self._action.add(6, self.TOKEN_OPEN_PAR, (_s, 6))

        self._action.add(7, self.EOF, (_s, 14))
        self._action.add(8, self.TOKEN_DEFAULT, (_r, 1))

        self._action.add(9, self.TOKEN_AND, (_s, 15))
        self._action.add(9, self.TOKEN_OR, (_s, 16))
        self._action.add(9, self.TOKEN_DEFAULT, (_r, 2))

        self._action.add(10, self.TOKEN_DEFAULT, (_r, 4))
        self._action.add(11, self.TOKEN_OPEN_BR, (_s, 18))
        self._action.add(12, self.TOKEN_DEFAULT, (_r, 5))
        self._action.add(13, self.TOKEN_CLOSE_PAR, (_s, 19))
        self._action.add(14, self.TOKEN_DEFAULT, (self._accept, None))
        self._action.add(15, self.TOKEN_DEFAULT, (_r, 8))
        self._action.add(16, self.TOKEN_DEFAULT, (_r, 9))

        self._action.add(17, self.TOKEN_TYPE, (_s, 2))
        self._action.add(17, self.TOKEN_PERM, (_s, 3))
        self._action.add(17, self.TOKEN_OWNER, (_s, 4))
        self._action.add(17, self.TOKEN_NAME, (_s, 5))
        self._action.add(17, self.TOKEN_INAME, (_s, 5))
        self._action.add(17, self.TOKEN_SIZE, (_s, 27))
        self._action.add(17, self.TOKEN_LINK_TYPE, (_s, 27))
        self._action.add(17, self.TOKEN_LINK_PERM, (_s, 27))
        self._action.add(17, self.TOKEN_LINK_OWNER, (_s, 27))
        self._action.add(17, self.TOKEN_LINK_NAME, (_s, 27))
        self._action.add(17, self.TOKEN_LINK_INAME, (_s, 27))
        self._action.add(17, self.TOKEN_LINK_EXISTS, (_s, 27))
        self._action.add(17, self.TOKEN_LINK_SIZE, (_s, 27))
        self._action.add(17, self.TOKEN_NOT, (_s, 1))
        self._action.add(17, self.TOKEN_OPEN_PAR, (_s, 6))

        self._action.add(18, self.TOKEN_ARG, (_s, 21))
        self._action.add(19, self.TOKEN_DEFAULT, (_r, 6))
        self._action.add(20, self.TOKEN_DEFAULT, (_r, 3))
        self._action.add(21, self.TOKEN_CLOSE_BR, (_s, 22))
        self._action.add(22, self.TOKEN_DEFAULT, (_r, 7))
        self._action.add(23, self.TOKEN_OPEN_BR, (_s, 24))
        self._action.add(24, self.TOKEN_ARG, (_s, 25))
        self._action.add(25, self.TOKEN_CLOSE_BR, (_s, 26))
        self._action.add(26, self.TOKEN_DEFAULT, (_r, 14))
        self._action.add(27, self.TOKEN_DEFAULT, (_r, 131))

        # For extended functionality
        for _ext_token in self.TOKENS_EXTENDED:
            for _state in (0, 1, 6, 17):
                self._action.add(_state, _ext_token, (_s, 27))

        self._rules = parser.lr.Rules()

        self._rules.add(1, self.NTOKEN_START, 1)
        self._rules.add(2, self.NTOKEN_RULE, 1)
        self._rules.add(3, self.NTOKEN_RULE, 3)
        self._rules.add(4, self.NTOKEN_EXPR, 1)
        self._rules.add(5, self.NTOKEN_EXPR, 2)
        self._rules.add(6, self.NTOKEN_EXPR, 3)
        self._rules.add(7, self.NTOKEN_EXPR_BODY, 4)
        self._rules.add(8, self.NTOKEN_OP, 1)
        self._rules.add(9, self.NTOKEN_OP, 1)
        self._rules.add(10, self.NTOKEN_FTYPE, 1)
        self._rules.add(11, self.NTOKEN_FTYPE, 1)
        self._rules.add(12, self.NTOKEN_FTYPE, 1)
        self._rules.add(13, self.NTOKEN_FTYPE, 1)
        self._rules.add(14, self.NTOKEN_EXPR_BODY, 5)
        self._rules.add(131, self.NTOKEN_FTYPE, 1)

        # Goto table
        self._goto = parser.lr.GotoTable()

        self._goto.add(0, self.NTOKEN_START, 7)
        self._goto.add(0, self.NTOKEN_RULE, 8)
        self._goto.add(0, self.NTOKEN_EXPR, 9)
        self._goto.add(0, self.NTOKEN_EXPR_BODY, 10)
        self._goto.add(0, self.NTOKEN_FTYPE, 11)

        self._goto.add(1, self.NTOKEN_EXPR_BODY, 10)
        self._goto.add(1, self.NTOKEN_FTYPE, 23)

        self._goto.add(6, self.NTOKEN_RULE, 13)
        self._goto.add(6, self.NTOKEN_EXPR, 9)
        self._goto.add(6, self.NTOKEN_EXPR_BODY, 10)
        self._goto.add(6, self.NTOKEN_FTYPE, 11)

        self._goto.add(9, self.NTOKEN_OP, 17)

        self._goto.add(17, self.NTOKEN_RULE, 20)
        self._goto.add(17, self.NTOKEN_EXPR, 9)
        self._goto.add(17, self.NTOKEN_EXPR_BODY, 10)
        self._goto.add(17, self.NTOKEN_FTYPE, 11)

        self._unget = []
        self._chain = self._parse(rule)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def match(self, obj):
        """
        Match given object against rule

        @param obj: VFSObject instance
        @return: True if matches and False otherwise
        """

        if not isinstance(obj, VFSObject):
            raise XYZValueError(_(u"Invalid argument type: %s, "\
                                  u"VFSObject expected") % type(obj))

        return self._match(obj, self._expressions)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _match(self, obj, _expressions):
        _op = None
        _res = None

        for exp in _expressions:
            if exp in ("AND", "OR"):
                _op = exp
                continue

            if isinstance(exp, parser.lr.Tree):
                # Recursive match subrule
                _r = self._match(obj, exp)
            else:
                _r = exp.match(obj)

            if _res is not None:
                if _op == "AND":
                    _res = _res and _r

                    # Short-circuit: do not continue if got false on AND
                    # expression
                    if not _res:
                        break
                elif _op == "OR":
                    _res = _res or _r

                    # Short-circuit: do not continue if got true on OR
                    # expression
                    if _res:
                        break
            else:
                _res = _r

            _op = None

        if _res is None:
            return _r
        else:
            return _res

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _parse(self, rule):
        """
        Parse rule
        """

        # Initial state
        self._stack.append(0)

        _tokens = (self.TOKEN_OPEN_PAR,
                   self.TOKEN_CLOSE_PAR,
                   self.TOKEN_OPEN_BR,
                   self.TOKEN_CLOSE_BR,
                   u"=", u",")

        self._lexer = parser.Lexer(rule, _tokens, u"#")
        self._lexer.escaping_on()

        try:
            while True:
                if self._done:
                    break

                if self._unget:
                    _tok = self._unget.pop()
                else:
                    _res = self._lexer.lexer()

                    if _res is not None:
                        _tok = _res[1]
                    else:
                        _tok = _res

                if _tok not in self.TOKENS:
                    _tok_type = self.TOKEN_ARG
                else:
                    _tok_type = _tok

                try:
                    _f, _arg = self._action.get(self._stack[-1], _tok_type)
                except KeyError:
                    try:
                        _f, _arg = self._action.get(self._stack[-1],
                                                    self.TOKEN_DEFAULT)
                    except KeyError:
                        self.error(_tok)

                _f(_tok, _arg)

        except LexerError, e:
            self.error(e)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _shift(self, token, state):
        """
        Shift token and state onto stack
        """

        self._stack.append(token)
        self._stack.append(state)

        if state == 6: # (
            _new = parser.lr.Tree()
            self._exp_pointer.add(_new)
            self._exp_stack.append(self._exp_pointer)
            self._exp_pointer = _new
        elif state == 19: # )
            if self._exp_stack:
                self._exp_pointer = self._exp_stack.pop()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _reduce(self, token, rule):
        """
        Reduce stack by rule
        """
        _transform = {
            u"type": self._type,
            u"name": self._name,
            u"iname": self._iname,
            u"owner": self._owner,
            u"perm": self._perm,
            u"size": self._size,
            u"link_type": self._type,
            u"link_name": self._name,
            u"link_iname": self._iname,
            u"link_owner": self._owner,
            u"link_perm": self._perm,
            u"link_size": self._size,
            }

        try:
            _ntok, _len = self._rules.get(rule)
        except KeyError:
            self.error(token)

        if rule in (10, 11, 12, 13, 131):
            self._cur_obj = Expression()
            self._cur_obj.otype = self._stack[-2]
        elif rule in (7, 14):
            _arg = self._stack[-4]
            _cur = self._cur_obj

            if _cur.otype in _transform:
                _cur.arg = _transform[_cur.otype](_arg)
            elif _cur.otype in self.TRANSFORM_EXTENDED:
                try:
                    _cur.arg = self.TRANSFORM_EXTENDED[_cur.otype](_arg)
                except Exception, e:
                    self.error(_(u"Error in calling extended transformation "\
                                 u"function: %s") % unicode(e))
            else:
                _cur.arg = _arg

            if rule == 14:
                self._cur_obj.negative = True
        elif rule in (4, 5):
            self._exp_pointer.add(self._cur_obj)
            self._cur_obj = None
        elif rule == 8:
            self._exp_pointer.add("AND")
        elif rule == 9:
            self._exp_pointer.add("OR")

        self._stack = self._stack[:(_len * -2)]
        _top = self._stack[-1]
        self._stack.append(_ntok)

        try:
            self._stack.append(self._goto.get(_top, _ntok))
        except KeyError:
            self.error(token)

        self._unget.append(token)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _accept(self, *args):
        """
        Complete parsing
        """

        self._done = True

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _type(self, arg):
        _types ={
            u"file": VFSTypeFile,
            u"file_or_link2":
            lambda x: x.is_file() or (x.is_link() and x.data.is_file()),
            u"dir": VFSTypeDir,
            u"dir_or_link2":
            lambda x: x.is_dir() or (x.is_link() and x.data.is_dir()),
            u"link": VFSTypeLink,
            u"socket": VFSTypeSocket,
            u"socket_or_link2":
            lambda x: x.is_socket() or (x.is_link() and x.data.is_socket()),
            u"fifo": VFSTypeFifo,
            u"fifo_or_link2":
            lambda x: x.is_fifo() or (x.is_link() and x.data.is_fifo()),
            u"char": VFSTypeChar,
            u"char_or_link2":
            lambda x: x.is_char() or (x.is_link() and x.data.is_char()),
            u"block": VFSTypeBlock,
            u"block_or_link2":
            lambda x: x.is_block() or (x.is_link() and x.data.is_block()),
            }

        try:
            return _types[arg]
        except KeyError:
            self.error(_(u"Invalid type{} argument: %s") % arg)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _name(self, arg):
        return re.compile(arg, re.U)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def _iname(self, arg):
        return re.compile(arg, re.U | re.I)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _owner(self, arg):
        if not re.match(r"^(\w+)?(:(\w+))?$", arg):
            self.error(_(u"Invalid owner{} argument: %s") % arg)

        _tmp = arg.split(":")
        _uid = _tmp[0]

        if _uid == "":
            _uid = None
        elif not _uid.isdigit():
            try:
                _uid = pwd.getpwnam(_uid).pw_uid
            except (KeyError, TypeError):
                self.error(_(u"Invalid uid: %s") % _uid)
        else:
            _uid = int(_uid)

        if len(_tmp) > 1:
            _gid = _tmp[1]

            if not _gid.isdigit():
                try:
                    _gid = grp.getgrnam(_gid).gr_gid
                except (KeyError, TypeError):
                    self.error(_(u"Invalid gid: %s") % _gid)
            else:
                _gid = int(_gid)
        else:
            _gid = None

        return (_uid, _gid)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _perm(self, arg):
        _any = False

        if not re.match(r"^\+?\d{4}$", arg):
            self.error(_(u"Invalid perm{} argument: %s") % arg)

        if arg.startswith(u"+"):
            _any = True
            _perm = int(arg[1:], 8)
        else:
            _perm = int(arg, 8)

        return (_any, _perm)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _size(self, arg):
        _bytes = {
                  u"B": 1,
                  u"K": 1024,
                  u"M": 1024 * 1024,
                  u"G": 1024 * 1024 * 1024,
                  u"T": 1024 * 1024 * 1024 * 1024,
                 }

        _re = re.match(r"^\s*([<>]?\=?)\s*(\d+)\s*([BbKkMmGgTt]?)\s*$", arg)

        if _re is None:
            self.error(_(u"Invalid size{} argument: %s") % arg)
        else:
            _op = _re.group(1) or u"="
            _size = long(_re.group(2))
            _mod = _re.group(3) or None

        if _mod is not None:
            _size *= _bytes[_mod.upper()]

        return (_op, _size)

#++++++++++++++++++++++++++++++++++++++++++++++++

def link(func):
    """
    Wrap matching func to aplly only for links
    """

    def _trans(vfsobj, arg):
        if isinstance(vfsobj.ftype, VFSTypeLink) and vfsobj.data is not None:
            return func(vfsobj.data, arg)
        else:
            return False

    return _trans

#++++++++++++++++++++++++++++++++++++++++++++++++

class Expression(object):
    """
    FS rule expression class
    """

    MATCH_EXTENDED = {}

    @classmethod
    def extend(cls, token, match_func):
        cls.MATCH_EXTENDED[token] = match_func

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @classmethod
    def unextend(cls, token):
        try:
            del(cls.MATCH_EXTENDED[token])
        except KeyError:
            pass

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __init__(self):
        self.otype = None
        self.arg = None
        self.negative = False

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def match(self, vfsobj):
        """
        Check if object matches the rule
        """

        def _match_type(obj, arg):
            if is_func(arg):
                return arg(obj)
            else:
                return isinstance(obj.ftype, arg)

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        def _match_name(obj, arg):
            if arg.search(ustring(obj.name)) is None:
                return False
            else:
                return True

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        
        def _match_iname(obj, arg):
            if arg.search(ustring(obj.name)) is None:
                return False
            else:
                return True

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        def _match_owner(obj, arg):
            if arg[0] is not None and arg[1] is not None:
                if (obj.uid, obj.gid) == arg:
                    return True
            elif arg[0] is not None and obj.uid == arg[0]:
                return True
            elif arg[1] is not None and obj.gid == arg[1]:
                return True

            return False

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        def _match_perm(obj, arg):
            if obj.mode is None:
                return False

            _any, _m = arg
            _mode = stat.S_IMODE(obj.mode.raw)

            if not _any and _mode == _m:
                return True
            elif _mode & _m:
                return True

            return False

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        def _match_size(obj, args):
            if obj.size is None:
                return False

            _op, _size = args

            _data = {u">": lambda x, y: x > y,
                     u">=": lambda x, y: x >= y,
                     u"<": lambda x, y: x < y,
                     u"<=": lambda x, y: x <= y,
                     u"=": lambda x, y: x == y,
                    }

            if _op in _data and _data[_op](obj.size, _size):
                return True

            return False

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        def _match_link_exists(obj, arg):
            if isinstance(obj.ftype, VFSTypeLink) and obj.data is not None:
                return True
            else:
                return False

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        _match_link_type = link(_match_type)
        _match_link_name = link(_match_name)
        _match_link_iname = link(_match_iname)
        _match_link_owner = link(_match_owner)
        _match_link_perm = link(_match_perm)
        _match_link_size = link(_match_size)

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        _match_f = {
            u"type": _match_type,
            u"name": _match_name,
            u"iname": _match_iname,
            u"owner": _match_owner,
            u"perm": _match_perm,
            u"size": _match_size,
            u"link_type": _match_link_type,
            u"link_name": _match_link_name,
            u"link_iname": _match_link_iname,
            u"link_owner": _match_link_owner,
            u"link_perm": _match_link_perm,
            u"link_exists": _match_link_exists,
            u"link_size": _match_link_size,
            }

        if self.otype in _match_f:
            _res = _match_f[self.otype](vfsobj, self.arg)
        elif self.otype in self.MATCH_EXTENDED:
            try:
                _res = self.MATCH_EXTENDED[self.otype](vfsobj, self.arg)
            except Exception, e:
                self.error(_(u"Error in calling extended match "\
                             u"function: %s") % unicode(e))
        else:
            raise FSRuleError(_(u"Unable to find match function for token: %s")
                              % self.otype)

        if self.negative:
            return not _res
        else:
            return _res

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __str__(self):
        return "<FSRule expression: %s, %s, %s>" % \
                (self.otype, str(self.arg), str(self.negative))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __repr__(self):
        return self.__str__()
