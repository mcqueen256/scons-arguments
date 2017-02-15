"""`SConsArguments.ar`

Defines arguments related to static library archiver AR

**Arguments**

Programs:

    AR
        The static library archiver

    RANLIB
        The archive indexer

Flags for programs:

    ARFLAGS
        General options passed to the static library archiver

    RANLIBFLAGS
        General options passed to the archive indexer
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
  'AR' : {
      'help'        : 'The static library archiver',
      'metavar'     : 'PROG'
  },
  'ARFLAGS' : {
      'help'        : 'General options passed to the static library archiver',
      'metavar'     : 'FLAGS',
      'converter'   : flags2list
  },
  'RANLIB' : {
      'help'        : 'The archive indexer',
      'metavar'     : 'PROG'
  },
  'RANLIBFLAGS' : {
      'help'        : 'General options passed to the archive indexer',
      'metavar'     : 'FLAGS',
      'converter'   : flags2list
  }
}

_groups = {
    'progs' : [ 'AR', 'RANLIB' ],
    'flags' : [ 'ARFLAGS', 'RANLIBFLAGS' ]
}


def arguments(**kw):
    """Returns argument declarations for 'ar' tool

       :Keywords:
            include_groups : str | list
                include only arguments assigned to these groups
            exclude_groups : str | list
                exclude arguments assigned to these groups
            ar_include_groups : str | list
                include only arguments assigned to these groups, this has
                higher priority than **include_groups**
            ar_exclude_groups : str | list
                exclude arguments assigned to these groups, this has higher
                priority than **exclude_groups**
    """
    return export_arguments('ar', _all_arguments, _groups, **kw)

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
