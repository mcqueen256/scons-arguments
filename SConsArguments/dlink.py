"""`SConsArguments.dlink`

Defines arguments related to D linker

**Arguments**

Programs:
    DLIB
        Executable used to create D libraries
    DLINK
        D linker

Flags for programs:
    DLINKFLAGS
        General options passed to D linker

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

from SConsArguments.Util import flags2list
from SConsArguments.Importer import export_arguments

_all_arguments = {
  'DLIB' : {
      'help'        : 'Executable used to create D libraries',
      'metavar'     : 'PROG'
  },
  'DLINK' : {
      'help'        : 'D linker',
      'metavar'     : 'PROG'
  },
  'DLINKFLAGS' : {
      'help'        : 'General options passed to D linker',
      'metavar'     : 'FLAGS',
      'converter'   : flags2list
  },
}

_groups = {
    'progs' : [ 'DLIB', 'DLINK' ],
    'flags' : [ 'DLINKFLAGS' ]
}

def arguments(**kw):
    """Returns argument declarations for 'dlink' tool

       :Keywords:
            include_groups : str | list
                include only arguments assigned to these groups
            exclude_groups : str | list
                exclude arguments assigned to these groups
            dlink_include_groups : str | list
                include only arguments assigned to these groups, this has
                higher priority than **include_groups**
            dlink_exclude_groups : str | list
                exclude arguments assigned to these groups, this has higher
                priority than **exclude_groups**
    """
    return export_arguments('dlink', _all_arguments, _groups, **kw)

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
