""" `SConsArgumentsT.m4Tests`

Unit tests for `SConsArguments.m4`
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

import SConsArguments.m4 as m4
import unittest
from . import TestCase

#############################################################################
class Test_m4(TestCase):
    """Test SConsArguments.m4"""
    def test_arguments1(self):
        "Test SConsArguments.m4.arguments()"
        decl = m4.arguments()
        self.assertEqual(decl['M4']['help'], 'The M4 macro preprocessor')
        self.assertEqual(decl['M4']['metavar'], 'PROG')
        self.assertEqual(decl['M4FLAGS']['help'], 'General options passed to the M4 macro preprocessor')
        self.assertEqual(decl['M4FLAGS']['metavar'], 'FLAGS')
        self.assertEqual(decl['M4FLAGS']['converter'], m4.flags2list)

    def test_arguments__groups_1(self):
        "Test SConsArguments.m4.arguments() with groups (exclude, include)"
        kws = [
                { 'exclude_groups' : 'progs' },
                { 'include_groups' : 'flags' },
                { 'm4_exclude_groups' : 'progs', 'exclude_groups' : 'flags' },
                { 'm4_include_groups' : 'flags', 'include_groups' : 'progs' },
        ]
        for kw in kws:
            decl = m4.arguments(**kw)
            self.assertAllMissing(decl, ['M4' ])
            self.assertAllPresent(decl, ['M4FLAGS'])

    def test_arguments__groups_2(self):
        "Test SConsArguments.m4.arguments() with groups (exclude, include)"
        kws = [
                { 'include_groups' : 'progs' },
                { 'exclude_groups' : 'flags' },
                { 'm4_include_groups' : 'progs', 'include_groups' : 'flags' },
                { 'm4_exclude_groups' : 'flags', 'exclude_groups' : 'progs' },
        ]
        for kw in kws:
            decl = m4.arguments(**kw)
            self.assertAllPresent(decl, ['M4'])
            self.assertAllMissing(decl, ['M4FLAGS'])


#############################################################################
if __name__ == "__main__":
    ldr = unittest.TestLoader()
    suite = unittest.TestSuite()
    # Load tests to test suite
    tclasses = [ Test_m4 ]

    for tclass in tclasses:
        suite.addTests(ldr.loadTestsFromTestCase(tclass))

    if not unittest.TextTestRunner(verbosity = 2).run(suite).wasSuccessful():
        sys.exit(1)

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
