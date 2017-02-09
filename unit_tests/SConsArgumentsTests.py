""" SConsArgumentsTests

Unit tests for SConsArguments
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

import SConsArguments
import SConsArguments.Util
import SConsArguments.NameConv
import SConsArguments.Proxy
import SConsArguments.Arguments
import SConsArguments.VariablesWrapper
import SConsArguments.Declaration
import SConsArguments.Declarations
import unittest

#############################################################################
class Test_module_imports(unittest.TestCase):
    """Test constants in SConsArguments module"""
    def test__ArgumentDeclaration(self):
        "Test SConsArguments._ArgumentDeclaration, should be SConsArguments.Declaration._ArgumentDeclaration"
        self.assertIs(SConsArguments._ArgumentDeclaration,SConsArguments.Declaration._ArgumentDeclaration)
    def test_ArgumentDeclaration(self):
        "Test SConsArguments.ArgumentDeclaration, should be SConsArguments.Declaration.ArgumentDeclaration"
        self.assertIs(SConsArguments.ArgumentDeclaration,SConsArguments.Declaration.ArgumentDeclaration)
    def test_DeclareArgument(self):
        "Test SConsArguments.DeclareArgument, should be SConsArguments.Declaration.DeclareArgument"
        self.assertIs(SConsArguments.DeclareArgument,SConsArguments.Declaration.DeclareArgument)
    def test__ArgumentDeclarations(self):
        "Test SConsArguments._ArgumentDeclarations, should be SConsArguments.Declarations._ArgumentDeclarations"
        self.assertIs(SConsArguments._ArgumentDeclarations,SConsArguments.Declarations._ArgumentDeclarations)
    def test_ArgumentDeclarations(self):
        "Test SConsArguments.ArgumentDeclarations, should be SConsArguments.Declarations.ArgumentDeclarations"
        self.assertIs(SConsArguments.ArgumentDeclarations,SConsArguments.Declarations.ArgumentDeclarations)
    def test_DeclareArguments(self):
        "Test SConsArguments.DeclareArguments, should be SConsArguments.Declarations.DeclareArguments"
        self.assertIs(SConsArguments.DeclareArguments,SConsArguments.Declarations.DeclareArguments)
    def test__Arguments(self):
        "Test SConsArguments._Arguments, should be SConsArguments.Arguments._Arguments"
        self.assertIs(SConsArguments._Arguments,SConsArguments.Arguments._Arguments)
    def test__ArgumentsProxy(self):
        "Test SConsArguments._ArgumentsProxy, should be SConsArguments.Proxy._ArgumentsProxy"
        self.assertIs(SConsArguments._ArgumentsProxy,SConsArguments.Proxy._ArgumentsProxy)
    def test__ArgumentNameConv(self):
        "Test SConsArguments._ArgumentNameConv, should be SConsArguments.NameConv._ArgumentNameConv"
        self.assertIs(SConsArguments._ArgumentNameConv,SConsArguments.NameConv._ArgumentNameConv)
    def test_ArgumentDeclarations(self):
        "Test SConsArguments.ArgumentDeclarations, should be SConsArguments.Declarations.ArgumentDeclarations"
        self.assertIs(SConsArguments.ArgumentDeclarations,SConsArguments.Declarations.ArgumentDeclarations)
    def test_ENV(self):
        "Test SConsArguments.ENV, should be SConsArguments.Util.ENV"
        self.assertIs(SConsArguments.ENV,SConsArguments.Util.ENV)
    def test_VAR(self):
        "Test SConsArguments.VAR, should be SConsArguments.Util.VAR"
        self.assertIs(SConsArguments.VAR,SConsArguments.Util.VAR)
    def test_OPT(self):
        "Test SConsArguments.OPT, should be SConsArguments.Util.OPT"
        self.assertIs(SConsArguments.OPT,SConsArguments.Util.OPT)
    def test_ALL(self):
        "Test SConsArguments.ALL, should be SConsArguments.Util.ALL"
        self.assertIs(SConsArguments.ALL,SConsArguments.Util.ALL)
    def test__missing(self):
        "Test SConsArguments._missing, should be SConsArguments.Util._missing"
        self.assertIs(SConsArguments._missing,SConsArguments.Util._missing)
    def test_MISSING(self):
        "Test SConsArguments.MISSING, should be SConsArguments.Util.MISSING"
        self.assertIs(SConsArguments.MISSING,SConsArguments.Util.MISSING)
    def test__undef(self):
        "Test SConsArguments._undef, should be SConsArguments.Util._undef"
        self.assertIs(SConsArguments._undef,SConsArguments.Util._undef)
    def test_UNDEFINED(self):
        "Test SConsArguments.UNDEFINED, should be SConsArguments.Util.UNDEFINED"
        self.assertIs(SConsArguments.UNDEFINED,SConsArguments.Util.UNDEFINED)
    def test__notfound(self):
        "Test SConsArguments._notfound, should be SConsArguments.Util._notfound"
        self.assertIs(SConsArguments._notfound,SConsArguments.Util._notfound)
    def test_NOTFOUND(self):
        "Test SConsArguments.NOTFOUND, should be SConsArguments.Util.NOTFOUND"
        self.assertIs(SConsArguments.NOTFOUND,SConsArguments.Util.NOTFOUND)
    def test__resubst(self):
        "Test SConsArguments._resubst, should be SConsArguments.Util._resubst"
        self.assertIs(SConsArguments._resubst,SConsArguments.Util._resubst)
    def test__build_resubst_dict(self):
        "Test SConsArguments._build_resubst_dict, should be SConsArguments.Util._build_resubst_dict"
        self.assertIs(SConsArguments._build_resubst_dict,SConsArguments.Util._build_resubst_dict)
    def test__build_iresubst_dict(self):
        "Test SConsArguments._build_iresubst_dict, should be SConsArguments.Util._build_iresubst_dict"
        self.assertIs(SConsArguments._build_iresubst_dict,SConsArguments.Util._build_iresubst_dict)
    def test__compose_mappings(self):
        "Test SConsArguments._compose_mappings, should be SConsArguments.Util._compose_mappings"
        self.assertIs(SConsArguments._compose_mappings,SConsArguments.Util._compose_mappings)
    def test__invert_dict(self):
        "Test SConsArguments._invert_dict, should be SConsArguments.Util._invert_dict"
        self.assertIs(SConsArguments._invert_dict,SConsArguments.Util._invert_dict)
    def test_VariablesWrapper(self):
        "Test SConsArguments._VariablesWrapper, should be SConsArguments.VariablesWrapper._VariablesWrapper"
        self.assertIs(SConsArguments._VariablesWrapper,SConsArguments.VariablesWrapper._VariablesWrapper)
    def test_ImportArguments(self):
        "Test SConsArguments._ImportArguments, should be SConsArguments.Importer.ImportArguments"
        self.assertIs(SConsArguments.ImportArguments,SConsArguments.Importer.ImportArguments)

#############################################################################
if __name__ == "__main__":
    ldr = unittest.TestLoader()
    suite = unittest.TestSuite()
    # Load tests to test suite
    tclasses = [ Test_module_imports
               ]

    for tclass in tclasses:
        suite.addTests(ldr.loadTestsFromTestCase(tclass))

    if not unittest.TextTestRunner(verbosity = 2).run(suite).wasSuccessful():
        sys.exit(1)

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
