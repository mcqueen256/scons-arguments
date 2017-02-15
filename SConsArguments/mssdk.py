"""`SConsArguments.mssdk`

Defines arguments related to Microsoft SDK

**Arguments**

Options:
    MSSDK_DIR
        The directory containing the Microsoft SDK

    MSSDK_VERSION
        The version string of the Microsoft SDK (either Platform SDK or Windows
        SDK) to be used for compilation

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

from SConsArguments.Importer import export_arguments

_all_arguments = {
  'MSSDK_DIR' : {
      'help'        : 'The directory containing the Microsoft SDK',
      'metavar'     : 'DIR'
  },
  'MSSDK_VERSION' : {
      'help'        : 'The version string of the Microsoft SDK (either Platform SDK or Windows SDK) to be used for compilation',
      'metavar'     : 'VERSION'
  },
}

_groups = {
    'flags' : [ 'MSSDK_DIR', 'MSSDK_VERSION' ]
}

def arguments(**kw):
    """Returns argument declarations for 'mssdk' tool

       :Keywords:
            include_groups : str | list
                include only arguments assigned to these groups
            exclude_groups : str | list
                exclude arguments assigned to these groups
            mssdk_include_groups : str | list
                include only arguments assigned to these groups, this has
                higher priority than **include_groups**
            mssdk_exclude_groups : str | list
                exclude arguments assigned to these groups, this has higher
                priority than **exclude_groups**
    """
    return export_arguments('mssdk', _all_arguments, _groups, **kw)

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
