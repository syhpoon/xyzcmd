#-*- coding: utf8 -*
#
# Max E. Kuznecov ~syhpoon <syhpoon@syhpoon.name> 2008
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

import os
import re
import string
import stat
import pwd
import grp

import libxyz.parser as parser

from libxyz.exceptions import ParseError
from libxyz.exceptions import SkinError
from libxyz.exceptions import XYZValueError
from libxyz.exceptions import LexerError
from libxyz.parser import Lexer
from libxyz.vfs.types import *
from libxyz.vfs.vfsobj import  VFSFile

import libxyz.ui as uilib

class Skin(object):
    """
    Skin object. Provides simple interface to defined skin rulesets.
    """

    def __init__(self, path):
        """
        @param path: Path to skin file
        """

        if not os.access(path, os.R_OK):
            raise SkinError(_(u"Unable to open skin file for reading"))
        else:
            self.path = path

        self._data = {}

        self.screen = None

        # Default fallback palette
        self._default = uilib.colors.Palette(u"default",
                        uilib.colors.Foreground(u"DEFAULT"),
                        uilib.colors.Background(u"DEFAULT"),
                        uilib.colors.Monochrome(u"DEFAULT"))

        # 1. Parse
        self._data = self._parse()

        # 2. Order parsed data
        self._check()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __str__(self):
        return u"<Skin object: %s>" % str(self.path)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __repr__(self):
        return self.__str__()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __getitem__(self, key):
        return self._data[key]

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def set_screen(self, screen):
        self.screen = screen

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _parse(self):
        def palette_validator(block, var, val):
            """
            Make L{libxyz.ui.colors.Palette} object of palette definition
            """

            _p = self._default.copy()

            if isinstance(val, basestring):
                _val = (val,)
            else:
                _val = [x.strip() for x in val]

            _p.fg = uilib.colors.Foreground(_val[0])

            if len(_val) > 1:
                _p.bg = uilib.colors.Background(_val[1])
            if len(_val) > 2:
                _p.ma = tuple([uilib.colors.Monochrome(x) for x in _val[2:]])

            _p.name = self._make_name(block, var)

            return _p

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        def trans_cr(rule):
            """
            Transform string rules to CombinedRule objects
            """

            try:
                return CombinedRule(rule)
            except ParseError, e:
                raise XYZValueError(e)

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        # Prepare parsers

        _fs_rules_opt = {u"count": 1,
                            u"value_validator": palette_validator,
                            u"varre": re.compile(r".+"),
                            u"var_transform": trans_cr,
                           }

        _fs_rules_p = parser.BlockParser(_fs_rules_opt)

        _ui_opt = {u"count": 1,
                   u"value_validator": palette_validator,
                   }
        _ui_p = parser.BlockParser(_ui_opt)

        _flat_opt = {u"count": 1}
        _flat_p = parser.FlatParser(_flat_opt)

        _parsers = {
                    u"fs.rules": _fs_rules_p,
                    re.compile(r"ui\.(\w)+"): _ui_p,
                    (u"AUTHOR", u"VERSION", u"DESCRIPTION"): _flat_p,
                    }

        _multi_opt = {u"tokens": (":",)}
        _multi_p = parser.MultiParser(_parsers, _multi_opt)

        _skinfile = open(self.path, "r")

        try:
            _data = _multi_p.parse(_skinfile)
        except ParseError, e:
            raise SkinError(_(u"Error parsing skin file: %s" % str(e)))
        finally:
            _skinfile.close()

        return _data

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _make_name(self, block, resource):
        return "%(resource)s@%(block)s" % locals()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _check(self):
        """
        Check and variables
        """

        for _required in (u"AUTHOR", u"DESCRIPTION", u"VERSION"):
            if _required not in self._data:
                raise SkinError(_(u"Missing required variable: %s"%_required))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def get_palette_list(self):
        """
        Return list of defined palettes.
        It is usually passed to register_palette() function
        """

        _list = [self._default.get_palette()]

        for _name, _pdata in self._data.iteritems():
            if not isinstance(_pdata, parser.ParsedData):
                continue

            for _var, _val in _pdata.iteritems():
                if isinstance(_val, uilib.colors.Palette):
                    _list.append(_val.get_palette())

        return _list

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def attr(self, resolution, name, default=True):
        """
        Search for first matching attribute <name> according to resolution
        @param resolution: Sequence of ruleset names
        @param name: Attribute name
        @param default: If True, return default palette in case attr
                        is not found, otherwise return None
        @return: Registered palette name
        """

        return self.palette(resolution, name, default).name

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def palette(self, resolution, name, default=True):
        """
        Search for first matching palette <name> according to resolution
        """

        for _w in resolution:
            # Normalize name
            if not _w.startswith(u"ui."):
                _w = u"ui.%s" % _w

            try:
                return self._data[_w][name]
            except KeyError:
                pass

        if default:
            return self._default
        else:
            return None

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def get_palette(self, block, name):
        try:
            return self._data[block][name].name
        except KeyError:
            return None

