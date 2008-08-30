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

class VFSTypeFile(object):
    """
    Regular file type
    """

    str_type = u"-"
    vtype = u" "

    def __str__(self):
        return "<Regular file type>"

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __repr__(self):
        return self.__str__()

#++++++++++++++++++++++++++++++++++++++++++++++++

class VFSTypeBlock(object):
    """
    Block device type
    """

    str_type = u"b"
    vtype = u"+"

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __str__(self):
        return "<Block device type>"

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __repr__(self):
        return self.__str__()

#++++++++++++++++++++++++++++++++++++++++++++++++

class VFSTypeChar(object):
    """
    Character device type
    """

    str_type = u"c"
    vtype = u"-"

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __str__(self):
        return "<Char device type>"

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __repr__(self):
        return self.__str__()

#++++++++++++++++++++++++++++++++++++++++++++++++

class VFSTypeDir(object):
    """
    Directory type
    """

    str_type = u"d"
    vtype = u"/"

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __str__(self):
        return "<Directory type>"

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __repr__(self):
        return self.__str__()

#++++++++++++++++++++++++++++++++++++++++++++++++

class VFSTypeLink(object):
    """
    Symbolic link type
    """

    str_type = u"l"
    vtype = u"@"

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __str__(self):
        return "<Soft link type>"

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __repr__(self):
        return self.__str__()

#++++++++++++++++++++++++++++++++++++++++++++++++

class VFSTypeFifo(object):
    """
    FIFO type
    """

    str_type = u"p"
    vtype = u"|"

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def __str__(self):
        return "<FIFO type>"

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __repr__(self):
        return self.__str__()

#++++++++++++++++++++++++++++++++++++++++++++++++

class VFSTypeSocket(object):
    """
    Socket type
    """

    str_type = u"s"
    vtype = u"="

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __str__(self):
        return "<Socket type>"

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __repr__(self):
        return self.__str__()

#++++++++++++++++++++++++++++++++++++++++++++++++

class VFSTypeUnknown(object):
    """
    Unknown type
    """

    str_type = u"?"

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __str__(self):
        return "<Unknown file type>"

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __repr__(self):
        return self.__str__()
