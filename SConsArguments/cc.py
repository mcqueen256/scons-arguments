"""`SConsArguments.cc`

Defines arguments related to C compiler

**Arguments**

Programs:

    CC
        The C compiler

    SHCC
        The C compiler used for generating shared-library objects

Flags for programs:

    CCFLAGS
        General options that are passed to the C and C++ compilers

    CCPCHFLAGS
        Options added to the compiler command line to support building with
        precompiled headers

    CCPDBFLAGS
        Options added to the compiler command line to support storing debugging
        information in a Microsoft Visual C++ PDB file

    CFLAGS
        General options that are passed to the C compiler (C only; not C++)

    CPPDEFINES
        A platform independent specification of C preprocessor definitions

    CPPFLAGS
        User-specified C preprocessor options

    CPPPATH
        The list of directories that the C preprocessor will search for include
        directories

    SHCCFLAGS
        Options that are passed to the C and C++ compilers to generate
        shared-library objects

    SHCFLAGS
        Options that are passed to the C compiler (only; not C++) to generate
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

from SConsArguments.Util import flags2list, cdefs2list, paths2list
from SConsArguments.Importer import export_arguments


_all_arguments = {
  'CC' : {
      'help'        : 'The C compiler',
      'metavar'     : 'PROG'
  },
  'CCFLAGS' : {
      'help'        : 'General options that are passed to the C and C++ compilers',
      'metavar'     : 'FLAGS',
      'converter'   : flags2list
  },
  'CCPCHFLAGS' : {
      'help'        : 'Options added to the compiler command line to support building with precompiled headers',
      'metavar'     : 'FLAGS',
      'converter'   : flags2list
  },
  'CCPDBFLAGS' : {
      'help'        : 'Options added to the compiler command line to support storing debugging information in a Microsoft Visual C++ PDB file',
      'metavar'     : 'FLAGS',
      'converter'   : flags2list
  },
  'CFLAGS' : {
      'help'        : 'General options that are passed to the C compiler (C only; not C++).',
      'metavar'     : 'FLAGS',
      'converter'   : flags2list
  },
  'CPPDEFINES' : {
      'help'        : 'A platform independent specification of C preprocessor definitions',
      'metavar'     : 'DEFS',
      'converter'   : cdefs2list
  },
  'CPPFLAGS' : {
      'help'        : 'User-specified C preprocessor options',
      'metavar'     : 'FLAGS',
      'converter'   : flags2list
  },
  'CPPPATH' : {
      'help'        : 'The list of directories that the C preprocessor will search for include directories',
      'metavar'     : 'PATHS',
      'converter'   : paths2list
  },
  'SHCC' : {
      'help'        : 'The C compiler used for generating shared-library objects',
      'metavar'     : 'PROG',
  },
  'SHCCFLAGS' : {
      'help'        : 'Options that are passed to the C and C++ compilers to generate shared-library objects',
      'metavar'     : 'FLAGS',
      'converter'   : flags2list
  },
  'SHCFLAGS' : {
      'help'        : 'Options that are passed to the C compiler (only; not C++) to generate shared-library objects',
      'metavar'     : 'FLAGS',
      'converter'   : flags2list
  },
}

_groups = {
    'progs' : [ 'CC', 'SHCC' ],
    'flags' : [ 'CCFLAGS', 'CCPCHFLAGS', 'CCPDBFLAGS', 'CFLAGS', 'CPPDEFINES',
                'CPPFLAGS', 'CPPPATH', 'SHCCFLAGS', 'SHCFLAGS' ]
}

def arguments(**kw):
    """Returns argument declarations for 'cc' tool

       :Keywords:
            include_groups : str | list
                include only arguments assigned to these groups
            exclude_groups : str | list
                exclude arguments assigned to these groups
            cc_include_groups : str | list
                include only arguments assigned to these groups, this has
                higher priority than **include_groups**
            cc_exclude_groups : str | list
                exclude arguments assigned to these groups, this has higher
                priority than **exclude_groups**
    """
    return export_arguments('cc', _all_arguments, _groups, **kw)

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
