"""`SConsArguments.f08`

Defines arguments related to Fortran 08 compiler

**Arguments**

Programs:
    F08
        The Fortran 08 compiler

    SHF08
        The Fortran 08 compiler used for generating shared-library objects


Flags for programs:
    F08FLAGS
        General user-specified options that are passed to the Fortran 08
        compiler

    F08PATH
        The list of directories that the Fortran 08 compiler will search for
        include directories

    SHF08FLAGS
        Options that are passed to the Fortran 08 compiler to generated
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
  'F08' : {
      'help'        : 'The Fortran 08 compiler',
      'metavar'     : 'PROG'
  },
  'F08FLAGS' : {
      'help'        : 'General user-specified options that are passed to the Fortran 08 compiler',
      'metavar'     : 'FLAGS',
      'converter'   : flags2list
  },
  'F08PATH' : {
      'help'        : 'The list of directories that the Fortran 08 compiler will search for include directories',
      'metavar'     : 'PATHS',
      'converter'   : paths2list
  },
  'SHF08' : {
      'help'        : 'The Fortran 08 compiler used for generating shared-library objects',
      'metavar'     : 'PROG',
  },
  'SHF08FLAGS' : {
      'help'        : 'Options that are passed to the Fortran 08 compiler to generated shared-library objects',
      'metavar'     : 'FLAGS',
      'converter'   : flags2list
  },
}

_groups = {
    'progs' : [ 'F08', 'SHF08' ],
    'flags' : [ 'F08FLAGS', 'F08PATH', 'SHF08FLAGS' ]
}

def arguments(**kw):
    """Returns argument declarations for 'f08' tool

       :Keywords:
            include_groups : str | list
                include only arguments assigned to these groups
            exclude_groups : str | list
                exclude arguents assigned to these groups
            f08_include_groups : str | list
                include only arguments assigned to these groups, this has
                higher priority than **include_groups**
            f08_exclude_groups : str | list
                exclude arguents assigned to these groups, this has higher
                priority than **exclude_groups**
    """
    return export_arguments('f08', _all_arguments, _groups, **kw)

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
