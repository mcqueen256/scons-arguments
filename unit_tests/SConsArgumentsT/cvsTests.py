""" `SConsArgumentsTestsT.cvsTests`

Unit tests for `SConsArguments.cvs`
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

import SConsArguments.cvs as cvs
import unittest
from . import TestCase

#############################################################################
class Test_cvs(TestCase):
    """Test SConsArguments.cvs"""
    def test_arguments1(self):
        "Test SConsArguments.cvs.arguments()"
        decl = cvs.arguments()
        self.assertEqual(decl['CVS']['help'], 'The CVS executable')
        self.assertEqual(decl['CVS']['metavar'], 'PROG')

        self.assertEqual(decl['CVSCOFLAGS']['help'], 'Options that are passed to the CVS checkout subcommand')
        self.assertEqual(decl['CVSCOFLAGS']['metavar'], 'FLAGS')
        self.assertEqual(decl['CVSCOFLAGS']['converter'], cvs.flags2list)

        self.assertEqual(decl['CVSFLAGS']['help'], 'General options that are passed to CVS')
        self.assertEqual(decl['CVSFLAGS']['metavar'], 'FLAGS')
        self.assertEqual(decl['CVSFLAGS']['converter'], cvs.flags2list)

    def test_arguments__group_1(self):
        "Test SConsArguments.cvs.arguments(exclude_progs = True)"
        kws = [
                { 'exclude_groups' : 'progs' },
                { 'include_groups' : 'flags' },
                { 'cvs_exclude_groups' : 'progs', 'exclude_groups' : 'flags' },
                { 'cvs_include_groups' : 'flags', 'include_groups' : 'progs' },
        ]
        for kw in kws:
            decl = cvs.arguments(**kw)
            self.assertAllMissing(decl, ['CVS'])
            self.assertAllPresent(decl, ['CVSCOFLAGS', 'CVSFLAGS'])

    def test_arguments__group_2(self):
        "Test SConsArguments.cvs.arguments(exclude_progs = True)"
        kws = [
                { 'include_groups' : 'progs' },
                { 'exclude_groups' : 'flags' },
                { 'cvs_include_groups' : 'progs', 'include_groups' : 'flags' },
                { 'cvs_exclude_groups' : 'flags', 'exclude_groups' : 'progs' },
        ]
        for kw in kws:
            decl = cvs.arguments(**kw)
            self.assertAllPresent(decl, ['CVS'])
            self.assertAllMissing(decl, ['CVSCOFLAGS', 'CVSFLAGS'])

#############################################################################
if __name__ == "__main__":
    ldr = unittest.TestLoader()
    suite = unittest.TestSuite()
    # Load tests to test suite
    tclasses = [ Test_cvs ]

    for tclass in tclasses:
        suite.addTests(ldr.loadTestsFromTestCase(tclass))

    if not unittest.TextTestRunner(verbosity = 2).run(suite).wasSuccessful():
        sys.exit(1)

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
