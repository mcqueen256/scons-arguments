""" `SConsArgumentsT.cxxTests`

Unit tests for `SConsArguments.c++`
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
import SConsArguments.cxx as tested
from . import TestCase

cplusplus = importlib.import_module('SConsArguments.c++')

#############################################################################
class Test_cxx(TestCase):
    """Test SConsArguments.cxx"""
    def test_arguments_1(self):
        "Test SConsArguments.cxx.arguments()"
        decl = tested.arguments()
        self.assertEqual(decl['CXX']['help'], 'The C++ compiler')
        self.assertEqual(decl['CXX']['metavar'], 'PROG')
        self.assertEqual(decl['SHCXX']['help'], 'The C++ compiler used for generating shared-library objects')
        self.assertEqual(decl['SHCXX']['metavar'], 'PROG')
        self.assertEqual(decl['CXXFLAGS']['help'], 'General options that are passed to the C++ compiler')
        self.assertEqual(decl['CXXFLAGS']['metavar'], 'FLAGS')
        self.assertEqual(decl['CXXFLAGS']['converter'], tested.flags2list)
        self.assertEqual(decl['SHCXXFLAGS']['help'], 'Options that are passed to the C++ compiler to generate shared-library objects')
        self.assertEqual(decl['SHCXXFLAGS']['metavar'], 'FLAGS')
        self.assertEqual(decl['SHCXXFLAGS']['converter'], tested.flags2list)

    def test_arguments__groups_1(self):
        "Test SConsArguments.cxx.arguments() with groups (exclude, include)"
        kws = [
                { 'exclude_groups' : 'progs' },
                { 'include_groups' : 'flags' },
                { 'cxx_exclude_groups' : 'progs', 'exclude_groups' : 'flags' },
                { 'cxx_include_groups' : 'flags', 'include_groups' : 'progs' },
        ]
        for kw in kws:
            decl = tested.arguments(**kw)
            self.assertAllMissing(decl, ['CXX', 'SHCXX'])
            self.assertAllPresent(decl, ['CXXFLAGS', 'SHCXXFLAGS'])

    def test_arguments__groups_2(self):
        "Test SConsArguments.cxx.arguments() with groups (exclude, include)"
        kws = [
                { 'include_groups' : 'progs' },
                { 'exclude_groups' : 'flags' },
                { 'cxx_include_groups' : 'progs', 'include_groups' : 'flags' },
                { 'cxx_exclude_groups' : 'flags', 'exclude_groups' : 'progs' },
        ]
        for kw in kws:
            decl = tested.arguments(**kw)
            self.assertAllPresent(decl, ['CXX', 'SHCXX'])
            self.assertAllMissing(decl, ['CXXFLAGS', 'SHCXXFLAGS'])

#############################################################################
class Test_cplusplus(TestCase):
    """Test SConsArguments.c++"""
    def test_arguments_1(self):
        "Test SConsArguments.c++.arguments()"
        self.assertIs(cplusplus.arguments, tested.arguments)

#############################################################################
if __name__ == "__main__":
    ldr = unittest.TestLoader()
    suite = unittest.TestSuite()
    # Load tests to test suite
    tclasses = [ Test_cxx, Test_cplusplus ]

    for tclass in tclasses:
        suite.addTests(ldr.loadTestsFromTestCase(tclass))

    if not unittest.TextTestRunner(verbosity = 2).run(suite).wasSuccessful():
        sys.exit(1)

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
