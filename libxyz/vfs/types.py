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

from libxyz.core.utils import ustring

class VFSTypeBase(object):
    """
    VFS type parent class
    """
    
    def __unicode__(self):
        return ustring(str(self))
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def __repr__(self):
        return self.__str__()

#++++++++++++++++++++++++++++++++++++++++++++++++

class VFSTypeFile(VFSTypeBase):
    """
    Regular file type
    """

    str_type = "-"
    vtype = " "

    def __str__(self):
        return "<Regular file type>"

#++++++++++++++++++++++++++++++++++++++++++++++++

class VFSTypeBlock(VFSTypeBase):
    """
    Block device type
    """

    str_type = "b"
    vtype = "+"

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __str__(self):
        return "<Block device type>"

#++++++++++++++++++++++++++++++++++++++++++++++++

class VFSTypeChar(VFSTypeBase):
    """
    Character device type
    """

    str_type = "c"
    vtype = "-"

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __str__(self):
        return "<Char device type>"

#++++++++++++++++++++++++++++++++++++++++++++++++

class VFSTypeDir(VFSTypeBase):
    """
    Directory type
    """

    str_type = "d"
    vtype = "/"

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __str__(self):
        return "<Directory type>"

#++++++++++++++++++++++++++++++++++++++++++++++++

class VFSTypeLink(VFSTypeBase):
    """
    Symbolic link type
    """

    str_type = "l"
    vtype = "@"

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __str__(self):
        return "<Soft link type>"

#++++++++++++++++++++++++++++++++++++++++++++++++

class VFSTypeFifo(VFSTypeBase):
    """
    FIFO type
    """

    str_type = "p"
    vtype = "|"

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def __str__(self):
        return "<FIFO type>"

#++++++++++++++++++++++++++++++++++++++++++++++++

class VFSTypeSocket(VFSTypeBase):
    """
    Socket type
    """

    str_type = "s"
    vtype = "="

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __str__(self):
        return "<Socket type>"

#++++++++++++++++++++++++++++++++++++++++++++++++

class VFSTypeUnknown(VFSTypeBase):
    """
    Unknown type
    """

    str_type = "?"

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __str__(self):
        return "<Unknown file type>"
