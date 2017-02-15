"""`SConsArguments.gettext`

Defines arguments related to gettext tool

**Arguments**

Programs:
    MSGFMT
        The msgfmt executable

    MSGINIT
        The msginit executable

    MSGMERGE
        The msgmerge executable

    XGETTEXT
        The xgettext executable

Flags for programs:
    MSGFMTFLAGS
        General user options passed to msgfmt

    MSGINITFLAGS
        General user options passed to msginit

    MSGMERGEFLAGS
        General user options passed to msgmerge

    XGETTEXTFLAGS
        General user flags passed to xgettext.

    XGETTEXTPATH
        List of directories, where xgettext will look for source files
"""

#
# Copyright (c) 2017 by Pawel Tomulik
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE

__docformat__ = "restructuredText"

from SConsArguments.Util import flags2list, paths2list
from SConsArguments.Importer import export_arguments


_all_arguments = {
  'MSGFMT' : {
      'help'        : 'The msgfmt executable',
      'metavar'     : 'PROG'
  },
  'MSGFMTFLAGS' : {
      'help'        : 'General user options passed to msgfmt',
      'metavar'     : 'FLAGS',
      'converter'   : flags2list
  },
  'MSGINIT' : {
      'help'        : 'The msginit executable',
      'metavar'     : 'PROG',
  },
  'MSGINITFLAGS' : {
      'help'        : 'General user options passed to msginit',
      'metavar'     : 'FLAGS',
      'converter'   : flags2list
  },
  'MSGMERGE' : {
      'help'        : 'The msgmerge executable',
      'metavar'     : 'PROG',
  },
  'MSGMERGEFLAGS' : {
      'help'        : 'General user options passed to msgmerge',
      'metavar'     : 'FLAGS',
      'converter'   : flags2list
  },
  'XGETTEXT' : {
      'help'        : 'The xgettext executable',
      'metavar'     : 'PROG',
  },
  'XGETTEXTFLAGS' : {
      'help'        : 'General user flags passed to xgettext.',
      'metavar'     : 'FLAGS',
      'converter'   : flags2list
  },
  'XGETTEXTPATH' : {
      'help'        : 'List of directories, where xgettext will look for source files',
      'metavar'     : 'PATHS',
      'converter'   : paths2list
  },
}

_groups = {
    'progs' : [ 'MSGFMT', 'MSGINIT', 'MSGMERGE', 'XGETTEXT' ],
    'flags' : [ 'MSGFMTFLAGS', 'MSGINITFLAGS', 'MSGMERGEFLAGS', 'XGETTEXTFLAGS', 'XGETTEXTPATH' ]
}

def arguments(**kw):
    """Returns argument declarations for 'gettext' tool

       :Keywords:
            include_groups : str | list
                include only arguments assigned to these groups
            exclude_groups : str | list
                exclude arguments assigned to these groups
            gettext_include_groups : str | list
                include only arguments assigned to these groups, this has
                higher priority than **include_groups**
            gettext_exclude_groups : str | list
                exclude arguments assigned to these groups, this has higher
                priority than **exclude_groups**
    """
    return export_arguments('gettext', _all_arguments, _groups, **kw)

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
