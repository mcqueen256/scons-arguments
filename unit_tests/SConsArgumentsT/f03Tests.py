""" `SConsArgumentsT.f03Tests`

Unit tests for `SConsArguments.f03`
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

import SConsArguments.f03 as f03
import unittest
from . import TestCase

#############################################################################
class Test_f03(TestCase):
    """Test SConsArguments.f03"""
    def test_arguments1(self):
        "Test SConsArguments.f03.arguments()"
        decl = f03.arguments()
        self.assertEqual(decl['F03']['help'], 'The Fortran 03 compiler')
        self.assertEqual(decl['F03']['metavar'], 'PROG')
        self.assertEqual(decl['SHF03']['help'], 'The Fortran 03 compiler used for generating shared-library objects')
        self.assertEqual(decl['SHF03']['metavar'], 'PROG')
        self.assertEqual(decl['F03FLAGS']['help'], 'General user-specified options that are passed to the Fortran 03 compiler')
        self.assertEqual(decl['F03FLAGS']['metavar'], 'FLAGS')
        self.assertEqual(decl['F03FLAGS']['converter'], f03.flags2list)
        self.assertEqual(decl['F03PATH']['help'], 'The list of directories that the Fortran 03 compiler will search for include directories')
        self.assertEqual(decl['F03PATH']['metavar'], 'PATHS')
        self.assertEqual(decl['F03PATH']['converter'], f03.paths2list)
        self.assertEqual(decl['SHF03FLAGS']['help'], 'Options that are passed to the Fortran 03 compiler to generated shared-library objects')
        self.assertEqual(decl['SHF03FLAGS']['metavar'], 'FLAGS')
        self.assertEqual(decl['SHF03FLAGS']['converter'], f03.flags2list)

    def test_arguments__groups_1(self):
        "Test SConsArguments.f03.arguments() with groups (exclude, include)"
        kws = [
                { 'exclude_groups' : 'progs' },
                { 'include_groups' : 'flags' },
                { 'f03_exclude_groups' : 'progs', 'exclude_groups' : 'flags' },
                { 'f03_include_groups' : 'flags', 'include_groups' : 'progs' },
        ]
        for kw in kws:
            decl = f03.arguments(**kw)
            self.assertAllMissing(decl, ['F03', 'SHF03'])
            self.assertAllPresent(decl, ['F03FLAGS', 'F03PATH', 'SHF03FLAGS'])

    def test_arguments__groups_2(self):
        "Test SConsArguments.f03.arguments() with groups (exclude, include)"
        kws = [
                { 'include_groups' : 'progs' },
                { 'exclude_groups' : 'flags' },
                { 'f03_include_groups' : 'progs', 'include_groups' : 'flags' },
                { 'f03_exclude_groups' : 'flags', 'exclude_groups' : 'progs' },
        ]
        for kw in kws:
            decl = f03.arguments(**kw)
            self.assertAllPresent(decl, ['F03', 'SHF03'])
            self.assertAllMissing(decl, ['F03FLAGS', 'F03PATH', 'SHF03FLAGS'])


#############################################################################
if __name__ == "__main__":
    ldr = unittest.TestLoader()
    suite = unittest.TestSuite()
    # Load tests to test suite
    tclasses = [ Test_f03 ]

    for tclass in tclasses:
        suite.addTests(ldr.loadTestsFromTestCase(tclass))

    if not unittest.TextTestRunner(verbosity = 2).run(suite).wasSuccessful():
        sys.exit(1)

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
