"""`SConsArguments.link`

Defines arguments related to the linker

**Arguments**

Programs:
    LDMODULE
        The linker for building loadable modules

    LINK
        The linker

    SHLINK
        The linker for programs that use shared libraries


Flags for programs:
    LDMODULEFLAGS
        General user options passed to the linker for building loadable modules

    LIBPATH
        The list of directories that will be searched for libraries

    LINKFLAGS
        General user options passed to the linker

    SHLIBVERSIONFLAGS
        Extra flags added to $SHLINKCOM when building versioned SharedLibrary

    SHLINKFLAGS
        General user options passed to the linker for programs using shared libraries
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
  'LDMODULE' : {
      'help'        : 'The linker for building loadable modules',
      'metavar'     : 'PROG'
  },
  'LDMODULEFLAGS' : {
      'help'        : 'General user options passed to the linker for building loadable modules',
      'metavar'     : 'FLAGS',
      'converter'   : flags2list
  },
  'LIBPATH' : {
      'help'        : 'The list of directories that will be searched for libraries',
      'metavar'     : 'PATHS',
      'converter'   : paths2list
  },
  'LINK' : {
      'help'        : 'The linker',
      'metavar'     : 'PROG'
  },
  'LINKFLAGS' : {
      'help'        : 'General user options passed to the linker',
      'metavar'     : 'FLAGS',
      'converter'   : flags2list
  },
  'SHLIBVERSIONFLAGS' : {
      'help'        : 'Extra flags added to $SHLINKCOM when building versioned SharedLibrary',
      'metavar'     : 'FLAGS',
      'converter'   : flags2list
  },
  'SHLINK' : {
      'help'        : 'The linker for programs that use shared libraries',
      'metavar'     : 'PROG'
  },
  'SHLINKFLAGS' : {
      'help'        : 'General user options passed to the linker for programs using shared libraries',
      'metavar'     : 'FLAGS',
      'converter'   : flags2list
  },
}

_groups = {
    'progs' : [ 'LDMODULE', 'LINK', 'SHLINK' ],
    'flags' : [ 'LDMODULEFLAGS', 'LIBPATH', 'LINKFLAGS', 'SHLIBVERSIONFLAGS', 'SHLINKFLAGS' ]
}

def arguments(**kw):
    """Returns argument declarations for 'link' tool

       :Keywords:
            include_groups : str | list
                include only arguments assigned to these groups
            exclude_groups : str | list
                exclude arguments assigned to these groups
            link_include_groups : str | list
                include only arguments assigned to these groups, this has
                higher priority than **include_groups**
            link_exclude_groups : str | list
                exclude arguments assigned to these groups, this has higher
                priority than **exclude_groups**
    """
    return export_arguments('link', _all_arguments, _groups, **kw)

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
