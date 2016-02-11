""" SConsGnuArguments.UtilTests

Unit tests for SConsGnuArguments.Util
"""

__docformat__ = "restructuredText"

#
# Copyright (c) 2016 by Pawel Tomulik
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

import SConsArguments.Util
import unittest

#############################################################################
class Test_module_constants(unittest.TestCase):
    """Test global variables"""
    def test_ENV(self):
        """Test 'Util.ENV'"""
        self.assertEqual(SConsArguments.Util.ENV,0)
    def test_VAR(self):
        """Test 'Util.VAR'"""
        self.assertEqual(SConsArguments.Util.VAR,1)
    def test_OPT(self):
        """Test 'Util.OPT'"""
        self.assertEqual(SConsArguments.Util.OPT,2)
    def test_ALL(self):
        """Test 'Util.ALL'"""
        self.assertEqual(SConsArguments.Util.ALL,3)
    def test_MISSING(self):
        """Test 'Util.MISSING'"""
        self.assertIs(SConsArguments.Util.MISSING, SConsArguments.Util._missing)
    def test_UNDEFINED(self):
        """Test 'Util.UNDEFINED'"""
        self.assertIs(SConsArguments.Util.UNDEFINED, SConsArguments.Util._undef)
    def test_NOTFOUND(self):
        """Test 'Util.NOTFOUND'"""
        self.assertIs(SConsArguments.Util.NOTFOUND, SConsArguments.Util._notfound)
    def test__missing(self):
        "Test SConsArguments.Util._missing, it should be a class with certain characteristics"
        self.assertTrue(isinstance(SConsArguments.Util._missing,type))
        self.assertFalse(bool(SConsArguments.Util._missing))
        self.assertEqual(str(SConsArguments.Util._missing), 'MISSING')
    def test_MISSING(self):
        "Test SConsArguments.Util.MISSING, it should be same as SConsArguments.Util._missing"
        self.assertTrue(isinstance(SConsArguments.Util.MISSING,type))
        self.assertIs(SConsArguments.Util.MISSING, SConsArguments.Util._missing)
    def test__undef(self):
        "Test SConsArguments.Util._undef, it should be a class with certain characteristics"
        self.assertTrue(isinstance(SConsArguments.Util._undef,type))
        self.assertFalse(bool(SConsArguments.Util._undef))
        self.assertEqual(str(SConsArguments.Util._undef), 'UNDEFINED')
    def test_UNDEFINED(self):
        "Test SConsArguments.Util.UNDEFINED, it should be a class"
        self.assertTrue(isinstance(SConsArguments.Util.UNDEFINED,type))
        self.assertIs(SConsArguments.Util.UNDEFINED, SConsArguments.Util._undef)
    def test__notfound(self):
        "Test SConsArguments.Util._notfound, it should be a class"
        self.assertTrue(isinstance(SConsArguments.Util._notfound,type))
    def test_NOTFOUND(self):
        "Test SConsArguments.Util.NOTFOUND, it should be a class"
        self.assertTrue(isinstance(SConsArguments.Util.NOTFOUND,type))
        self.assertIs(SConsArguments.Util.NOTFOUND, SConsArguments.Util._notfound)

#############################################################################
class Test__resubst(unittest.TestCase):
    """Test SConsArguments.Util._resubst() function"""
    def test__resubst_1(self):
        """_resubst('foo bar') should return 'foo bar'"""
        self.assertEqual(SConsArguments.Util._resubst('foo bar'), 'foo bar')
    def test__resubst_2(self):
        """_resubst('foo bar', {'foo' : 'XFOO'}) should return 'foo bar'"""
        self.assertEqual(SConsArguments.Util._resubst('foo bar', {'foo' : 'XFOO'}), 'foo bar')
    def test__resubst_3(self):
        """_resubst('foo $bar', {'bar' : 'XBAR'}) should return 'foo XBAR'"""
        self.assertEqual(SConsArguments.Util._resubst('foo $bar', {'bar' : 'XBAR'}), 'foo XBAR')
    def test__resubst_4(self):
        """_resubst('$foo $bar', {'foo' : 'XFOO', 'bar' : 'XBAR'}) should return 'XFOO XBAR'"""
        self.assertEqual(SConsArguments.Util._resubst('$foo $bar', {'foo' : 'XFOO', 'bar' : 'XBAR'}), 'XFOO XBAR')
    def test__resubst_5(self):
        """_resubst('$foo $bar', {'foo' : '$bar', 'bar' : 'XBAR'}) should return '$bar XBAR'"""
        self.assertEqual(SConsArguments.Util._resubst('$foo $bar', {'foo' : '$bar', 'bar' : 'XBAR'}), '$bar XBAR')
    def test__resubst_6(self):
        """_resubst('foo ${bar}', {'bar' : 'XBAR'}) should return 'foo XBAR'"""
        self.assertEqual(SConsArguments.Util._resubst('foo ${bar}', {'bar' : 'XBAR'}), 'foo XBAR')
    def test__resubst_7(self):
        """_resubst('${foo} ${bar}', {'foo' : 'XFOO', 'bar' : 'XBAR'}) should return 'XFOO XBAR'"""
        self.assertEqual(SConsArguments.Util._resubst('${foo} ${bar}', {'foo' : 'XFOO', 'bar' : 'XBAR'}), 'XFOO XBAR')
    def test__resubst_8(self):
        """_resubst('${foo} ${bar}', {'foo' : '${bar}', 'bar' : 'XBAR'}) should return '${bar} XBAR'"""
        self.assertEqual(SConsArguments.Util._resubst('${foo} ${bar}', {'foo' : '${bar}', 'bar' : 'XBAR'}), '${bar} XBAR')

