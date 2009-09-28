#-*- coding: utf8 -*
#
# Max E. Kuznecov <syhpoon@syhpoon.name> 2009
#

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
        self.export(self.remove)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def mkdir(self):
        """
        Create new directory dialog
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
        Remove VFS object dialog
        """
        
        self._load_panel()

        tagged = self._panel.get_tagged()

        if tagged:
            objs, msg = tagged, _(u"Really remove %d objects?") % len(tagged)
        else:
            selected = self._panel.get_selected()
            objs, msg = [selected], \
                       _(u"Really remove %s (%s)?") % \
                       (ustring(selected.name),
                        ustring(selected.ftype))

        _deletep = uilib.YesNoBox(self.xyz, self.xyz.top, msg,
                                  title=_(u"Remove object"))

        if not _deletep.show():
            return

        # TODO: All, None, Skip, Stop buttons
        force = False
        
        for obj in objs:
            if not force and obj.is_dir() and not obj.is_dir_empty():
                _rec = uilib.YesNoBox(
                    self.xyz, self.xyz.top,
                    _(u"Directory is not empty\nRemove it recursively?"),
                    title=_(u"Remove %s") % ustring(obj.full_path))

                if not _rec.show():
                    continue
                else:
                    force = True
                    
            uilib.MessageBox(self.xyz, self.xyz.top,
                             _(u"Removing object: %s") %
                             ustring(obj.full_path),
                             _(u"Removing")).show(wait=False)

            try:
                obj.remove()
            except Exception, e:
                uilib.ErrorBox(self.xyz, self.xyz.top,
                               _(u"Unable to remove object: %s") %
                               (ustring(str(e))),
                               _(u"Error")).show()
                xyzlog.error(_(u"Error removing object: %s") %
                             ustring(str(e)))
                break

        self._panel.reload()
                
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def _load_panel(self):
        """
        Load :sys:panel plugin
        """

        if self._panel is None:
            self._panel = self.xyz.pm.load(":sys:panel")
