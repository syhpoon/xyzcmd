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

from libxyz.core import FSRule
from libxyz.core.utils import ustring
from libxyz.exceptions import XYZRuntimeError

class ActionManager(object):
    """
    Action rules handler
    """

    def __init__(self, xyz):
        self.xyz = xyz
        self._actions = []

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def register(self, rule, fn):
        """
        Register function to be run upon matching rule
        @param rule: String FS rule
        @param fn: Action function. Function receives matched VFS object as
                   its only argument.
        """

        try:
            _rule = FSRule(rule)
        except Exception, e:
            raise XYZRuntimeError(
                _(u"Unable to register action: invalid rule: %s") % 
                unicode(e))
        
        self._actions.insert(0, (_rule, fn))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def match(self, vfsobj):
        """
        Loop through registered actions and return action assosiated
        with the first matched rule. If no rule matched return None
        """

        for r, f in self._actions:
            if r.match(vfsobj):
                return f

        return None
