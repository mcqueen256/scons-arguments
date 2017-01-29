""" `SConsArgumentsT.perforceTests`

Unit tests for `SConsArguments.perforce`
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

import SConsArguments.perforce as perforce
import unittest
from . import TestCase

#############################################################################
class Test_perforce(TestCase):
    """Test SConsArguments.perforce"""
    def test_arguments1(self):
        "Test SConsArguments.perforce.arguments()"
        decl = perforce.arguments()
        self.assertEqual(decl['P4']['help'], 'The Perforce executable')
        self.assertEqual(decl['P4']['metavar'], 'PROG')

        self.assertEqual(decl['P4FLAGS']['help'], 'General options that are passed to Perforce')
        self.assertEqual(decl['P4FLAGS']['metavar'], 'FLAGS')
        self.assertEqual(decl['P4FLAGS']['converter'], perforce.flags2list)

    def test_arguments__groups_1(self):
        "Test SConsArguments.perforce.arguments() with groups (exclude, include)"
        kws = [
                { 'exclude_groups' : 'progs' },
                { 'include_groups' : 'flags' },
                { 'perforce_exclude_groups' : 'progs', 'exclude_groups' : 'flags' },
                { 'perforce_include_groups' : 'flags', 'include_groups' : 'progs' },
        ]
        for kw in kws:
            decl = perforce.arguments(**kw)
            self.assertAllMissing(decl, ['P4' ])
            self.assertAllPresent(decl, ['P4FLAGS'])

    def test_arguments__groups_2(self):
        "Test SConsArguments.perforce.arguments() with groups (exclude, include)"
        kws = [
                { 'include_groups' : 'progs' },
                { 'exclude_groups' : 'flags' },
                { 'perforce_include_groups' : 'progs', 'include_groups' : 'flags' },
                { 'perforce_exclude_groups' : 'flags', 'exclude_groups' : 'progs' },
        ]
        for kw in kws:
            decl = perforce.arguments(**kw)
            self.assertAllPresent(decl, ['P4'])
            self.assertAllMissing(decl, ['P4FLAGS'])


#############################################################################
if __name__ == "__main__":
    ldr = unittest.TestLoader()
    suite = unittest.TestSuite()
    # Load tests to test suite
    tclasses = [ Test_perforce ]

    for tclass in tclasses:
        suite.addTests(ldr.loadTestsFromTestCase(tclass))

    if not unittest.TextTestRunner(verbosity = 2).run(suite).wasSuccessful():
        sys.exit(1)

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
