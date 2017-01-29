""" `SConsArgumentsT.f90Tests`

Unit tests for `SConsArguments.f90`
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

import SConsArguments.f90 as f90
import unittest
from . import TestCase

#############################################################################
class Test_f90(TestCase):
    """Test SConsArguments.f90"""
    def test_arguments1(self):
        "Test SConsArguments.f90.arguments()"
        decl = f90.arguments()
        self.assertEqual(decl['F90']['help'], 'The Fortran 90 compiler')
        self.assertEqual(decl['F90']['metavar'], 'PROG')
        self.assertEqual(decl['SHF90']['help'], 'The Fortran 90 compiler used for generating shared-library objects')
        self.assertEqual(decl['SHF90']['metavar'], 'PROG')
        self.assertEqual(decl['F90FLAGS']['help'], 'General user-specified options that are passed to the Fortran 90 compiler')
        self.assertEqual(decl['F90FLAGS']['metavar'], 'FLAGS')
        self.assertEqual(decl['F90FLAGS']['converter'], f90.flags2list)
        self.assertEqual(decl['F90PATH']['help'], 'The list of directories that the Fortran 90 compiler will search for include directories')
        self.assertEqual(decl['F90PATH']['metavar'], 'PATHS')
        self.assertEqual(decl['F90PATH']['converter'], f90.paths2list)
        self.assertEqual(decl['SHF90FLAGS']['help'], 'Options that are passed to the Fortran 90 compiler to generated shared-library objects')
        self.assertEqual(decl['SHF90FLAGS']['metavar'], 'FLAGS')
        self.assertEqual(decl['SHF90FLAGS']['converter'], f90.flags2list)

    def test_arguments__groups_1(self):
        "Test SConsArguments.f90.arguments() with groups (exclude, include)"
        kws = [
                { 'exclude_groups' : 'progs' },
                { 'include_groups' : 'flags' },
                { 'f90_exclude_groups' : 'progs', 'exclude_groups' : 'flags' },
                { 'f90_include_groups' : 'flags', 'include_groups' : 'progs' },
        ]
        for kw in kws:
            decl = f90.arguments(**kw)
            self.assertAllMissing(decl, ['F90', 'SHF90'])
            self.assertAllPresent(decl, ['F90FLAGS', 'F90PATH', 'SHF90FLAGS'])

    def test_arguments__groups_2(self):
        "Test SConsArguments.f90.arguments() with groups (exclude, include)"
        kws = [
                { 'include_groups' : 'progs' },
                { 'exclude_groups' : 'flags' },
                { 'f90_include_groups' : 'progs', 'include_groups' : 'flags' },
                { 'f90_exclude_groups' : 'flags', 'exclude_groups' : 'progs' },
        ]
        for kw in kws:
            decl = f90.arguments(**kw)
            self.assertAllPresent(decl, ['F90', 'SHF90'])
            self.assertAllMissing(decl, ['F90FLAGS', 'F90PATH', 'SHF90FLAGS'])


#############################################################################
if __name__ == "__main__":
    ldr = unittest.TestLoader()
    suite = unittest.TestSuite()
    # Load tests to test suite
    tclasses = [ Test_f90 ]

    for tclass in tclasses:
        suite.addTests(ldr.loadTestsFromTestCase(tclass))

    if not unittest.TextTestRunner(verbosity = 2).run(suite).wasSuccessful():
        sys.exit(1)

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
