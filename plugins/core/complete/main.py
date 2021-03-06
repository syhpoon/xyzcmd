#-*- coding: utf8 -*
#
# Max E. Kuznecov <syhpoon@syhpoon.name> 2010
#

import os
import re

from libxyz.core import ODict
from libxyz.core.utils import ustring, bstring, intersect, split_cmd
from libxyz.core.plugins import BasePlugin

from libxyz.ui import lowui
from libxyz.ui import ListEntry
from libxyz.ui import Keys
from libxyz.ui import XYZListBox

class XYZPlugin(BasePlugin):
    "Auto-completion plugin"

    NAME = u"complete"
    AUTHOR = u"Max E. Kuznecov <syhpoon@syhpoon.name>"
    VERSION = u"0.1"
    BRIEF_DESCRIPTION = u"Auto-completion system"
    FULL_DESCRIPTION = u"Plugin-based completion system"
    NAMESPACE = u"core"
    MIN_XYZ_VERSION = None
    DOC = u"Configuration variables:\n"\
          u"domains - List of domains to use.\n"\
          u"Default: ['binpath', 'fs']"
    HOMEPAGE = u"http://xyzcmd.syhpoon.name/"
    EVENTS = None

    def __init__(self, xyz):
        super(XYZPlugin, self).__init__(xyz)

        self._domains = ODict()

        self.export(self.complete)
        self.export(self.smart_complete)
        self.export(self.dialog)
        self._keys = Keys()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def prepare(self):
        # Domains initialization
        try:

            for domain in self.conf["domains"]:
                self._domains[domain] = self._init_domain(domain)

            behaviour = []

            for (pattern, domain) in self.conf["behaviour"]:
                behaviour.append((re.compile(pattern), domain))

            self.conf["behaviour"] = behaviour
        except Exception, e:
            xyzlog.warning(_(u"Error ininitalizing plugin: %s") %
                           (unicode(e)))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def finalize(self):
        for domain in self._domains:
            try:
                domain.finalize()
            except Exception:
                pass

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def complete(self, buf, domains=None):
        """
        Take current buffer and return list of list-generator each entry for
        each domain.

        @param buf: Current buffer
        @param domains: List of domains to search in,
               if None search in all available domains.
        @return: List of list-generator each entry for each domain
        """

        buf = bstring(buf)

        result = []

        if domains is None:
            domains = self._domains.keys()

        for d in domains:
            result.append(self._domains[d].complete(buf))

        return result

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def smart_complete(self, cmd):
        """
        Try to guess what completion domain can be used based on
        provided buffer and defined behaviour.

        @param cmd: Current buffer
        @return: List of list-generator each entry for each domain
        """

        if not cmd:
            return

        data = None
        pat_used = False
        buf = bstring(split_cmd(cmd)[-1])

        # First check the behaviour patterns
        for (pattern, domain) in self.conf["behaviour"]:
            if pattern.search(cmd) is not None:
                pat_used = True
                data = self.dialog(cmd, [domain])
                break

        # Else default fallback behaviour applied
        if pat_used == False:
            # Treat as path
            if buf.startswith(os.path.sep) or buf.startswith("./") or \
                   buf.startswith("../"):
                data = self.dialog(buf, ["fs"])
            else:
                # Treat as command in $PATH
                data = self.dialog(buf, ["binpath"])

        if data is not None:
            data = intersect(buf, data)
            self.xyz.pm.from_load(":sys:cmd", "append")(data)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def dialog(self, buf, domains=None):
        """
        Show a window containing matched entries
        and return user selected one
        """

        match = self.complete(buf, domains)

        _chdir = self.xyz.pm.from_load(u":sys:panel", u"chdir")

        _sel_attr = self.xyz.skin.attr(CompleteWindow.resolution, u"selected")
        _wdata = []

        for gen in match:
            for entry in sorted(gen):
                _wdata.append(ListEntry(entry, _sel_attr))

        if len(_wdata) == 1:
            return _wdata[0].text

        _walker = lowui.PollingListWalker(_wdata)
        _dim = tuple([x - 2 for x in self.xyz.screen.get_cols_rows()])

        return CompleteWindow(self.xyz, self.xyz.top, _walker, _(u"Complete"),
                              _dim, extra=_wdata, buf=buf).show()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _init_domain(self, dom):
        """
        Try to load and initialize domain class

        @param dom: Domain name string. Class name is constructed by
                    prepending domain_ prefix
        """

        domain_class = __import__("domain_%s" % dom, globals(), locals(), [])
        domain_obj = domain_class.Domain()

        domain_obj.prepare()

        return domain_obj

#++++++++++++++++++++++++++++++++++++++++++++++++

class CompleteWindow(XYZListBox):
    def __init__(self, *args, **kwargs):
        if "extra" in kwargs:
            self._extra = kwargs["extra"]
            del(kwargs["extra"])
        else:
            self._extra = None

        if "buf" in kwargs:
            self._buf = kwargs["buf"]
            del(kwargs["buf"])
        else:
            self._buf = u""

        super(CompleteWindow, self).__init__(*args, **kwargs)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def show(self, dim=None, exit_keys=None):
        """
        Show window. Update contents as user types
        """

        exit_keys = exit_keys or []

        if dim is None:
            dim = self.xyz.screen.get_cols_rows()

        _buf = u""
        _title = self.title

        while True:
            self.xyz.screen.draw_screen(dim, self.render(dim, True))

            _i = self.xyz.input.get()

            if self.xyz.input.WIN_RESIZE in _i:
                dim = self.xyz.screen.get_cols_rows()
                continue

            update = False

            if _i:
                for _k in _i:
                    if _k == self._keys.ESC:
                        return
                    elif _k == self._keys.BACKSPACE:
                        _buf = _buf[:-1]
                        update = True
                    elif _k == self._keys.ENTER:
                        entry, _ = self.listbox.get_focus()
                        return entry.text
                    elif len(ustring(_k)) == 1:
                        _buf += _k
                        update = True
                    else:
                        self._listbox.keypress(dim, _k)

                if update:
                    _b = bstring(_buf)
                    self.set_title(u"%s: %s" % (_title, _buf))

                    self.listbox.body.contents = [x for x in self._extra
                                                  if _b in x._text]
