""" `SConsArgumentsT.f77Tests`

Unit tests for `SConsArguments.f77`
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

import SConsArguments.f77 as f77
import unittest
from . import TestCase

#############################################################################
class Test_f77(TestCase):
    """Test SConsArguments.f77"""
    def test_arguments1(self):
        "Test SConsArguments.f77.arguments()"
        decl = f77.arguments()
        self.assertEqual(decl['F77']['help'], 'The Fortran 77 compiler')
        self.assertEqual(decl['F77']['metavar'], 'PROG')
        self.assertEqual(decl['SHF77']['help'], 'The Fortran 77 compiler used for generating shared-library objects')
        self.assertEqual(decl['SHF77']['metavar'], 'PROG')
        self.assertEqual(decl['F77FLAGS']['help'], 'General user-specified options that are passed to the Fortran 77 compiler')
        self.assertEqual(decl['F77FLAGS']['metavar'], 'FLAGS')
        self.assertEqual(decl['F77FLAGS']['converter'], f77.flags2list)
        self.assertEqual(decl['F77PATH']['help'], 'The list of directories that the Fortran 77 compiler will search for include directories')
        self.assertEqual(decl['F77PATH']['metavar'], 'PATHS')
        self.assertEqual(decl['F77PATH']['converter'], f77.paths2list)
        self.assertEqual(decl['SHF77FLAGS']['help'], 'Options that are passed to the Fortran 77 compiler to generated shared-library objects')
        self.assertEqual(decl['SHF77FLAGS']['metavar'], 'FLAGS')
        self.assertEqual(decl['SHF77FLAGS']['converter'], f77.flags2list)

    def test_arguments__groups_1(self):
        "Test SConsArguments.f77.arguments() with groups (exclude, include)"
        kws = [
                { 'exclude_groups' : 'progs' },
                { 'include_groups' : 'flags' },
                { 'f77_exclude_groups' : 'progs', 'exclude_groups' : 'flags' },
                { 'f77_include_groups' : 'flags', 'include_groups' : 'progs' },
        ]
        for kw in kws:
            decl = f77.arguments(**kw)
            self.assertAllMissing(decl, ['F77', 'SHF77'])
            self.assertAllPresent(decl, ['F77FLAGS', 'F77PATH', 'SHF77FLAGS'])

    def test_arguments__groups_2(self):
        "Test SConsArguments.f77.arguments() with groups (exclude, include)"
        kws = [
                { 'include_groups' : 'progs' },
                { 'exclude_groups' : 'flags' },
                { 'f77_include_groups' : 'progs', 'include_groups' : 'flags' },
                { 'f77_exclude_groups' : 'flags', 'exclude_groups' : 'progs' },
        ]
        for kw in kws:
            decl = f77.arguments(**kw)
            self.assertAllPresent(decl, ['F77', 'SHF77'])
            self.assertAllMissing(decl, ['F77FLAGS', 'F77PATH', 'SHF77FLAGS'])


#############################################################################
if __name__ == "__main__":
    ldr = unittest.TestLoader()
    suite = unittest.TestSuite()
    # Load tests to test suite
    tclasses = [ Test_f77 ]

    for tclass in tclasses:
        suite.addTests(ldr.loadTestsFromTestCase(tclass))

    if not unittest.TextTestRunner(verbosity = 2).run(suite).wasSuccessful():
        sys.exit(1)

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
