#-*- coding: utf8 -*
#
# Max E. Kuznecov ~syhpoon <mek@mek.uz.ua> 2008
#

from libxyz.exceptions import ParseError

class BaseParser(object):
    """
    Common parser interface
    """

    error_unexpected = 1

    def parse(self, *args, **kwargs):
        raise NotImplementedError(_("Must be implemented in child class"))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def error(self, msg=None, etype=None):
        """
        Parsing error. Raise exception
        """

        _emsg = ""
        if self._lexer:
            _lineno = self._lexer.sdata.lineno
            _pre = _("Parse error on line %d" % _lineno)
        else:
            _pre = _("Parse error")

        if etype == self.error_unexpected and msg and len(msg) == 2:
            _emsg = _("Unexpected token '%s'. Waiting for '%s'" % \
                    (msg[0].encode("string-escape"),
                     msg[1].encode("string-escape")))
        elif msg:
            _emsg = msg
        else:
            _emsg = _("Syntax error")

        raise ParseError("%s: %s" % (_pre, _emsg))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def set_opt(self, default, opt):
        for _opt in default.keys():
            setattr(self, _opt, opt.get(_opt, default[_opt]))
