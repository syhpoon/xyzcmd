#-*- coding: utf8 -*
#
# Max E. Kuznecov <mek@mek.uz.ua> 2010
#

from libxyz.core.utils import is_func
from libxyz.core.plugins import BasePlugin
from libxyz.ui import Shortcut
from libxyz.core.dsl import XYZ

class XYZPlugin(BasePlugin):
    "Plugin vixyz"

    NAME = u"vixyz"
    AUTHOR = u"Max E. Kuznecov <mek@mek.uz.ua>"
    VERSION = u"0.1"
    BRIEF_DESCRIPTION = _(u"Vi-like navigation mode")
    FULL_DESCRIPTION = _(u"")
    NAMESPACE = u"ui"
    MIN_XYZ_VERSION = 6
    DOC = None
    HOMEPAGE = u"http://xyzcmd.syhpoon.name/"
    EVENTS = None

    def __init__(self, xyz):
        super(XYZPlugin, self).__init__(xyz)

        # Insert mode flag
        self._insert = False
        self._esc = Shortcut(sc=['ESCAPE'])
        self._marks = {}

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def prepare(self):
        self.panel = self.xyz.pm.load(":sys:panel")
        self.vfs = self.xyz.pm.load(":vfs:vfsutils")

        self.keys = [
            (XYZ.kbd("i"), lambda _: self.toggle_insert_mode),
            (XYZ.kbd("j"), lambda _: self.panel.entry_next),
            (XYZ.kbd("l"), lambda _: self.panel.action),
            (XYZ.kbd("h"), lambda _: self.panel.chdir(XYZ.macro("ACT_BASE"))),
            (XYZ.kbd("k"), lambda _: self.panel.entry_prev),
            (XYZ.kbd("/"), lambda _: self.panel.search_cycle),
            (XYZ.kbd("?"), lambda _: self.panel.search_backward),
            (XYZ.kbd("t"), lambda _: self.panel.toggle_tag),
            (XYZ.kbd("CTRL-g"), lambda _:
             self.xyz.pm.from_load(":vfs:fileinfo", "fileinfo")),
            (XYZ.kbd("d"), [ (XYZ.kbd("d"), lambda _: self.vfs.remove) ]),
            (XYZ.kbd("y"), [ (XYZ.kbd("y"), lambda _: self.vfs.copy) ]),
            (XYZ.kbd("G"), lambda _: self.panel.entry_bottom),
            (XYZ.kbd("g"), [ (XYZ.kbd("g"),
                              lambda _: self.panel.entry_top) ]),
            (XYZ.kbd("m"), [ (lambda x: x.raw[0].isalpha(),
                 lambda k: self.set_mark(k, self.panel.get_selected())) ]),
            (XYZ.kbd("`"), [
                (lambda x: x.raw[0].isalpha(), lambda k: self.goto_mark(k)) ])
            ]

        self.xyz.km.reader = self.reader

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def finalize(self):
        self.xyz.km.reset_reader()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def reader(self, raw, context=None, keys=None):
        """
        Custom reader
        """

        keys = keys or self.keys
        key = Shortcut(raw=raw)

        # Break insert mode if any
        if key == self._esc and self._insert:
            self._insert = False

            return self.reader(self.xyz.input.get(), context)
        # In non-insert treat keys as commands
        elif not self._insert:
            for k, v in keys:
                if (is_func(k) and k(key)) or k == key:
                    if isinstance(v, list):
                        return self.reader(self.xyz.input.get(),
                                           context, keys=v)
                    else:
                        return v(key)

        return self.xyz.km.default_reader(raw, context)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def toggle_insert_mode(self, value=None):
        """
        Toggle insert mode
        """

        # Toggle
        if value is None:
            self._insert = not self._insert
        else:
            self._insert = value

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def set_mark(self, sc, selected):
        """
        Set current object path as mark
        """

        self._marks[sc] = (XYZ.macro("ACT_CWD"), selected.name)
        return lambda: None

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def goto_mark(self, sc):
        """
        Chdir to mark
        """

        path = self._marks.get(sc, None)

        if path is not None:
            dir, file = path

            try:
                self.panel.chdir(dir)
                self.panel.select(file)
            except Exception:
                pass

        return lambda: None
