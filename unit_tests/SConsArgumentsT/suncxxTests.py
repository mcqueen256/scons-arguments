""" `SConsArgumentsT.suncxxTests`

Unit tests for `SConsArguments.suncxx`
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

suncxx = importlib.import_module('SConsArguments.sunc++')

#############################################################################
class Test_suncxx(TestCase):
    """Test SConsArguments.suncxx"""
    def test_arguments1(self):
        "Test SConsArguments.suncxx.arguments()"
        decl = suncxx.arguments()
        self.assertEqual(decl['PKGCHK']['help'], 'On Solaris systems, the package-checking program')
        self.assertEqual(decl['PKGCHK']['metavar'], 'PROG')
        self.assertEqual(decl['PKGINFO']['help'], 'On Solaris systems, the package information program')
        self.assertEqual(decl['PKGINFO']['metavar'], 'PROG')

    def test_arguments__groups_1(self):
        "Test SConsArguments.suncxx.arguments() with groups (exclude, include)"
        kws = [
                { 'exclude_groups' : 'progs' },
                { 'suncxx_exclude_groups' : 'progs', 'exclude_groups' : 'flags' },
        ]
        for kw in kws:
            decl = suncxx.arguments(**kw)
            self.assertAllMissing(decl, ['PKGCHK', 'PKGINFO'])

    def test_arguments__groups_2(self):
        "Test SConsArguments.suncxx.arguments() with groups (exclude, include)"
        kws = [
                { 'include_groups' : 'progs' },
                { 'suncxx_include_groups' : 'progs', 'include_groups' : 'flags' },
        ]
        for kw in kws:
            decl = suncxx.arguments(**kw)
            self.assertAllPresent(decl, ['PKGCHK', 'PKGINFO'])


#############################################################################
if __name__ == "__main__":
    ldr = unittest.TestLoader()
    suite = unittest.TestSuite()
    # Load tests to test suite
    tclasses = [ Test_suncxx ]

    for tclass in tclasses:
        suite.addTests(ldr.loadTestsFromTestCase(tclass))

    if not unittest.TextTestRunner(verbosity = 2).run(suite).wasSuccessful():
        sys.exit(1)

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
