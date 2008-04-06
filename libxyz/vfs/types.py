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

class VFSTypeFile(object):
    """
    Regular file type
    """

    str_type = u"-"

#++++++++++++++++++++++++++++++++++++++++++++++++

class VFSTypeBlock(object):
    """
    Block device type
    """

    str_type = u"b"

#++++++++++++++++++++++++++++++++++++++++++++++++

class VFSTypeChar(object):
    """
    Character device type
    """

    str_type = u"c"

#++++++++++++++++++++++++++++++++++++++++++++++++

class VFSTypeDir(object):
    """
    Directory type
    """

    str_type = u"d"

#++++++++++++++++++++++++++++++++++++++++++++++++

class VFSTypeLink(object):
    """
    Symbolic link type
    """

    str_type = u"l"

#++++++++++++++++++++++++++++++++++++++++++++++++

class VFSTypeFifo(object):
    """
    FIFO type
    """

    str_type = u"p"

#++++++++++++++++++++++++++++++++++++++++++++++++

class VFSTypeSocket(object):
    """
    Socket type
    """

    str_type = u"s"

#++++++++++++++++++++++++++++++++++++++++++++++++

class VFSTypeUnknown(object):
    """
    Unknown type
    """

    str_type = u"?"
