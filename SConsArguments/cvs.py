"""`SConsArguments.cvs`

Defines arguments related to CVS

**Arguments**

Programs:

    CVS
        The CVS executable

Flags for programs:

    CVSCOFLAGS
        Options that are passed to the CVS checkout subcommand

    CVSFLAGS
        General options that are passed to CVS
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
  'CVS' : {
      'help'        : 'The CVS executable',
      'metavar'     : 'PROG'
  },
  'CVSCOFLAGS' : {
      'help'        : 'Options that are passed to the CVS checkout subcommand',
      'metavar'     : 'FLAGS',
      'converter'   : flags2list
  },
  'CVSFLAGS' : {
      'help'        : 'General options that are passed to CVS',
      'metavar'     : 'FLAGS',
      'converter'   : flags2list
  },
}

_groups = {
    'progs' : [ 'CVS' ],
    'flags' : [ 'CVSCOFLAGS', 'CVSFLAGS' ]
}

def arguments(**kw):
    """Returns argument declarations for 'cvs' tool

       :Keywords:
            include_groups : str | list
                include only arguments assigned to these groups
            exclude_groups : str | list
                exclude arguments assigned to these groups
            cvs_include_groups : str | list
                include only arguments assigned to these groups, this has
                higher priority than **include_groups**
            cvs_exclude_groups : str | list
                exclude arguments assigned to these groups, this has higher
                priority than **exclude_groups**
    """
    return export_arguments('cvs', _all_arguments, _groups, **kw)

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
