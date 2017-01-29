"""`SConsArguments.mslink`

Defines arguments related to Microsoft linker

**Arguments**

Programs:
    MT
        The program used on Windows systems to embed manifests into DLLs and EXEs

    REGSVR
        The program used on Windows systems to register a newly-built DLL library

Flags for programs:
    MTFLAGS
        Flags passed to the mt manifest embedding program (Windows only)

    REGSVRFLAGS
        Flags passed to the DLL registration program on Windows systems

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
  'MT' : {
      'help'        : 'The program used on Windows systems to embed manifests into DLLs and EXEs',
      'metavar'     : 'PROG'
  },
  'MTFLAGS' : {
      'help'        : 'Flags passed to the mt manifest embedding program (Windows only)',
      'metavar'     : 'FLAGS',
      'converter'   : flags2list
  },
  'REGSVR' : {
      'help'        : 'The program used on Windows systems to register a newly-built DLL library',
      'metavar'     : 'PROG'
  },
  'REGSVRFLAGS' : {
      'help'        : 'Flags passed to the DLL registration program on Windows systems',
      'metavar'     : 'FLAGS',
      'converter'   : flags2list
  },
}

_groups = {
    'progs' : [ 'MT', 'REGSVR' ],
    'flags' : [ 'MTFLAGS', 'REGSVRFLAGS' ]
}

def arguments(**kw):
    """Returns argument declarations for 'mslink' tool

       :Keywords:
            include_groups : str | list
                include only arguments assigned to these groups
            exclude_groups : str | list
                exclude arguents assigned to these groups
            mslink_include_groups : str | list
                include only arguments assigned to these groups, this has
                higher priority than **include_groups**
            mslink_exclude_groups : str | list
                exclude arguents assigned to these groups, this has higher
                priority than **exclude_groups**
    """
    return export_arguments('mslink', _all_arguments, _groups, **kw)

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
