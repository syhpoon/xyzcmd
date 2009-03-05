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

class XYZData(object):
    """
    XYZ system data container
    """

    __slots__ = ["screen",
                 "top",
                 "skin",
                 "pm",
                 "km",
                 "hm",
                 "conf",
                 "input",
                 "term",
                ]

    def __init__(self):
        object.__setattr__(self, "screen", None)
        object.__setattr__(self, "top", None)
        object.__setattr__(self, "skin", None)
        object.__setattr__(self, "pm", None)
        object.__setattr__(self, "km", None)
        object.__setattr__(self, "hm", None)
        object.__setattr__(self, "conf", None)
        object.__setattr__(self, "input", None)
        object.__setattr__(self, "term", None)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __setattr__(self, attr, val):
        # Assure attributes get assigned only once

        if object.__getattribute__(self, attr) is not None:
            raise AttributeError(_(u"Attribute %s is a constant" % attr))
        else:
            object.__setattr__(self, attr, val)
