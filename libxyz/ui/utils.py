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

from libxyz.ui import lowui
from libxyz.core.utils import ustring

def refresh(func):
    """
    Invalidate canvas after calling function
    """

    def _touch(instance, *args, **kwargs):
        _res = func(instance, *args, **kwargs)
        instance._invalidate()

        return _res

    return _touch

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def truncate(text, cols, enc, backward=False):
    """
    Truncate text if its length exceeds cols
    If backward is True, text will be truncated from the beginning
    """

    text = ustring(text, enc)

    _len = lowui.util.calc_width(text, 0, len(text))

    if _len < cols:
        return text
    else:
        if backward:
            return u"~%s" % text[-(cols - 1):]
        else:
            return u"%s~" % text[:cols - 1]
