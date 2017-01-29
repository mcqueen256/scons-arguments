""" `SConsArguments.UtilTests`

Unit tests for `SConsArguments.Util`
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

import SConsArguments.Util as tested
import unittest
import SCons.Util

#############################################################################
class Test_module_constants(unittest.TestCase):
    """Test global variables"""
    def test_ENV(self):
        """Test 'Util.ENV'"""
        self.assertEqual(tested.ENV,0)
    def test_VAR(self):
        """Test 'Util.VAR'"""
        self.assertEqual(tested.VAR,1)
    def test_OPT(self):
        """Test 'Util.OPT'"""
        self.assertEqual(tested.OPT,2)
    def test_ALL(self):
        """Test 'Util.ALL'"""
        self.assertEqual(tested.ALL,3)
    def test_MISSING(self):
        """Test 'Util.MISSING'"""
        self.assertIs(tested.MISSING, tested._missing)
    def test_UNDEFINED(self):
        """Test 'Util.UNDEFINED'"""
        self.assertIs(tested.UNDEFINED, tested._undef)
    def test_NOTFOUND(self):
        """Test 'Util.NOTFOUND'"""
        self.assertIs(tested.NOTFOUND, tested._notfound)
    def test__missing(self):
        "Test SConsArguments.Util._missing, it should be a class with certain characteristics"
        self.assertTrue(isinstance(tested._missing,type))
        self.assertFalse(bool(tested._missing))
        self.assertEqual(str(tested._missing), 'MISSING')
    def test_MISSING(self):
        "Test SConsArguments.Util.MISSING, it should be same as SConsArguments.Util._missing"
        self.assertTrue(isinstance(tested.MISSING,type))
        self.assertIs(tested.MISSING, tested._missing)
    def test__undef(self):
        "Test SConsArguments.Util._undef, it should be a class with certain characteristics"
        self.assertTrue(isinstance(tested._undef,type))
        self.assertFalse(bool(tested._undef))
        self.assertEqual(str(tested._undef), 'UNDEFINED')
    def test_UNDEFINED(self):
        "Test SConsArguments.Util.UNDEFINED, it should be a class"
        self.assertTrue(isinstance(tested.UNDEFINED,type))
        self.assertIs(tested.UNDEFINED, tested._undef)
    def test__notfound(self):
        "Test SConsArguments.Util._notfound, it should be a class"
        self.assertTrue(isinstance(tested._notfound,type))
        self.assertFalse(bool(tested._notfound))
        self.assertEqual(str(tested._notfound), 'NOTFOUND')
    def test_NOTFOUND(self):
        "Test SConsArguments.Util.NOTFOUND, it should be a class"
        self.assertTrue(isinstance(tested.NOTFOUND,type))
        self.assertIs(tested.NOTFOUND, tested._notfound)

#############################################################################
class Test__resubst(unittest.TestCase):
    """Test SConsArguments.Util._resubst() function"""
    def test__resubst_1(self):
        """_resubst('foo bar') should return 'foo bar'"""
        self.assertEqual(tested._resubst('foo bar'), 'foo bar')
    def test__resubst_2(self):
        """_resubst('foo bar', {'foo' : 'XFOO'}) should return 'foo bar'"""
        self.assertEqual(tested._resubst('foo bar', {'foo' : 'XFOO'}), 'foo bar')
    def test__resubst_3(self):
        """_resubst('foo $bar', {'bar' : 'XBAR'}) should return 'foo XBAR'"""
        self.assertEqual(tested._resubst('foo $bar', {'bar' : 'XBAR'}), 'foo XBAR')
    def test__resubst_4(self):
        """_resubst('$foo $bar', {'foo' : 'XFOO', 'bar' : 'XBAR'}) should return 'XFOO XBAR'"""
        self.assertEqual(tested._resubst('$foo $bar', {'foo' : 'XFOO', 'bar' : 'XBAR'}), 'XFOO XBAR')
    def test__resubst_5(self):
        """_resubst('$foo $bar', {'foo' : '$bar', 'bar' : 'XBAR'}) should return '$bar XBAR'"""
        self.assertEqual(tested._resubst('$foo $bar', {'foo' : '$bar', 'bar' : 'XBAR'}), '$bar XBAR')
    def test__resubst_6(self):
        """_resubst('foo ${bar}', {'bar' : 'XBAR'}) should return 'foo XBAR'"""
        self.assertEqual(tested._resubst('foo ${bar}', {'bar' : 'XBAR'}), 'foo XBAR')
    def test__resubst_7(self):
        """_resubst('${foo} ${bar}', {'foo' : 'XFOO', 'bar' : 'XBAR'}) should return 'XFOO XBAR'"""
        self.assertEqual(tested._resubst('${foo} ${bar}', {'foo' : 'XFOO', 'bar' : 'XBAR'}), 'XFOO XBAR')
    def test__resubst_8(self):
        """_resubst('${foo} ${bar}', {'foo' : '${bar}', 'bar' : 'XBAR'}) should return '${bar} XBAR'"""
        self.assertEqual(tested._resubst('${foo} ${bar}', {'foo' : '${bar}', 'bar' : 'XBAR'}), '${bar} XBAR')

#############################################################################
class Test__build_resubst_dict(unittest.TestCase):
    """Test SConsArguments.Util._build_resubst_dict() function"""
    def test__build_resubst_dict_1(self):
        """_build_resubst_dict({}) should == {}"""
        self.assertEqual(tested._build_resubst_dict({}),{})
    def test__build_resubst_dict_2(self):
        """_build_resubst_dict({'xxx' : 'yyy', 'vvv' : 'www'}) should == {'xxx' : '${yyy}', 'vvv' : '${www}'}"""
        self.assertEqual(tested._build_resubst_dict({'xxx' : 'yyy', 'vvv' : 'www'}), {'xxx' : '${yyy}', 'vvv' : '${www}'})

#############################################################################
class Test__build_iresubst_dict(unittest.TestCase):
    """Test SConsArguments.Util._build_iresubst_dict() function"""
    def test__build_iresubst_dict_1(self):
        """_build_iresubst_dict({}) should == {}"""
        self.assertEqual(tested._build_iresubst_dict({}),{})
    def test__build_iresubst_dict_2(self):
        """_build_iresubst_dict({'xxx' : 'yyy', 'vvv' : 'www'}) should == {'yyy' : '${xxx}', 'www' : '${vvv}'}"""
        self.assertEqual(tested._build_iresubst_dict({'xxx' : 'yyy', 'vvv' : 'www'}), {'yyy' : '${xxx}', 'www' : '${vvv}'})

#############################################################################
class Test__compose_mappings(unittest.TestCase):
    """Test SConsArguments.Util._compose_mappings() function"""
    def test__compose_mappings_1(self):
        """_compose_mappings({},{}) should == {}"""
        self.assertEqual(tested._compose_mappings({},{}),{})
    def test__compose_mappings_2(self):
        """_compose_mappings({'uuu' : 'vvv', 'xxx' : 'yyy'} ,{ 'vvv' : 'VVV', 'yyy' : 'YYY'}) should == {'uuu' : 'VVV'}"""
        self.assertEqual(tested._compose_mappings({'uuu' : 'vvv', 'xxx' : 'yyy'}, { 'vvv' : 'VVV', 'yyy' : 'YYY'}), {'uuu' : 'VVV', 'xxx' : 'YYY'})

#############################################################################
class Test__invert_dict(unittest.TestCase):
    def test__invert_dict_1(self):
        """_invert_dict({}) should == {}"""
        self.assertEqual(tested._invert_dict({}), {})
    def test__invert_dict_2(self):
        """_invert_dict({ 'x' : 'y' }) should == { 'y' : 'x'}"""
        self.assertEqual(tested._invert_dict({'x' : 'y'}), { 'y' : 'x'})
    def test__invert_dict_3(self):
        """_invert_dict({ 'v' : 'w', 'x' : 'y' }) should == { 'w' : 'v', 'y' : 'x'}"""
        self.assertEqual(tested._invert_dict({'v' : 'w', 'x' : 'y'}), { 'w' : 'v', 'y' : 'x'})

#############################################################################
class Test__flags2list(unittest.TestCase):
    def test__flags2list_0(self):
        """flags2list('') should be an instance of SCons.Util.CLVar"""
        self.assertIsInstance(tested.flags2list(''), SCons.Util.CLVar)
    def test__flags2list_1(self):
        """flags2list('') should == []"""
        self.assertEqual(tested.flags2list(''),[])
    def test__flags2list_2(self):
        """flags2list('xyz') should == ['xyz']"""
        self.assertEqual(tested.flags2list('xyz'),['xyz'])
    def test__flags2list_3(self):
        """flags2list('foo bar') should == ['foo', 'bar']"""
        self.assertEqual(tested.flags2list('foo bar'), ['foo', 'bar'])

#############################################################################
class Test__paths2list(unittest.TestCase):
    def test__paths2list_0(self):
        """paths2list('') should be an instance of SCons.Util.CLVar"""
        self.assertIsInstance(tested.paths2list(''), SCons.Util.CLVar)
    def test__paths2list_1(self):
        """paths2list('') should == []"""
        self.assertEqual(tested.paths2list(''),[])
    def test__paths2list_2(self):
        """paths2list('xyz') should == ['xyz']"""
        self.assertEqual(tested.paths2list('xyz'),['xyz'])
    def test__paths2list_3(self):
        """paths2list('foo bar') should == ['foo bar']"""
        self.assertEqual(tested.paths2list('foo bar'), ['foo bar'])
    def test__paths2list_4(self):
        """paths2list('foo:bar') should == ['foo', 'bar']"""
        self.assertEqual(tested.paths2list('foo:bar'), ['foo', 'bar'])
    def test__paths2list_5(self):
        """paths2list('"C:\windows":foo:bar') should == ['C:\windows', 'foo', 'bar']"""
        self.assertEqual(tested.paths2list('"C:\windows":foo:bar'), ['C:\windows', 'foo', 'bar'])

#############################################################################
class Test__cdefs2list(unittest.TestCase):
    def test__cdefs2list_0(self):
        """cdefs2list('') should be an instance of SCons.Util.CLVar"""
        self.assertIsInstance(tested.cdefs2list(''), SCons.Util.CLVar)
    def test__cdefs2list_1(self):
        """cdefs2list('') should == []"""
        self.assertEqual(tested.cdefs2list(''),[])
    def test__cdefs2list_2(self):
        """cdefs2list('-Dxyz') should == ['-Dxyz']"""
        self.assertEqual(tested.cdefs2list('-Dxyz'),['-Dxyz'])
    def test__cdefs2list_3(self):
        """cdefs2list('-Dfoo -Dbar') should == ['-Dfoo', '-Dbar']"""
        self.assertEqual(tested.cdefs2list('-Dfoo -Dbar'), ['-Dfoo', '-Dbar'])
    def test__cdefs2list_4(self):
        """cdefs2list('-Dfoo="string with spaces"') should == ['-Dfoo=string with spaces']"""
        self.assertEqual(tested.cdefs2list('-Dfoo="string with spaces"'), ['-Dfoo=string with spaces'])
    def test__cdefs2list_5(self):
        """cdefs2list("-Dfoo='string with spaces'") should == ["-Dfoo=string with spaces"]"""
        self.assertEqual(tested.cdefs2list("-Dfoo='string with spaces'"), ["-Dfoo=string with spaces"])
    def test__cdefs2list_6(self):
        """cdefs2list("'-Dfoo=\"string with spaces\"' -Dother") should == ["-Dfoo=string with spaces"]"""
        self.assertEqual(tested.cdefs2list("'-Dfoo=\"string with spaces\"' -Dother"), ["-Dfoo=\"string with spaces\"", '-Dother'])

#############################################################################
class Test__yesno2bool(unittest.TestCase):
    def test__yesno2bool_1(self):
        """yesno2bool(...)"""
        positives = ('y','yes','true','on','enable','enabled')
        negatives = ('n','no','false','off','disable','disabled')
        for p in positives:
            self.assertIs(tested.yesno2bool(p), True)
            self.assertIs(tested.yesno2bool(p.upper()), True)
        for n in negatives:
            self.assertIs(tested.yesno2bool(n), False)
            self.assertIs(tested.yesno2bool(n.upper()), False)

        self.assertIs(tested.yesno2bool('foo'), None)


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
               , Test__flags2list
               , Test__paths2list
               , Test__cdefs2list
               , Test__yesno2bool
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
