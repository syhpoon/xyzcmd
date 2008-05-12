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

import os
import os.path

import libxyz.const

from libxyz.exceptions import XYZRuntimeError

class UserData(object):
    """
    Common interface for access data-files in user directory
    """

    def __init__(self):
        self.user_dir = os.path.join(os.path.expanduser("~"),
                                     libxyz.const.USER_DIR)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def openfile(self, filename, mode, subdir=None):
        """
        Open data file and return open file-object
        For instance:
        > openfile("keycodes", "rb", "data")
        Will open file ~/.xyzcmd/data/keycodes for binary reading etc.

        @param filename: File name
        @param mode: Open mode
        @param subdir: Optional subdirectory
        @return open file-object or XYZRuntimeError raised on error
        """

        try:
            return open(self.makepath(filename, subdir), mode)
        except IOError, e:
            raise XYZRuntimeError(e)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def delfile(self, filename, subdir=None):
        """
        Delete file in user-directory
        """

        _path = self.makepath(filename, subdir)

        if os.path.isfile(_path):
            try:
                os.unlink(_path)
            except OSError, e:
                raise XYZRuntimeError(e)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def makepath(self, filename, subdir=None):
        """
        Make absolute path to file
        """

        _path = [self.user_dir]

        if subdir is not None:
            _path.append(subdir)

            _prelpath = os.path.join(*_path)

            # Create subdirectory if it doesn't exist
            if not os.access(_prelpath, os.F_OK):
                try:
                    os.mkdir(_prelpath)
                except OSError, e:
                    raise XYZRuntimeError(e)

        _path.append(filename)

        return os.path.join(*_path)
