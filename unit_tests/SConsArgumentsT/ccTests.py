""" `SConsArgumentsTestsT.ccTests`

Unit tests for `SConsArguments.cc`
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

import SConsArguments.cc as cc
import unittest
from . import TestCase

#############################################################################
class Test_cc(TestCase):
    """Test SConsArguments.ar"""
    def test_arguments1(self):
        "Test SConsArguments.cc.arguments()"
        decl = cc.arguments()
        self.assertEqual(decl['CC']['help'], 'The C compiler')
        self.assertEqual(decl['CC']['metavar'], 'PROG')
        self.assertEqual(decl['SHCC']['help'], 'The C compiler used for generating shared-library objects')
        self.assertEqual(decl['SHCC']['metavar'], 'PROG')

        self.assertEqual(decl['CCFLAGS']['help'], 'General options that are passed to the C and C++ compilers')
        self.assertEqual(decl['CCFLAGS']['metavar'], 'FLAGS')
        self.assertEqual(decl['CCFLAGS']['converter'], cc.flags2list)

        self.assertEqual(decl['CCPCHFLAGS']['help'], 'Options added to the compiler command line to support building with precompiled headers')
        self.assertEqual(decl['CCPCHFLAGS']['metavar'], 'FLAGS')
        self.assertEqual(decl['CCPCHFLAGS']['converter'], cc.flags2list)

        self.assertEqual(decl['CCPDBFLAGS']['help'], 'Options added to the compiler command line to support storing debugging information in a Microsoft Visual C++ PDB file')
        self.assertEqual(decl['CCPDBFLAGS']['metavar'], 'FLAGS')
        self.assertEqual(decl['CCPDBFLAGS']['converter'], cc.flags2list)

        self.assertEqual(decl['CFLAGS']['help'], 'General options that are passed to the C compiler (C only; not C++).')
        self.assertEqual(decl['CFLAGS']['metavar'], 'FLAGS')
        self.assertEqual(decl['CFLAGS']['converter'], cc.flags2list)

        self.assertEqual(decl['CPPDEFINES']['help'], 'A platform independent specification of C preprocessor definitions')
        self.assertEqual(decl['CPPDEFINES']['metavar'], 'DEFS')
        self.assertEqual(decl['CPPDEFINES']['converter'], cc.cdefs2list)

        self.assertEqual(decl['CPPFLAGS']['help'], 'User-specified C preprocessor options')
        self.assertEqual(decl['CPPFLAGS']['metavar'], 'FLAGS')
        self.assertEqual(decl['CPPFLAGS']['converter'], cc.flags2list)

        self.assertEqual(decl['CPPPATH']['help'], 'The list of directories that the C preprocessor will search for include directories')
        self.assertEqual(decl['CPPPATH']['metavar'], 'PATHS')
        self.assertEqual(decl['CPPPATH']['converter'], cc.paths2list)

        self.assertEqual(decl['SHCCFLAGS']['help'], 'Options that are passed to the C and C++ compilers to generate shared-library objects')
        self.assertEqual(decl['SHCCFLAGS']['metavar'], 'FLAGS')
        self.assertEqual(decl['SHCCFLAGS']['converter'], cc.flags2list)

        self.assertEqual(decl['SHCFLAGS']['help'], 'Options that are passed to the C compiler (only; not C++) to generate shared-library objects')
        self.assertEqual(decl['SHCFLAGS']['metavar'], 'FLAGS')
        self.assertEqual(decl['SHCFLAGS']['converter'], cc.flags2list)

    def test_arguments__groups_1(self):
        "Test SConsArguments.cc.arguments() with groups (exclude, include)"
        kws = [
                { 'exclude_groups' : 'progs' },
                { 'include_groups' : 'flags' },
                { 'cc_exclude_groups' : 'progs', 'exclude_groups' : 'flags' },
                { 'cc_include_groups' : 'flags', 'include_groups' : 'progs' },
        ]
        for kw in kws:
            decl = cc.arguments(**kw)
            self.assertAllMissing(decl, [ 'CC', 'SHCC' ])
            self.assertAllPresent(decl, [ 'CCFLAGS', 'CCPCHFLAGS', 'CCPDBFLAGS',
                                          'CFLAGS', 'CPPDEFINES', 'CPPFLAGS',
                                          'CPPPATH', 'SHCCFLAGS', 'SHCFLAGS' ])

    def test_arguments__groups_2(self):
        "Test SConsArguments.cc.arguments() with groups (exclude, include)"
        kws = [
                { 'include_groups' : 'progs' },
                { 'exclude_groups' : 'flags' },
                { 'cc_include_groups' : 'progs', 'include_groups' : 'flags' },
                { 'cc_exclude_groups' : 'flags', 'exclude_groups' : 'progs' },
        ]
        for kw in kws:
            decl = cc.arguments(**kw)
            self.assertAllPresent(decl, [ 'CC', 'SHCC' ])
            self.assertAllMissing(decl, [ 'CCFLAGS', 'CCPCHFLAGS', 'CCPDBFLAGS',
                                          'CFLAGS', 'CPPDEFINES', 'CPPFLAGS',
                                          'CPPPATH', 'SHCCFLAGS', 'SHCFLAGS' ])



#############################################################################
if __name__ == "__main__":
    ldr = unittest.TestLoader()
    suite = unittest.TestSuite()
    # Load tests to test suite
    tclasses = [ Test_cc ]

    for tclass in tclasses:
        suite.addTests(ldr.loadTestsFromTestCase(tclass))

    if not unittest.TextTestRunner(verbosity = 2).run(suite).wasSuccessful():
        sys.exit(1)

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
