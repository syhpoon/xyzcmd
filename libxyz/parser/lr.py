#-*- coding: utf8 -*
#
# Max E. Kuznecov <syhpoon@syhpoon.name> 2008
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

'''
LR parser stuff
'''

class ActionTable(object):
    """
    Action table for LR parsing
    """

    def __init__(self):
        self._table = {}

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def add(self, state, token, args):
        """
        Add table entry
        """

        if state not in self._table:
            self._table[state] = {}

        self._table[state][token] = args

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def get(self, state, token):
        """
        Get action for state and token or raise KeyError
        """

        return self._table[state][token]

#++++++++++++++++++++++++++++++++++++++++++++++++

class GotoTable(object):
    """
    Goto table
    """

    def __init__(self):
        self._table = {}

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def add(self, state, ntoken, newstate):
        """
        Add table entry
        """

        if state not in self._table:
            self._table[state] = {}

        self._table[state][ntoken] = newstate

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def get(self, state, ntoken):
        return self._table[state][ntoken]

#++++++++++++++++++++++++++++++++++++++++++++++++

class Rules(object):
    """
    Parsing rules
    """

    def __init__(self):
        self._rules = {}

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def add(self, ruleno, ntoken, size):
        """
        Add rule

        @param ruleno: Rule number, used by REDUCE action
        @param ntoken: Left side non-terminal of the rule
        @param size: RHS size
        """

        self._rules[ruleno] = (ntoken, size)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def get(self, ruleno):
        """
        Return tuple: ntoken, size or raise KeyError
        """

        return self._rules[ruleno]

#++++++++++++++++++++++++++++++++++++++++++++++++

class Tree(list):
    """
    Tree class
    """

    def __init__(self):
        super(Tree, self).__init__()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def add(self, obj):
        self.append(obj)
