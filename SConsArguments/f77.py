"""`SConsArguments.f77`

Defines arguments related to Fortran 77 compiler

**Arguments**

Programs:
    F77
        The Fortran 77 compiler

    SHF77
        The Fortran 77 compiler used for generating shared-library objects


Flags for programs:
    F77FLAGS
        General user-specified options that are passed to the Fortran 77
        compiler

    F77PATH
        The list of directories that the Fortran 77 compiler will search for
        include directories

    SHF77FLAGS
        Options that are passed to the Fortran 77 compiler to generated
        shared-library objects

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
  'F77' : {
      'help'        : 'The Fortran 77 compiler',
      'metavar'     : 'PROG'
  },
  'F77FLAGS' : {
      'help'        : 'General user-specified options that are passed to the Fortran 77 compiler',
      'metavar'     : 'FLAGS',
      'converter'   : flags2list
  },
  'F77PATH' : {
      'help'        : 'The list of directories that the Fortran 77 compiler will search for include directories',
      'metavar'     : 'PATHS',
      'converter'   : paths2list
  },
  'SHF77' : {
      'help'        : 'The Fortran 77 compiler used for generating shared-library objects',
      'metavar'     : 'PROG',
  },
  'SHF77FLAGS' : {
      'help'        : 'Options that are passed to the Fortran 77 compiler to generated shared-library objects',
      'metavar'     : 'FLAGS',
      'converter'   : flags2list
  },
}

_groups = {
    'progs' : [ 'F77', 'SHF77' ],
    'flags' : [ 'F77FLAGS', 'F77PATH', 'SHF77FLAGS' ]
}

def arguments(**kw):
    """Returns argument declarations for 'f77' tool

       :Keywords:
            include_groups : str | list
                include only arguments assigned to these groups
            exclude_groups : str | list
                exclude arguents assigned to these groups
            f77_include_groups : str | list
                include only arguments assigned to these groups, this has
                higher priority than **include_groups**
            f77_exclude_groups : str | list
                exclude arguents assigned to these groups, this has higher
                priority than **exclude_groups**
    """
    return export_arguments('f77', _all_arguments, _groups, **kw)

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
