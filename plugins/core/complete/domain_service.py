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

import os
import itertools

from libxyz.core.utils import bstring, split_cmd

from domain_base import BaseDomain

class Domain(BaseDomain):
    """
    service(8) domain
    """

    INITD_DIR = "/etc/init.d"

    def complete(self, buf):
        """
        Take current buffer and return list-generator of all
                matched entries in current domain.

        @param buf: Current buffer
        @return: list-generator
        """

        cmd = split_cmd(bstring(buf))

        _len = len(cmd)

        if len(cmd) == 1:
            obj = ""
        else:
            obj = cmd[-1]

        _, _, files = os.walk(self.INITD_DIR).next()

        return itertools.ifilter(lambda x: x.startswith(obj), files)
