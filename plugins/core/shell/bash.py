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

"""
Bash setup function
"""

import subprocess
import re

from libxyz.core.dsl import XYZ
from libxyz.core.utils import ustring

def bash_setup(path):
    # Fake PS1 in order to process .bashrc

    aliasre = re.compile(r"^alias\s+(.+?)='(.+?)'\s*$")
    
    try:
        result = subprocess.Popen([
            path, "-c", "PS1='.'; source ~/.bashrc ; alias"],
                                  stdout=subprocess.PIPE
                                  ).communicate()[0].strip()

        if result:
            for line in result.split("\n"):
                match = aliasre.search(line)

                if match:
                    XYZ.alias(match.group(1), match.group(2))
    except Exception, e:
        xyzlog.warning(_(u"Error setting up bash: %s") % unicode(e))