#############################################################################
class Test__build_resubst_dict(unittest.TestCase):
    """Test SConsArguments.Util._build_resubst_dict() function"""
    def test__build_resubst_dict_1(self):
        """_build_resubst_dict({}) should == {}"""
        self.assertEqual(SConsArguments.Util._build_resubst_dict({}),{})
    def test__build_resubst_dict_2(self):
        """_build_resubst_dict({'xxx' : 'yyy', 'vvv' : 'www'}) should == {'xxx' : '${yyy}', 'vvv' : '${www}'}"""
        self.assertEqual(SConsArguments.Util._build_resubst_dict({'xxx' : 'yyy', 'vvv' : 'www'}), {'xxx' : '${yyy}', 'vvv' : '${www}'})

#############################################################################
class Test__build_iresubst_dict(unittest.TestCase):
    """Test SConsArguments.Util._build_iresubst_dict() function"""
    def test__build_iresubst_dict_1(self):
        """_build_iresubst_dict({}) should == {}"""
        self.assertEqual(SConsArguments.Util._build_iresubst_dict({}),{})
    def test__build_iresubst_dict_2(self):
        """_build_iresubst_dict({'xxx' : 'yyy', 'vvv' : 'www'}) should == {'yyy' : '${xxx}', 'www' : '${vvv}'}"""
        self.assertEqual(SConsArguments.Util._build_iresubst_dict({'xxx' : 'yyy', 'vvv' : 'www'}), {'yyy' : '${xxx}', 'www' : '${vvv}'})

#############################################################################
class Test__compose_mappings(unittest.TestCase):
    """Test SConsArguments.Util._compose_mappings() function"""
    def test__compose_mappings_1(self):
        """_compose_mappings({},{}) should == {}"""
        self.assertEqual(SConsArguments.Util._compose_mappings({},{}),{})
    def test__compose_mappings_2(self):
        """_compose_mappings({'uuu' : 'vvv', 'xxx' : 'yyy'} ,{ 'vvv' : 'VVV', 'yyy' : 'YYY'}) should == {'uuu' : 'VVV'}"""
        self.assertEqual(SConsArguments.Util._compose_mappings({'uuu' : 'vvv', 'xxx' : 'yyy'}, { 'vvv' : 'VVV', 'yyy' : 'YYY'}), {'uuu' : 'VVV', 'xxx' : 'YYY'})

#############################################################################
class Test__invert_dict(unittest.TestCase):
    def test__invert_dict_1(self):
        """_invert_dict({}) should == {}"""
        self.assertEqual(SConsArguments.Util._invert_dict({}), {})
    def test__invert_dict_2(self):
        """_invert_dict({ 'x' : 'y' }) should == { 'y' : 'x'}"""
        self.assertEqual(SConsArguments.Util._invert_dict({'x' : 'y'}), { 'y' : 'x'})
    def test__invert_dict_3(self):
        """_invert_dict({ 'v' : 'w', 'x' : 'y' }) should == { 'w' : 'v', 'y' : 'x'}"""
        self.assertEqual(SConsArguments.Util._invert_dict({'v' : 'w', 'x' : 'y'}), { 'w' : 'v', 'y' : 'x'})

#############################################################################
if __name__ == "__main__":
    ldr = unittest.TestLoader()
    suite = unittest.TestSuite()
    # Load tests to test suite
    tclasses = [ Test_module_constants
               , Test__resubst
               , Test__build_resubst_dict
               , Test__build_iresubst_dict
               , Test__compose_mappings
               , Test__invert_dict
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
