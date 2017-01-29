""" `SConsArgumentsT.linkTests`

Unit tests for `SConsArguments.link`
"""

__docformat__ = "restructuredText"

#
# Copyright (c) 2015 by Pawel Tomulik
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

import SConsArguments.link as link
import unittest
from . import TestCase

#############################################################################
class Test_link(TestCase):
    """Test SConsArguments.link"""
    def test_arguments1(self):
        "Test SConsArguments.link.arguments()"
        decl = link.arguments()
        self.assertEqual(decl['LDMODULE']['help'], 'The linker for building loadable modules')
        self.assertEqual(decl['LDMODULE']['metavar'], 'PROG')

        self.assertEqual(decl['LDMODULEFLAGS']['help'], 'General user options passed to the linker for building loadable modules')
        self.assertEqual(decl['LDMODULEFLAGS']['metavar'], 'FLAGS')
        self.assertEqual(decl['LDMODULEFLAGS']['converter'], link.flags2list)

        self.assertEqual(decl['LIBPATH']['help'], 'The list of directories that will be searched for libraries')
        self.assertEqual(decl['LIBPATH']['metavar'], 'PATHS')
        self.assertEqual(decl['LIBPATH']['converter'], link.paths2list)

        self.assertEqual(decl['LINK']['help'], 'The linker')
        self.assertEqual(decl['LINK']['metavar'], 'PROG')

        self.assertEqual(decl['LINKFLAGS']['help'], 'General user options passed to the linker')
        self.assertEqual(decl['LINKFLAGS']['metavar'], 'FLAGS')
        self.assertEqual(decl['LINKFLAGS']['converter'], link.flags2list)

        self.assertEqual(decl['SHLIBVERSIONFLAGS']['help'], 'Extra flags added to $SHLINKCOM when building versioned SharedLibrary')
        self.assertEqual(decl['SHLIBVERSIONFLAGS']['metavar'], 'FLAGS')
        self.assertEqual(decl['SHLIBVERSIONFLAGS']['converter'], link.flags2list)

        self.assertEqual(decl['SHLINK']['help'], 'The linker for programs that use shared libraries')
        self.assertEqual(decl['SHLINK']['metavar'], 'PROG')

        self.assertEqual(decl['SHLINKFLAGS']['help'], 'General user options passed to the linker for programs using shared libraries')
        self.assertEqual(decl['SHLINKFLAGS']['metavar'], 'FLAGS')
        self.assertEqual(decl['SHLINKFLAGS']['converter'], link.flags2list)


    def test_arguments__groups_1(self):
        "Test SConsArguments.link.arguments() with groups (exclude, include)"
        kws = [
                { 'exclude_groups' : 'progs' },
                { 'include_groups' : 'flags' },
                { 'link_exclude_groups' : 'progs', 'exclude_groups' : 'flags' },
                { 'link_include_groups' : 'flags', 'include_groups' : 'progs' },
        ]
        for kw in kws:
            decl = link.arguments(**kw)
            self.assertAllMissing(decl, ['LDMODULE', 'LINK', 'SHLINK'])
            self.assertAllPresent(decl, ['LDMODULEFLAGS', 'LIBPATH', 'LINKFLAGS', 'SHLIBVERSIONFLAGS', 'SHLINKFLAGS'])

    def test_arguments__groups_2(self):
        "Test SConsArguments.link.arguments() with groups (exclude, include)"
        kws = [
                { 'include_groups' : 'progs' },
                { 'exclude_groups' : 'flags' },
                { 'link_include_groups' : 'progs', 'include_groups' : 'flags' },
                { 'link_exclude_groups' : 'flags', 'exclude_groups' : 'progs' },
        ]
        for kw in kws:
            decl = link.arguments(**kw)
            self.assertAllPresent(decl, ['LDMODULE', 'LINK', 'SHLINK'])
            self.assertAllMissing(decl, ['LDMODULEFLAGS', 'LIBPATH', 'LINKFLAGS', 'SHLIBVERSIONFLAGS', 'SHLINKFLAGS'])


#############################################################################
if __name__ == "__main__":
    ldr = unittest.TestLoader()
    suite = unittest.TestSuite()
    # Load tests to test suite
    tclasses = [ Test_link ]

    for tclass in tclasses:
        suite.addTests(ldr.loadTestsFromTestCase(tclass))

    if not unittest.TextTestRunner(verbosity = 2).run(suite).wasSuccessful():
        sys.exit(1)

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
