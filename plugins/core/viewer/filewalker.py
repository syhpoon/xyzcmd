#-*- coding: utf8 -*
#
# Max E. Kuznecov ~syhpoon <mek@mek.uz.ua> 2008
#

import libxyz

from libxyz.ui import lowui
from libxyz.exceptions import XYZError

class FileWalker(lowui.ListWalker):
    """
    Walker class for lazy file reading
    """

    def __init__(self, filename):
        # File contents
        self._data = []
        self._focus = 0

        self._file = None

        try:
            self._file = open(filename)
        except IOError, e:
            raise XYZError(_(u"Unable to open file %s: %s") %
                           (filename.decode(xyzenc),
                            e.message.decode(xyzenc)))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __del__(self):
        if self._file is not None and not self._file.closed:
            self._file.close()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def get_focus(self):
        return self._get_at_pos(self._focus)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def set_focus(self, focus):
        self._focus = focus
        self._modified()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def get_next(self, start):
        return self._get_at_pos(start + 1)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def get_prev(self, start):
        return self._get_at_pos(start - 1)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _get_at_pos(self, pos):
        """
        Return widget at position
        """

        if pos < 0:
            return None, None

        if len(self._data) > pos:
            return self._data[pos], pos

        if self._file.closed:
            return None, None

        if pos != len(self._data):
            raise XYZError(_(u"Invalid request order"))

        return self._read_next(), pos

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _read_next(self):
        """
        Read next file line
        """

        _line = self._file.readline()

        if not _line:
            self._file.close()
            return None

        _line = _line.rstrip("\n")

        self._data.append(lowui.Text(_line.expandtabs()))

        return self._data[-1]
