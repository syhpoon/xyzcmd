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

from libxyz.exceptions import ParseError

class BaseParser(object):
    """
    Common parser interface
    """

    error_unexpected = 1

    def parse(self, *args, **kwargs):
        raise NotImplementedError(_(u"Must be implemented in child class"))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def error(self, msg=None, etype=None):
        """
        Parsing error. Raise exception
        """

        _emsg = ""
        if self._lexer:
            _lineno = self._lexer.sdata.lineno
            _pre = _(u"Parse error on line %d" % _lineno)
        else:
            _pre = _(u"Parse error")

        if etype == self.error_unexpected and msg and len(msg) == 2:
            _emsg = _(u"Unexpected token '%s'. Waiting for '%s'" % \
                    (msg[0].encode("unicode-escape"),
                     msg[1].encode("unicode-escape")))
        elif msg:
            _emsg = msg
        else:
            _emsg = _(u"Syntax error")

        raise ParseError("%s: %s" % (_pre, _emsg))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def set_opt(self, default, opt):
        for _opt in default.keys():
            setattr(self, _opt, opt.get(_opt, default[_opt]))
