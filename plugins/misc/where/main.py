#-*- coding: utf8 -*
#
# Max E. Kuznecov <syhpoon@syhpoon.name> 2009
#

from libxyz.core.plugins import BasePlugin
from libxyz.core import UserData

class XYZPlugin(BasePlugin):
    "Plugin where"

    NAME = u"where"
    AUTHOR = u"Max E. Kuznecov <syhpoon@syhpoon.name>"
    VERSION = u"0.1"
    BRIEF_DESCRIPTION = _(u"Save panels locations")
    FULL_DESCRIPTION = _(u"When starting load previously saved locations")
    NAMESPACE = u"misc"
    MIN_XYZ_VERSION = 2
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
        Restore locations on startup
        """

        f = None
        try:
            f = self._ud.openfile(self._wfile, "r", "data")
            data = f.readlines()
            act = data[0].strip()
            inact = data[1].strip()

            chdir = self.xyz.pm.from_load(":sys:panel", "chdir")
            chdir(act)
            chdir(inact, active=False)
        except Exception, e:
            pass
        finally:
            if f:
                f.close()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def save(self):
        """
        Save locations on shutdown
        """

        cwdf = self.xyz.pm.from_load(":sys:panel", "cwd")
        act = cwdf()
        inact = cwdf(active=False)

        f = None
        try:
            f = self._ud.openfile(self._wfile, "w", "data")
            f.write("\n".join([act, inact]))
        except XYZRuntimeError, e:
            xyzlog.info(_(u"Unable to open where data file: %s")
                        % ustring(str(e)))
        finally:
            if f:
                f.close()
