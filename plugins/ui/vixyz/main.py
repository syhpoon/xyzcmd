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
    DOC = _(u"Available commands:\n"\
            u"j - move cursor one entry down\n"\
            u"k - move cursor one entry up\n"\
            u"l - perform an action on selected object\n"\
            u"h - step to the parent directory\n"\
            u"gg - move to the first entry\n"\
            u"G - move to the last entry\n"\
            u"Ctrl-G - show VFS object information\n"\
            u"m[a-z][A-Z][0-9] - set a mark to the current file\n"\
            u"'[a-z][A-Z][0-9] - jump to the marked file\n"\
            u"/ - search for object\n"\
            u"? - search for object backwards\n"\
            u"dd - remove object\n"\
            u"yy - copy object\n"\
            u"t - toggle tag\n"\
            u"i, I - switch to insert mode\n"\
            u"ESC - switch to command command mode")

    HOMEPAGE = u"http://xyzcmd.syhpoon.name/"
    EVENTS = None
    PALETTES = {
        'command_mode': {
            'monochrome': {
                'foreground': 'BLACK',
                'background': 'LIGHT_GRAY'
                },
            'seablue': {
                'foreground': 'DARK_BLUE',
                'background': 'LIGHT_GRAY'
                },
            'grass': {
                'foreground': 'DARK_GREEN',
                'background': 'LIGHT_GRAY'
                },
            'glamour': {
                'foreground': 'DARK_MAGENTA',
                'background': 'LIGHT_GRAY'
                },
            'lighty': {
                "foreground": "DEFAULT",
                "background": "DEFAULT",
                'foreground_high': '#ffd',
                "background_high": '#008'
                },
            None: {
                'foreground': 'DEFAULT',
                'background': 'DEFAULT'
                }
            }
        }

    def __init__(self, xyz):
        super(XYZPlugin, self).__init__(xyz)

        # Insert mode flag
        self._insert = False
        self._esc = Shortcut(sc=['ESCAPE'])
        self._marks = {}
        self._empty = lambda: None

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def prepare(self):
        self.panel = self.xyz.pm.load(":sys:panel")
        self.vfs = self.xyz.pm.load(":vfs:vfsutils")
        self.cmd = self.xyz.pm.load(":sys:cmd")

        cmd_mode_attr = self.xyz.skin.attr((self.ns.pfull,), "command_mode")

        self.insert_mode_attrf = self.cmd.get_attr_f()
        self.cmd_mode_attrf = lambda _: cmd_mode_attr

        self.toggle_insert_mode(False)

        def cd_parent():
            self.panel.chdir(XYZ.macro("ACT_BASE"))

            return self._empty

        self.keys = [
            (XYZ.kbd("i"), lambda _: self.toggle_insert_mode),
            (XYZ.kbd("I"), lambda _: self.toggle_insert_mode),
            (XYZ.kbd("j"), lambda _: self.panel.entry_next),
            (XYZ.kbd("l"), lambda _: self.panel.action),
            (XYZ.kbd("h"), lambda _: cd_parent),
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
        self.cmd.set_attr_f(self.insert_mode_attrf)
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
            self.toggle_insert_mode(False)

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

            if not key.composite:
                return self._empty

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

        if self._insert:
            self.cmd.set_attr_f(self.insert_mode_attrf)
        else:
            self.cmd.set_attr_f(self.cmd_mode_attrf)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def set_mark(self, sc, selected):
        """
        Set current object path as mark
        """

        self._marks[sc] = (XYZ.macro("ACT_CWD"), selected.name)
        return self._empty

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

        return self._empty
