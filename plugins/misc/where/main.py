#-*- coding: utf8 -*
#
# Max E. Kuznecov <syhpoon@syhpoon.name> 2009
#

import os

from libxyz.core.plugins import BasePlugin
from libxyz.core import UserData

from libxyz.exceptions import XYZRuntimeError

class XYZPlugin(BasePlugin):
    "Plugin where"

    NAME = u"where"
    AUTHOR = u"Max E. Kuznecov <syhpoon@syhpoon.name>"
    VERSION = u"0.2"
    BRIEF_DESCRIPTION = _(u"Save panels locations")
    FULL_DESCRIPTION = _(u"When starting load previously saved locations")
    NAMESPACE = u"misc"
    MIN_XYZ_VERSION = 4
    DOC = None
    HOMEPAGE = "http://xyzcmd.syhpoon.name/"
    EVENTS = None

    def __init__(self, xyz):
        super(XYZPlugin, self).__init__(xyz)
        self._ud = UserData()
        self._wfile = "where"

        self.xyz.hm.register("event:startup", self.load)
        self.xyz.hm.register("event:shutdown", self.save)

        self.export(self.save)
        self.export(self.load)
        
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def load(self):
        """
        Restore locations on startup.
        File format is following:
        /panel-1/path
        /panel-2/path
        <Number of tabs in panel-1>
        <Active tab index in panel-1>
        <Active tab selected name in panel-1>
        panel-1 tab-1 path
        panel-1 tab-1 selected
        panel-1 tab-n path
        panel-1 tab-n selected
        <Number of tabs in panel-2>
        <Active tab index in panel-2>
        <Active tab selected name in panel-2>
        panel-2 tab-1 path
        panel-2 tab-1 selected
        panel-2 tab-n path
        panel-2 tab-n selected
        """

        chdir = self.xyz.pm.from_load(":sys:panel", "chdir")
        new_tab = self.xyz.pm.from_load(":sys:panel", "new_tab")
        select = self.xyz.pm.from_load(":sys:panel", "select")
        switch = self.xyz.pm.from_load(":sys:panel", "switch_tab")

        def restore_tabs(d, num, active):
            i = 0

            while i < num:
                tab_path = d[i].rstrip()
                tab_selected = d[i + 1].rstrip()

                chdir(tab_path, active=active)
                select(tab_selected, active=active)

                if i < num - 2:
                    new_tab(active=active)
                    
                i += 2

            return i

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        f = None

        try:
            f = self._ud.openfile(self._wfile, "r", "data")
            data = [x.rstrip() for x in f.readlines()]
            act = data[0]
            inact = data[1]

            chdir(act)
            chdir(inact, active=False)

            tabsnum = int(data[2]) * 2
            active_tab = int(data[3])
            selected = data[4]

            data = data[5:]

            restored = restore_tabs(data, tabsnum, True)

            tabsnum = int(data[restored]) * 2
            iactive_tab = int(data[restored + 1])
            iselected = data[restored + 2]

            data = data[restored + 3:]

            restore_tabs(data, tabsnum, False)

            switch(iactive_tab, active=False)
            switch(active_tab)
            select(iselected, active=False)
            select(selected)
        except Exception:
            pass
        
        if f:
            f.close()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def save(self):
        """
        Save locations on shutdown
        """

        panel = self.xyz.pm.load(":sys:panel")

        act = panel.cwd()
        inact = panel.cwd(active=False)
        tabs = panel.get_tabs()
        inacttabs = panel.get_tabs(active=False)

        f = None

        try:
            data = [act, inact]
            data.append(str(len(tabs)))
            data.append(str(panel.active_tab()))
            data.append(str(panel.get_selected().name))

            for tab_path, tab_selected in tabs:
                if tab_selected is None:
                    tab_selected = os.path.sep

                data.extend([tab_path, tab_selected])

            data.append(str(len(inacttabs)))
            data.append(str(panel.active_tab(active=False)))
            data.append(str(panel.get_selected(active=False).name))

            for itab_path, itab_selected in inacttabs:
                if itab_selected is None:
                    itab_selected = os.path.sep

                data.extend([itab_path, itab_selected])

            f = self._ud.openfile(self._wfile, "w", "data")

            f.write("\n".join(data))
        except XYZRuntimeError, e:
            xyzlog.info(_(u"Unable to open where data file: %s")
                        % ustring(str(e)))
        if f:
            f.close()

