""" `SConsArgumentsT.rpcgenTests`

Unit tests for `SConsArguments.rpcgen`
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

import SConsArguments.rpcgen as rpcgen
import unittest
from . import TestCase

#############################################################################
class Test_rpcgen(TestCase):
    """Test SConsArguments.rpcgen"""
    def test_arguments1(self):
        "Test SConsArguments.rpcgen.arguments()"
        decl = rpcgen.arguments()
        self.assertEqual(decl['RPCGEN']['help'], 'The RPC protocol compiler')
        self.assertEqual(decl['RPCGEN']['metavar'], 'PROG')

        self.assertEqual(decl['RPCGENCLIENTFLAGS']['help'], 'Options passed to the RPC protocol compiler when generating client side stubs')
        self.assertEqual(decl['RPCGENCLIENTFLAGS']['metavar'], 'FLAGS')
        self.assertEqual(decl['RPCGENCLIENTFLAGS']['converter'], rpcgen.flags2list)

        self.assertEqual(decl['RPCGENFLAGS']['help'], 'General options passed to the RPC protocol compiler')
        self.assertEqual(decl['RPCGENFLAGS']['metavar'], 'FLAGS')
        self.assertEqual(decl['RPCGENFLAGS']['converter'], rpcgen.flags2list)

        self.assertEqual(decl['RPCGENHEADERFLAGS']['help'], 'Options passed to the RPC protocol compiler when generating a header file')
        self.assertEqual(decl['RPCGENHEADERFLAGS']['metavar'], 'FLAGS')
        self.assertEqual(decl['RPCGENHEADERFLAGS']['converter'], rpcgen.flags2list)

        self.assertEqual(decl['RPCGENSERVICEFLAGS']['help'], 'Options passed to the RPC protocol compiler when generating server side stubs')
        self.assertEqual(decl['RPCGENSERVICEFLAGS']['metavar'], 'FLAGS')
        self.assertEqual(decl['RPCGENSERVICEFLAGS']['converter'], rpcgen.flags2list)

        self.assertEqual(decl['RPCGENXDRFLAGS']['help'], 'Options passed to the RPC protocol compiler when generating XDR routines')
        self.assertEqual(decl['RPCGENXDRFLAGS']['metavar'], 'FLAGS')
        self.assertEqual(decl['RPCGENXDRFLAGS']['converter'], rpcgen.flags2list)

    def test_arguments__groups_1(self):
        "Test SConsArguments.rpcgen.arguments() with groups (exclude, include)"
        kws = [
                { 'exclude_groups' : 'progs' },
                { 'include_groups' : 'flags' },
                { 'rpcgen_exclude_groups' : 'progs', 'exclude_groups' : 'flags' },
                { 'rpcgen_include_groups' : 'flags', 'include_groups' : 'progs' },
        ]
        for kw in kws:
            decl = rpcgen.arguments(**kw)
            self.assertAllMissing(decl, ['RPCGEN' ])
            self.assertAllPresent(decl, ['RPCGENCLIENTFLAGS', 'RPCGENFLAGS', 'RPCGENHEADERFLAGS', 'RPCGENSERVICEFLAGS', 'RPCGENXDRFLAGS'])


    def test_arguments__groups_2(self):
        "Test SConsArguments.rpcgen.arguments() with groups (exclude, include)"
        kws = [
                { 'include_groups' : 'progs' },
                { 'exclude_groups' : 'flags' },
                { 'rpcgen_include_groups' : 'progs', 'include_groups' : 'flags' },
                { 'rpcgen_exclude_groups' : 'flags', 'exclude_groups' : 'progs' },
        ]
        for kw in kws:
            decl = rpcgen.arguments(**kw)
            self.assertAllPresent(decl, ['RPCGEN' ])
            self.assertAllMissing(decl, ['RPCGENCLIENTFLAGS', 'RPCGENFLAGS', 'RPCGENHEADERFLAGS', 'RPCGENSERVICEFLAGS', 'RPCGENXDRFLAGS'])


#############################################################################
if __name__ == "__main__":
    ldr = unittest.TestLoader()
    suite = unittest.TestSuite()
    # Load tests to test suite
    tclasses = [ Test_rpcgen ]

    for tclass in tclasses:
        suite.addTests(ldr.loadTestsFromTestCase(tclass))

    if not unittest.TextTestRunner(verbosity = 2).run(suite).wasSuccessful():
        sys.exit(1)

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
