"""`SConsArguments.swig`

Defines arguments related to SWIG

**Arguments**

Programs:
    SWIG
        The scripting language wrapper and interface generator


Flags for programs:
    SWIGFLAGS
        General options passed to the SWIG

    SWIGPATH
        The list of directories that the scripting language wrapper and
        interface generate will search for included files

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
  'SWIG' : {
      'help'        : 'The scripting language wrapper and interface generator',
      'metavar'     : 'PROG'
  },
  'SWIGFLAGS' : {
      'help'        : 'General options passed to the SWIG',
      'metavar'     : 'FLAGS',
      'converter'   : flags2list
  },
  'SWIGPATH' : {
      'help'        : 'The list of directories that the scripting language wrapper and interface generate will search for included files',
      'metavar'     : 'PATHS',
      'converter'   : paths2list
  },
}

_groups = {
    'progs' : [ 'SWIG' ],
    'flags' : [ 'SWIGFLAGS', 'SWIGPATH' ]
}

def arguments(**kw):
    """Returns argument declarations for 'swig' tool

       :Keywords:
            include_groups : str | list
                include only arguments assigned to these groups
            exclude_groups : str | list
                exclude arguents assigned to these groups
            swig_include_groups : str | list
                include only arguments assigned to these groups, this has
                higher priority than **include_groups**
            swig_exclude_groups : str | list
                exclude arguents assigned to these groups, this has higher
                priority than **exclude_groups**
    """
    return export_arguments('swig', _all_arguments, _groups, **kw)

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