#++++++++++++++++++++++++++++++++++++++++++++++++

#TODO: Tests for CombinedRule

class CombinedRule(parser.BaseParser):
    """
    Combined rule parser

    Rule syntax is following:

    rule            ::= expr $
                        | expr op rule
    expr            ::= expr_body
                        | NOT expr_body
                        | "(" rule ")"
    expr_body       ::= ftype "{" ARG "}"
    op              ::= AND | OR
    ftype           ::= TYPE | PERM | OWNER | REGEXP

    Examples:

    type{file} and perm{+0111}
    (owner{user} and not owner{:group}) or owner{root}
    """

    # Tokens
    TOKEN_TYPE = "type"
    TOKEN_PERM = "perm"
    TOKEN_OWNER = "owner"
    TOKEN_REGEXP = "regexp"
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

    TOKENS = (TOKEN_TYPE, TOKEN_PERM, TOKEN_OWNER, TOKEN_REGEXP,
              TOKEN_AND, TOKEN_OR, TOKEN_NOT, TOKEN_OPEN_BR, TOKEN_CLOSE_BR,
              TOKEN_OPEN_PAR, TOKEN_CLOSE_PAR, TOKEN_DEFAULT, EOF)

    # Nonterminals
    NTOKEN_START = 100
    NTOKEN_RULE = 101
    NTOKEN_EXPR = 102
    NTOKEN_EXPR_BODY = 103
    NTOKEN_OP = 104
    NTOKEN_FTYPE = 105

    FTYPE = (TOKEN_TYPE,
             TOKEN_PERM,
             TOKEN_OWNER,
             TOKEN_REGEXP,
            )

    INFIX_OP = (TOKEN_AND, TOKEN_OR)

    def __init__(self, rule):
        """
        @param rule: String rule
        """

        super(CombinedRule, self).__init__()

        self._stack = []
        self._done = False
        self._cur_obj = None
        self._expressions = parser.lr.Tree()
        self._exp_pointer = self._expressions
        self._exp_stack = []

        # Action table
        self._action = parser.lr.ActionTable()

        # Here go grammar and closures
        # Grammar

        # 0 $accept: start $end
        # 1 start: rule
        # 2 rule: expr
        # 3     | expr op rule
        # 4 expr: expr_body
        # 5     | NOT expr_body
        # 6     | "(" rule ")"
        # 7 expr_body: ftype "{" ARG "}"
        # 8 op: AND
        # 9   | OR
        # 10 ftype: TYPE
        # 11      | PERM
        # 12      | OWNER
        # 13      | REGEXP
        # 14 expr_body: NOT ftype "{" ARG "}"

        # Closures

        # state 0
        #    0 $accept: . start $end
        #    NOT     shift, and go to state 1
        #    TYPE    shift, and go to state 2
        #    PERM    shift, and go to state 3
        #    OWNER   shift, and go to state 4
        #    REGEXP  shift, and go to state 5
        #    "("     shift, and go to state 6
        #    start      go to state 7
        #    rule       go to state 8
        #    expr       go to state 9
        #    expr_body  go to state 10
        #    ftype      go to state 11

        # state 1
        #    5 expr: NOT . expr_body
        #    TYPE    shift, and go to state 2
        #    PERM    shift, and go to state 3
        #    OWNER   shift, and go to state 4
        #    REGEXP  shift, and go to state 5
        #    expr_body  go to state 12
        #    ftype      go to state 23

        # state 2
        #    10 ftype: TYPE .
        #    $default  reduce using rule 10 (ftype)

        # state 3
        #    11 ftype: PERM .
        #    $default  reduce using rule 11 (ftype)

        # state 4
        #    12 ftype: OWNER .
        #    $default  reduce using rule 12 (ftype)

        # state 5
        #    13 ftype: REGEXP .
        #    $default  reduce using rule 13 (ftype)

        # state 6
        #    6 expr: "(" . rule ")"
        #    NOT     shift, and go to state 1
        #    TYPE    shift, and go to state 2
        #    PERM    shift, and go to state 3
        #    OWNER   shift, and go to state 4
        #    REGEXP  shift, and go to state 5
        #    "("     shift, and go to state 6
        #    rule       go to state 13
        #    expr       go to state 9
        #    expr_body  go to state 10
        #    ftype      go to state 11

        # state 7
        #    0 $accept: start . $end
        #    $end  shift, and go to state 14

        # state 8
        #    1 start: rule .
        #    $default  reduce using rule 1 (start)

        # state 9
        #    2 rule: expr .
        #    3     | expr . op rule
        #    AND  shift, and go to state 15
        #    OR   shift, and go to state 16
        #    $default  reduce using rule 2 (rule)
        #    op  go to state 17

        # state 10
        #    4 expr: expr_body .
        #    $default  reduce using rule 4 (expr)

        # state 11
        #    7 expr_body: ftype . "{" ARG "}"
        #    "{"  shift, and go to state 18

        # state 12
        #    5 expr: NOT expr_body .
        #    $default  reduce using rule 5 (expr)

        # state 13
        #    6 expr: "(" rule . ")"
        #    ")"  shift, and go to state 19

        # state 14
        #    0 $accept: start $end .
        #    $default  accept

        # state 15
        #    8 op: AND .
        #    $default  reduce using rule 8 (op)

        # state 16
        #    9 op: OR .
        #    $default  reduce using rule 9 (op)

        #state 17
        #    3 rule: expr op . rule
        #    NOT     shift, and go to state 1
        #    TYPE    shift, and go to state 2
        #    PERM    shift, and go to state 3
        #    OWNER   shift, and go to state 4
        #    REGEXP  shift, and go to state 5
        #    "("     shift, and go to state 6
        #    rule       go to state 20
        #    expr       go to state 9
        #    expr_body  go to state 10
        #    ftype      go to state 11

        # state 18
        #    7 expr_body: ftype "{" . ARG "}"
        #    ARG  shift, and go to state 21

        # state 19
        #    6 expr: "(" rule ")" .
        #    $default  reduce using rule 6 (expr)

        # state 20
        #    3 rule: expr op rule .
        #    $default  reduce using rule 3 (rule)

        # state 21
        #    7 expr_body: ftype "{" ARG . "}"
        #    "}"  shift, and go to state 22

        # state 22
        #    7 expr_body: ftype "{" ARG "}" .
        #    $default  reduce using rule 7 (expr_body)

        # state 23
        #    7 expr_body: NOT ftype . "{" ARG "}"
        #    "{"  shift, and go to state 24

        # state 24
        #    7 expr_body: NOT ftype "{" . ARG "}"
        #    ARG  shift, and go to state 25

        # state 25
        #    7 expr_body: NOT ftype "{" ARG . "}"
        #    "}"  shift, and go to state 26

        # !state 26
        #    7 expr_body: NOT ftype "{" ARG "}" .
        #    $default  reduce using rule 14 (expr_body)

        _s = self._shift
        _r = self._reduce

        self._action.add(0, self.TOKEN_TYPE, (_s, 2))
        self._action.add(0, self.TOKEN_PERM, (_s, 3))
        self._action.add(0, self.TOKEN_OWNER, (_s, 4))
        self._action.add(0, self.TOKEN_REGEXP, (_s, 5))
        self._action.add(0, self.TOKEN_NOT, (_s, 1))
        self._action.add(0, self.TOKEN_OPEN_PAR, (_s, 6))

        self._action.add(1, self.TOKEN_TYPE, (_s, 2))
        self._action.add(1, self.TOKEN_PERM, (_s, 3))
        self._action.add(1, self.TOKEN_OWNER, (_s, 4))
        self._action.add(1, self.TOKEN_REGEXP, (_s, 5))

        self._action.add(2, self.TOKEN_DEFAULT, (_r, 10))
        self._action.add(3, self.TOKEN_DEFAULT, (_r, 11))
        self._action.add(4, self.TOKEN_DEFAULT, (_r, 12))
        self._action.add(5, self.TOKEN_DEFAULT, (_r, 13))

        self._action.add(6, self.TOKEN_TYPE, (_s, 2))
        self._action.add(6, self.TOKEN_PERM, (_s, 3))
        self._action.add(6, self.TOKEN_OWNER, (_s, 4))
        self._action.add(6, self.TOKEN_REGEXP, (_s, 5))
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
        self._action.add(17, self.TOKEN_REGEXP, (_s, 5))
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

        @param obj: VFSFile instance
        @return: True if matches and False otherwise
        """

        if not isinstance(obj, VFSFile):
            raise XYZValueError(_(u"Invalid argument type: %s, "\
                                  u"VFSFile expected") % type(obj))

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
                      u"regexp": self._regexp,
                      u"owner": self._owner,
                      u"perm": self._perm,
                     }

        try:
            _ntok, _len = self._rules.get(rule)
        except KeyError:
            self.error(token)

        if rule in (10, 11, 12, 13):
            self._cur_obj = Expression()
            self._cur_obj.otype = self._stack[-2]
        elif rule in (7, 14):
            _arg = self._stack[-4]

            if self._cur_obj.otype in _transform:
                self._cur_obj.arg = _transform[self._cur_obj.otype](_arg)
            else:
                self._cur_obj.arg = _arg

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
                 u"dir": VFSTypeDir,
                 u"link": VFSTypeLink,
                 u"socket": VFSTypeSocket,
                 u"fifo": VFSTypeFifo,
                 u"char": VFSTypeChar,
                 u"block": VFSTypeBlock,
                }

        try:
            return _types[arg]
        except KeyError:
            self.error(_(u"Invalid type{} argument: %s" % arg))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _regexp(self, arg):
        return re.compile(arg, re.U)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _owner(self, arg):
        if not re.match(r"^(\w+)?(:(\w+))?$", arg):
            self.error(_(u"Invalid owner{} argument: %s" % arg))

        _tmp = arg.split(":")
        _uid = _tmp[0]

        if _uid == "":
            _uid = None
        elif not _uid.isdigit():
            try:
                _uid = pwd.getpwnam(_uid).pw_uid
            except (KeyError, TypeError):
                self.error(_(u"Invalid uid: %s" % _uid))
        else:
            _uid = int(_uid)

        if len(_tmp) > 1:
            _gid = _tmp[1]

            if not _gid.isdigit():
                try:
                    _gid = grp.getgrnam(_gid).gr_gid
                except (KeyError, TypeError):
                    self.error(_(u"Invalid gid: %s" % _gid))
            else:
                _gid = int(_gid)
        else:
            _gid = None

        return (_uid, _gid)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _perm(self, arg):
        _any = False

        if not re.match(r"^\+?\d{4}$", arg):
            self.error(_(u"Invalid perm{} argument: %s" % arg))

        if arg.startswith(u"+"):
            _any = True
            _perm = int(arg[1:], 8)
        else:
            _perm = int(arg, 8)

        return (_any, _perm)

#++++++++++++++++++++++++++++++++++++++++++++++++

class Expression(object):
    """
    Combined rule expression class
    """

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
            return type(obj.ftype) == arg

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        def _match_regexp(obj, arg):
            if arg.search(obj.name) is None:
                return False
            else:
                return True

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        def _match_owner(obj, arg):
            if arg[0] is not None and arg[1] is not None:
                if (obj.uid, obj.gid) == arg:
                    return True
            elif arg[0] is not None:
                if obj.uid == arg[0]:
                    return True
            elif arg[1] is not None:
                if obj.gid == arg[1]:
                    return True

            return False

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        def _match_perm(obj, arg):
            _any, _m = arg
            _mode = stat.S_IMODE(obj.mode.raw)

            if not _any and _mode == _m:
                return True
            elif _mode & _m:
                return True

            return False

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        _match_f = {
                    u"type": _match_type,
                    u"regexp": _match_regexp,
                    u"owner": _match_owner,
                    u"perm": _match_perm,
                   }

        _res = _match_f[self.otype](vfsobj, self.arg)

        if self.negative:
            return not _res
        else:
            return _res

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __str__(self):
        return "<CombinedRule expression: %s, %s, %s>" % \
                (self.otype, str(self.arg), str(self.negative))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __repr__(self):
        return self.__str__()
