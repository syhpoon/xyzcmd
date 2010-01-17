#-*- coding: utf8 -*
#
# Max E. Kuznecov <syhpoon@syhpoon.name> 2009
#

import threading

import libxyz.ui as uilib

from libxyz.core.utils import ustring, bstring
from libxyz.core.plugins import BasePlugin

from box_copy import CopyBox

class XYZPlugin(BasePlugin):
    """
    Plugin vfsutils
    """

    NAME = u"vfsutils"
    AUTHOR = u"Max E. Kuznecov <syhpoon@syhpoon.name>"
    VERSION = u"0.1"
    BRIEF_DESCRIPTION = _(u"Useful VFS routines")
    FULL_DESCRIPTION = _(u"Dialogs for common VFS operations")
    NAMESPACE = u"vfs"
    MIN_XYZ_VERSION = None
    DOC = None
    HOMEPAGE = "http://xyzcmd.syhpoon.name"

    def __init__(self, xyz):
        super(XYZPlugin, self).__init__(xyz)

        self.keys = uilib.Keys()
        self._panel = None

        self.export(self.mkdir)
        self.export(self.remove)
        self.export(self.copy)
        self.export(self.move)

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
        else:
            _dir = bstring(_dir)

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
        objs = self._panel.get_active()

        if not objs:
            return

        _len = len(objs)
        
        if _len > 1:
            msg = _(u"Really remove %d objects?") % _len
        else:
            selected = objs[0]
            msg = _(u"Really remove %s (%s)?") % \
                  (ustring(selected.name), ustring(selected.ftype))

        _deletep = uilib.YesNoBox(self.xyz, self.xyz.top, msg,
                                  title=_(u"Remove object"))

        if not _deletep.show():
            return

        force = False

        CODE_ALL = 10
        CODE_YES = 20
        CODE_NO = 30
        CODE_ABORT = 40
        
        buttons = [
            (_(u"All"), CODE_ALL),
            (_(u"Yes"), CODE_YES),
            (_(u"No"), CODE_NO),
            (_(u"Abort"), CODE_ABORT),
            ]
        
        for obj in objs:
            if not force and obj.is_dir() and not obj.is_dir_empty():
                _rec = uilib.ButtonBox(
                    self.xyz, self.xyz.top,
                    _(u"Directory is not empty\nRemove it recursively?"),
                    buttons,
                    title=_(u"Remove %s") % ustring(obj.full_path)).show()

                if _rec == CODE_ABORT:
                    break
                elif _rec == CODE_ALL:
                    force = True
                elif _rec == CODE_NO:
                    continue

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

    def copy(self, move=False):
        """
        Copy objects dialog
        """

        self._load_panel()
        objs = self._panel.get_active()

        if not objs:
            return

        if len(objs) == 1:
            srctxt = ustring(objs[0].full_path)
        else:
            srctxt = _(u"%d objects") % len(objs)
            
        srctxt = bstring(srctxt)

        if move:
            _m = _(u"Move")
            msg = _(u"Moving object: %s")
            caption = _(u"Moving")
            unable_msg = _(u"Unable to move object: %s")
            unable_caption = _(u"Move error")
        else:
            _m = _(u"Copy")
            msg = _(u"Copying object: %s")
            caption = _(u"Copying")
            unable_msg = _(u"Unable to copy object: %s")
            unable_caption = _(u"Copy error")

        msg += _(u"\nESCAPE to abort")
        data = CopyBox(self.xyz, srctxt, self._panel.cwd(active=False),
                       bstring(_m)).show()

        if data is None:
            return

        stopped = threading.Event()
        cancel = threading.Event()
        free = threading.Event()
        free.set()

        def existcb(vfsobj):
            free.clear()
            
            buttons = [
                (_(u"Yes"), "override"),
                (_(u"All"), "override all"),
                (_(u"Skip"), "skip"),
                (_(u"Skip all"), "skip all"),
                (_(u"Abort"), "abort"),
                ]

            try:
                name = ustring(vfsobj.name)
            
                _rec = uilib.ButtonBox(
                    self.xyz, self.xyz.top,
                    _(u"Object %s already exists. Really override?") % name,
                    buttons, title=_(u"Override %s") % name).show()

                uilib.MessageBox(self.xyz, self.xyz.top,
                                 caption, caption).show(wait=False)

                free.set()
                return _rec or 'abort'
            except Exception:
                free.set()

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        def errorcb(vfsobj, errstr):
            free.clear()

            buttons = [
                (_(u"Skip"), "skip"),
                (_(u"Skip all"), "skip all"),
                (_(u"Abort"), "abort"),
                ]

            try:
                _rec = uilib.ButtonBox(
                    self.xyz, self.xyz.top,
                    _(u"An error occured %s: %s") % (
                        ustring(vfsobj.full_path), ustring(errstr)),
                    buttons, title=_(u"Copy error")).show()

                uilib.MessageBox(self.xyz, self.xyz.top,
                                 caption, caption).show(wait=False)

                free.set()
                return _rec or 'abort'
            except Exception:
                free.set()

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        args = {
            "existcb": existcb,
            "errorcb": errorcb,
            "save_attrs": data["save_attributes"],
            "follow_links": data["follow_links"],
            "cancel": cancel
            }

        runner_error = []
        
        def frun(o, err):
            stopped.clear()

            try:
                if move:
                    attr = "move"
                else:
                    attr = "copy"

                getattr(o, attr)(data["dst"], **args)
            except StopIteration, e:
                pass
            except Exception, e:
                err.append(ustring(str(e)))

            stopped.set()

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        
        for obj in objs:
            if cancel.isSet():
                break

            uilib.MessageBox(self.xyz, self.xyz.top,
                             msg % ustring(obj.full_path),
                             caption).show(wait=False)

            try:
                runner = threading.Thread(target=lambda:
                                          frun(obj, runner_error))
                runner.start()

                # While runner is running, poll for the user input
                # abort if ESCAPE pressed
                while True:
                    # Callback handler is active
                    if not free.isSet():
                        free.wait()

                    # Runner thread terminated, continue
                    if stopped.isSet():
                        runner.join()
                        if runner_error:
                            uilib.ErrorBox(self.xyz, self.xyz.top,
                                           unable_msg % runner_error[0],
                                           unable_caption).show()
                            xyzlog.error(unable_msg % runner_error[0])

                        break

                    _in = self.xyz.input.get(True)

                    # User abort
                    if self.keys.ESCAPE in _in:
                        cancel.set()
                        runner.join()
                        break
            except Exception:
                break

        self._panel.reload()
        self._panel.reload(active=False)
        
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def move(self):
        """
        Move objects dialog
        """

        return self.copy(move=True)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def _load_panel(self):
        """
        Load :sys:panel plugin
        """

        if self._panel is None:
            self._panel = self.xyz.pm.load(":sys:panel")
