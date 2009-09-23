#-*- coding: utf8 -*
#
# Max E. Kuznecov <syhpoon@syhpoon.name> 2009
#

import os

import libxyz.ui as uilib

from libxyz.core.utils import ustring
from libxyz.core.plugins import BasePlugin

class XYZPlugin(BasePlugin):
    "Plugin vfsutils"

    NAME = u"vfsutils"
    AUTHOR = u"Max E. Kuznecov <syhpoon@syhpoon.name>"
    VERSION = u"0.1"
    BRIEF_DESCRIPTION = u"Useful VFS routines"
    FULL_DESCRIPTION = u""
    NAMESPACE = u"vfs"
    MIN_XYZ_VERSION = None
    DOC = None
    HOMEPAGE = "http://xyzcmd.syhpoon.name"

    def __init__(self, xyz):
        super(XYZPlugin, self).__init__(xyz)

        self._panel = None

        self.export(self.mkdir)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _load_panel(self):
        """
        Load :sys:panel plugin
        """

        if self._panel is None:
            self._panel = self.xyz.pm.load(":sys:panel")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def mkdir(self, newdir=None):
        """
        Create new directory
        """

        self._load_panel()

        _box = uilib.InputBox(self.xyz, self.xyz.top,
                              _(u"New directory name"),
                              title=_(u"Create directory"))

        _dir = _box.show()

        if not _dir:
            return

        try:
            self._panel.get_current().mkdir(_dir)
        except Exception, e:
            xyzlog.error(_(u"Unable to create directory: %s") %
                         ustring(str(e)))
        else:
            self._panel.reload()
            self._panel.select(_dir)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def remove(self):
        """
        Remove VFS object (if possible)
        """

        pass
