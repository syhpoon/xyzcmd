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

from libxyz.ui import lowui
from libxyz.core.utils import ustring

class Prompt(lowui.Text):
    """
    Command line prompt
    """

    def __init__(self, text, attr=None):
        """
        @param text: Prompt text
        """

        if attr is not None:
            _arg = (attr, text)
        else:
            _arg = text

        super(Prompt, self).__init__(_arg)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __len__(self):
        """
        Return prompt text length
        """

        return len(ustring(self.get_text()[0]))
