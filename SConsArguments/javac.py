"""`SConsArguments.javac`

Defines arguments related to Java compiler

**Arguments**

Programs:
    JAVAC
        The Java compiler

    JAVAH
        The Java generator for C header and stub files

Flags for programs:
    JAVACFLAGS
        General options that are passed to the Java compiler

    JAVACLASSPATH
        Specifies the list of directories that will be searched for Java .class
        file

    JAVASOURCEPATH
        Specifies the list of directories that will be searched for input .java
        file

    JAVAHFLAGS
        General options passed to the C header and stub file generator for Java
        classes
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
  'JAVAC' : {
      'help'        : 'The Java compiler',
      'metavar'     : 'PROG'
  },
  'JAVACFLAGS' : {
      'help'        : 'General options that are passed to the Java compiler',
      'metavar'     : 'FLAGS',
      'converter'   : flags2list
  },
  'JAVACLASSPATH' : {
      'help'        : 'Specifies the list of directories that will be searched for Java .class file',
      'metavar'     : 'PATHS',
      'converter'   : paths2list
  },
  'JAVASOURCEPATH' : {
      'help'        : 'Specifies the list of directories that will be searched for input .java file',
      'metavar'     : 'PATHS',
      'converter'   : paths2list
  },
  'JAVAH' : {
      'help'        : 'The Java generator for C header and stub files',
      'metavar'     : 'PROG'
  },
  'JAVAHFLAGS' : {
      'help'        : 'General options passed to the C header and stub file generator for Java classes',
      'metavar'     : 'FLAGS',
      'converter'   : flags2list
  },
}

_groups = {
    'progs' : [ 'JAVAC', 'JAVAH' ],
    'flags' : [ 'JAVACFLAGS', 'JAVACLASSPATH', 'JAVASOURCEPATH', 'JAVAHFLAGS' ]
}

def arguments(**kw):
    """Returns argument declarations for 'javac' tool

       :Keywords:
            include_groups : str | list
                include only arguments assigned to these groups
            exclude_groups : str | list
                exclude arguments assigned to these groups
            javac_include_groups : str | list
                include only arguments assigned to these groups, this has
                higher priority than **include_groups**
            javac_exclude_groups : str | list
                exclude arguments assigned to these groups, this has higher
                priority than **exclude_groups**
    """
    return export_arguments('javac', _all_arguments, _groups, **kw)

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
