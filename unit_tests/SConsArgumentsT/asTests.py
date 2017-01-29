""" `SConsArgumentsT.asTests`

Unit tests for `SConsArguments.as`
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

import unittest
import importlib
from . import TestCase

_as = importlib.import_module('SConsArguments.as')

#############################################################################
class Test_as(TestCase):
    """Test SConsArguments.as"""
    def test_arguments1(self):
        "Test SConsArguments.as.arguments()"
        decl = _as.arguments()
        self.assertEqual(decl['AS']['help'], 'The assembler')
        self.assertEqual(decl['AS']['metavar'], 'PROG')
        self.assertEqual(decl['ASFLAGS']['help'], 'General options passed to the assembler')
        self.assertEqual(decl['ASFLAGS']['metavar'], 'FLAGS')
        self.assertEqual(decl['ASFLAGS']['converter'], _as.flags2list)
        self.assertEqual(decl['ASPPFLAGS']['help'], 'General options when an assembling an assembly-language source file into an object file after first running the file through the C preprocessor')
        self.assertEqual(decl['ASPPFLAGS']['metavar'], 'FLAGS')
        self.assertEqual(decl['ASPPFLAGS']['converter'], _as.flags2list)

    def test_arguments__groups_1(self):
        "Test SConsArguments.as.arguments() with groups (exclude, include)"
        kws = [
            { 'exclude_groups' : 'progs' },
            { 'include_groups' : 'flags' },
            { 'as_exclude_groups' : 'progs', 'exclude_groups' : 'flags' },
            { 'as_include_groups' : 'flags', 'include_groups' : 'progs' }
        ]
        for kw in kws:
            decl = _as.arguments(**kw)
            self.assertAllMissing(decl, ['AS'])
            self.assertAllPresent(decl, ['ASFLAGS', 'ASPPFLAGS'])

    def test_arguments__groups_2(self):
        "Test SConsArguments.as.arguments() with groups (exclude, include)"
        kws = [
            { 'exclude_groups' : 'flags' },
            { 'include_groups' : 'progs' },
            { 'as_exclude_groups' : 'flags', 'exclude_groups' : 'progs' },
            { 'as_include_groups' : 'progs', 'include_groups' : 'flags' }
        ]
        for kw in kws:
            decl = _as.arguments(**kw)
            self.assertAllPresent(decl, ['AS'])
            self.assertAllMissing(decl, ['ASFLAGS', 'ASPPFLAGS'])


#############################################################################
if __name__ == "__main__":
    ldr = unittest.TestLoader()
    suite = unittest.TestSuite()
    # Load tests to test suite
    tclasses = [ Test_as ]

    for tclass in tclasses:
        suite.addTests(ldr.loadTestsFromTestCase(tclass))

    if not unittest.TextTestRunner(verbosity = 2).run(suite).wasSuccessful():
        sys.exit(1)

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
