""" `SConsArgumentsT.dcTests`

Unit tests for `SConsArguments.dc`
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

import SConsArguments.dc as dc
import unittest
from . import TestCase

#############################################################################
class Test_dc(TestCase):
    """Test SConsArguments.dc"""
    def test_arguments1(self):
        "Test SConsArguments.dc.arguments()"
        decl = dc.arguments()
        self.assertEqual(decl['DC']['help'], 'D compiler')
        self.assertEqual(decl['DC']['metavar'], 'PROG')
        self.assertEqual(decl['SHDC']['help'], 'SHDC')
        self.assertEqual(decl['SHDC']['metavar'], 'PROG')
        self.assertEqual(decl['DFLAGS']['help'], 'General options passed to D compiler')
        self.assertEqual(decl['DFLAGS']['metavar'], 'FLAGS')
        self.assertEqual(decl['DFLAGS']['converter'], dc.flags2list)
        self.assertEqual(decl['DPATH']['help'], 'DPATH')
        self.assertEqual(decl['DPATH']['metavar'], 'PATHS')
        self.assertEqual(decl['DPATH']['converter'], dc.paths2list)

    def test_arguments__groups_1(self):
        "Test SConsArguments.dc.arguments() with groups (exclude, include)"
        kws = [
                { 'exclude_groups' : 'progs' },
                { 'include_groups' : 'flags' },
                { 'dc_exclude_groups' : 'progs', 'exclude_groups' : 'flags' },
                { 'dc_include_groups' : 'flags', 'include_groups' : 'progs' },
        ]
        for kw in kws:
            decl = dc.arguments(**kw)
            self.assertAllMissing(decl, ['DC', 'SHDC'])
            self.assertAllPresent(decl, ['DFLAGS', 'DPATH'])

    def test_arguments__groups_2(self):
        "Test SConsArguments.dc.arguments() with groups (exclude, include)"
        kws = [
                { 'include_groups' : 'progs' },
                { 'exclude_groups' : 'flags' },
                { 'dc_include_groups' : 'progs', 'include_groups' : 'flags' },
                { 'dc_exclude_groups' : 'flags', 'exclude_groups' : 'progs' },
        ]
        for kw in kws:
            decl = dc.arguments(**kw)
            self.assertAllPresent(decl, ['DC', 'SHDC'])
            self.assertAllMissing(decl, ['DFLAGS', 'DPATH'])


#############################################################################
if __name__ == "__main__":
    ldr = unittest.TestLoader()
    suite = unittest.TestSuite()
    # Load tests to test suite
    tclasses = [ Test_dc ]

    for tclass in tclasses:
        suite.addTests(ldr.loadTestsFromTestCase(tclass))

    if not unittest.TextTestRunner(verbosity = 2).run(suite).wasSuccessful():
        sys.exit(1)

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
