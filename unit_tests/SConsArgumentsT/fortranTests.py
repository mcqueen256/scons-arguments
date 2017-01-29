""" `SConsArgumentsT.fortranTests`

Unit tests for `SConsArguments.fortran`
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

import SConsArguments.fortran as fortran
import unittest
from . import TestCase

#############################################################################
class Test_fortran(TestCase):
    """Test SConsArguments.fortran"""
    def test_arguments1(self):
        "Test SConsArguments.fortran.arguments()"
        decl = fortran.arguments()
        self.assertEqual(decl['FORTRAN']['help'], 'The default Fortran compiler for all versions of Fortran')
        self.assertEqual(decl['FORTRAN']['metavar'], 'PROG')
        self.assertEqual(decl['SHFORTRAN']['help'], 'The default Fortran compiler used for generating shared-library objects')
        self.assertEqual(decl['SHFORTRAN']['metavar'], 'PROG')
        self.assertEqual(decl['FORTRANFLAGS']['help'], 'General user-specified options that are passed to the Fortran compiler')
        self.assertEqual(decl['FORTRANFLAGS']['metavar'], 'FLAGS')
        self.assertEqual(decl['FORTRANFLAGS']['converter'], fortran.flags2list)
        self.assertEqual(decl['FORTRANMODDIR']['help'], 'Directory location where the Fortran compiler should place any module files it generates')
        self.assertEqual(decl['FORTRANMODDIR']['metavar'], 'DIR')
        self.assertEqual(decl['FORTRANPATH']['help'], 'The list of directories that the Fortran compiler will search for include files and (for some compilers) module files')
        self.assertEqual(decl['FORTRANPATH']['metavar'], 'PATHS')
        self.assertEqual(decl['FORTRANPATH']['converter'], fortran.paths2list)
        self.assertEqual(decl['SHFORTRANFLAGS']['help'], 'Options that are passed to the Fortran compiler to generate shared-library objects')
        self.assertEqual(decl['SHFORTRANFLAGS']['metavar'], 'FLAGS')
        self.assertEqual(decl['SHFORTRANFLAGS']['converter'], fortran.flags2list)

    def test_arguments__groups_1(self):
        "Test SConsArguments.fortran.arguments() with groups (exclude, include)"
        kws = [
                { 'exclude_groups' : 'progs' },
                { 'include_groups' : 'flags' },
                { 'fortran_exclude_groups' : 'progs', 'exclude_groups' : 'flags' },
                { 'fortran_include_groups' : 'flags', 'include_groups' : 'progs' },
        ]
        for kw in kws:
            decl = fortran.arguments(**kw)
            self.assertAllMissing(decl, ['FORTRAN', 'SHFORTRAN'])
            self.assertAllPresent(decl, ['FORTRANFLAGS', 'FORTRANMODDIR', 'FORTRANPATH', 'SHFORTRANFLAGS'])

    def test_arguments__groups_2(self):
        "Test SConsArguments.fortran.arguments() with groups (exclude, include)"
        kws = [
                { 'include_groups' : 'progs' },
                { 'exclude_groups' : 'flags' },
                { 'fortran_include_groups' : 'progs', 'include_groups' : 'flags' },
                { 'fortran_exclude_groups' : 'flags', 'exclude_groups' : 'progs' },
        ]
        for kw in kws:
            decl = fortran.arguments(**kw)
            self.assertAllPresent(decl, ['FORTRAN', 'SHFORTRAN'])
            self.assertAllMissing(decl, ['FORTRANFLAGS', 'FORTRANMODDIR', 'FORTRANPATH', 'SHFORTRANFLAGS'])


#############################################################################
if __name__ == "__main__":
    ldr = unittest.TestLoader()
    suite = unittest.TestSuite()
    # Load tests to test suite
    tclasses = [ Test_fortran ]

    for tclass in tclasses:
        suite.addTests(ldr.loadTestsFromTestCase(tclass))

    if not unittest.TextTestRunner(verbosity = 2).run(suite).wasSuccessful():
        sys.exit(1)

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
