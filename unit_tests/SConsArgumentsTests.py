""" SConsArgumentsTest

Unit tests for SConsArguments
"""

__docformat__ = "restructuredText"

#
# Copyright (c) 2012-2014 by Pawel Tomulik
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
import unittest
import mock

#############################################################################
class Test_module_constants(unittest.TestCase):
    """Test constants in SConsArguments module"""
    def test_ENV(self):
        "Test SConsArguments.ENV, it should == 0"
        self.assertEqual(SConsArguments.ENV,0)
    def test_VAR(self):
        "Test SConsArguments.VAR, it should == 1"
        self.assertEqual(SConsArguments.VAR,1)
    def test_OPT(self):
        "Test SConsArguments.OPT, it should == 2"
        self.assertEqual(SConsArguments.OPT,2)
    def test_ALL(self):
        "Test SConsArguments.ALL, it should == 3"
        self.assertEqual(SConsArguments.ALL,3)
    def test__missing(self):
        "Test SConsArguments._missing, it should be a class with certain characteristics"
        self.assertTrue(isinstance(SConsArguments._missing,type))
        self.assertFalse(bool(SConsArguments._missing))
        self.assertEqual(str(SConsArguments._missing), 'MISSING')
    def test_MISSING(self):
        "Test SConsArguments.MISSING, it should be same as SConsArguments._missing"
        self.assertTrue(isinstance(SConsArguments.MISSING,type))
        self.assertIs(SConsArguments.MISSING, SConsArguments._missing)
    def test__undef(self):
        "Test SConsArguments._undef, it should be a class with certain characteristics"
        self.assertTrue(isinstance(SConsArguments._undef,type))
        self.assertFalse(bool(SConsArguments._undef))
        self.assertEqual(str(SConsArguments._undef), 'UNDEFINED')
    def test_UNDEFINED(self):
        "Test SConsArguments.UNDEFINED, it should be a class"
        self.assertTrue(isinstance(SConsArguments.UNDEFINED,type))
        self.assertIs(SConsArguments.UNDEFINED, SConsArguments._undef)
    def test__notfound(self):
        "Test SConsArguments._notfound, it should be a class"
        self.assertTrue(isinstance(SConsArguments._notfound,type))

#############################################################################
class Test__resubst(unittest.TestCase):
    """Test SConsArguments._resubst() function"""
    def test__resubst_1(self):
        """_resubst('foo bar') should return 'foo bar'"""
        self.assertEqual(SConsArguments._resubst('foo bar'), 'foo bar')
    def test__resubst_2(self):
        """_resubst('foo bar', {'foo' : 'XFOO'}) should return 'foo bar'"""
        self.assertEqual(SConsArguments._resubst('foo bar', {'foo' : 'XFOO'}), 'foo bar')
    def test__resubst_3(self):
        """_resubst('foo $bar', {'bar' : 'XBAR'}) should return 'foo XBAR'"""
        self.assertEqual(SConsArguments._resubst('foo $bar', {'bar' : 'XBAR'}), 'foo XBAR')
    def test__resubst_4(self):
        """_resubst('$foo $bar', {'foo' : 'XFOO', 'bar' : 'XBAR'}) should return 'XFOO XBAR'"""
        self.assertEqual(SConsArguments._resubst('$foo $bar', {'foo' : 'XFOO', 'bar' : 'XBAR'}), 'XFOO XBAR')
    def test__resubst_5(self):
        """_resubst('$foo $bar', {'foo' : '$bar', 'bar' : 'XBAR'}) should return '$bar XBAR'"""
        self.assertEqual(SConsArguments._resubst('$foo $bar', {'foo' : '$bar', 'bar' : 'XBAR'}), '$bar XBAR')
    def test__resubst_6(self):
        """_resubst('foo ${bar}', {'bar' : 'XBAR'}) should return 'foo XBAR'"""
        self.assertEqual(SConsArguments._resubst('foo ${bar}', {'bar' : 'XBAR'}), 'foo XBAR')
    def test__resubst_7(self):
        """_resubst('${foo} ${bar}', {'foo' : 'XFOO', 'bar' : 'XBAR'}) should return 'XFOO XBAR'"""
        self.assertEqual(SConsArguments._resubst('${foo} ${bar}', {'foo' : 'XFOO', 'bar' : 'XBAR'}), 'XFOO XBAR')
    def test__resubst_8(self):
        """_resubst('${foo} ${bar}', {'foo' : '${bar}', 'bar' : 'XBAR'}) should return '${bar} XBAR'"""
        self.assertEqual(SConsArguments._resubst('${foo} ${bar}', {'foo' : '${bar}', 'bar' : 'XBAR'}), '${bar} XBAR')

#############################################################################
class Test__build_resubst_dict(unittest.TestCase):
    """Test SConsArguments._build_resubst_dict() function"""
    def test__build_resubst_dict_1(self):
        """_build_resubst_dict({}) should == {}"""
        self.assertEqual(SConsArguments._build_resubst_dict({}),{})
    def test__build_resubst_dict_2(self):
        """_build_resubst_dict({'xxx' : 'yyy', 'vvv' : 'www'}) should == {'xxx' : '${yyy}', 'vvv' : '${www}'}"""
        self.assertEqual(SConsArguments._build_resubst_dict({'xxx' : 'yyy', 'vvv' : 'www'}), {'xxx' : '${yyy}', 'vvv' : '${www}'})

#############################################################################
class Test__build_iresubst_dict(unittest.TestCase):
    """Test SConsArguments._build_iresubst_dict() function"""
    def test__build_iresubst_dict_1(self):
        """_build_iresubst_dict({}) should == {}"""
        self.assertEqual(SConsArguments._build_iresubst_dict({}),{})
    def test__build_iresubst_dict_2(self):
        """_build_iresubst_dict({'xxx' : 'yyy', 'vvv' : 'www'}) should == {'yyy' : '${xxx}', 'www' : '${vvv}'}"""
        self.assertEqual(SConsArguments._build_iresubst_dict({'xxx' : 'yyy', 'vvv' : 'www'}), {'yyy' : '${xxx}', 'www' : '${vvv}'})

#############################################################################
class Test__compose_mappings(unittest.TestCase):
    """Test SConsArguments._compose_mappings() function"""
    def test__compose_mappings_1(self):
        """_compose_mappings({},{}) should == {}"""
        self.assertEqual(SConsArguments._compose_mappings({},{}),{})
    def test__compose_mappings_2(self):
        """_compose_mappings({'uuu' : 'vvv', 'xxx' : 'yyy'} ,{ 'vvv' : 'VVV', 'yyy' : 'YYY'}) should == {'uuu' : 'VVV'}"""
        self.assertEqual(SConsArguments._compose_mappings({'uuu' : 'vvv', 'xxx' : 'yyy'}, { 'vvv' : 'VVV', 'yyy' : 'YYY'}), {'uuu' : 'VVV', 'xxx' : 'YYY'})

#############################################################################
class Test__invert_dict(unittest.TestCase):
    def test__invert_dict_1(self):
        """_invert_dict({}) should == {}"""
        self.assertEqual(SConsArguments._invert_dict({}), {})
    def test__invert_dict_2(self):
        """_invert_dict({ 'x' : 'y' }) should == { 'y' : 'x'}"""
        self.assertEqual(SConsArguments._invert_dict({'x' : 'y'}), { 'y' : 'x'})
    def test__invert_dict_3(self):
        """_invert_dict({ 'v' : 'w', 'x' : 'y' }) should == { 'w' : 'v', 'y' : 'x'}"""
        self.assertEqual(SConsArguments._invert_dict({'v' : 'w', 'x' : 'y'}), { 'w' : 'v', 'y' : 'x'})

#############################################################################
class Test__ArgumentsProxy(unittest.TestCase):
    def test___init___1(self):
        """_ArgumentsProxy.__init__(target) should set default attributes"""
        target = 'target'
        proxy = SConsArguments._ArgumentsProxy(target)
        self.assertIs(proxy.target, target)
        self.assertEqual(proxy._ArgumentsProxy__rename, {})
        self.assertEqual(proxy._ArgumentsProxy__irename, {})
        self.assertEqual(proxy._ArgumentsProxy__resubst, {})
        self.assertEqual(proxy._ArgumentsProxy__iresubst, {})
        self.assertEqual(proxy.is_strict(), False)

    def test___init___2(self):
        """_ArgumentsProxy.__init__(target, arg1, arg2, arg3, arg4, True) should set attributes"""
        target = 'target'
        arg1, arg2, arg3, arg4 = 'arg1', 'arg2', 'arg3', 'arg4'
        proxy = SConsArguments._ArgumentsProxy(target, arg1, arg2, arg3, arg4, True)
        self.assertIs(proxy.target, target)
        self.assertIs(proxy._ArgumentsProxy__rename,   arg1)
        self.assertIs(proxy._ArgumentsProxy__resubst,  arg2)
        self.assertIs(proxy._ArgumentsProxy__irename,  arg3)
        self.assertIs(proxy._ArgumentsProxy__iresubst, arg4)
        self.assertIs(proxy.is_strict(), True)

    def test_is_strict(self):
        """Test <_ArgumentsProxy>.is_strict()"""
        self.assertIs(SConsArguments._ArgumentsProxy('tgt', strict = False).is_strict(), False)
        self.assertIs(SConsArguments._ArgumentsProxy('tgt', strict = True).is_strict(), True)

    def test_set_strict_False_calls__setup_methods_False(self):
        """<_ArgumentsProxy>.set_strict(False) should call <_ArgumentsProxy>.__setup_methods(False)"""
        proxy = SConsArguments._ArgumentsProxy('tgt')
        proxy._ArgumentsProxy__setup_methods = mock.Mock(name = '__setup_methods')
        proxy.set_strict(False)
        try:
            proxy._ArgumentsProxy__setup_methods.assert_called_with(False)
        except AssertionError as e:
            self.fail(str(e))

    def test_set_strict_True_calls__setup_methods_True(self):
        """<_ArgumentsProxy>.set_strict(True) should call <_ArgumentsProxy>.__setup_methods(True)"""
        proxy = SConsArguments._ArgumentsProxy('tgt')
        proxy._ArgumentsProxy__setup_methods = mock.Mock(name = '__setup_methods')
        proxy.set_strict(True)
        try:
            proxy._ArgumentsProxy__setup_methods.assert_called_with(True)
        except AssertionError as e:
            self.fail(str(e))

    def test_set_strict_False(self):
        """<_ArgumentsProxy>.is_strict() should be False after <_ArgumentsProxy>.set_strict(False)"""
        proxy = SConsArguments._ArgumentsProxy('tgt')
        proxy.set_strict(False)
        self.assertIs(proxy.is_strict(), False)

    def test_set_strict_True(self):
        """<_ArgumentsProxy>.is_strict() should be True after <_ArgumentsProxy>.set_strict(True)"""
        proxy = SConsArguments._ArgumentsProxy('tgt')
        proxy.set_strict(True)
        self.assertIs(proxy.is_strict(), True)

    def test___setup_methods_True(self):
        """<_ArgumentsProxy>.__setup_methods(True) should setup appropriate methods"""
        proxy = SConsArguments._ArgumentsProxy('tgt', strict = False)
        proxy._ArgumentsProxy__setup_methods(True)
        self.assertEqual(proxy._ArgumentsProxy__delitem__impl, proxy._ArgumentsProxy__delitem__strict)
        self.assertEqual(proxy._ArgumentsProxy__getitem__impl, proxy._ArgumentsProxy__getitem__strict)
        self.assertEqual(proxy._ArgumentsProxy__setitem__impl, proxy._ArgumentsProxy__setitem__strict)
        self.assertEqual(proxy.get, proxy._get_strict)
        self.assertEqual(proxy.has_key, proxy._has_key_strict)
        self.assertEqual(proxy._ArgumentsProxy__contains__impl, proxy._ArgumentsProxy__contains__strict)
        self.assertEqual(proxy.items, proxy._items_strict)

    def test___setup_methods_False(self):
        """<_ArgumentsProxy>.__setup_methods(False) should setup appropriate methods"""
        proxy = SConsArguments._ArgumentsProxy('tgt', strict = True)
        proxy._ArgumentsProxy__setup_methods(False)
        self.assertEqual(proxy._ArgumentsProxy__delitem__impl, proxy._ArgumentsProxy__delitem__nonstrict)
        self.assertEqual(proxy._ArgumentsProxy__getitem__impl, proxy._ArgumentsProxy__getitem__nonstrict)
        self.assertEqual(proxy._ArgumentsProxy__setitem__impl, proxy._ArgumentsProxy__setitem__nonstrict)
        self.assertEqual(proxy.get, proxy._get_nonstrict)
        self.assertEqual(proxy.has_key, proxy._has_key_nonstrict)
        self.assertEqual(proxy._ArgumentsProxy__contains__impl, proxy._ArgumentsProxy__contains__nonstrict)
        self.assertEqual(proxy.items, proxy._items_nonstrict)

    def test___delitem___1(self):
        """_ArgumentsProxy({'a' : 'A'}).__delitem__('a') should delete item 'a'"""
        tgt = { 'a' : 'A' }
        SConsArguments._ArgumentsProxy(tgt).__delitem__('a')
        self.assertEqual(tgt, {})

    def test___delitem___2(self):
        """_ArgumentsProxy({'a' : 'A'}, strict = True).__delitem__('a') should raise KeyError"""
        with self.assertRaises(KeyError):
            SConsArguments._ArgumentsProxy({'a' : 'A'}, strict = True).__delitem__('a')

    def test___delitem___3(self):
        """_ArgumentsProxy({'b' : 'B'}, rename = {'a' : 'b'}).__delitem__('a') should delete item 'b'"""
        tgt = { 'b' : 'B' }
        SConsArguments._ArgumentsProxy(tgt, rename = { 'a' : 'b'}).__delitem__('a')
        self.assertEqual(tgt, {})

    def test___delitem___4(self):
        """_ArgumentsProxy({'b' : 'B'}, rename = {'a' : 'b'}, strict = True).__delitem__('a') should delete item 'b'"""
        tgt = { 'b' : 'B' }
        SConsArguments._ArgumentsProxy(tgt, rename = { 'a' : 'b'}, strict = True).__delitem__('a')
        self.assertEqual(tgt, {})

    def test___getitem___1(self):
        """_ArgumentsProxy({'a' : 'A'}).__getitem__('a') should return 'A'"""
        tgt = { 'a' : 'A' }
        self.assertEqual(SConsArguments._ArgumentsProxy({'a' : 'A'}).__getitem__('a'), 'A')

    def test___getitem___2(self):
        """_ArgumentsProxy({'a' : 'A'}, strict = True).__getitem__('a') should raise KeyError"""
        with self.assertRaises(KeyError):
            SConsArguments._ArgumentsProxy({'a' : 'A'}, strict = True).__getitem__('a')

    def test__getitem___3(self):
        """_ArgumentsProxy({'b' : 'B'}, rename = {'a' : 'b'}).__getitem__('a') should return 'B'"""
        self.assertEqual(SConsArguments._ArgumentsProxy({'b' : 'B'}, rename = {'a' : 'b'}).__getitem__('a'), 'B')

    def test___getitem___4(self):
        """_ArgumentsProxy({'b' : 'B'}, rename = {'a' : 'b'}, strict = True).__getitem__('a') should return 'B'"""
        self.assertEqual(SConsArguments._ArgumentsProxy({'b' : 'B'}, rename = {'a' : 'b'}, strict = True).__getitem__('a'), 'B')

    def test__setitem___1(self):
        """_ArgumentsProxy({}).__setitem__('a', 'A') should set item 'a' to 'A'"""
        proxy = SConsArguments._ArgumentsProxy({})
        proxy.__setitem__('a', 'A')
        self.assertEqual(proxy['a'], 'A')

    def test___setitem___2(self):
        """_ArgumentsProxy({'a' : 'B'}).__setitem__('a', 'A') should set item 'a' to 'A'"""
        tgt = {'a' : 'B'}
        proxy = SConsArguments._ArgumentsProxy(tgt)
        proxy.__setitem__('a', 'A')
        self.assertEqual(tgt['a'], 'A')

    def test__setitem___3(self):
        """_ArgumentsProxy({'a' : 'B'}, rename = { 'a' : 'a' }, strict = True).__setitem__('a', 'A') should set item 'a' to 'A'"""
        tgt = {'a' : 'B'}
        proxy = SConsArguments._ArgumentsProxy(tgt, rename = { 'a' : 'a' }, strict = True)
        proxy.__setitem__('a', 'A')
        self.assertEqual(tgt['a'], 'A')

    def test___setitem___4(self):
        """_ArgumentsProxy({'a' : 'B'}, strict = True).__setitem__('a', 'A') should raise KeyError"""
        tgt = {'a' : 'B'}
        proxy = SConsArguments._ArgumentsProxy(tgt, strict = True)
        with self.assertRaises(KeyError):
            proxy.__setitem__('a', 'A')
        self.assertEqual(tgt['a'], 'B')

    def test_get_1(self):
        """_ArgumentsProxy({'a' : 'A'}).get('a') should return 'A'"""
        self.assertEqual(SConsArguments._ArgumentsProxy({'a' : 'A'}).get('a'), 'A')

    def test_get_2(self):
        """_ArgumentsProxy({'a' : 'A'}).get('b') should return None"""
        self.assertEqual(SConsArguments._ArgumentsProxy({'a' : 'A'}).get('b'), None)

    def test_get_3(self):
        """_ArgumentsProxy({'a' : 'A'}, rename = { 'b' : 'a' }).get('b') should return 'A'"""
        self.assertEqual(SConsArguments._ArgumentsProxy({'a' : 'A'}, rename = { 'b' : 'a'}).get('b'), 'A')

    def test_get_4(self):
        """_ArgumentsProxy({'a' : 'A'}, rename = { 'b' : 'a' }).get('a') should return 'A'"""
        self.assertEqual(SConsArguments._ArgumentsProxy({'a' : 'A'}, rename = { 'b' : 'a'}).get('a'), 'A')

    def test_get_5(self):
        """_ArgumentsProxy({'a' : 'A'}, strict = True).get('a') should raise KeyError"""
        with self.assertRaises(KeyError):
            SConsArguments._ArgumentsProxy({'a' : 'A'}, strict = True).get('a')

    def test_get_6(self):
        """_ArgumentsProxy({'a' : 'A'}, rename = { 'b' : 'a' }, strict = True).get('b') should return 'A'"""
        self.assertEqual(SConsArguments._ArgumentsProxy({'a' : 'A'}, rename = { 'b' : 'a' }, strict = True).get('b'), 'A')

    def test_has_key_1(self):
        """_ArgumentsProxy({'a' : 'A'}).has_key('a') should return True"""
        self.assertTrue(SConsArguments._ArgumentsProxy({'a' : 'A'}).has_key('a'))

    def test_has_key_2(self):
        """_ArgumentsProxy({'a' : 'A'}).has_key('b') should return False"""
        self.assertFalse(SConsArguments._ArgumentsProxy({'a' : 'A'}).has_key('b'))

    def test_has_key_3(self):
        """_ArgumentsProxy({'a' : 'A'}, rename = {'b' : 'a'}).has_key('a') should return True"""
        self.assertTrue(SConsArguments._ArgumentsProxy({'a' : 'A'}, rename = {'b' : 'a'}).has_key('a'))

    def test_has_key_4(self):
        """_ArgumentsProxy({'a' : 'A'}, rename = {'b' : 'a'}).has_key('b') should return True"""
        self.assertTrue(SConsArguments._ArgumentsProxy({'a' : 'A'}, rename = {'b' : 'a'}).has_key('b'))

    def test_has_key_5(self):
        """_ArgumentsProxy({'a' : 'A'}, rename = {'b' : 'a'}, strict = True).has_key('a') should return False"""
        self.assertFalse(SConsArguments._ArgumentsProxy({'a' : 'A'}, rename = {'b' : 'a'}, strict = True).has_key('a'))

    def test_has_key_6(self):
        """_ArgumentsProxy({'a' : 'A'}, rename = {'b' : 'a'}, strict = True).has_key('b') should return True"""
        self.assertTrue(SConsArguments._ArgumentsProxy({'a' : 'A'}, rename = {'b' : 'a'}, strict = True).has_key('b'))

    def test_has_key_7(self):
        """_ArgumentsProxy({'a' : 'A'}, rename = {'b' : 'c'}, strict = True).has_key('b') should return False"""
        self.assertFalse(SConsArguments._ArgumentsProxy({'a' : 'A'}, rename = {'b' : 'c'}, strict = True).has_key('b'))

    def test___contains___1(self):
        """_ArgumentsProxy({'a' : 'A'}).__contains__('a') should return True"""
        self.assertTrue(SConsArguments._ArgumentsProxy({'a' : 'A'}).__contains__('a'))

    def test___contains___2(self):
        """_ArgumentsProxy({'a' : 'A'}).__contains__('b') should return False"""
        self.assertFalse(SConsArguments._ArgumentsProxy({'a' : 'A'}).__contains__('b'))

    def test___contains___3(self):
        """_ArgumentsProxy({'a' : 'A'}, rename = {'b' : 'a'}).__contains__('a') should return True"""
        self.assertTrue(SConsArguments._ArgumentsProxy({'a' : 'A'}, rename = {'b' : 'a'}).__contains__('a'))

    def test___contains___4(self):
        """_ArgumentsProxy({'a' : 'A'}, rename = {'b' : 'a'}).__contains__('b') should return True"""
        self.assertTrue(SConsArguments._ArgumentsProxy({'a' : 'A'}, rename = {'b' : 'a'}).__contains__('b'))

    def test___contains___5(self):
        """_ArgumentsProxy({'a' : 'A'}, rename = {'b' : 'a'}, strict = True).__contains__('a') should return False"""
        self.assertFalse(SConsArguments._ArgumentsProxy({'a' : 'A'}, rename = {'b' : 'a'}, strict = True).__contains__('a'))

    def test___contains___6(self):
        """_ArgumentsProxy({'a' : 'A'}, rename = {'b' : 'a'}, strict = True).__contains__('b') should return True"""
        self.assertTrue(SConsArguments._ArgumentsProxy({'a' : 'A'}, rename = {'b' : 'a'}, strict = True).__contains__('b'))

    def test___contains___7(self):
        """_ArgumentsProxy({'a' : 'A'}, rename = {'b' : 'c'}, strict = True).__contains__('b') should return False"""
        self.assertFalse(SConsArguments._ArgumentsProxy({'a' : 'A'}, rename = {'b' : 'c'}, strict = True).__contains__('b'))

    def test_items_1(self):
        """_ArgumentsProxy({'a' : 'A', 'b' : 'B'}).items() should be [('a', 'A'), ('b', 'B')]"""
        self.assertEqual(SConsArguments._ArgumentsProxy({'a' : 'A', 'b' : 'B'}).items(), ([('a', 'A'), ('b', 'B')]))

    def test_items_2(self):
        """_ArgumentsProxy({'a' : 'A', 'b' : 'B'}, irename = {'a' : 'c'}).items() should be [('c', 'A'), ('b', 'B')]"""
        self.assertEqual(SConsArguments._ArgumentsProxy({'a' : 'A', 'b' : 'B'}, irename = { 'a' : 'c'}).items(), ([('c', 'A'), ('b', 'B')]))

    def test_items_3(self):
        """_ArgumentsProxy({'a' : 'A', 'b' : 'B'}, rename = {'c' : 'a'}, strict = True).items() should be [('c', 'A')]"""
        self.assertEqual(SConsArguments._ArgumentsProxy({'a' : 'A', 'b' : 'B'}, rename = { 'c' : 'a'}, strict = True).items(), ([('c', 'A')]))

    def test_items_4(self):
        """_ArgumentsProxy({'a' : '${a}'}, irename = {'a' : 'b'}, iresubst = {'a' : '${b}'}).items() should be [('b', '${b}')]"""
        self.assertEqual(SConsArguments._ArgumentsProxy({'a' : '${a}'}, irename = {'a' : 'b'}, iresubst = {'a' : '${b}'}).items(), [('b', '${b}')])

    def test_items_5(self):
        """_ArgumentsProxy({'a' : 'a'}, irename = {'a' : 'b'}, iresubst = {'a' : '${b}'}).items() should be [('b', 'a')]"""
        self.assertEqual(SConsArguments._ArgumentsProxy({'a' : 'a'}, irename = {'a' : 'b'}, iresubst = {'a' : '${b}'}).items(), [('b', 'a')])

    def test_subst_1(self):
        """_ArgumentsProxy(tgt).subst('${a} ${b}') should call tgt.subst('${a} ${b}')"""
        tgt = mock.Mock(name = 'tgt')
        tgt.subst = mock.Mock(name = 'tgt.subst')
        SConsArguments._ArgumentsProxy(tgt).subst('${a} ${b}')
        try:
            tgt.subst.assert_called_with('${a} ${b}')
        except AssertionError as e:
            self.fail(str(e))

    def test_subst_2(self):
        """_ArgumentsProxy(tgt, resubst = {'b' : '${c}}).subst('${a} ${b}') should call tgt.subst('${a} ${c}')"""
        tgt = mock.Mock(name = 'tgt')
        tgt.subst = mock.Mock(name = 'tgt.subst')
        SConsArguments._ArgumentsProxy(tgt, resubst = {'b' : '${c}'}).subst('${a} ${b}')
        try:
            tgt.subst.assert_called_with('${a} ${c}')
        except AssertionError as e:
            self.fail(str(e))

#############################################################################
class Test__VariablesWrapper(unittest.TestCase):
    class _Option:
        def __init__(self, key, default = None, validator = None, converter = None, aliases = []):
            self.key = key
            self.default = default
            self.validator = validator
            self.converter = converter
            self.aliases = aliases

    class _Variables:
        def __init__(self, files=[], args={}, is_global=1):
            self.files = files
            self.args = args
            self.is_global = is_global
            self.unknown = dict()

    def test___init___1(self):
        """_VariablesWrapper.__init__(variables) should initialize variables"""
        class _test_variables: pass
        wrap = SConsArguments._VariablesWrapper(_test_variables)
        self.assertIs(wrap.variables, _test_variables)

    def test___getattr___1(self):
        """_VariablesWrapper.foo should return _VariablesWrapper.variables.foo"""
        class _test_variables:
            foo = 10
        wrap = SConsArguments._VariablesWrapper(_test_variables)
        self.assertIs(wrap.foo, _test_variables.foo)

    def test_Update_1(self):
        """Test <_VaraiblesWrapper>.Update()"""
        _Variables = Test__VariablesWrapper._Variables
        _Option = Test__VariablesWrapper._Option
        validate_d = mock.Mock(name = 'validate_d')
        variables = _Variables( files = ['existing/file', 'inexistent/file'])
        variables.options = [ 
            _Option('a', SConsArguments._undef),
            _Option('b'),
            _Option('c', 'C def'),
            _Option('d', validator = validate_d),
            _Option('e', 'E def', converter = lambda x : x + ' converted'),
            _Option('f', 'F def'),
            _Option('g', 'G def', aliases = ['g_alias']),
            _Option('h', 'H def', aliases = ['h_alias'])
        ]
        args = { 'd' : 'D', 'e' : 'E', 'g_alias' : 'G' , 'z' : 'Z'}
        env = dict()
        fd = mock.Mock(name = 'fd')
        fd.read = mock.Mock(name = 'read', return_value = "b='B file'\nf=None\nh_alias='H file'")
        wrapper = SConsArguments._VariablesWrapper(variables)
        with mock.patch('__builtin__.open', spec=open, return_value = fd) as _open, \
             mock.patch('os.path.exists', side_effect = lambda f : f == 'existing/file') as _os_path_exists:
            wrapper.Update(env, args)
        _os_path_exists.assert_has_calls([mock.call('existing/file'), mock.call('inexistent/file')])
        _open.assert_called_once_with('existing/file','rU')
        validate_d.assert_called_once_with('d', 'D', env)
        self.assertEqual(env, {'c' : 'C def', 'b' : 'B file', 'd' :'D', 'e' : 'E converted', 'f' : None, 'g' : 'G', 'h' : 'H def'})
        self.assertEqual(variables.unknown, {'z' : 'Z'})
            

#############################################################################
class Test__Arguments(unittest.TestCase):

    @classmethod
    def _decls_mock_1(cls):
        # decls0 is a substitute of _ArgumentDecls instance, with only keys()
        # method defined
        decls = mock.Mock(name = 'decls0')
        decls.keys = mock.Mock(name = 'keys', return_value = ['k','e','y','s'])
        return decls

    @classmethod
    def _decls_mock_2(cls):
        decls = cls._decls_mock_1()
        return cls._mock_decls_supp_dicts_2(decls)

    @classmethod
    def _decls_mock_3(cls):
        decls = cls._decls_mock_1()
        return cls._mock_decls_supp_dicts_3(decls)

    @classmethod
    def _decls_mock_4(cls):
        decls = cls._decls_mock_1()
        return cls._mock_decls_supp_dicts_4(decls)

    @classmethod
    def _decls_mock_5(cls):
        decls = cls._decls_mock_1()
        return cls._mock_decls_supp_dicts_5(decls)

    @classmethod
    def _arguments_mock_4_UpdateEnvironment(cls):
        args = SConsArguments._Arguments(cls._decls_mock_1())
        args.update_env_from_vars = mock.Mock(name = 'update_env_from_vars')
        args.update_env_from_opts = mock.Mock(name = 'update_env_from_opts')
        return args

    @classmethod
    def _mock_decls_supp_dicts_2(cls, decls):
        def get_rename_dict(xxx):   return "rename_dict[%d]" % xxx
        def get_resubst_dict(xxx):  return "resubst_dict[%d]" % xxx
        def get_irename_dict(xxx):  return "irename_dict[%d]" % xxx
        def get_iresubst_dict(xxx): return "iresubst_dict[%d]" % xxx
        decls.get_rename_dict = mock.Mock(name = 'get_rename_dict', side_effect = get_rename_dict)
        decls.get_irename_dict = mock.Mock(name = 'get_rename_dict', side_effect = get_irename_dict)
        decls.get_resubst_dict = mock.Mock(name = 'get_rename_dict', side_effect = get_resubst_dict)
        decls.get_iresubst_dict = mock.Mock(name = 'get_iresubst_dict',  side_effect = get_iresubst_dict)
        return decls

    @classmethod
    def _mock_decls_supp_dicts_3(cls, decls):
        def get_rename_dict(xxx):   return None
        def get_resubst_dict(xxx):  return None
        def get_irename_dict(xxx):  return None
        def get_iresubst_dict(xxx): return None
        decls.get_rename_dict = mock.Mock(name = 'get_rename_dict', side_effect = get_rename_dict)
        decls.get_irename_dict = mock.Mock(name = 'get_rename_dict', side_effect = get_irename_dict)
        decls.get_resubst_dict = mock.Mock(name = 'get_rename_dict', side_effect = get_resubst_dict)
        decls.get_iresubst_dict = mock.Mock(name = 'get_iresubst_dict',  side_effect = get_iresubst_dict)
        return decls

    @classmethod
    def _mock_decls_supp_dicts_4(cls, decls):
        def get_rename_dict(xxx):
            return  [ {'a' : 'env_a'},    {'a' : 'var_a'},    {'a' : 'opt_a'}    ][xxx]
        def get_resubst_dict(xxx):
            return  [ {'a' : '${env_a}'}, {'a' : '${var_a}'}, {'a' : '${opt_a}'} ][xxx]
        def get_irename_dict(xxx):
            return  [ {'env_a' : 'a'},    {'var_a' : 'a'},    {'opt_a' : 'a'}    ][xxx]
        def get_iresubst_dict(xxx):
            return  [ {'env_a' : '${a}'}, {'var_a' : '${a}'}, {'opt_a' : '${a}'} ][xxx]
        decls.get_rename_dict = mock.Mock(name = 'get_rename_dict', side_effect = get_rename_dict)
        decls.get_irename_dict = mock.Mock(name = 'get_rename_dict', side_effect = get_irename_dict)
        decls.get_resubst_dict = mock.Mock(name = 'get_rename_dict', side_effect = get_resubst_dict)
        decls.get_iresubst_dict = mock.Mock(name = 'get_iresubst_dict',  side_effect = get_iresubst_dict)
        return decls

    @classmethod
    def _mock_decls_supp_dicts_5(cls, decls):
        def get_rename_dict(xxx):
            return  [
                {'k' : 'env_k', 'e' : 'env_e', 'y' : 'env_y', 's' : 'env_s'},
                {'k' : 'var_k', 'e' : 'var_e', 'y' : 'var_y', 's' : 'var_s'},
                {'k' : 'opt_k', 'e' : 'opt_e', 'y' : 'opt_y', 's' : 'opt_s'}
            ][xxx]
        def get_resubst_dict(xxx):
            return  [
                {'k' : '${env_k}', 'e' : '${env_e}', 'y' : '${env_y}', 's' : '${env_s}'},
                {'k' : '${var_k}', 'e' : '${var_e}', 'y' : '${var_y}', 's' : '${var_s}'},
                {'k' : '${opt_k}', 'e' : '${opt_e}', 'y' : '${opt_y}', 's' : '${opt_s}'}
            ][xxx]
        def get_irename_dict(xxx):
            return  [
                {'env_k' : 'k', 'env_e' : 'e', 'env_y' : 'y', 'env_s' : 's' },
                {'var_k' : 'k', 'var_e' : 'e', 'var_y' : 'y', 'var_s' : 's' },
                {'opt_k' : 'k', 'opt_e' : 'e', 'opt_y' : 'y', 'opt_s' : 's' }
            ][xxx]
        def get_iresubst_dict(xxx):
            return  [
                {'env_k' : '${k}','env_e' : '${e}',  'env_y' : '${y}', 'env_s' : '${s}' },
                {'var_k' : '${k}','var_e' : '${e}',  'var_y' : '${y}', 'var_s' : '${s}' },
                {'opt_k' : '${k}','opt_e' : '${e}',  'opt_y' : '${y}', 'opt_s' : '${s}' },
            ][xxx]
        decls.get_rename_dict = mock.Mock(name = 'get_rename_dict', side_effect = get_rename_dict)
        decls.get_irename_dict = mock.Mock(name = 'get_rename_dict', side_effect = get_irename_dict)
        decls.get_resubst_dict = mock.Mock(name = 'get_rename_dict', side_effect = get_resubst_dict)
        decls.get_iresubst_dict = mock.Mock(name = 'get_iresubst_dict',  side_effect = get_iresubst_dict)
        return decls

    def test___init___1(self):
        """_Arguments.__init__(decls) should call decls.keys() and self.__init_supp_dicts(decls)"""
        decls = self._decls_mock_1()
        with mock.patch.object(SConsArguments._Arguments, '_Arguments__init_supp_dicts', autospec=True) as m:
            args = SConsArguments._Arguments(decls)
            try:
                m.assert_called_once_with(args, decls)
                decls.keys.assert_called_once_with()
            except AssertionError as e:
                self.fail(str(e))
        self.assertIsInstance(args, SConsArguments._Arguments)
        self.assertEqual(args._Arguments__keys, ['k', 'e', 'y', 's'])

    def test___init___2(self):
        """_Arguments.__init__(decls) should initialize its iternal dicts"""
        args = SConsArguments._Arguments(self._decls_mock_2())
        self.assertEqual(args._Arguments__rename, ['rename_dict[0]', 'rename_dict[1]', 'rename_dict[2]'])
        self.assertEqual(args._Arguments__resubst, ['resubst_dict[0]', 'resubst_dict[1]', 'resubst_dict[2]'])
        self.assertEqual(args._Arguments__irename, ['irename_dict[0]', 'irename_dict[1]', 'irename_dict[2]'])
        self.assertEqual(args._Arguments__iresubst, ['iresubst_dict[0]', 'iresubst_dict[1]', 'iresubst_dict[2]'])


    def test___reset_supp_dicts(self):
        """<_Arguments>.__reset_supp_dicts() should reset internal dicts to {}"""
        args = SConsArguments._Arguments(self._decls_mock_2())
        args._Arguments__reset_supp_dicts()
        self.assertEqual(args._Arguments__rename, [{},{},{}])
        self.assertEqual(args._Arguments__resubst, [{},{},{}])
        self.assertEqual(args._Arguments__irename, [{},{},{}])
        self.assertEqual(args._Arguments__iresubst, [{},{},{}])

    def test___init_supp_dicts(self):
        """<_Arguments>.__init_supp_dicts(decls) should initialize internal dicts appropriately"""
        decls = self._decls_mock_3()
        args = SConsArguments._Arguments(decls)
        self.assertEqual(args._Arguments__rename, [None, None, None])
        self.assertEqual(args._Arguments__resubst, [None, None, None])
        self.assertEqual(args._Arguments__irename, [None, None, None])
        self.assertEqual(args._Arguments__iresubst, [None, None, None])
        self._mock_decls_supp_dicts_2(decls)
        args._Arguments__init_supp_dicts(decls)
        self.assertEqual(args._Arguments__rename, ['rename_dict[0]', 'rename_dict[1]', 'rename_dict[2]'])
        self.assertEqual(args._Arguments__resubst, ['resubst_dict[0]', 'resubst_dict[1]', 'resubst_dict[2]'])
        self.assertEqual(args._Arguments__irename, ['irename_dict[0]', 'irename_dict[1]', 'irename_dict[2]'])
        self.assertEqual(args._Arguments__iresubst, ['iresubst_dict[0]', 'iresubst_dict[1]', 'iresubst_dict[2]'])

    def XxxEnvProxy_test(self, x):
        args = SConsArguments._Arguments(self._decls_mock_4())
        env = { 'env_a' : 'A', 'env_b' : 'B'}
        with mock.patch('SConsArguments._ArgumentsProxy', return_value = 'ok') as ProxyClass:
            if x == 'var_':
                proxy = args.VarEnvProxy(env)
            elif x == 'opt_':
                proxy = args.OptEnvProxy(env)
            else:
                proxy = args.EnvProxy(env)

            try:
                ProxyClass.assert_called_once_with(env, { '%sa' % x : 'env_a' }, {'%sa' % x : '${env_a}'}, {'env_a' : '%sa' % x}, {'env_a' : '${%sa}' % x})
            except AssertionError as e:
                self.fail(str(e))
            self.assertEqual(proxy, 'ok')

    def test_VarEnvProxy(self):
        """_Arguments(decls).VarEnvProxy(env) should _ArgumentsProxy() with appropriate arguments"""
        self.XxxEnvProxy_test('var_')

    def test_OptEnvProxy(self):
        """_Arguments(decls).OptEnvProxy(env) should _ArgumentsProxy() with appropriate arguments"""
        self.XxxEnvProxy_test('opt_')

    def test_EnvProxy(self):
        """_Arguments(decls).EnvProxy(env) should _ArgumentsProxy() with appropriate arguments"""
        self.XxxEnvProxy_test('')
        
    def test_get_keys(self):
        """_Arguments(decls).get_keys() should return attribute __keys"""
        args = SConsArguments._Arguments(self._decls_mock_1())
        self.assertEqual(args.get_keys(), ['k','e','y','s'])
        # expect a copy of __keys, not __keys
        self.assertIsNot(args.get_keys(), args._Arguments__keys)

    def test_get_key_ENV_x(self):
        """_Arguments(decls).get_key(ENV, 'x') should be raise KeyError"""
        args = SConsArguments._Arguments(self._decls_mock_4())
        with self.assertRaises(KeyError):
            args.get_key(SConsArguments.ENV, 'x')

    def test_get_key_VAR_x(self):
        """_Arguments(decls).get_key(VAR, 'x') should be raise KeyError"""
        args = SConsArguments._Arguments(self._decls_mock_4())
        with self.assertRaises(KeyError):
            args.get_key(SConsArguments.VAR, 'x')

    def test_get_key_OPT_x(self):
        """_Arguments(decls).get_key(OPT, 'x') should be raise KeyError"""
        args = SConsArguments._Arguments(self._decls_mock_4())
        with self.assertRaises(KeyError):
            args.get_key(SConsArguments.OPT, 'x')

    def test_get_key_123_a(self):
        """_Arguments(decls).get_key(123, 'a') should be raise KeyError"""
        args = SConsArguments._Arguments(self._decls_mock_4())
        with self.assertRaises(IndexError):
            args.get_key(123, 'a')

    def test_get_key_ENV_a(self):
        """_Arguments(decls).get_key(ENV, 'a') should == 'env_a'"""
        args = SConsArguments._Arguments(self._decls_mock_4())
        self.assertEqual(args.get_key(SConsArguments.ENV, 'a'), 'env_a')

    def test_get_key_VAR_a(self):
        """_Arguments(decls).get_key(VAR, 'a') should == 'var_a'"""
        args = SConsArguments._Arguments(self._decls_mock_4())
        self.assertEqual(args.get_key(SConsArguments.VAR, 'a'), 'var_a')

    def test_get_key_OPT_a(self):
        """_Arguments(decls).get_key(OPT, 'a') should == 'opt_a'"""
        args = SConsArguments._Arguments(self._decls_mock_4())
        self.assertEqual(args.get_key(SConsArguments.OPT, 'a'), 'opt_a')

    def test_get_key_1(self):
        """_Arguments(decls).get_key(ns, 'foo') test 1"""
        decls = SConsArguments.DeclareArguments(
            foo = { 'env_key' : 'ENV_FOO', 'var_key' : 'VAR_FOO', 'opt_key' : 'OPT_FOO', 'option' : '--foo' },
            bar = { 'env_key' : 'ENV_BAR', 'var_key' : 'VAR_BAR', 'opt_key' : 'OPT_BAR', 'option' : '--bar' }
        )
        args = decls.Commit()
        self.assertEqual(args.get_key(SConsArguments.ENV, 'foo'), 'ENV_FOO')
        self.assertEqual(args.get_key(SConsArguments.VAR, 'foo'), 'VAR_FOO')
        self.assertEqual(args.get_key(SConsArguments.OPT, 'foo'), 'OPT_FOO')
        self.assertEqual(args.get_key(SConsArguments.ENV, 'bar'), 'ENV_BAR')
        self.assertEqual(args.get_key(SConsArguments.VAR, 'bar'), 'VAR_BAR')
        self.assertEqual(args.get_key(SConsArguments.OPT, 'bar'), 'OPT_BAR')

    def test_get_env_key_x(self):
        """_Arguments(decls).get_env_key('x') should raise KeyError"""
        args = SConsArguments._Arguments(self._decls_mock_4())
        with self.assertRaises(KeyError):
            args.get_env_key('x')

    def test_get_env_key_a(self):
        """_Arguments(decls).get_env_key('a') should == 'env_a'"""
        args = SConsArguments._Arguments(self._decls_mock_4())
        self.assertEqual(args.get_env_key('a'), 'env_a')

    def test_get_var_key_x(self):
        """_Arguments(decls).get_var_key('x') should raise KeyError"""
        args = SConsArguments._Arguments(self._decls_mock_4())
        with self.assertRaises(KeyError):
            args.get_var_key('x')

    def test_get_var_key_a(self):
        """_Arguments(decls).get_var_key('a') should == 'var_a'"""
        args = SConsArguments._Arguments(self._decls_mock_4())
        self.assertEqual(args.get_var_key('a'), 'var_a')

    def test_get_opt_key_x(self):
        """_Arguments(decls).get_opt_key('x') should raise KeyError"""
        args = SConsArguments._Arguments(self._decls_mock_4())
        with self.assertRaises(KeyError):
            args.get_opt_key('x')

    def test_get_opt_key_a(self):
        """_Arguments(decls).get_opt_key('a') should == 'opt_a'"""
        args = SConsArguments._Arguments(self._decls_mock_4())
        self.assertEqual(args.get_opt_key('a'), 'opt_a')

    def test_update_env_from_vars_1(self):
        """_Arguments(decls).update_env_from_vars('env', variables)"""
        args = SConsArguments._Arguments(self._decls_mock_4())
        args.VarEnvProxy = mock.Mock(name = 'VarEnvProxy', return_value = 'proxy123')
        with mock.patch('SConsArguments._VariablesWrapper') as WrapperClass:
            wrapper = WrapperClass.return_value
            wrapper.Update = mock.Mock(name = 'Update')
            args.update_env_from_vars('env', 'variables')
            try:
                WrapperClass.assert_called_once_with('variables')
                args.VarEnvProxy.assert_called_once_with('env')
                wrapper.Update.assert_called_once_with('proxy123',None)
            except AssertionError as e:
                self.fail(str(e))

    def test_update_env_from_vars_2(self):
        """_Arguments(decls).update_env_from_vars('env', variables, 'arg')"""
        args = SConsArguments._Arguments(self._decls_mock_4())
        args.VarEnvProxy = mock.Mock(name = 'VarEnvProxy', return_value = 'proxy123')
        with mock.patch('SConsArguments._VariablesWrapper') as WrapperClass:
            wrapper = WrapperClass.return_value
            wrapper.Update = mock.Mock(name = 'Update')
            args.update_env_from_vars('env', 'variables', 'args2')
            try:
                WrapperClass.assert_called_once_with('variables')
                args.VarEnvProxy.assert_called_once_with('env')
                wrapper.Update.assert_called_once_with('proxy123','args2')
            except AssertionError as e:
                self.fail(str(e))

    def test_update_env_from_opts_1(self):
        """_Arguments(decls).update_env_from_opts('env')"""
        proxy = { 'env1' : {} }
        def OptEnvProxy(arg): return proxy[arg]
        args = SConsArguments._Arguments(self._decls_mock_4())
        args.OptEnvProxy = mock.Mock(name = 'OptEnvProxy', side_effect = OptEnvProxy)
        with mock.patch('SCons.Script.Main.GetOption', side_effect = lambda key : 'val_%s' % key) as GetOption:
            args.update_env_from_opts('env1')
            try:
                GetOption.assert_called_once_with('opt_a')
            except AssertionError as e:
                self.fail(str(e))
            self.assertEqual(proxy['env1']['opt_a'], 'val_opt_a')

    def test_UpdateEnvironment_1(self):
        """_Arguments(decls).UpdateEnvironment('env') never calls update_env_from_{vars,opts}"""
        args = self._arguments_mock_4_UpdateEnvironment()
        args.UpdateEnvironment('env')
        try:
            args.update_env_from_vars.assert_not_called()
            args.update_env_from_opts.assert_not_called()
        except AssertionError as e:
            self.fail(str(e))

    def test_UpdateEnvironment_2(self):
        """_Arguments(decls).UpdateEnvironment('env','variables1') calls update_env_from_vars('env', 'variables1') once"""
        args = self._arguments_mock_4_UpdateEnvironment()
        args.UpdateEnvironment('env', 'variables1')
        try:
            args.update_env_from_vars.assert_called_once_with('env', 'variables1', None)
            args.update_env_from_opts.assert_not_called()
        except AssertionError as e:
            self.fail(str(e))

    def test_UpdateEnvironment_3(self):
        """_Arguments(decls).UpdateEnvironment('env',None,True) calls update_env_from_opts('env') once"""
        args = self._arguments_mock_4_UpdateEnvironment()
        args.UpdateEnvironment('env', None, True)
        try:
            args.update_env_from_vars.assert_not_called()
            args.update_env_from_opts.assert_called_once_with('env')
        except AssertionError as e:
            self.fail(str(e))

    def test_UpdateEnvironment_4(self):
        """_Arguments(decls).UpdateEnvironment('env','variables1',True) calls update_env_from_{opts,vars} once"""
        args = self._arguments_mock_4_UpdateEnvironment()
        args.UpdateEnvironment('env', 'variables1', True)
        try:
            args.update_env_from_vars.assert_called_once_with('env', 'variables1', None)
            args.update_env_from_opts.assert_called_once_with('env')
        except AssertionError as e:
            self.fail(str(e))

    def test_SaveVariables(self):
        """_Arguments(decls).SaveVariables(variables, 'filename1', 'env1')"""
        def VarEnvProxy(arg): return 'var_%s_proxy' % arg
        args = SConsArguments._Arguments(self._decls_mock_1())
        args.VarEnvProxy = mock.Mock(name = 'VarEnvProxy', side_effect = VarEnvProxy)
        variables = mock.Mock(name = 'variables')
        variables.Save = mock.Mock(name = 'Save')
        args.SaveVariables(variables, 'filename1', 'env1')
        try:
            variables.Save.assert_called_once_with('filename1','var_env1_proxy')
        except AssertionError as e:
            self.fail(str(e))

    def test_GenerateVariablesHelpText_1(self):
        """_Arguments(decls).GenerateVariablesHelpText(variables, 'env1')"""
        def VarEnvProxy(arg): return 'var_%s_proxy' % arg
        args = SConsArguments._Arguments(self._decls_mock_1())
        args.VarEnvProxy = mock.Mock(name = 'VarEnvProxy', side_effect = VarEnvProxy)
        variables = mock.Mock(name = 'variables')
        variables.GenerateHelpText = mock.Mock(name = 'GenerateHelpText')
        args.GenerateVariablesHelpText(variables, 'env1')
        try:
            variables.GenerateHelpText.assert_called_once_with('var_env1_proxy')
        except AssertionError as e:
            self.fail(str(e))

    def test_GenerateVariablesHelpText_2(self):
        """_Arguments(decls).GenerateVariablesHelpText(variables, 'env1', 'arg1', 'arg2')"""
        def VarEnvProxy(arg): return 'var_%s_proxy' % arg
        args = SConsArguments._Arguments(self._decls_mock_1())
        args.VarEnvProxy = mock.Mock(name = 'VarEnvProxy', side_effect = VarEnvProxy)
        variables = mock.Mock(name = 'variables')
        variables.GenerateHelpText = mock.Mock(name = 'GenerateHelpText')
        args.GenerateVariablesHelpText(variables, 'env1', 'arg1', 'arg2')
        try:
            variables.GenerateHelpText.assert_called_once_with('var_env1_proxy', 'arg1', 'arg2')
        except AssertionError as e:
            self.fail(str(e))

    def test_GetCurrentValues_1(self):
        """_Arguments(decls).GetCurrentValues(env) works as expected"""
        args = SConsArguments._Arguments(self._decls_mock_5())
        env = { 'env_k' : 'K', 'env_e' : 'E', 'env_x' : 'X' }
        current = args.GetCurrentValues(env)
        self.assertIs(current['env_k'], env['env_k'])
        self.assertIs(current['env_e'], env['env_e'])
        self.assertEqual(current, {'env_k' : 'K', 'env_e' : 'E'})

    def test__is_unaltered_1(self):
        """<_Arguments>._is_unaltered({}, {}, 'a') should be True"""
        self.assertTrue(SConsArguments._Arguments._is_unaltered({}, {}, 'a'))

    def test__is_unaltered_2(self):
        """<_Arguments>._is_unaltered({'a' : 'foo' }, {'a' : 'foo'}, 'a') should be True"""
        self.assertTrue(SConsArguments._Arguments._is_unaltered({'a' : 'foo'}, { 'a' : 'foo' }, 'a'))

    def test__is_unaltered_3(self):
        """<_Arguments>._is_unaltered({'a' : 'foo'}, {}, 'a') should be False"""
        self.assertFalse(SConsArguments._Arguments._is_unaltered({'a' : 'foo'}, {}, 'a'))

    def test__is_unaltered_4(self):
        """<_Arguments>._is_unaltered({}, {'a' : 'foo'}, 'a') should be False"""
        self.assertFalse(SConsArguments._Arguments._is_unaltered({'a' : 'foo'}, {}, 'a'))

    def test__is_unaltered_5(self):
        """<_Arguments>._is_unaltered({'a' : 'foo' }, {'a' : 'bar'}, 'a') should be False"""
        self.assertFalse(SConsArguments._Arguments._is_unaltered({'a' : 'foo'}, { 'a' : 'bar' }, 'a'))

    def test__is_unaltered_6(self):
        """<_Arguments>._is_unaltered({}, {'a' : None}, 'a') should be False"""
        self.assertFalse(SConsArguments._Arguments._is_unaltered({}, { 'a' : None }, 'a'))

    def test__is_unaltered_7(self):
        """<_Arguments>._is_unaltered({'a' : None}, {}, 'a') should be False"""
        self.assertFalse(SConsArguments._Arguments._is_unaltered({ 'a' : None }, {}, 'a'))

    def test_GetAltered_1(self):
        """Test <_Arguments>.GetAltered()"""
        args = SConsArguments._Arguments(self._decls_mock_5())
        env = { 'env_k' : 'K', 'env_e' : 'E', 'env_s' : None, 'env_x' : 'X' }
        org = { 'env_k' : 'k', 'env_e' : 'E' }
        altered = args.GetAltered(env, org)
        self.assertEqual(altered, {'env_k' : 'K', 'env_s' : None})

    def test_ReplaceUnaltered_1(self):
        """Test <_Arguments>.ReplaceUnaltered()"""
        args = SConsArguments._Arguments(self._decls_mock_5())
        env = { 'env_k' : 'K', 'env_e' : 'E', 'env_s' : None, 'env_x' : 'X' }
        org = { 'env_k' : 'k', 'env_e' : 'E' }
        new = { 'k' : 'new K', 'e' : 'new E', 's' : 'new S', 'x' : 'new X'}
        chg = args.ReplaceUnaltered(env, org, new)
        self.assertEqual(env, { 'env_k' : 'K', 'env_e' : 'new E', 'env_s' : None, 'env_x' : 'X' })
        self.assertEqual(chg, { 'env_e' : 'new E' })

    def test_WithUnalteredReplaced_1(self):
        """Test <_Arguments>.ReplaceUnaltered()"""
        args = SConsArguments._Arguments(self._decls_mock_5())
        env = { 'env_k' : 'K',      'env_e' : 'E',                      'env_x' : 'X'       }
        org = { 'env_k' : 'org K',  'env_e' : 'E',      'env_y' : 'y',                      }
        new = { 'k'     : 'new K',  'e'     : 'new E',                  'x'     : 'new X'   }
        ret = args.WithUnalteredReplaced(env, org, new)
        self.assertEqual(ret, { 'env_k' : 'K', 'env_e' : 'new E'              })
        self.assertEqual(env, { 'env_k' : 'K', 'env_e' : 'E',   'env_x' : 'X' })

    def test_Postprocess_1(self):
        """Test <_Arguments>.Postorpcess()"""
        class _test_alt(object): pass
        _test_alt.update = mock.Mock(name = 'update')
            
        args = SConsArguments._Arguments(self._decls_mock_5())
        args.GetCurrentValues = mock.Mock(name = 'GetCurrentValues', return_value  = 'org')
        args.UpdateEnvironment = mock.Mock(name = 'UpdateEnvironment')
        args.GetAltered = mock.Mock(name = 'GetAltered', return_value = _test_alt)
        args.SaveVariables = mock.Mock(name = 'SaveVariables')
        args.ReplaceUnaltered = mock.Mock(name = 'ReplaceUnaltered', return_value = 'chg')

        args.Postprocess('env', 'variables', 'options', 'ose', 'args', 'filename')

        args.GetCurrentValues.assert_called_once_with('env')
        args.UpdateEnvironment.assert_called_once_with('env', 'variables', 'options', 'args')
        args.GetAltered.assert_called_once_with('env', 'org')
        args.SaveVariables.assert_called_once_with('variables', 'filename', 'env')
        args.ReplaceUnaltered.assert_called_once_with('env', 'org', 'ose')
        _test_alt.update.assert_called_once_with('chg')

    def test_Demangle_1(self):
        """Test <_Arguments>.Demangle()"""
        args = SConsArguments._Arguments(self._decls_mock_5())
        env = { 'env_k' : 'K', 'env_e' : 'E', 'env_s' : None, 'env_x' : 'X' }
        res = args.Demangle(env)
        self.assertEqual(res, { 'k' : 'K', 'e' : 'E', 's' : None })

#############################################################################
class Test__ArgumentDecl(unittest.TestCase):
    def test___init___1(self):
        """_ArgumentDecl.__init__() should not call any of _set_XXX_decl()"""
        with mock.patch.object(SConsArguments._ArgumentDecl, 'set_env_decl') as m_env, \
             mock.patch.object(SConsArguments._ArgumentDecl, 'set_var_decl') as m_var, \
             mock.patch.object(SConsArguments._ArgumentDecl, 'set_opt_decl') as m_opt:
            decl = SConsArguments._ArgumentDecl()
            try:
                m_env.assert_not_called()
                m_var.assert_not_called()
                m_opt.assert_not_called()
            except AssertionError as e:
                self.fail(str(e))

    def test___init___2(self):
        """_ArgumentDecl.__init__() should set __decl_tab to [None, None, None]"""
        with mock.patch.object(SConsArguments._ArgumentDecl, '_ArgumentDecl__decl_tab', create=True) as m:
            decl = SConsArguments._ArgumentDecl()
            self.assertEqual(len(decl._ArgumentDecl__decl_tab), SConsArguments.ALL)
            self.assertIs(decl._ArgumentDecl__decl_tab[SConsArguments.ENV], None)
            self.assertIs(decl._ArgumentDecl__decl_tab[SConsArguments.VAR], None)
            self.assertIs(decl._ArgumentDecl__decl_tab[SConsArguments.OPT], None)

    def test___init___3(self):
        """_ArgumentDecl.__init__('a', 'b', 'c') should call of set_env_decl('a'), set_var_decl('b'), set_opt_decl('c')"""
        with mock.patch.object(SConsArguments._ArgumentDecl, 'set_env_decl', autospec=True) as m_env, \
             mock.patch.object(SConsArguments._ArgumentDecl, 'set_var_decl', autospec=True) as m_var, \
             mock.patch.object(SConsArguments._ArgumentDecl, 'set_opt_decl', autospec=True) as m_opt:
            decl = SConsArguments._ArgumentDecl('a', 'b', 'c')
            try:
                m_env.assert_called_once_with(decl,'a')
                m_var.assert_called_once_with(decl,'b')
                m_opt.assert_called_once_with(decl,'c')
            except AssertionError as e:
                self.fail(str(e))

    def test_set_decl_1(self):
        """<_ArgumentDecl>.set_decl(123,'a') should raise IndexError"""
        decl = SConsArguments._ArgumentDecl()
        with self.assertRaises(IndexError):
            decl.set_decl(123,'a')

    def test_set_decl__ENV(self):
        """<_ArgumentDecl>.set_decl(ENV,'a') should call set_env_decl('a')"""
        decl = SConsArguments._ArgumentDecl()
        decl.set_env_decl = mock.Mock(name='set_env_decl')
        decl.set_var_decl = mock.Mock(name='set_var_decl')
        decl.set_opt_decl = mock.Mock(name='set_opt_decl')
        decl.set_decl(SConsArguments.ENV, 'a')
        try:
            decl.set_env_decl.assert_called_once_with('a')
            decl.set_var_decl.assert_not_called()
            decl.set_opt_decl.assert_not_called()
        except AssertionError as e:
            self.fail(str(e))

    def test_set_decl__VAR(self):
        """<_ArgumentDecl>.set_decl(VAR,'b') should call set_var_decl('b')"""
        decl = SConsArguments._ArgumentDecl()
        decl.set_env_decl = mock.Mock(name='set_env_decl')
        decl.set_var_decl = mock.Mock(name='set_var_decl')
        decl.set_opt_decl = mock.Mock(name='set_opt_decl')
        decl.set_decl(SConsArguments.VAR, 'b')
        try:
            decl.set_env_decl.assert_not_called()
            decl.set_var_decl.assert_called_once_with('b')
            decl.set_opt_decl.assert_not_called()
        except AssertionError as e:
            self.fail(str(e))

    def test_set_decl__OPT(self):
        """<_ArgumentDecl>.set_decl(OPT,'a') should call set_opt_decl('a')"""
        decl = SConsArguments._ArgumentDecl()
        decl.set_env_decl = mock.Mock(name='set_env_decl')
        decl.set_var_decl = mock.Mock(name='set_var_decl')
        decl.set_opt_decl = mock.Mock(name='set_opt_decl')
        decl.set_decl(SConsArguments.OPT, 'a')
        try:
            decl.set_env_decl.assert_not_called()
            decl.set_var_decl.assert_not_called()
            decl.set_opt_decl.assert_called_once_with('a')
        except AssertionError as e:
            self.fail(str(e))

    def test_set_env_decl__tuple_ValueError_1(self):
        """<_ArgumentDecl>.set_env_decl(tuple()) should raise ValueError"""
        decl = SConsArguments._ArgumentDecl()
        with self.assertRaises(ValueError):
            decl.set_env_decl(tuple())

    def test_set_env_decl__tuple_ValueError_2(self):
        """<_ArgumentDecl>.set_env_decl(('a',)) should raise ValueError"""
        decl = SConsArguments._ArgumentDecl()
        with self.assertRaises(ValueError):
            decl.set_env_decl(('a',))

    def test_set_env_decl__tuple_1(self):
        """<_ArgumentDecl>.set_env_decl(('A','B')) should set __decl_tab[ENV] to {'key' : 'A', 'default' : 'B'}"""
        decl = SConsArguments._ArgumentDecl()
        decl.set_env_decl(('A','B'))
        self.assertEqual(decl._ArgumentDecl__decl_tab[SConsArguments.ENV], {'key' : 'A', 'default' : 'B'})

    def test_set_env_decl__dict_ValueError_1(self):
        """<_ArgumentDecl>.set_env_decl(dict()) should raise ValueError"""
        decl = SConsArguments._ArgumentDecl()
        with self.assertRaises(ValueError):
            decl.set_env_decl(dict())

    def test_set_env_decl__dict_ValueError_2(self):
        """<_ArgumentDecl>.set_env_decl({'a' : 'A', 'b' : 'B'}) should raise ValueError"""
        decl = SConsArguments._ArgumentDecl()
        with self.assertRaises(ValueError):
            decl.set_env_decl({'a' : 'A', 'b' : 'B'})

    def test_set_env_decl__dict_TypeError_1(self):
        """<_ArgumentDecl>.set_env_decl(None) should raise TypeError"""
        decl = SConsArguments._ArgumentDecl()
        with self.assertRaises(TypeError):
            decl.set_env_decl(None)

    def test_set_env_decl__dict_TypeError_2(self):
        """<_ArgumentDecl>.set_env_decl(123) should raise TypeError"""
        decl = SConsArguments._ArgumentDecl()
        with self.assertRaises(TypeError):
            decl.set_env_decl(123)

    def test_set_env_decl__dict_1(self):
        """<_ArgumentDecl>.set_env_decl({'a':'A'}) should set __decl_tab[ENV] to {'key' : 'a', 'default' : 'A'}"""
        decl = SConsArguments._ArgumentDecl()
        decl.set_env_decl({'a':'A'})
        self.assertEqual(decl._ArgumentDecl__decl_tab[SConsArguments.ENV], {'key' : 'a', 'default' : 'A'})

    def test_set_env_decl__string_1(self):
        """<_ArgumentDecl>.set_env_decl('foo') should set __decl_tab[ENV] to {'key' : 'foo', 'default' : _undef}"""
        decl = SConsArguments._ArgumentDecl()
        decl.set_env_decl('foo')
        self.assertEqual(decl._ArgumentDecl__decl_tab[SConsArguments.ENV], {'key' : 'foo', 'default' : SConsArguments._undef})

    def test_set_var_decl__ValueError_1(self):
        """<_ArgumentDecl>.set_var_decl((1, 2, 3, 4, 5, 6, 7)) should raise ValueError"""
        decl = SConsArguments._ArgumentDecl()
        with self.assertRaises(ValueError):
            decl.set_var_decl((1,2,3,4,5,6,7))

    def test_set_var_decl__ValueError_2(self):
        """<_ArgumentDecl>.set_var_decl([1, 2, 3, 4, 5, 6, 7]) should raise ValueError"""
        decl = SConsArguments._ArgumentDecl()
        with self.assertRaises(ValueError):
            decl.set_var_decl([1,2,3,4,5,6,7])

    def test_set_var_decl__TypeError_1(self):
        """<_ArgumentDecl>.set_var_decl(None) should raise TypeError"""
        decl = SConsArguments._ArgumentDecl()
        with self.assertRaises(TypeError):
            decl.set_var_decl(None)

    def test_set_var_decl__TypeError_2(self):
        """<_ArgumentDecl>.set_var_decl("foo") should raise TypeError"""
        decl = SConsArguments._ArgumentDecl()
        with self.assertRaises(TypeError):
            decl.set_var_decl("foo")

    def test_set_var_decl__TypeError_3(self):
        """<_ArgumentDecl>.set_var_decl(123) should raise TypeError"""
        decl = SConsArguments._ArgumentDecl()
        with self.assertRaises(TypeError):
            decl.set_var_decl(123)

    def test_set_var_decl__TypeError_4(self):
        """<_ArgumentDecl>.set_var_decl({'kw' : None}) should raise TypeError"""
        decl = SConsArguments._ArgumentDecl()
        with self.assertRaises(TypeError):
            decl.set_var_decl({'kw' : None})

    def test_set_var_decl__TypeError_4(self):
        """<_ArgumentDecl>.set_var_decl({'kw' : 'foo'}) should raise TypeError"""
        decl = SConsArguments._ArgumentDecl()
        with self.assertRaises(TypeError):
            decl.set_var_decl({'kw' : 'foo'})

    def test_set_var_decl__TypeError_5(self):
        """<_ArgumentDecl>.set_var_decl({'kw' : 123}) should raise TypeError"""
        decl = SConsArguments._ArgumentDecl()
        with self.assertRaises(TypeError):
            decl.set_var_decl({'kw' : 123})

    def test_set_var_decl__tuple_0(self):
        """<_ArgumentDecl>.set_var_decl(tuple()) should set __decl_tab[VAR] = {}"""
        decl = SConsArguments._ArgumentDecl()
        decl.set_var_decl(tuple())
        self.assertEqual(decl._ArgumentDecl__decl_tab[SConsArguments.VAR], {})

    def test_set_var_decl__tuple_1(self):
        """<_ArgumentDecl>.set_var_decl(('K',)) should set __decl_tab[VAR] = {'key' : 'K'}"""
        decl = SConsArguments._ArgumentDecl()
        decl.set_var_decl(('K',))
        self.assertEqual(decl._ArgumentDecl__decl_tab[SConsArguments.VAR], {'key' : 'K'})

    def test_set_var_decl__tuple_2(self):
        """<_ArgumentDecl>.set_var_decl(('K','H')) should set __decl_tab[VAR] = {'key' : 'K', 'help' : 'H'}"""
        decl = SConsArguments._ArgumentDecl()
        decl.set_var_decl(('K','H'))
        self.assertEqual(decl._ArgumentDecl__decl_tab[SConsArguments.VAR], {'key' : 'K', 'help' : 'H'})

    def test_set_var_decl__tuple_3(self):
        """<_ArgumentDecl>.set_var_decl(('K','H','D')) should set __decl_tab[VAR] = {'key' : 'K', 'help' : 'H', 'default' : 'D'}"""
        decl = SConsArguments._ArgumentDecl()
        decl.set_var_decl(('K','H', 'D'))
        self.assertEqual(decl._ArgumentDecl__decl_tab[SConsArguments.VAR], {'key' : 'K', 'help' : 'H', 'default' : 'D'})

    def test_set_var_decl__tuple_4(self):
        """<_ArgumentDecl>.set_var_decl(('K','H','D','V')) should set __decl_tab[VAR] = {'key' : 'K', 'help' : 'H', 'default' : 'D', 'validator' : 'V'}"""
        decl = SConsArguments._ArgumentDecl()
        decl.set_var_decl(('K','H','D','V'))
        self.assertEqual(decl._ArgumentDecl__decl_tab[SConsArguments.VAR], {'key' : 'K', 'help' : 'H', 'default' : 'D', 'validator' : 'V'})

    def test_set_var_decl__tuple_5(self):
        """<_ArgumentDecl>.set_var_decl(('K','H','D','V','C')) should set __decl_tab[VAR] = {'key' : 'K', 'help' : 'H', 'default' : 'D', 'validator' : 'V', 'converter' : 'C'}"""
        decl = SConsArguments._ArgumentDecl()
        decl.set_var_decl(('K','H','D','V','C'))
        self.assertEqual(decl._ArgumentDecl__decl_tab[SConsArguments.VAR], {'key' : 'K', 'help' : 'H', 'default' : 'D', 'validator' : 'V', 'converter' : 'C'})

    def test_set_var_decl__tuple_6(self):
        """<_ArgumentDecl>.set_var_decl(('K','H','D','V','C',{'a':'A'})) should set __decl_tab[VAR] = {'key' : 'K', 'help' : 'H', 'default' : 'D', 'validator' : 'V', 'converter' : 'C', 'a' : 'A'}"""
        decl = SConsArguments._ArgumentDecl()
        decl.set_var_decl(('K','H','D','V','C',{'a':'A'}))
        self.assertEqual(decl._ArgumentDecl__decl_tab[SConsArguments.VAR], {'key' : 'K', 'help' : 'H', 'default' : 'D', 'validator' : 'V', 'converter' : 'C', 'a' : 'A'})

    def test_set_var_decl__list_0(self):
        """<_ArgumentDecl>.set_var_decl(list()) should set __decl_tab[VAR] = {}"""
        decl = SConsArguments._ArgumentDecl()
        decl.set_var_decl(list())
        self.assertEqual(decl._ArgumentDecl__decl_tab[SConsArguments.VAR], {})

    def test_set_var_decl__list_1(self):
        """<_ArgumentDecl>.set_var_decl(['K']) should set __decl_tab[VAR] = {'key' : 'K'}"""
        decl = SConsArguments._ArgumentDecl()
        decl.set_var_decl(['K'])
        self.assertEqual(decl._ArgumentDecl__decl_tab[SConsArguments.VAR], {'key' : 'K'})

    def test_set_var_decl__list_2(self):
        """<_ArgumentDecl>.set_var_decl(['K','H']) should set __decl_tab[VAR] = {'key' : 'K', 'help' : 'H'}"""
        decl = SConsArguments._ArgumentDecl()
        decl.set_var_decl(['K','H'])
        self.assertEqual(decl._ArgumentDecl__decl_tab[SConsArguments.VAR], {'key' : 'K', 'help' : 'H'})

    def test_set_var_decl__list_3(self):
        """<_ArgumentDecl>.set_var_decl(['K','H','D']) should set __decl_tab[VAR] = {'key' : 'K', 'help' : 'H', 'default' : 'D'}"""
        decl = SConsArguments._ArgumentDecl()
        decl.set_var_decl(['K','H', 'D'])
        self.assertEqual(decl._ArgumentDecl__decl_tab[SConsArguments.VAR], {'key' : 'K', 'help' : 'H', 'default' : 'D'})

    def test_set_var_decl__list_4(self):
        """<_ArgumentDecl>.set_var_decl(['K','H','D','V']) should set __decl_tab[VAR] = {'key' : 'K', 'help' : 'H', 'default' : 'D', 'validator' : 'V'}"""
        decl = SConsArguments._ArgumentDecl()
        decl.set_var_decl(['K','H','D','V'])
        self.assertEqual(decl._ArgumentDecl__decl_tab[SConsArguments.VAR], {'key' : 'K', 'help' : 'H', 'default' : 'D', 'validator' : 'V'})

    def test_set_var_decl__list_5(self):
        """<_ArgumentDecl>.set_var_decl(['K','H','D','V','C']) should set __decl_tab[VAR] = {'key' : 'K', 'help' : 'H', 'default' : 'D', 'validator' : 'V', 'converter' : 'C'}"""
        decl = SConsArguments._ArgumentDecl()
        decl.set_var_decl(['K','H','D','V','C'])
        self.assertEqual(decl._ArgumentDecl__decl_tab[SConsArguments.VAR], {'key' : 'K', 'help' : 'H', 'default' : 'D', 'validator' : 'V', 'converter' : 'C'})

    def test_set_var_decl__list_6(self):
        """<_ArgumentDecl>.set_var_decl(['K','H','D','V','C',{'a':'A'}]) should set __decl_tab[VAR] = {'key' : 'K', 'help' : 'H', 'default' : 'D', 'validator' : 'V', 'converter' : 'C', 'a' : 'A'}"""
        decl = SConsArguments._ArgumentDecl()
        decl.set_var_decl(['K','H','D','V','C',{'a':'A'}])
        self.assertEqual(decl._ArgumentDecl__decl_tab[SConsArguments.VAR], {'key' : 'K', 'help' : 'H', 'default' : 'D', 'validator' : 'V', 'converter' : 'C', 'a' : 'A'})

    def test_set_opt_decl__ValueError_1(self):
        """<_ArgumentDecl>.set_opt_decl(tuple()) should raise ValueError"""
        empty = tuple()
        decl = SConsArguments._ArgumentDecl()
        with self.assertRaises(ValueError) as cm:
            decl.set_opt_decl(empty)
        self.assertEqual(str(cm.exception), "'decl' must not be empty, got %(empty)r" % locals())

    def test_set_opt_decl__ValueError_2(self):
        """<_ArgumentDecl>.set_opt_decl(('--foo',)) should raise ValueError"""
        decl = SConsArguments._ArgumentDecl()
        with self.assertRaises(ValueError) as cm:
            decl.set_opt_decl(('-foo',))
        self.assertEqual(str(cm.exception), "missing parameter 'dest' in option specification")

    def test_set_opt_decl__ValueError_3(self):
        """<_ArgumentDecl>.set_opt_decl(['--foo']) should raise ValueError"""
        decl = SConsArguments._ArgumentDecl()
        with self.assertRaises(ValueError) as cm:
            decl.set_opt_decl(['-foo'])
        self.assertEqual(str(cm.exception), "missing parameter 'dest' in option specification")

    def test_set_opt_decl__ValueError_4(self):
        """<_ArgumentDecl>.set_opt_decl({'names' : '--foo'}) should raise ValueError (missing 'dest')"""
        decl = SConsArguments._ArgumentDecl()
        with self.assertRaises(ValueError) as cm:
            decl.set_opt_decl({'names' : '--foo'})
        self.assertEqual(str(cm.exception), "missing parameter 'dest' in option specification")

    def test_set_opt_decl__KeyError_1(self):
        """<_ArgumentDecl>.set_opt_decl(dict()) should raise KeyError"""
        decl = SConsArguments._ArgumentDecl()
        with self.assertRaises(KeyError):
            decl.set_opt_decl(dict())

    def test_set_opt_decl__TypeError_1(self):
        """<_ArgumentDecl>.set_opt_decl((None,)) should raise TypeError"""
        decl = SConsArguments._ArgumentDecl()
        with self.assertRaises(TypeError):
            decl.set_opt_decl((None,))

    def test_set_opt_decl__TypeError_2(self):
        """<_ArgumentDecl>.set_opt_decl((123,)) should raise TypeError"""
        decl = SConsArguments._ArgumentDecl()
        with self.assertRaises(TypeError):
            decl.set_opt_decl((123,))

    def test_set_opt_decl__TypeError_3(self):
        """<_ArgumentDecl>.set_opt_decl({'names' : None)) should raise TypeError"""
        decl = SConsArguments._ArgumentDecl()
        with self.assertRaises(TypeError):
            decl.set_opt_decl({'names' : None})

    def test_set_opt_decl__TypeError_4(self):
        """<_ArgumentDecl>.set_opt_decl({'names' : 123}) should raise TypeError"""
        decl = SConsArguments._ArgumentDecl()
        with self.assertRaises(TypeError):
            decl.set_opt_decl({'names' : 123})

    def test_set_opt_decl__TypeError_5(self):
        """<_ArgumentDecl>.set_opt_decl(None) should raise TypeError"""
        decl = SConsArguments._ArgumentDecl()
        with self.assertRaises(TypeError):
            decl.set_opt_decl(None)

    def test_set_opt_decl__TypeError_6(self):
        """<_ArgumentDecl>.set_opt_decl('foo') should raise TypeError"""
        decl = SConsArguments._ArgumentDecl()
        with self.assertRaises(TypeError):
            decl.set_opt_decl('foo')

    def test_set_opt_decl__TypeError_7(self):
        """<_ArgumentDecl>.set_opt_decl(123) should raise TypeError"""
        decl = SConsArguments._ArgumentDecl()
        with self.assertRaises(TypeError):
            decl.set_opt_decl(123)

    def test_set_opt_decl__tuple_1(self):
        """<_ArgumentDecl>.set_opt_decl(('--foo', {'dest' : 'foo'})) sets __decl_tab[OPT] = (('--foo',), {'dest' : 'foo'})"""
        decl = SConsArguments._ArgumentDecl()
        decl.set_opt_decl(('--foo', {'dest' : 'foo'}))
        self.assertEqual(decl._ArgumentDecl__decl_tab[SConsArguments.OPT], (('--foo',), {'dest' : 'foo'}))

    def test_set_opt_decl__tuple_2(self):
        """<_ArgumentDecl>.set_opt_decl(('--foo -f', {'dest' : 'foo'})) sets __decl_tab[OPT] = (('--foo','-f'), {'dest' : 'foo'})"""
        decl = SConsArguments._ArgumentDecl()
        decl.set_opt_decl(('--foo -f', {'dest' : 'foo'}))
        self.assertEqual(decl._ArgumentDecl__decl_tab[SConsArguments.OPT], (('--foo','-f'), {'dest' : 'foo'}))

    def test_set_opt_decl__tuple_3(self):
        """<_ArgumentDecl>.set_opt_decl((('--foo','-f'), {'dest' : 'foo'})) sets __decl_tab[OPT] = (('--foo','-f'), {'dest' : 'foo'})"""
        decl = SConsArguments._ArgumentDecl()
        decl.set_opt_decl((('--foo', '-f'), {'dest' : 'foo'}))
        self.assertEqual(decl._ArgumentDecl__decl_tab[SConsArguments.OPT], (('--foo','-f'), {'dest' : 'foo'}))

    def test_set_opt_decl__tuple_4(self):
        """<_ArgumentDecl>.set_opt_decl((['--foo','-f'], {'dest' : 'foo'})) sets __decl_tab[OPT] = (('--foo','-f'), {'dest' : 'foo'})"""
        decl = SConsArguments._ArgumentDecl()
        decl.set_opt_decl((['--foo', '-f'], {'dest' : 'foo'}))
        self.assertEqual(decl._ArgumentDecl__decl_tab[SConsArguments.OPT], (('--foo','-f'), {'dest' : 'foo'}))

    def test_set_opt_decl__list_1(self):
        """<_ArgumentDecl>.set_opt_decl(['--foo', {'dest' : 'foo'}]) sets __decl_tab[OPT] = (('--foo',), {'dest' : 'foo'})"""
        decl = SConsArguments._ArgumentDecl()
        decl.set_opt_decl(['--foo', {'dest' : 'foo'}])
        self.assertEqual(decl._ArgumentDecl__decl_tab[SConsArguments.OPT], (('--foo',), {'dest' : 'foo'}))

    def test_set_opt_decl__list_2(self):
        """<_ArgumentDecl>.set_opt_decl(['--foo -f', {'dest' : 'foo'}]) sets __decl_tab[OPT] = (('--foo','-f'), {'dest' : 'foo'})"""
        decl = SConsArguments._ArgumentDecl()
        decl.set_opt_decl(['--foo -f', {'dest' : 'foo'}])
        self.assertEqual(decl._ArgumentDecl__decl_tab[SConsArguments.OPT], (('--foo','-f'), {'dest' : 'foo'}))

    def test_set_opt_decl__list_3(self):
        """<_ArgumentDecl>.set_opt_decl([('--foo','-f'), {'dest' : 'foo'}]) sets __decl_tab[OPT] = (('--foo','-f'), {'dest' : 'foo'})"""
        decl = SConsArguments._ArgumentDecl()
        decl.set_opt_decl([('--foo', '-f'), {'dest' : 'foo'}])
        self.assertEqual(decl._ArgumentDecl__decl_tab[SConsArguments.OPT], (('--foo','-f'), {'dest' : 'foo'}))

    def test_set_opt_decl__list_4(self):
        """<_ArgumentDecl>.set_opt_decl([['--foo','-f'], {'dest' : 'foo'}]) sets __decl_tab[OPT] = (('--foo','-f'), {'dest' : 'foo'})"""
        decl = SConsArguments._ArgumentDecl()
        decl.set_opt_decl([['--foo', '-f'], {'dest' : 'foo'}])
        self.assertEqual(decl._ArgumentDecl__decl_tab[SConsArguments.OPT], (('--foo','-f'), {'dest' : 'foo'}))

    def test_set_opt_decl__dict_1(self):
        """<_ArgumentDecl>.set_opt_decl({'names' : '--foo', 'dest' : 'foo'}) sets __decl_tab[OPT] = (('--foo',), {'dest' : 'foo'})"""
        decl = SConsArguments._ArgumentDecl()
        decl.set_opt_decl({'names' : '--foo', 'dest' : 'foo'})
        self.assertEqual(decl._ArgumentDecl__decl_tab[SConsArguments.OPT], (('--foo',), {'dest' : 'foo'}))

    def test_set_opt_decl__dict_2(self):
        """<_ArgumentDecl>.set_opt_decl({'names' : '--foo -f', 'dest' : 'foo'}) sets __decl_tab[OPT] = (('--foo','-f'), {'dest' : 'foo'})"""
        decl = SConsArguments._ArgumentDecl()
        decl.set_opt_decl({'names' : '--foo -f', 'dest' : 'foo'})
        self.assertEqual(decl._ArgumentDecl__decl_tab[SConsArguments.OPT], (('--foo','-f'), {'dest' : 'foo'}))

    def test_set_opt_decl__dict_3(self):
        """<_ArgumentDecl>.set_opt_decl({'names' : ('--foo','-f'), 'dest' : 'foo'}) sets __decl_tab[OPT] = (('--foo','-f'), {'dest' : 'foo'})"""
        decl = SConsArguments._ArgumentDecl()
        decl.set_opt_decl({'names' : ('--foo', '-f'), 'dest' : 'foo'})
        self.assertEqual(decl._ArgumentDecl__decl_tab[SConsArguments.OPT], (('--foo','-f'), {'dest' : 'foo'}))

    def test_set_opt_decl__dict_4(self):
        """<_ArgumentDecl>.set_opt_decl({'names' : ['--foo','-f'], 'dest' : 'foo'}) sets __decl_tab[OPT] = (('--foo','-f'), {'dest' : 'foo'})"""
        decl = SConsArguments._ArgumentDecl()
        decl.set_opt_decl({'names' : ['--foo', '-f'], 'dest' : 'foo'})
        self.assertEqual(decl._ArgumentDecl__decl_tab[SConsArguments.OPT], (('--foo','-f'), {'dest' : 'foo'}))

    def test_has_decl_0(self):
        """_ArgumentDecl().has_decl(...) should always return False"""
        self.assertFalse(SConsArguments._ArgumentDecl().has_decl(SConsArguments.ENV))
        self.assertFalse(SConsArguments._ArgumentDecl().has_decl(SConsArguments.VAR))
        self.assertFalse(SConsArguments._ArgumentDecl().has_decl(SConsArguments.OPT))

    def test_has_decl_ENV_1(self):
        """<_ArgumentDecl>.has_decl(EVN) should return true when ENV declaration was provided"""
        decl = SConsArguments._ArgumentDecl()
        decl.set_env_decl({'FOO' : 123})
        self.assertTrue(decl.has_decl(SConsArguments.ENV))
        self.assertFalse(decl.has_decl(SConsArguments.VAR))
        self.assertFalse(decl.has_decl(SConsArguments.OPT))

    def test_has_decl_VAR_1(self):
        """<_ArgumentDecl>.has_decl(VAR) should return true when VAR declaration was provided"""
        decl = SConsArguments._ArgumentDecl()
        decl.set_var_decl(('FOO',))
        self.assertFalse(decl.has_decl(SConsArguments.ENV))
        self.assertTrue(decl.has_decl(SConsArguments.VAR))
        self.assertFalse(decl.has_decl(SConsArguments.OPT))

    def test_has_decl_OPT_1(self):
        """<_ArgumentDecl>.has_decl(EVN) should return true when OPT declaration was provided"""
        decl = SConsArguments._ArgumentDecl()
        decl.set_opt_decl(('--foo', {'dest' : 'foo'}))
        self.assertFalse(decl.has_decl(SConsArguments.ENV))
        self.assertFalse(decl.has_decl(SConsArguments.VAR))
        self.assertTrue(decl.has_decl(SConsArguments.OPT))

    def test_has_env_decl_1(self):
        """<_ArgumentDecl>.has_env_decl() should invoke has_decl(ENV)"""
        class _test_val: pass
        decl = SConsArguments._ArgumentDecl()
        decl.has_decl = mock.Mock(name = 'has_decl', return_value = _test_val)
        ret = decl.has_env_decl()
        self.assertIs(ret, _test_val)
        try:
            decl.has_decl.assert_called_once_with(SConsArguments.ENV)
        except AssertionError as e:
            self.fail(str(e))

    def test_has_var_decl_1(self):
        """<_ArgumentDecl>.has_var_decl() should invoke has_decl(VAR)"""
        class _test_val: pass
        decl = SConsArguments._ArgumentDecl()
        decl.has_decl = mock.Mock(name = 'has_decl', return_value = _test_val)
        ret = decl.has_var_decl()
        self.assertIs(ret, _test_val)
        try:
            decl.has_decl.assert_called_once_with(SConsArguments.VAR)
        except AssertionError as e:
            self.fail(str(e))

    def test_has_opt_decl_1(self):
        """<_ArgumentDecl>.has_opt_decl() should invoke has_decl(OPT)"""
        class _test_val: pass
        decl = SConsArguments._ArgumentDecl()
        decl.has_decl = mock.Mock(name = 'has_decl', return_value = _test_val)
        ret = decl.has_opt_decl()
        self.assertIs(ret, _test_val)
        try:
            decl.has_decl.assert_called_once_with(SConsArguments.OPT)
        except AssertionError as e:
            self.fail(str(e))

    def test_get_decl__123_IndexError_1(self):
        """<_ArgumentDecl>.get_decl(123) should raise IndexError"""
        with self.assertRaises(IndexError):
            SConsArguments._ArgumentDecl(env_decl = {'a' : 'A'}).get_decl(123)

    def test_get_decl__ENV_IndexError(self):
        """_ArgumentDecl().get_decl(ENV) should raise IndexError"""
        with self.assertRaises(IndexError):
            SConsArguments._ArgumentDecl().get_decl(SConsArguments.ENV)

    def test_get_decl__VAR_IndexError(self):
        """_ArgumentDecl().get_decl(VAR) should raise IndexError"""
        with self.assertRaises(IndexError):
            SConsArguments._ArgumentDecl().get_decl(SConsArguments.VAR)

    def test_get_decl__OPT_IndexError(self):
        """_ArgumentDecl().get_decl(OPT) should raise IndexError"""
        with self.assertRaises(IndexError):
            SConsArguments._ArgumentDecl().get_decl(SConsArguments.OPT)

    def test_get_decl__ENV_1(self):
        """<_ArgumentDecl>.get_decl(ENV) should return __decl_tab[ENV]"""
        class _test_val: pass
        decl = SConsArguments._ArgumentDecl()
        decl._ArgumentDecl__decl_tab[SConsArguments.ENV] = _test_val
        self.assertIs(decl.get_decl(SConsArguments.ENV), _test_val)

    def test_get_decl__VAR_1(self):
        """<_ArgumentDecl>.get_decl(VAR) should return __decl_tab[VAR]"""
        class _test_val: pass
        decl = SConsArguments._ArgumentDecl()
        decl._ArgumentDecl__decl_tab[SConsArguments.VAR] = _test_val
        self.assertIs(decl.get_decl(SConsArguments.VAR), _test_val)

    def test_get_decl__OPT_1(self):
        """<_ArgumentDecl>.get_decl(OPT) should return __decl_tab[OPT]"""
        class _test_val: pass
        decl = SConsArguments._ArgumentDecl()
        decl._ArgumentDecl__decl_tab[SConsArguments.OPT] = _test_val
        self.assertIs(decl.get_decl(SConsArguments.OPT), _test_val)

    def test_get_key__123_IndexError_1(self):
        """<_ArgumentDecl>.get_key(123) should raise IndexError"""
        decl = SConsArguments._ArgumentDecl()
        with self.assertRaises(IndexError) as cm:
            decl.get_key(123)
        self.assertEqual(str(cm.exception), "index out of range")

    def test_get_env_decl_1(self):
        """<_ArgumentDecl>.get_env_decl() should invoke get_decl(ENV)"""
        class _test_val: pass
        decl = SConsArguments._ArgumentDecl()
        decl.get_decl = mock.Mock(name = 'get_decl', return_value = _test_val)
        ret = decl.get_env_decl()
        self.assertIs(ret, _test_val)
        try:
            decl.get_decl.assert_called_once_with(SConsArguments.ENV)
        except AssertionError as e:
            self.fail(str(e))

    def test_get_var_decl_1(self):
        """<_ArgumentDecl>.get_var_decl() should invoke get_decl(VAR)"""
        class _test_val: pass
        decl = SConsArguments._ArgumentDecl()
        decl.get_decl = mock.Mock(name = 'get_decl', return_value = _test_val)
        ret = decl.get_var_decl()
        self.assertIs(ret, _test_val)
        try:
            decl.get_decl.assert_called_once_with(SConsArguments.VAR)
        except AssertionError as e:
            self.fail(str(e))

    def test_get_opt_decl_1(self):
        """<_ArgumentDecl>.get_opt_decl() should invoke get_decl(OPT)"""
        class _test_val: pass
        decl = SConsArguments._ArgumentDecl()
        decl.get_decl = mock.Mock(name = 'get_decl', return_value = _test_val)
        ret = decl.get_opt_decl()
        self.assertIs(ret, _test_val)
        try:
            decl.get_decl.assert_called_once_with(SConsArguments.OPT)
        except AssertionError as e:
            self.fail(str(e))

    def test_get_key__ENV_IndexError_1(self):
        """_ArgumentDecl().get_key(ENV) should raise IndexError"""
        with self.assertRaises(IndexError):
            SConsArguments._ArgumentDecl().get_key(SConsArguments.ENV)

    def test_get_key__VAR_IndexError_1(self):
        """_ArgumentDecl().get_key(VAR) should raise IndexError"""
        with self.assertRaises(IndexError):
            SConsArguments._ArgumentDecl().get_key(SConsArguments.VAR)

    def test_get_key__OPT_IndexError_1(self):
        """_ArgumentDecl().get_key(OPT) should raise IndexError"""
        with self.assertRaises(IndexError):
            SConsArguments._ArgumentDecl().get_key(SConsArguments.OPT)

    def test_get_key__ENV_1(self):
        """_ArgumentDecl({'ENV_FOO' : 1}).get_key(ENV) should return 'ENV_FOO'"""
        self.assertEqual(SConsArguments._ArgumentDecl({'ENV_FOO' : 1}).get_key(SConsArguments.ENV), 'ENV_FOO')

    def test_get_key__VAR_1(self):
        """_ArgumentDecl(var_decl = ('VAR_FOO',)).get_key(VAR) should return 'VAR_FOO'"""
        self.assertEqual(SConsArguments._ArgumentDecl(var_decl = ('VAR_FOO',)).get_key(SConsArguments.VAR), 'VAR_FOO')

    def test_get_key__OPT_1(self):
        """_ArgumentDecl(opt_decl = ('--foo', {'dest' : 'OPT_FOO'})).get_key(OPT) should return 'OPT_FOO'"""
        self.assertEqual(SConsArguments._ArgumentDecl(opt_decl = ('--foo', {'dest' : 'OPT_FOO'})).get_key(SConsArguments.OPT), 'OPT_FOO')

    def test_get_env_key_1(self):
        """<_ArgumentDecl>.get_env_key() should invoke get_key(ENV)"""
        class _test_val: pass
        decl = SConsArguments._ArgumentDecl()
        decl.get_key = mock.Mock(name = 'get_key', return_value = _test_val)
        ret = decl.get_env_key()
        self.assertIs(ret, _test_val)
        try:
            decl.get_key.assert_called_once_with(SConsArguments.ENV)
        except AssertionError as e:
            self.fail(str(e))

    def test_get_var_key_1(self):
        """<_ArgumentDecl>.get_var_key() should invoke get_key(VAR)"""
        class _test_val: pass
        decl = SConsArguments._ArgumentDecl()
        decl.get_key = mock.Mock(name = 'get_key', return_value = _test_val)
        ret = decl.get_var_key()
        self.assertIs(ret, _test_val)
        try:
            decl.get_key.assert_called_once_with(SConsArguments.VAR)
        except AssertionError as e:
            self.fail(str(e))

    def test_get_opt_key_1(self):
        """<_ArgumentDecl>.get_opt_key() should invoke get_key(OPT)"""
        class _test_val: pass
        decl = SConsArguments._ArgumentDecl()
        decl.get_key = mock.Mock(name = 'get_key', return_value = _test_val)
        ret = decl.get_opt_key()
        self.assertIs(ret, _test_val)
        try:
            decl.get_key.assert_called_once_with(SConsArguments.OPT)
        except AssertionError as e:
            self.fail(str(e))

    def test_set_key__IndexError_1(self):
        """_ArgumentDecl().set_key(123,'a') should raise IndexError"""
        with self.assertRaises(IndexError):
            SConsArguments._ArgumentDecl().set_key(123,'a')

    def test_set_key__ENV_IndexError_1(self):
        """_ArgumentDecl().set_key(ENV,'a') should raise IndexError"""
        with self.assertRaises(IndexError):
            SConsArguments._ArgumentDecl().set_key(SConsArguments.ENV,'a')

    def test_set_key__VAR_IndexError_1(self):
        """_ArgumentDecl().set_key(VAR,'a') should raise IndexError"""
        with self.assertRaises(IndexError):
            SConsArguments._ArgumentDecl().set_key(SConsArguments.VAR,'a')

    def test_set_key__OPT_IndexError_1(self):
        """_ArgumentDecl().set_key(OPT,'a') should raise IndexError"""
        with self.assertRaises(IndexError):
            SConsArguments._ArgumentDecl().set_key(SConsArguments.OPT,'a')

    def test_set_key__ENV_1(self):
        """<_ArgumentDecl>.set_key(ENV,'BAR') should set new ENV key"""
        valu = {'xyz' : 'bobo'}
        decl = SConsArguments._ArgumentDecl(env_decl = {'FOO' : valu})
        self.assertEqual(decl.get_key(SConsArguments.ENV), 'FOO')
        decl.set_key(SConsArguments.ENV,'BAR');
        self.assertEqual(decl.get_key(SConsArguments.ENV), 'BAR')
        self.assertIs(decl._ArgumentDecl__decl_tab[SConsArguments.ENV]['default'], valu)

    def test_set_key__VAR_1(self):
        """<_ArgumentDecl>.set_key(VAR,'BAR') should set new VAR key"""
        valu = {'xyz' : 'bobo'}
        decl = SConsArguments._ArgumentDecl(var_decl = {'key' : 'FOO', 'default' : valu})
        self.assertEqual(decl.get_key(SConsArguments.VAR), 'FOO')
        decl.set_key(SConsArguments.VAR,'BAR');
        self.assertEqual(decl.get_key(SConsArguments.VAR), 'BAR')
        self.assertIs(decl._ArgumentDecl__decl_tab[SConsArguments.VAR]['key'], 'BAR')
        self.assertIs(decl._ArgumentDecl__decl_tab[SConsArguments.VAR]['default'], valu)

    def test_set_key__OPT_1(self):
        """<_ArgumentDecl>.set_key(OPT,'BAR') should set new OPT key"""
        valu = {'xyz' : 'bobo'}
        decl = SConsArguments._ArgumentDecl(opt_decl = ('--foo', {'dest' : 'FOO', 'default' :  valu}))
        self.assertEqual(decl.get_key(SConsArguments.OPT), 'FOO')
        decl.set_key(SConsArguments.OPT,'BAR');
        self.assertEqual(decl.get_key(SConsArguments.OPT), 'BAR')
        self.assertIs(decl._ArgumentDecl__decl_tab[SConsArguments.OPT][1]['dest'], 'BAR')
        self.assertIs(decl._ArgumentDecl__decl_tab[SConsArguments.OPT][1]['default'], valu)

    def test_set_env_key_1(self):
        """<_ArgumentDecl>.set_env_key(key) should invoke set_key(ENV,key)"""
        class _test_key: pass
        decl = SConsArguments._ArgumentDecl()
        decl.set_key = mock.Mock(name = 'set_key')
        decl.set_env_key(_test_key)
        try:
            decl.set_key.assert_called_once_with(SConsArguments.ENV, _test_key)
        except AssertionError as e:
            self.fail(str(e))

    def test_set_var_key_1(self):
        """<_ArgumentDecl>.set_var_key(key) should invoke set_key(VAR,key)"""
        class _test_key: pass
        decl = SConsArguments._ArgumentDecl()
        decl.set_key = mock.Mock(name = 'set_key')
        decl.set_var_key(_test_key)
        try:
            decl.set_key.assert_called_once_with(SConsArguments.VAR, _test_key)
        except AssertionError as e:
            self.fail(str(e))

    def test_set_opt_key_1(self):
        """<_ArgumentDecl>.set_opt_key(key) should invoke set_key(OPT,key)"""
        class _test_key: pass
        decl = SConsArguments._ArgumentDecl()
        decl.set_key = mock.Mock(name = 'set_key')
        decl.set_opt_key(_test_key)
        try:
            decl.set_key.assert_called_once_with(SConsArguments.OPT, _test_key)
        except AssertionError as e:
            self.fail(str(e))

    def test_get_default__123_IndexError_1(self):
        """<_ArgumentDecl>.get_default(123) should raise IndexError"""
        decl = SConsArguments._ArgumentDecl('FOO', ('FOO',1), ('-foo', {'dest' : 'FOO', 'default' : 1}))
        with self.assertRaises(IndexError):
            decl.get_default(123)

    def test_get_default__ENV_IndexError_1(self):
        """_ArgumentDecl().get_default(ENV) should raise IndexError"""
        with self.assertRaises(IndexError):
            SConsArguments._ArgumentDecl().get_default(SConsArguments.ENV)

    def test_get_default__VAR_IndexError_1(self):
        """_ArgumentDecl().get_default(VAR) should raise IndexError"""
        with self.assertRaises(IndexError):
            SConsArguments._ArgumentDecl().get_default(SConsArguments.VAR)

    def test_get_default__OPT_IndexError_1(self):
        """_ArgumentDecl().get_default(OPT) should raise IndexError"""
        with self.assertRaises(IndexError):
            SConsArguments._ArgumentDecl().get_default(SConsArguments.OPT)

    def test_get_default__ENV_1(self):
        """_ArgumentDecl(env_decl = 'FOO').get_default(ENV) should return _undef"""
        decl = SConsArguments._ArgumentDecl(env_decl = 'FOO')
        self.assertIs(decl.get_default(SConsArguments.ENV), SConsArguments._undef)

    def test_get_default__ENV_2(self):
        """_ArgumentDecl(env_decl = {'FOO': 123}).get_default(ENV) should return 123"""
        decl = SConsArguments._ArgumentDecl(env_decl = {'FOO' : 123})
        self.assertEqual(decl.get_default(SConsArguments.ENV), 123)

    def test_get_default__VAR_1(self):
        """_ArgumentDecl(var_decl = ('FOO',)).get_default(VAR) should return _undef"""
        decl = SConsArguments._ArgumentDecl(var_decl = ('FOO',))
        self.assertIs(decl.get_default(SConsArguments.VAR), SConsArguments._undef)

    def test_get_default__VAR_2(self):
        """_ArgumentDecl(var_decl = {'key': 'FOO', 'default': 123}).get_default(VAR) should return 123"""
        decl = SConsArguments._ArgumentDecl(var_decl = {'key' : 'FOO', 'default' : 123})
        self.assertEqual(decl.get_default(SConsArguments.VAR), 123)

    def test_get_env_default_1(self):
        """<_ArgumentDecl>.get_env_default() should invoke get_default(ENV)"""
        class _test_val: pass
        decl = SConsArguments._ArgumentDecl()
        decl.get_default = mock.Mock(name = 'get_default', return_value = _test_val)
        ret = decl.get_env_default()
        self.assertIs(ret, _test_val)
        try:
            decl.get_default.assert_called_once_with(SConsArguments.ENV)
        except AssertionError as e:
            self.fail(str(e))

    def test_get_var_default_1(self):
        """<_ArgumentDecl>.get_var_default() should invoke get_default(VAR)"""
        class _test_val: pass
        decl = SConsArguments._ArgumentDecl()
        decl.get_default = mock.Mock(name = 'get_default', return_value = _test_val)
        ret = decl.get_var_default()
        self.assertIs(ret, _test_val)
        try:
            decl.get_default.assert_called_once_with(SConsArguments.VAR)
        except AssertionError as e:
            self.fail(str(e))

    def test_get_opt_default_1(self):
        """<_ArgumentDecl>.get_opt_default() should invoke get_default(OPT)"""
        class _test_val: pass
        decl = SConsArguments._ArgumentDecl()
        decl.get_default = mock.Mock(name = 'get_default', return_value = _test_val)
        ret = decl.get_opt_default()
        self.assertIs(ret, _test_val)
        try:
            decl.get_default.assert_called_once_with(SConsArguments.OPT)
        except AssertionError as e:
            self.fail(str(e))

    def test_set_default__123_IndexError_1(self):
        """<_ArgumentDecl>.set_default(123, 1) should raise IndexError"""
        decl = SConsArguments._ArgumentDecl('FOO', ('FOO',), ('-foo', {'dest' : 'FOO'}))
        with self.assertRaises(IndexError):
            decl.set_default(123, 1)

    def test_set_default__ENV_IndexError_1(self):
        """_ArgumentDecl().set_default(ENV, 1) should raise IndexError"""
        with self.assertRaises(IndexError):
            SConsArguments._ArgumentDecl().set_default(SConsArguments.ENV, 1)

    def test_set_default__VAR_IndexError_1(self):
        """_ArgumentDecl().set_default(VAR, 1) should raise IndexError"""
        with self.assertRaises(IndexError):
            SConsArguments._ArgumentDecl().set_default(SConsArguments.VAR, 1)

    def test_set_default__OPT_IndexError_1(self):
        """_ArgumentDecl().set_default(OPT, 1) should raise IndexError"""
        with self.assertRaises(IndexError):
            SConsArguments._ArgumentDecl().set_default(SConsArguments.OPT, 1)

    def test_set_default__ENV_1(self):
        """<_ArgumentDecl>.set_default(ENV, 123) should set ENV default to 123"""
        decl = SConsArguments._ArgumentDecl(env_decl = 'FOO')
        decl.set_default(SConsArguments.ENV, 123)
        self.assertEqual(decl.get_default(SConsArguments.ENV), 123)

    def test_set_default__VAR_1(self):
        """<_ArgumentDecl>.set_default(VAR, 123) should set VAR default to 123"""
        decl = SConsArguments._ArgumentDecl(var_decl = ('FOO',))
        decl.set_default(SConsArguments.VAR, 123)
        self.assertEqual(decl.get_default(SConsArguments.VAR), 123)

    def test_set_default__OPT_1(self):
        """<_ArgumentDecl>.set_default(OPT, 123) should set OPT default to 123"""
        decl = SConsArguments._ArgumentDecl(opt_decl = ('--foo', {'dest' : 'FOO'}))
        decl.set_default(SConsArguments.OPT, 123)
        self.assertEqual(decl.get_default(SConsArguments.OPT), 123)

    def test_set_env_default_1(self):
        """<_ArgumentDecl>.set_env_default(default) should invoke set_default(ENV,default)"""
        class _test_default: pass
        decl = SConsArguments._ArgumentDecl()
        decl.set_default = mock.Mock(name = 'set_default')
        decl.set_env_default(_test_default)
        try:
            decl.set_default.assert_called_once_with(SConsArguments.ENV, _test_default)
        except AssertionError as e:
            self.fail(str(e))

    def test_set_var_default_1(self):
        """<_ArgumentDecl>.set_var_default(default) should invoke set_default(VAR,default)"""
        class _test_default: pass
        decl = SConsArguments._ArgumentDecl()
        decl.set_default = mock.Mock(name = 'set_default')
        decl.set_var_default(_test_default)
        try:
            decl.set_default.assert_called_once_with(SConsArguments.VAR, _test_default)
        except AssertionError as e:
            self.fail(str(e))

    def test_set_opt_default_1(self):
        """<_ArgumentDecl>.set_opt_default(default) should invoke set_default(OPT,default)"""
        class _test_default: pass
        decl = SConsArguments._ArgumentDecl()
        decl.set_default = mock.Mock(name = 'set_default')
        decl.set_opt_default(_test_default)
        try:
            decl.set_default.assert_called_once_with(SConsArguments.OPT, _test_default)
        except AssertionError as e:
            self.fail(str(e))

    def test_add_to__123_IndexError_1(self):
        """<_ArgumentDecl>.add_to(123) should raise IndexError"""
        decl = SConsArguments._ArgumentDecl('FOO', ('FOO',), ('--foo', {'dest' : 'FOO'}))
        with self.assertRaises(IndexError):
            decl.add_to(123)

    def test_add_to__ENV_IndexError_1(self):
        """_ArgumentDecl().add_to(ENV) should raise IndexError"""
        with self.assertRaises(IndexError):
            SConsArguments._ArgumentDecl().add_to(SConsArguments.ENV)

    def test_add_to__VAR_IndexError_1(self):
        """_ArgumentDecl().add_to(VAR) should raise IndexError"""
        with self.assertRaises(IndexError):
            SConsArguments._ArgumentDecl().add_to(SConsArguments.VAR)

    def test_add_to__OPT_IndexError_1(self):
        """_ArgumentDecl().add_to(OPT) should raise IndexError"""
        with self.assertRaises(IndexError):
            SConsArguments._ArgumentDecl().add_to(SConsArguments.OPT)

    def test_add_to__ENV_0(self):
        """_ArgumentDecl(env_decl = 'FOO').add_to(ENV,env) should not call env.SetDefault()"""
        env = mock.Mock(name = 'env')
        env.SetDefault = mock.Mock(name = 'SetDefault')
        decl1 = SConsArguments._ArgumentDecl(env_decl = 'FOO')
        decl1.add_to(SConsArguments.ENV, env)
        try:
            env.SetDefault.assert_not_called()
        except AssertionError as e:
            self.fail(str(e))

        decl2 = SConsArguments._ArgumentDecl(env_decl = {'FOO' : SConsArguments._undef})
        decl2.add_to(SConsArguments.ENV, env)
        try:
            env.SetDefault.assert_not_called()
        except AssertionError as e:
            self.fail(str(e))

    def test_add_to__ENV_1(self):
        """_ArgumentDecl(env_decl = {'FOO' : 123}).add_to(ENV,env) should call env.SetDefault(FOO = 123)"""
        env = mock.Mock(name = 'env')
        env.SetDefault = mock.Mock(name = 'SetDefault')
        decl = SConsArguments._ArgumentDecl(env_decl = {'FOO' : 123})
        decl.add_to(SConsArguments.ENV, env)
        try:
            env.SetDefault.assert_called_once_with(FOO = 123)
        except AssertionError as e:
            self.fail(str(e))

    def test_add_to__VAR_1(self):
        """_ArgumentDecl(var_decl = ('FOO',)).add_to(VAR,var) should call var.Add(key='FOO')"""
        var = mock.Mock(name = 'var')
        var.Add = mock.Mock(name = 'Add')
        decl1 = SConsArguments._ArgumentDecl(var_decl = ('FOO',))
        decl1.add_to(SConsArguments.VAR, var)
        try:
            var.Add.assert_called_once_with(key = 'FOO')
        except AssertionError as e:
            self.fail(str(e))

    def test_add_to__VAR_2(self):
        """_ArgumentDecl(var_decl = ('FOO', 'some help', 123)).add_to(VAR,var) should call var.Add(key = 'FOO', default = 123)"""
        var = mock.Mock(name = 'var')
        var.Add = mock.Mock(name = 'Add')
        decl = SConsArguments._ArgumentDecl(var_decl = ('FOO', 'some help', 123))
        decl.add_to(SConsArguments.VAR, var)
        try:
            var.Add.assert_called_once_with(key = 'FOO', help = 'some help', default = 123)
        except AssertionError as e:
            self.fail(str(e))

    def test_add_to__OPT_1(self):
        """_ArgumentDecl(opt_decl = ('--foo',{'dest' : 'FOO'})).add_to(OPT,opt) should call SCons.Script.Main.AddOption('--foo', dest='FOO')"""
        with mock.patch('SCons.Script.Main.AddOption') as AddOption:
            decl1 = SConsArguments._ArgumentDecl(opt_decl = ('--foo',{'dest' : 'FOO'}))
            decl1.add_to(SConsArguments.OPT)
            try:
                AddOption.assert_called_once_with('--foo', dest = 'FOO')
            except AssertionError as e:
                self.fail(str(e))

    def test_safe_add_to__ENV_0(self):
        """_ArgumentDecl().safe_add_to(ENV,env) should not call <_ArgumentDecl>.add_to()"""
        decl = SConsArguments._ArgumentDecl()
        decl.add_to = mock.Mock(name = 'add_to')
        env = mock.Mock(name = 'env')
        ret = decl.safe_add_to(SConsArguments.ENV, env)
        try:
            decl.add_to.assert_not_called()
        except AssertionError as e:
            self.fail(str(e))
        self.assertFalse(ret)

    def test_safe_add_to__VAR_0(self):
        """_ArgumentDecl().safe_add_to(VAR,var) should not call <_ArgumentDecl>.add_to()"""
        decl = SConsArguments._ArgumentDecl()
        decl.add_to = mock.Mock(name = 'add_to')
        var = mock.Mock(name = 'var')
        ret = decl.safe_add_to(SConsArguments.VAR, var)
        try:
            decl.add_to.assert_not_called()
        except AssertionError as e:
            self.fail(str(e))
        self.assertFalse(ret)

    def test_safe_add_to__OPT_0(self):
        """_ArgumentDecl().safe_add_to(OPT) should not call <_ArgumentDecl>.add_to()"""
        decl = SConsArguments._ArgumentDecl()
        decl.add_to = mock.Mock(name = 'add_to')
        ret = decl.safe_add_to(SConsArguments.OPT)
        try:
            decl.add_to.assert_not_called()
        except AssertionError as e:
            self.fail(str(e))
        self.assertFalse(ret)

    def test_safe_add_to__ENV_1(self):
        """_ArgumentDecl(env_decl = 'FOO').safe_add_to(ENV,env) should call <_ArgumentDecl>.add_to(ENV,env)"""
        decl = SConsArguments._ArgumentDecl(env_decl = 'FOO')
        decl.add_to = mock.Mock(name = 'add_to')
        env = mock.Mock(name = 'env')
        ret = decl.safe_add_to(SConsArguments.ENV, env)
        try:
            decl.add_to.assert_called_once_with(SConsArguments.ENV,env)
        except AssertionError as e:
            self.fail(str(e))
        self.assertTrue(ret)

    def test_safe_add_to__VAR_1(self):
        """_ArgumentDecl(var_decl = ('FOO',)).safe_add_to(VAR,var) should call <_ArgumentDecl>.add_to(VAR,var)"""
        decl = SConsArguments._ArgumentDecl(var_decl = ('FOO',))
        decl.add_to = mock.Mock(name = 'add_to')
        var = mock.Mock(name = 'var')
        ret = decl.safe_add_to(SConsArguments.VAR, var)
        try:
            decl.add_to.assert_called_once_with(SConsArguments.VAR, var)
        except AssertionError as e:
            self.fail(str(e))
        self.assertTrue(ret)

    def test_safe_add_to__OPT_1(self):
        """_ArgumentDecl(opt_decl = ('--foo', {'dest' : 'FOO'})).safe_add_to(OPT) should call <_ArgumentDecl>.add_to(OPT)"""
        decl = SConsArguments._ArgumentDecl(opt_decl = ('--foo', {'dest' : 'FOO'}))
        decl.add_to = mock.Mock(name = 'add_to')
        ret = decl.safe_add_to(SConsArguments.OPT)
        try:
            decl.add_to.assert_called_once_with(SConsArguments.OPT)
        except AssertionError as e:
            self.fail(str(e))
        self.assertTrue(ret)

#############################################################################
class Test__ArgumentDecls(unittest.TestCase):
    def test___init___mock_1(self):
        """Test, using mock, _ArgumentDecls.__init__() with no arguments"""
        with mock.patch.object(SConsArguments._ArgumentDecls, '_ArgumentDecls__validate_values') as __validate_values, \
             mock.patch.object(SConsArguments._ArgumentDecls, '_ArgumentDecls__update_supp_dicts') as __update_supp_dicts:
            decls = SConsArguments._ArgumentDecls()
            self.assertFalse(decls._ArgumentDecls__committed)
            try:
                __validate_values.assert_called_once_with()
                __update_supp_dicts.assert_called_once_with()
            except AssertionError as e:
                self.fail(str(e))

    def test___init___mock_2(self):
        """Test, using mocks, _ArgumentDecls.__init__() with mixed arguments"""
        with mock.patch.object(SConsArguments._ArgumentDecls, '_ArgumentDecls__validate_values') as __validate_values, \
             mock.patch.object(SConsArguments._ArgumentDecls, '_ArgumentDecls__update_supp_dicts') as __update_supp_dicts:
            decls = SConsArguments._ArgumentDecls([('a','A'),('b','B')], d = 'D')
        self.assertFalse(decls._ArgumentDecls__committed)
        try:
            __validate_values.assert_called_once_with([('a','A'),('b','B')], d = 'D')
            __update_supp_dicts.assert_called_once_with()
        except AssertionError as e:
            self.fail(str(e))

    def test___init___noargs_1(self):
        """Test _ArgumentDecls.__init__() without arguments"""
        decls = SConsArguments._ArgumentDecls()
        self.assertFalse(decls._ArgumentDecls__committed)
        self.assertEqual(decls, dict())

    def test___init___dict_1(self):
        """Test _ArgumentDecls.__init__() with dict argument"""
        a = SConsArguments.DeclareArgument()
        b = SConsArguments.DeclareArgument()
        decls = SConsArguments._ArgumentDecls({'a' : a, 'b' : b})
        self.assertFalse(decls._ArgumentDecls__committed)
        self.assertEqual(decls, {'a' : a, 'b' : b})

    def test___init___list_1(self):
        """Test _ArgumentDecls.__init__() with list argument"""
        a = SConsArguments.DeclareArgument()
        b = SConsArguments.DeclareArgument()
        decls = SConsArguments._ArgumentDecls([('a' , a), ('b' , b)])
        self.assertFalse(decls._ArgumentDecls__committed)
        self.assertEqual(decls, {'a' : a, 'b' : b})

    def test___init___kwargs_1(self):
        """Test _ArgumentDecls.__init__() with keyword arguments"""
        a = SConsArguments.DeclareArgument()
        b = SConsArguments.DeclareArgument()
        decls = SConsArguments._ArgumentDecls(a = a, b = b)
        self.assertFalse(decls._ArgumentDecls__committed)
        self.assertEqual(decls, {'a' : a, 'b' : b})

    def test___init___mix_2(self):
        """Test _ArgumentDecls.__init__() with mix of arguments and keywords"""
        a = SConsArguments.DeclareArgument()
        b = SConsArguments.DeclareArgument()
        decls = SConsArguments._ArgumentDecls({'a' : a}, b = b)
        self.assertFalse(decls._ArgumentDecls__committed)
        self.assertEqual(decls, {'a' : a, 'b' : b})

    def test___init___TypeError_1(self):
        """_ArgumentDecls.__init__({'a': 'b'}) should raise TypeError"""
        with self.assertRaises(TypeError) as cm:
            SConsArguments._ArgumentDecls({'a' : 'A'})
        self.assertEqual(str(cm.exception), "value must be an instance of _ArgumentDecl, %r is not allowed" % 'A')

    def test___init___error_ENV_already_declared(self):
        """_ArgumentDecls.__init__() should raise RuntimeError when two declarations refer to same construction variable"""
        a1 = SConsArguments._ArgumentDecl(('a', None))
        a2 = SConsArguments._ArgumentDecl(('a', None))
        with self.assertRaises(RuntimeError) as cm:
            decls = SConsArguments._ArgumentDecls(a1 = a1, a2 = a2)
        self.assertEqual(str(cm.exception), "variable 'a' is already declared")

    def test___init___error_VAR_already_declared(self):
        """_ArgumentDecls.__init__() should raise RuntimeError when two declarations refer to same command-line variable"""
        a1 = SConsArguments._ArgumentDecl(None, ('a',))
        a2 = SConsArguments._ArgumentDecl(None, ('a',))
        with self.assertRaises(RuntimeError) as cm:
            decls = SConsArguments._ArgumentDecls(a1 = a1, a2 = a2)
        self.assertEqual(str(cm.exception), "variable 'a' is already declared")

    def test___init___error_OPT_already_declared(self):
        """_ArgumentDecls.__init__() should raise RuntimeError when two declarations refer to command-line option with same 'dest'"""
        a1 = SConsArguments._ArgumentDecl(None, None, ('--a1', {'dest' : 'a'}))
        a2 = SConsArguments._ArgumentDecl(None, None, ('--a2', {'dest' : 'a'}))
        with self.assertRaises(RuntimeError) as cm:
            decls = SConsArguments._ArgumentDecls(a1 = a1, a2 = a2)
        self.assertEqual(str(cm.exception), "variable 'a' is already declared")

    def test___reset_supp_dicts_1(self):
        """<_ArgumentDecls>.__reset_supp_dicts() should reset all supplementary dictionaries, including resubst dicts"""
        a = SConsArguments._ArgumentDecl(('ENV_a',None), ('VAR_a',), ('--a', {'dest' : 'OPT_a'}))
        b = SConsArguments._ArgumentDecl(('ENV_b',None), ('VAR_b',), ('--b', {'dest' : 'OPT_b'}))
        decls = SConsArguments._ArgumentDecls(a = a, b = b)
        decls.commit() # to generate resubst/iresubst dicts
        decls._ArgumentDecls__reset_supp_dicts()
        self.assertEqual(decls._ArgumentDecls__rename,   [dict(),dict(),dict()])
        self.assertEqual(decls._ArgumentDecls__irename,  [dict(),dict(),dict()])
        self.assertEqual(decls._ArgumentDecls__resubst,  [dict(),dict(),dict()])
        self.assertEqual(decls._ArgumentDecls__iresubst, [dict(),dict(),dict()])

    def test___replace_key_in_supp_dicts__ENV_1(self):
        """<_ArgumentDecls>.__replace_key_in_supp_dicts(ENV,'a','ENX_a') should replace 'ENV_a' with 'ENX_a' in rename/irename dicts"""
        a = SConsArguments._ArgumentDecl(('ENV_a',None), ('VAR_a',), ('--a', {'dest' : 'OPT_a'}))
        b = SConsArguments._ArgumentDecl(('ENV_b',None), ('VAR_b',), ('--b', {'dest' : 'OPT_b'}))
        decls = SConsArguments._ArgumentDecls(a = a, b = b)
        decls._ArgumentDecls__replace_key_in_supp_dicts(SConsArguments.ENV, 'a', 'ENX_a')
        self.assertEqual(decls._ArgumentDecls__rename,   [  {'a' : 'ENX_a', 'b' : 'ENV_b'},
                                                            {'a' : 'VAR_a', 'b' : 'VAR_b'},
                                                            {'a' : 'OPT_a', 'b' : 'OPT_b'} ])
        self.assertEqual(decls._ArgumentDecls__irename,  [  {'ENX_a' : 'a', 'ENV_b' : 'b'},
                                                            {'VAR_a' : 'a', 'VAR_b' : 'b'},
                                                            {'OPT_a' : 'a', 'OPT_b' : 'b'} ])

    def test___replace_key_in_supp_dicts__VAR_1(self):
        """<_ArgumentDecls>.__replace_key_in_supp_dicts(VAR,'a','VAX_a') should replace 'VAR_a' with 'VAX_a' in rename/irename dicts"""
        a = SConsArguments._ArgumentDecl(('ENV_a',None), ('VAR_a',), ('--a', {'dest' : 'OPT_a'}))
        b = SConsArguments._ArgumentDecl(('ENV_b',None), ('VAR_b',), ('--b', {'dest' : 'OPT_b'}))
        decls = SConsArguments._ArgumentDecls(a = a, b = b)
        decls._ArgumentDecls__replace_key_in_supp_dicts(SConsArguments.VAR, 'a', 'VAX_a')
        self.assertEqual(decls._ArgumentDecls__rename,   [  {'a' : 'ENV_a', 'b' : 'ENV_b'},
                                                            {'a' : 'VAX_a', 'b' : 'VAR_b'},
                                                            {'a' : 'OPT_a', 'b' : 'OPT_b'} ])
        self.assertEqual(decls._ArgumentDecls__irename,  [  {'ENV_a' : 'a', 'ENV_b' : 'b'},
                                                            {'VAX_a' : 'a', 'VAR_b' : 'b'},
                                                            {'OPT_a' : 'a', 'OPT_b' : 'b'} ])

    def test___replace_key_in_supp_dicts__OPT_1(self):
        """<_ArgumentDecls>.__replace_key_in_supp_dicts(OPT,'a','OPX_a') should replace 'OPT_a' with 'OPX_a' in rename/irename dicts"""
        a = SConsArguments._ArgumentDecl(('ENV_a',None), ('VAR_a',), ('--a', {'dest' : 'OPT_a'}))
        b = SConsArguments._ArgumentDecl(('ENV_b',None), ('VAR_b',), ('--b', {'dest' : 'OPT_b'}))
        decls = SConsArguments._ArgumentDecls(a = a, b = b)
        decls._ArgumentDecls__replace_key_in_supp_dicts(SConsArguments.OPT, 'a', 'OPX_a')
        self.assertEqual(decls._ArgumentDecls__rename,   [  {'a' : 'ENV_a', 'b' : 'ENV_b'},
                                                            {'a' : 'VAR_a', 'b' : 'VAR_b'},
                                                            {'a' : 'OPX_a', 'b' : 'OPT_b'} ])
        self.assertEqual(decls._ArgumentDecls__irename,  [  {'ENV_a' : 'a', 'ENV_b' : 'b'},
                                                            {'VAR_a' : 'a', 'VAR_b' : 'b'},
                                                            {'OPX_a' : 'a', 'OPT_b' : 'b'} ])
    def test___replace_key_in_supp_dicts__nokey_1(self):
        """<_ArgumentDecls>.__replace_key_in_supp_dicts(ENV,'inexistent', 'foo') should add new name mapping"""
        a = SConsArguments._ArgumentDecl(('ENV_a',None), ('VAR_a',), ('--a', {'dest' : 'OPT_a'}))
        b = SConsArguments._ArgumentDecl(('ENV_b',None), ('VAR_b',), ('--b', {'dest' : 'OPT_b'}))
        decls = SConsArguments._ArgumentDecls(a = a, b = b)
        decls._ArgumentDecls__replace_key_in_supp_dicts(SConsArguments.ENV, 'inexistent', 'foo')
        self.assertEqual(decls._ArgumentDecls__rename,   [  {'a' : 'ENV_a', 'b' : 'ENV_b', 'inexistent' : 'foo'},
                                                            {'a' : 'VAR_a', 'b' : 'VAR_b'},
                                                            {'a' : 'OPT_a', 'b' : 'OPT_b'} ])
        self.assertEqual(decls._ArgumentDecls__irename,  [  {'ENV_a' : 'a', 'ENV_b' : 'b', 'foo': 'inexistent'},
                                                            {'VAR_a' : 'a', 'VAR_b' : 'b'},
                                                            {'OPT_a' : 'a', 'OPT_b' : 'b'} ])

    def test___del_from_supp_dicts_1(self):
        """<_ArgumentDecls>.__del_from_supp_dicts('a') should delete 'a' from rename/irename dictionaries"""
        a = SConsArguments._ArgumentDecl(('ENV_a',None), ('VAR_a',), ('--a', {'dest' : 'OPT_a'}))
        b = SConsArguments._ArgumentDecl(('ENV_b',None), ('VAR_b',), ('--b', {'dest' : 'OPT_b'}))
        decls = SConsArguments._ArgumentDecls(a = a, b = b)
        decls._ArgumentDecls__del_from_supp_dicts('a')
        self.assertEqual(decls._ArgumentDecls__rename,   [  {'b' : 'ENV_b'},
                                                            {'b' : 'VAR_b'},
                                                            {'b' : 'OPT_b'} ])
        self.assertEqual(decls._ArgumentDecls__irename,  [  {'ENV_b' : 'b'},
                                                            {'VAR_b' : 'b'},
                                                            {'OPT_b' : 'b'} ])

    def test___del_from_supp_dicts_2(self):
        """<_ArgumentDecls>.__del_from_supp_dicts('b') should delete 'a' from rename/irename dictionaries"""
        a = SConsArguments._ArgumentDecl(('ENV_a',None), ('VAR_a',), ('--a', {'dest' : 'OPT_a'}))
        b = SConsArguments._ArgumentDecl(('ENV_b',None), ('VAR_b',), ('--b', {'dest' : 'OPT_b'}))
        decls = SConsArguments._ArgumentDecls(a = a, b = b)
        decls._ArgumentDecls__del_from_supp_dicts('b')
        self.assertEqual(decls._ArgumentDecls__rename,   [  {'a' : 'ENV_a'},
                                                            {'a' : 'VAR_a'},
                                                            {'a' : 'OPT_a'} ])
        self.assertEqual(decls._ArgumentDecls__irename,  [  {'ENV_a' : 'a'},
                                                            {'VAR_a' : 'a'},
                                                            {'OPT_a' : 'a'} ])

    def test___ensure_not_committed_1(self):
        """<_ArgumetnDecls>.__ensure_not_committed() should not raise on a committed <_ArgumentDecls>"""
        decls = SConsArguments._ArgumentDecls()
        try:
            decls._ArgumentDecls__ensure_not_committed()
        except RuntimeError:
            self.fail("__ensure_not_committed() raised RuntimeError unexpectedly")

    def test___ensure_not_committed_2(self):
        """<_ArgumetnDecls>.__ensure_not_committed() should raise RuntimeError on an uncommitted <_ArgumentDecls>"""
        decls = SConsArguments._ArgumentDecls()
        decls.commit()
        with self.assertRaises(RuntimeError) as cm:
           decls._ArgumentDecls__ensure_not_committed()
        self.assertEqual(str(cm.exception), "declarations are already committed, can't be modified")
        
    def test___ensure_committed_1(self):
        """<_ArgumetnDecls>.__ensure_committed() should not raise on a committed <_ArgumentDecls>"""
        decls = SConsArguments._ArgumentDecls()
        decls.commit()
        try:
            decls._ArgumentDecls__ensure_committed()
        except RuntimeError:
            self.fail("__ensure_committed() raised RuntimeError unexpectedly")

    def test___ensure_committed_2(self):
        """<_ArgumetnDecls>.__ensure_committed() should raise RuntimeError on an uncommitted <_ArgumentDecls>"""
        decls = SConsArguments._ArgumentDecls()
        with self.assertRaises(RuntimeError) as cm:
           decls._ArgumentDecls__ensure_committed()
        self.assertEqual(str(cm.exception), "declarations must be committed before performing this operation")
        
    def test_setdefault__TypeError_1(self):
        """<_ArgumentDecls>.setdefault('foo', None) should raise TypeError"""
        decls = SConsArguments._ArgumentDecls()
        with self.assertRaises(TypeError) as cm:
            decls.setdefault('foo', None)
        self.assertEqual(str(cm.exception), "value must be an instance of _ArgumentDecl, None is not allowed")

    def test_setdefault__0(self):
        """<_ArgumentDecls>.setdefault('foo', 'bar') does not invoke __ensure_not_committed() nor __validate_value()"""
        decls = SConsArguments._ArgumentDecls()
        decls._ArgumentDecls__ensure_not_committed = mock.Mock(name = '__ensure_not_commited')
        with mock.patch.object(SConsArguments._ArgumentDecls, '_ArgumentDecls__validate_value') as __validate_value:
            decls.setdefault('foo')
        try:
            decls._ArgumentDecls__ensure_not_committed.assert_not_called()
            __validate_value.assert_not_called()
        except AssertionError as e:
            self.fail(str(e))
        foo = decls['foo']
        self.assertIs(foo, None)

    def test_setdefault__1(self):
        """<_ArgumentDecls>.setdefault('foo', 'bar') invokes __ensure_not_committed() and __validate_value()"""
        decls = SConsArguments._ArgumentDecls()
        decls._ArgumentDecls__ensure_not_committed = mock.Mock(name = '__ensure_not_commited')
        with mock.patch.object(SConsArguments._ArgumentDecls, '_ArgumentDecls__validate_value') as __validate_value:
            decls.setdefault('foo', 'bar')
        try:
            decls._ArgumentDecls__ensure_not_committed.assert_called_once_with()
            __validate_value.assert_called_once_with('bar')
        except AssertionError as e:
            self.fail(str(e))
        foo = decls['foo']
        self.assertEqual(foo, 'bar')

    def test_setdefault__2(self):
        """<_ArgumentDecls>.setdefault('a', <_ArgumentDecl>) should set default value appropriatelly"""
        a1 = SConsArguments._ArgumentDecl(('ENV_a1','A1'), ('VAR_a1',), ('--a1', {'dest' : 'OPT_a1'}))
        a2 = SConsArguments._ArgumentDecl(('ENV_a2','A2'), ('VAR_a2',), ('--a2', {'dest' : 'OPT_a2'}))
        decls = SConsArguments._ArgumentDecls()
        decls.setdefault('a', a1)
        self.assertIs(decls['a'], a1)
        decls.update(a = a2)
        self.assertIs(decls['a'], a2)

    def test_setdefault__3(self):
        """<_ArgumentDecls>.setdefault('a', <_ArgumentDecl>) should not oeverwrite existing values"""
        a1 = SConsArguments._ArgumentDecl(('ENV_a1','A1'), ('VAR_a1',), ('--a1', {'dest' : 'OPT_a1'}))
        a2 = SConsArguments._ArgumentDecl(('ENV_a2','A2'), ('VAR_a2',), ('--a2', {'dest' : 'OPT_a2'}))
        decls = SConsArguments._ArgumentDecls(a = a1)
        decls.setdefault('a', a2)
        self.assertIs(decls['a'], a1)

    def test_setdefault__4(self):
        """<_ArgumentDecls>.setdefault('a', <_ArgumentDecl>) should raise RuntimeError on committed object"""
        a = SConsArguments._ArgumentDecl(('ENV_a1','A1'), ('VAR_a1',), ('--a1', {'dest' : 'OPT_a1'}))
        decls = SConsArguments._ArgumentDecls()
        decls.commit()
        with self.assertRaises(RuntimeError) as cm:
            decls.setdefault('a', a)
        self.assertEqual(str(cm.exception), "declarations are already committed, can't be modified")

    def test_update__TypeError_1(self):
        """<_ArgumentDecls>.update({'foo' : 'bar'}) should raise TypeError"""
        decls = SConsArguments._ArgumentDecls()
        with self.assertRaises(TypeError) as cm:
            decls.update({'a' : 'b'})
        self.assertEqual(str(cm.exception), "value must be an instance of _ArgumentDecl, %r is not allowed" % 'b')

    def test_update__1(self):
        """<_ArgumentDecls>.update(*args, **kw) invokes __ensure_not_committed(), __validate_values() and __update_supp_dicts()"""
        decls = SConsArguments._ArgumentDecls()
        decls._ArgumentDecls__ensure_not_committed = mock.Mock(name = '__ensure_not_commited')
        decls._ArgumentDecls__update_supp_dicts = mock.Mock(name = '__update_supp_dicts')
        with mock.patch.object(SConsArguments._ArgumentDecls, '_ArgumentDecls__validate_values') as __validate_values:
            decls.update({'foo' : 'bar'}, geez = 123)
        try:
            __validate_values.assert_called_once_with({'foo' : 'bar'}, geez = 123)
            decls._ArgumentDecls__ensure_not_committed.assert_called_once_with()
            decls._ArgumentDecls__update_supp_dicts.assert_called_once_with()
        except AssertionError as e:
            self.fail(str(e))
        self.assertEqual(decls['foo'], 'bar')
        self.assertEqual(decls['geez'], 123)

    def test_update__2(self):
        """<_ArgumentDecls>.update() should perform dict update appropriately"""
        a = SConsArguments._ArgumentDecl()
        b1 = SConsArguments._ArgumentDecl()
        b2 = SConsArguments._ArgumentDecl()
        c = SConsArguments._ArgumentDecl()
        decls = SConsArguments._ArgumentDecls(a = a, b = b1)
        decls.update({'b' : b2, 'c' : c})
        self.assertIs(decls['a'], a)
        self.assertIs(decls['b'], b2)
        self.assertIs(decls['c'], c)

    def test_clear__1(self):
        """<_ArgumentDecls>.clear() should invoke __ensure_not_committed() and __update_supp_dicts()"""
        a = SConsArguments._ArgumentDecl()
        b = SConsArguments._ArgumentDecl()
        decls = SConsArguments._ArgumentDecls(a = a, b = b)
        decls._ArgumentDecls__ensure_not_committed = mock.Mock(name = '__ensure_not_committed')
        decls._ArgumentDecls__update_supp_dicts = mock.Mock(name = '__update_supp_dicts')
        decls.clear()
        try:
            decls._ArgumentDecls__ensure_not_committed.assert_called_once_with()
            decls._ArgumentDecls__update_supp_dicts.assert_called_once_with()
        except AssertionError as e:
            self.fail(str(e))
        # BTW, it should also clear the dictionary, so...
        self.assertFalse(decls) # is empty


    def test_clear__2(self):
        """<_ArgumentDecls>.clear() should clear the dict"""
        a = SConsArguments._ArgumentDecl()
        b = SConsArguments._ArgumentDecl()
        decls = SConsArguments._ArgumentDecls(a = a, b = b)
        decls.clear()
        self.assertFalse(decls) # is empty

    def test_pop__1(self):
        """<_ArgumentDecls>.pop('a') should invoke __ensure_not_committed() and __del_from_supp_dicts()"""
        a = SConsArguments._ArgumentDecl()
        b = SConsArguments._ArgumentDecl()
        decls = SConsArguments._ArgumentDecls(a = a, b = b)
        decls._ArgumentDecls__ensure_not_committed = mock.Mock(name = '__ensure_not_committed')
        decls._ArgumentDecls__del_from_supp_dicts = mock.Mock(name = '__del_from_supp_dicts')
        ret = decls.pop('a')
        try:
            decls._ArgumentDecls__ensure_not_committed.assert_called_once_with()
            decls._ArgumentDecls__del_from_supp_dicts.assert_called_once_with('a')
        except AssertionError as e:
            self.fail(str(e))
        # BTW, it should return the value
        self.assertIs(ret, a)

    def test_pop__2(self):
        """<_ArgumentDecls>.pop('a') should pop key 'a' from dict and return it's value"""
        a = SConsArguments._ArgumentDecl()
        b = SConsArguments._ArgumentDecl()
        decls = SConsArguments._ArgumentDecls(a = a, b = b)
        ret = decls.pop('a')
        self.assertIs(ret, a)
        self.assertEqual(decls, {'b': b})

    def test_pop__3(self):
        """<_ArgumentDecls>.pop('inexistent', 'default') should return 'default'"""
        a = SConsArguments._ArgumentDecl()
        b = SConsArguments._ArgumentDecl()
        decls = SConsArguments._ArgumentDecls(a = a, b = b)
        ret = decls.pop('inexistent', 'default')
        self.assertIs(ret, 'default')
        # The operation should not touch anything
        self.assertEqual(decls, {'a' : a, 'b': b})

    def test_popitem__1(self):
        """<_ArgumentDecls>.popitem() should invoke __ensure_not_committed() and __del_from_supp_dicts()"""
        a = SConsArguments._ArgumentDecl()
        b = SConsArguments._ArgumentDecl()
        decls = SConsArguments._ArgumentDecls(a = a, b = b)
        decls._ArgumentDecls__ensure_not_committed = mock.Mock(name = '__ensure_not_committed')
        decls._ArgumentDecls__del_from_supp_dicts = mock.Mock(name = '__del_from_supp_dicts')
        ret = decls.popitem()
        try:
            decls._ArgumentDecls__ensure_not_committed.assert_called_once_with()
            decls._ArgumentDecls__del_from_supp_dicts.assert_called_once_with(ret[0])
        except AssertionError as e:
            self.fail(str(e))
        # BTW, it should return the value
        self.assertTrue(ret == ('a', a) or ret == ('b', b))

    def test_popitem__2(self):
        """<_ArgumentDecls>.popitem() should remove item from dict and return it"""
        a = SConsArguments._ArgumentDecl()
        b = SConsArguments._ArgumentDecl()
        decls = SConsArguments._ArgumentDecls(a = a, b = b)
        ret = decls.popitem()
        self.assertTrue(ret == ('a', a) or ret == ('b', b))
        if ret == ('a', a):
            self.assertEqual(decls, {'b' : b})
        else:
            self.assertEqual(decls, {'a' : a})

    def test_copy(self):
        """<_ArgumentDecls>.copy() should return a copy of the dict"""
        a = SConsArguments._ArgumentDecl()
        b = SConsArguments._ArgumentDecl()
        decls = SConsArguments._ArgumentDecls(a = a, b = b)
        dcopy = decls.copy()
        self.assertEqual(decls, dcopy) # equal objects,
        self.assertIsNot(decls, dcopy) # but not same object...
        self.assertIs(type(dcopy), SConsArguments._ArgumentDecls)

    def test___setitem___1(self):
        """<_ArgumentDecls>.__setitem__() should invoke __ensure_not_committed(), __validate_value() and __append_decl_to_supp_dicts()"""
        a = SConsArguments._ArgumentDecl()
        b1 = SConsArguments._ArgumentDecl()
        b2 = SConsArguments._ArgumentDecl()
        decls = SConsArguments._ArgumentDecls(a = a, b = b1)
        decls._ArgumentDecls__ensure_not_committed = mock.Mock(name = '__ensure_not_committed')
        decls._ArgumentDecls__append_decl_to_supp_dicts = mock.Mock(name = '__append_decl_to_supp_dicts')
        with mock.patch.object(SConsArguments._ArgumentDecls, '_ArgumentDecls__validate_value') as __validate_value:
            decls.__setitem__('b',b2)
        try:
            decls._ArgumentDecls__ensure_not_committed.assert_called_once_with()
            __validate_value.assert_called_once_with(b2)
            decls._ArgumentDecls__append_decl_to_supp_dicts.assert_called_once_with('b', b2)
        except AssertionError as e:
            self.fail(str(e))
        self.assertEqual(decls, {'a' : a, 'b' : b2 })

    def test___setitem___2(self):
        """<_ArgumentDecls>.__setitem__() should invoke __ensure_not_committed(), __validate_value() and __append_decl_to_supp_dicts()"""
        a = SConsArguments._ArgumentDecl()
        b1 = SConsArguments._ArgumentDecl()
        b2 = SConsArguments._ArgumentDecl()
        decls = SConsArguments._ArgumentDecls(a = a, b = b1)
        decls.__setitem__('b',b2)
        self.assertEqual(decls, {'a' : a, 'b' : b2 })

    def test___setitem___3(self):
        """<_ArgumentDecls>.__setitem__() should replace existing entry"""
        a = SConsArguments._ArgumentDecl()
        b1 = SConsArguments._ArgumentDecl()
        b2 = SConsArguments._ArgumentDecl()
        decls = SConsArguments._ArgumentDecls(a = a, b = b1)
        decls['b'] = b2
        self.assertEqual(decls, {'a' : a, 'b' : b2 })

    def test___setitem___4(self):
        """<_ArgumentDecls>.__setitem__() should add non-existing entry"""
        a = SConsArguments._ArgumentDecl()
        b = SConsArguments._ArgumentDecl()
        decls = SConsArguments._ArgumentDecls(a = a)
        decls['b'] = b
        self.assertEqual(decls, {'a' : a, 'b' : b })

    def test___setitem___5(self):
        """<_ArgumentDecls>.__setitem__() should work on empty dict"""
        b = SConsArguments._ArgumentDecl()
        decls = SConsArguments._ArgumentDecls()
        decls['b'] = b
        self.assertEqual(decls, { 'b' : b })

    def test___setitem___6(self):
        """<_ArgumentDecls>.__setitem__() should work on an entry with default value set"""
        b1 = SConsArguments._ArgumentDecl()
        b2 = SConsArguments._ArgumentDecl()
        decls = SConsArguments._ArgumentDecls()
        decls.setdefault('b', b1)
        decls['b'] = b2
        self.assertEqual(decls, { 'b' : b2 })

    def test___delitem___1(self):
        """<_ArgumentDecls>.__delitem__() should invoke __ensure_not_committed(), and __del_from_supp_dicts()"""
        a = SConsArguments._ArgumentDecl()
        b = SConsArguments._ArgumentDecl()
        decls = SConsArguments._ArgumentDecls(a = a, b = b)
        decls._ArgumentDecls__ensure_not_committed = mock.Mock(name = '__ensure_not_committed')
        decls._ArgumentDecls__del_from_supp_dicts = mock.Mock(name = '__del_from_supp_dicts')
        decls.__delitem__('b')
        try:
            decls._ArgumentDecls__ensure_not_committed.assert_called_once_with()
            decls._ArgumentDecls__del_from_supp_dicts.assert_called_once_with('b')
        except AssertionError as e:
            self.fail(str(e))
        self.assertEqual(decls, {'a' : a })

    def test___delitem___2(self):
        """<_ArgumentDecls>.__delitem__() should delete requested key"""
        a = SConsArguments._ArgumentDecl()
        b = SConsArguments._ArgumentDecl()
        decls = SConsArguments._ArgumentDecls(a = a, b = b)
        decls.__delitem__('b')
        self.assertEqual(decls, {'a' : a })

    def test___delitem___KeyError_1(self):
        """<_ArgumentDecls>.__delitem__('inexistent') should raise KeyError"""
        a = SConsArguments._ArgumentDecl()
        b = SConsArguments._ArgumentDecl()
        decls = SConsArguments._ArgumentDecls(a = a, b = b)
        with self.assertRaises(KeyError):
            decls.__delitem__('inexistent')
        self.assertEqual(decls, {'a' : a, 'b' : b })

    def test_get_rename_dict__ENV_1(self):
        """_ArgumentDecls().get_rename_dict(ENV) should return empty dict"""
        self.assertEqual(SConsArguments._ArgumentDecls().get_rename_dict(SConsArguments.ENV), dict())

    def test_get_rename_dict__ENV_2(self):
        """Test <_ArgumentDecls>.get_rename_dict(ENV) with trivial name mapping"""
        a = SConsArguments._ArgumentDecl(('a','A'))
        b = SConsArguments._ArgumentDecl(('b','B'))
        decls = SConsArguments._ArgumentDecls(a = a, b = b)
        self.assertEqual(decls.get_rename_dict(SConsArguments.ENV), {'a' : 'a', 'b' : 'b'})

    def test_get_rename_dict__ENV_3(self):
        """Test <_ArgumentDecls>.get_rename_dict(ENV) with non-trivial name mappint"""
        a = SConsArguments._ArgumentDecl(('ENV_a','A'))
        b = SConsArguments._ArgumentDecl(('ENV_b','B'))
        decls = SConsArguments._ArgumentDecls(a = a, b = b)
        self.assertEqual(decls.get_rename_dict(SConsArguments.ENV), {'a' : 'ENV_a', 'b' : 'ENV_b'})

    def test_get_irename_dict__ENV_1(self):
        """_ArgumentDecls().get_irename_dict(ENV) should return empty dict"""
        self.assertEqual(SConsArguments._ArgumentDecls().get_irename_dict(SConsArguments.ENV), dict())

    def test_get_irename_dict__ENV_2(self):
        """Test <_ArgumentDecls>.get_irename_dict(ENV) with trivial name mapping"""
        a = SConsArguments._ArgumentDecl(('a','A'))
        b = SConsArguments._ArgumentDecl(('b','B'))
        decls = SConsArguments._ArgumentDecls(a = a, b = b)
        self.assertEqual(decls.get_irename_dict(SConsArguments.ENV), {'a' : 'a', 'b' : 'b'})

    def test_get_irename_dict__ENV_3(self):
        """Test <_ArgumentDecls>.get_irename_dict(ENV) with non-trivial name mappint"""
        a = SConsArguments._ArgumentDecl(('ENV_a','A'))
        b = SConsArguments._ArgumentDecl(('ENV_b','B'))
        decls = SConsArguments._ArgumentDecls(a = a, b = b)
        self.assertEqual(decls.get_irename_dict(SConsArguments.ENV), {'ENV_a' : 'a', 'ENV_b' : 'b'})

    def test_get_rename_dict__VAR_1(self):
        """_ArgumentDecls().get_rename_dict(VAR) should return empty dict"""
        self.assertEqual(SConsArguments._ArgumentDecls().get_rename_dict(SConsArguments.VAR), dict())

    def test_get_rename_dict__VAR_2(self):
        """Test <_ArgumentDecls>.get_rename_dict(VAR) with trivial name mapping"""
        a = SConsArguments._ArgumentDecl(None, ('a',))
        b = SConsArguments._ArgumentDecl(None, ('b',))
        decls = SConsArguments._ArgumentDecls(a = a, b = b)
        self.assertEqual(decls.get_rename_dict(SConsArguments.VAR), {'a' : 'a', 'b' : 'b'})

    def test_get_rename_dict__VAR_3(self):
        """Test <_ArgumentDecls>.get_rename_dict(VAR) with non-trivial name mappint"""
        a = SConsArguments._ArgumentDecl(None, ('VAR_a',))
        b = SConsArguments._ArgumentDecl(None, ('VAR_b',))
        decls = SConsArguments._ArgumentDecls(a = a, b = b)
        self.assertEqual(decls.get_rename_dict(SConsArguments.VAR), {'a' : 'VAR_a', 'b' : 'VAR_b'})

    def test_get_irename_dict__VAR_1(self):
        """_ArgumentDecls().get_irename_dict(VAR) should return empty dict"""
        self.assertEqual(SConsArguments._ArgumentDecls().get_irename_dict(SConsArguments.VAR), dict())

    def test_get_irename_dict__VAR_2(self):
        """Test <_ArgumentDecls>.get_irename_dict(VAR) with trivial name mapping"""
        a = SConsArguments._ArgumentDecl(None, ('a',))
        b = SConsArguments._ArgumentDecl(None, ('b',))
        decls = SConsArguments._ArgumentDecls(a = a, b = b)
        self.assertEqual(decls.get_irename_dict(SConsArguments.VAR), {'a' : 'a', 'b' : 'b'})

    def test_get_irename_dict__VAR_3(self):
        """Test <_ArgumentDecls>.get_irename_dict(VAR) with non-trivial name mappint"""
        a = SConsArguments._ArgumentDecl(None, ('VAR_a',))
        b = SConsArguments._ArgumentDecl(None, ('VAR_b',))
        decls = SConsArguments._ArgumentDecls(a = a, b = b)
        self.assertEqual(decls.get_irename_dict(SConsArguments.VAR), {'VAR_a' : 'a', 'VAR_b' : 'b'})
    
    def test_get_rename_dict__OPT_1(self):
        """_ArgumentDecls().get_rename_dict(OPT) should return empty dict"""
        self.assertEqual(SConsArguments._ArgumentDecls().get_rename_dict(SConsArguments.OPT), dict())

    def test_get_rename_dict__OPT_2(self):
        """Test <_ArgumentDecls>.get_rename_dict(OPT) with trivial name mapping"""
        a = SConsArguments._ArgumentDecl(None, None, ('--a', {'dest' : 'a'}))
        b = SConsArguments._ArgumentDecl(None, None, ('--b', {'dest' : 'b'}))
        decls = SConsArguments._ArgumentDecls(a = a, b = b)
        self.assertEqual(decls.get_rename_dict(SConsArguments.OPT), {'a' : 'a', 'b' : 'b'})

    def test_get_rename_dict__OPT_3(self):
        """Test <_ArgumentDecls>.get_rename_dict(OPT) with non-trivial name mappint"""
        a = SConsArguments._ArgumentDecl(None, None, ('--a', {'dest' : 'OPT_a'}))
        b = SConsArguments._ArgumentDecl(None, None, ('--b', {'dest' : 'OPT_b'}))
        decls = SConsArguments._ArgumentDecls(a = a, b = b)
        self.assertEqual(decls.get_rename_dict(SConsArguments.OPT), {'a' : 'OPT_a', 'b' : 'OPT_b'})

    def test_get_irename_dict__OPT_1(self):
        """_ArgumentDecls().get_irename_dict(OPT) should return empty dict"""
        self.assertEqual(SConsArguments._ArgumentDecls().get_irename_dict(SConsArguments.OPT), dict())

    def test_get_irename_dict__OPT_2(self):
        """Test <_ArgumentDecls>.get_irename_dict(OPT) with trivial name mapping"""
        a = SConsArguments._ArgumentDecl(None, None, ('--a', {'dest' : 'a'}))
        b = SConsArguments._ArgumentDecl(None, None, ('--b', {'dest' : 'b'}))
        decls = SConsArguments._ArgumentDecls(a = a, b = b)
        self.assertEqual(decls.get_irename_dict(SConsArguments.OPT), {'a' : 'a', 'b' : 'b'})

    def test_get_irename_dict__OPT_3(self):
        """Test <_ArgumentDecls>.get_irename_dict(OPT) with non-trivial name mappint"""
        a = SConsArguments._ArgumentDecl(None, None, ('--a', {'dest' : 'OPT_a'}))
        b = SConsArguments._ArgumentDecl(None, None, ('--b', {'dest' : 'OPT_b'}))
        decls = SConsArguments._ArgumentDecls(a = a, b = b)
        self.assertEqual(decls.get_irename_dict(SConsArguments.OPT), {'OPT_a' : 'a', 'OPT_b' : 'b'})
    
    def test_get_resubst_dict__ENV_1(self):
        """_ArgumentDecls().get_resubst_dict(ENV) should return empty dict"""
        decls = SConsArguments._ArgumentDecls()
        decls.commit()
        self.assertEqual(decls.get_resubst_dict(SConsArguments.ENV), dict())

    def test_get_resubst_dict__ENV_2(self):
        """Test <_ArgumentDecls>.get_resubst_dict(ENV) with trivial name mapping"""
        a = SConsArguments._ArgumentDecl(('a','A'))
        b = SConsArguments._ArgumentDecl(('b','B'))
        decls = SConsArguments._ArgumentDecls(a = a, b = b)
        decls.commit()
        self.assertEqual(decls.get_resubst_dict(SConsArguments.ENV), dict())

    def test_get_resubst_dict__ENV_3(self):
        """Test <_ArgumentDecls>.get_resubst_dict(ENV) with non-trivial name mappint"""
        a = SConsArguments._ArgumentDecl(('ENV_a','A'))
        b = SConsArguments._ArgumentDecl(('ENV_b','B'))
        decls = SConsArguments._ArgumentDecls(a = a, b = b)
        decls.commit()
        self.assertEqual(decls.get_resubst_dict(SConsArguments.ENV), {'a' : '${ENV_a}', 'b' : '${ENV_b}'})

    def test_get_iresubst_dict__ENV_1(self):
        """_ArgumentDecls().get_iresubst_dict(ENV) should return empty dict"""
        decls = SConsArguments._ArgumentDecls()
        decls.commit()
        self.assertEqual(decls.get_iresubst_dict(SConsArguments.ENV), dict())

    def test_get_iresubst_dict__ENV_2(self):
        """Test <_ArgumentDecls>.get_iresubst_dict(ENV) with trivial name mapping"""
        a = SConsArguments._ArgumentDecl(('a','A'))
        b = SConsArguments._ArgumentDecl(('b','B'))
        decls = SConsArguments._ArgumentDecls(a = a, b = b)
        decls.commit()
        self.assertEqual(decls.get_iresubst_dict(SConsArguments.ENV), dict())

    def test_get_iresubst_dict__ENV_3(self):
        """Test <_ArgumentDecls>.get_iresubst_dict(ENV) with non-trivial name mappint"""
        a = SConsArguments._ArgumentDecl(('ENV_a','A'))
        b = SConsArguments._ArgumentDecl(('ENV_b','B'))
        decls = SConsArguments._ArgumentDecls(a = a, b = b)
        decls.commit()
        self.assertEqual(decls.get_iresubst_dict(SConsArguments.ENV), {'ENV_a' : '${a}', 'ENV_b' : '${b}'})
    
    def test_get_resubst_dict__VAR_1(self):
        """_ArgumentDecls().get_resubst_dict(VAR) should return empty dict"""
        decls = SConsArguments._ArgumentDecls()
        decls.commit()
        self.assertEqual(decls.get_resubst_dict(SConsArguments.VAR), dict())

    def test_get_resubst_dict__VAR_2(self):
        """Test <_ArgumentDecls>.get_resubst_dict(VAR) with trivial name mapping"""
        a = SConsArguments._ArgumentDecl(None, ('a',))
        b = SConsArguments._ArgumentDecl(None, ('b',))
        decls = SConsArguments._ArgumentDecls(a = a, b = b)
        decls.commit()
        self.assertEqual(decls.get_resubst_dict(SConsArguments.VAR), {})

    def test_get_resubst_dict__VAR_3(self):
        """Test <_ArgumentDecls>.get_resubst_dict(VAR) with non-trivial name mappint"""
        a = SConsArguments._ArgumentDecl(None, ('VAR_a',))
        b = SConsArguments._ArgumentDecl(None, ('VAR_b',))
        decls = SConsArguments._ArgumentDecls(a = a, b = b)
        decls.commit()
        self.assertEqual(decls.get_resubst_dict(SConsArguments.VAR), {'a' : '${VAR_a}', 'b' : '${VAR_b}'})

    def test_get_iresubst_dict__VAR_1(self):
        """_ArgumentDecls().get_iresubst_dict(VAR) should return empty dict"""
        decls = SConsArguments._ArgumentDecls()
        decls.commit()
        self.assertEqual(decls.get_iresubst_dict(SConsArguments.VAR), dict())

    def test_get_iresubst_dict__VAR_2(self):
        """Test <_ArgumentDecls>.get_iresubst_dict(VAR) with trivial name mapping"""
        a = SConsArguments._ArgumentDecl(None, ('a',))
        b = SConsArguments._ArgumentDecl(None, ('b',))
        decls = SConsArguments._ArgumentDecls(a = a, b = b)
        decls.commit()
        self.assertEqual(decls.get_iresubst_dict(SConsArguments.VAR), {})

    def test_get_iresubst_dict__VAR_3(self):
        """Test <_ArgumentDecls>.get_iresubst_dict(VAR) with non-trivial name mappint"""
        a = SConsArguments._ArgumentDecl(None, ('VAR_a',))
        b = SConsArguments._ArgumentDecl(None, ('VAR_b',))
        decls = SConsArguments._ArgumentDecls(a = a, b = b)
        decls.commit()
        self.assertEqual(decls.get_iresubst_dict(SConsArguments.VAR), {'VAR_a' : '${a}', 'VAR_b' : '${b}'})
    
    def test_get_resubst_dict__OPT_1(self):
        """_ArgumentDecls().get_resubst_dict(OPT) should return empty dict"""
        decls = SConsArguments._ArgumentDecls()
        decls.commit()
        self.assertEqual(decls.get_resubst_dict(SConsArguments.OPT), dict())

    def test_get_resubst_dict__OPT_2(self):
        """Test <_ArgumentDecls>.get_resubst_dict(OPT) with trivial name mapping"""
        a = SConsArguments._ArgumentDecl(None, None, ('--a', {'dest' : 'a'}))
        b = SConsArguments._ArgumentDecl(None, None, ('--b', {'dest' : 'b'}))
        decls = SConsArguments._ArgumentDecls(a = a, b = b)
        decls.commit()
        self.assertEqual(decls.get_resubst_dict(SConsArguments.OPT), {})

    def test_get_resubst_dict__OPT_3(self):
        """Test <_ArgumentDecls>.get_resubst_dict(OPT) with non-trivial name mappint"""
        a = SConsArguments._ArgumentDecl(None, None, ('--a', {'dest' : 'OPT_a'}))
        b = SConsArguments._ArgumentDecl(None, None, ('--b', {'dest' : 'OPT_b'}))
        decls = SConsArguments._ArgumentDecls(a = a, b = b)
        decls.commit()
        self.assertEqual(decls.get_resubst_dict(SConsArguments.OPT), {'a' : '${OPT_a}', 'b' : '${OPT_b}'})

    def test_get_iresubst_dict__OPT_1(self):
        """_ArgumentDecls().get_iresubst_dict(OPT) should return empty dict"""
        decls = SConsArguments._ArgumentDecls()
        decls.commit()
        self.assertEqual(decls.get_iresubst_dict(SConsArguments.OPT), dict())

    def test_get_iresubst_dict__OPT_2(self):
        """Test <_ArgumentDecls>.get_iresubst_dict(OPT) with trivial name mapping"""
        a = SConsArguments._ArgumentDecl(None, None, ('--a', {'dest' : 'a'}))
        b = SConsArguments._ArgumentDecl(None, None, ('--b', {'dest' : 'b'}))
        decls = SConsArguments._ArgumentDecls(a = a, b = b)
        decls.commit()
        self.assertEqual(decls.get_iresubst_dict(SConsArguments.OPT), {})

    def test_get_iresubst_dict__OPT_3(self):
        """Test <_ArgumentDecls>.get_iresubst_dict(OPT) with non-trivial name mappint"""
        a = SConsArguments._ArgumentDecl(None, None, ('--a', {'dest' : 'OPT_a'}))
        b = SConsArguments._ArgumentDecl(None, None, ('--b', {'dest' : 'OPT_b'}))
        decls = SConsArguments._ArgumentDecls(a = a, b = b)
        decls.commit()
        self.assertEqual(decls.get_iresubst_dict(SConsArguments.OPT), {'OPT_a' : '${a}', 'OPT_b' : '${b}'})

    def test_get_key_1(self):
        """<_ArgumentDecls>.get_key('ns','a') should return self[key].get_key(ENV)"""
        class _test_key: pass
        a = SConsArguments._ArgumentDecl()
        a.get_key = mock.Mock(name = 'get_key', return_value = _test_key)
        decls = SConsArguments._ArgumentDecls(a = a)
        key = decls.get_key('ns','a')
        self.assertIs(key, _test_key)
        try:
            a.get_key.assert_called_once_with('ns')
        except AssertionError as e:
            self.fail(str(e))

    def test_get_key_ENV_1(self):
        """<_ArgumentDecls>.get_key(ENV,'a') returns appropriate key"""
        a = SConsArguments._ArgumentDecl(('ENV_a','A'))
        b = SConsArguments._ArgumentDecl(('ENV_b','B'))
        decls = SConsArguments._ArgumentDecls(a = a, b = b)
        self.assertEqual(decls.get_key(SConsArguments.ENV, 'a'), 'ENV_a')
        self.assertEqual(decls.get_key(SConsArguments.ENV, 'b'), 'ENV_b')

    def test_get_key_VAR_1(self):
        """<_ArgumentDecls>.get_key(VAR,'a') returns appropriate key"""
        a = SConsArguments._ArgumentDecl(None, ('VAR_a',))
        b = SConsArguments._ArgumentDecl(None, ('VAR_b',))
        decls = SConsArguments._ArgumentDecls(a = a, b = b)
        self.assertEqual(decls.get_key(SConsArguments.VAR, 'a'), 'VAR_a')
        self.assertEqual(decls.get_key(SConsArguments.VAR, 'b'), 'VAR_b')

    def test_get_key_OPT_1(self):
        """<_ArgumentDecls>.get_key(OPT,'a') returns appropriate key"""
        a = SConsArguments._ArgumentDecl(None, None, ('--a', {'dest' : 'OPT_a'}))
        b = SConsArguments._ArgumentDecl(None, None, ('--b', {'dest' : 'OPT_b'}))
        decls = SConsArguments._ArgumentDecls(a = a, b = b)
        self.assertEqual(decls.get_key(SConsArguments.OPT, 'a'), 'OPT_a')
        self.assertEqual(decls.get_key(SConsArguments.OPT, 'b'), 'OPT_b')

    def test_set_key_1(self):
        """<_ArgumentDecls>.set_key('ns', 'a', 'ns_a') should invoke __ensure_not_committed(), self['a'].set_key('ns', 'ns_a') and __replace_key_in_supp_dicts('ns', 'a', 'ns_a')"""
        a = SConsArguments._ArgumentDecl()
        decls = SConsArguments._ArgumentDecls(a = a)
        decls._ArgumentDecls__ensure_not_committed = mock.Mock(name = '__ensure_not_committed')
        decls['a'].set_key = mock.Mock(name = 'set_key')
        decls._ArgumentDecls__replace_key_in_supp_dicts = mock.Mock(name = '__replace_key_in_supp_dicts')
        decls.set_key('ns', 'a', 'ns_a')
        try:
            decls._ArgumentDecls__ensure_not_committed.assert_called_once_with()
            a.set_key.ensure_called_once_with('ns', 'ns_a')
            decls._ArgumentDecls__replace_key_in_supp_dicts.assert_called_once_with('ns', 'a', 'ns_a')
        except AssertionError as e:
            self.fail(str(e))

    def test_set_key_ENV_1(self):
        """<_ArgumentDecls>.set_key(ENV, 'a', 'ENV_a') should replace the old key and update supplementary dicts"""
        a = SConsArguments._ArgumentDecl({'a' : 'A'})
        decls = SConsArguments._ArgumentDecls(a = a)
        decls.set_key(SConsArguments.ENV, 'a', 'ENV_a')
        self.assertEqual(a.get_key(SConsArguments.ENV), 'ENV_a')
        self.assertEqual(decls.get_rename_dict(SConsArguments.ENV), {'a' : 'ENV_a'})
        self.assertEqual(decls.get_irename_dict(SConsArguments.ENV), {'ENV_a' : 'a'})

    def test_set_key_VAR_1(self):
        """<_ArgumentDecls>.set_key(VAR, 'a', 'VAR_a') should replace the old key and update supplementary dicts"""
        a = SConsArguments._ArgumentDecl(None, ('a',))
        decls = SConsArguments._ArgumentDecls(a = a)
        decls.set_key(SConsArguments.VAR, 'a', 'VAR_a')
        self.assertEqual(a.get_key(SConsArguments.VAR), 'VAR_a')
        self.assertEqual(decls.get_rename_dict(SConsArguments.VAR), {'a' : 'VAR_a'})
        self.assertEqual(decls.get_irename_dict(SConsArguments.VAR), {'VAR_a' : 'a'})

    def test_set_key_OPT_1(self):
        """<_ArgumentDecls>.set_key(OPT, 'a', 'OPT_a') should replace the old key and update supplementary dicts"""
        a = SConsArguments._ArgumentDecl(None, None, ('--a', {'dest' : 'a'}))
        decls = SConsArguments._ArgumentDecls(a = a)
        decls.set_key(SConsArguments.OPT, 'a', 'OPT_a')
        self.assertEqual(a.get_key(SConsArguments.OPT), 'OPT_a')
        self.assertEqual(decls.get_rename_dict(SConsArguments.OPT), {'a' : 'OPT_a'})
        self.assertEqual(decls.get_irename_dict(SConsArguments.OPT), {'OPT_a' : 'a'})

    def test__add_to_1(self):
        """<_ArgumentDecls>._add_to(ns,*args) should invoke v.add_to(ns,*args) for each (k,v) in <_ArgumentDecls>.iteritems()"""
        a = SConsArguments._ArgumentDecl()
        b = SConsArguments._ArgumentDecl()
        a.add_to = mock.Mock(name = 'a.add_to')
        b.add_to = mock.Mock(name = 'b.add_to')
        decls = SConsArguments._ArgumentDecls(a = a, b = b)
        decls._add_to('ns', 'arg1', 'arg2')
        try:
            a.add_to.assert_called_once_with('ns','arg1','arg2')
            b.add_to.assert_called_once_with('ns','arg1','arg2')
        except AssertionError as e:
            self.fail(str(e))

    def test__safe_add_to_1(self):
        """<_ArgumentDecls>._add_to(ns,*args) should invoke v.add_to(ns,*args) for each (k,v) in <_ArgumentDecls>.iteritems()"""
        a = SConsArguments._ArgumentDecl()
        b = SConsArguments._ArgumentDecl()
        a.safe_add_to = mock.Mock(name = 'a.add_to')
        b.safe_add_to = mock.Mock(name = 'b.add_to')
        decls = SConsArguments._ArgumentDecls(a = a, b = b)
        decls._safe_add_to('ns', 'arg1', 'arg2')
        try:
            a.safe_add_to.assert_called_once_with('ns','arg1','arg2')
            b.safe_add_to.assert_called_once_with('ns','arg1','arg2')
        except AssertionError as e:
            self.fail(str(e))

    def test_commit_1(self):
        """<_ArgumentDecls>.commit(*args) should do nothing on already committed object"""
        decls = SConsArguments._ArgumentDecls()
        decls._build_resubst_dicts = mock.Mock(name = '_build_resubst_dict')
        decls._build_iresubst_dicts = mock.Mock(name = '_build_iresubst_dict')
        decls._ArgumentDecls__resubst_defaults = mock.Mock(name = '__resubst_defaults')
        decls.add_to = mock.Mock(name = 'add_to')
        decls._ArgumentDecls__committed = True # mark it already committed
        decls.commit(10,11,12)
        try:
            decls._build_resubst_dicts.assert_not_called()
            decls._build_iresubst_dicts.assert_not_called()
            decls._ArgumentDecls__resubst_defaults.assert_not_called()
            decls.add_to.assert_not_called()
        except AssertionError as e:
            self.fail(str(e))

    def test_commit_2(self):
        """<_ArgumentDecls>.commit(*args) should invoke appropriate methods"""
        decls = SConsArguments._ArgumentDecls()
        decls._build_resubst_dicts = mock.Mock(name = '_build_resubst_dict')
        decls._build_iresubst_dicts = mock.Mock(name = '_build_iresubst_dict')
        decls._ArgumentDecls__resubst_defaults = mock.Mock(name = '__resubst_defaults')
        decls.add_to = mock.Mock(name = 'add_to')
        decls.commit(10,11,12)
        try:
            decls._build_resubst_dicts.assert_called_once_with()
            decls._build_iresubst_dicts.assert_called_once_with()
            decls._ArgumentDecls__resubst_defaults.called_once_with()
            decls.add_to.assert_called_once_with(10,11,12)
        except AssertionError as e:
            self.fail(str(e))
        self.assertTrue(decls._ArgumentDecls__committed)

    def test_Commit_1(self):
        """<_ArgumentDecls>.Commit('env', 'variables', 'create_options') should invoke <_ArgumentDecls>.commit() and return <_Arguments>"""
        decls = SConsArguments._ArgumentDecls()
        decls.commit = mock.Mock(name = 'commit')
        with mock.patch('SConsArguments._Arguments', return_value = '_Arguments') as _Arguments:
            ret = decls.Commit('env', 'variables', 'create_options')
        try:
            decls.commit.assert_called_once_with('env','variables','create_options')
        except AssertionError as e:
            self.fail(str(e))
        self.assertIs(ret, '_Arguments')

    def test_Commit_2(self):
        """<_ArgumentDecls>.Commit('env', 'variables', 'create_options', True) should invoke <_ArgumentDecls>.commit() and return None"""
        decls = SConsArguments._ArgumentDecls()
        decls.commit = mock.Mock(name = 'commit')
        with mock.patch('SConsArguments._Arguments', return_value = '_Arguments') as _Arguments:
            ret = decls.Commit('env', 'variables', 'create_options', True)
        try:
            decls.commit.assert_called_once_with('env','variables','create_options')
        except AssertionError as e:
            self.fail(str(e))
        self.assertIs(ret, '_Arguments')

    def test_Commit_3(self):
        """<_ArgumentDecls>.Commit('env', 'variables', 'create_options', True, 'arg1', 'arg2') should invoke <_ArgumentDecls>.commit() and return None"""
        decls = SConsArguments._ArgumentDecls()
        decls.commit = mock.Mock(name = 'commit')
        with mock.patch('SConsArguments._Arguments', return_value = '_Arguments') as _Arguments:
            ret = decls.Commit('env', 'variables', 'create_options', True, 'arg1', 'arg2')
        try:
            decls.commit.assert_called_once_with('env','variables','create_options', 'arg1', 'arg2')
        except AssertionError as e:
            self.fail(str(e))
        self.assertIs(ret, '_Arguments')

    def test_Commit_4(self):
        """<_ArgumentDecls>.Commit('env', 'variables', 'create_options', False) should invoke <_ArgumentDecls>.commit() and return None"""
        decls = SConsArguments._ArgumentDecls()
        decls.commit = mock.Mock(name = 'commit')
        with mock.patch('SConsArguments._Arguments', return_value = '_Arguments') as _Arguments:
            ret = decls.Commit('env', 'variables', 'create_options', False)
        try:
            decls.commit.assert_called_once_with('env','variables','create_options')
        except AssertionError as e:
            self.fail(str(e))
        self.assertIs(ret, None)


    def test_Commit_5(self):
        """<_ArgumentDecls>.Commit('env', 'variables', 'create_options', False, 'arg1', 'arg2') should invoke <_ArgumentDecls>.commit() and return None"""
        decls = SConsArguments._ArgumentDecls()
        decls.commit = mock.Mock(name = 'commit')
        with mock.patch('SConsArguments._Arguments', return_value = '_Arguments') as _Arguments:
            ret = decls.Commit('env', 'variables', 'create_options', False, 'arg1', 'arg2')
        try:
            decls.commit.assert_called_once_with('env','variables','create_options', 'arg1', 'arg2')
        except AssertionError as e:
            self.fail(str(e))
        self.assertIs(ret, None)


    def test_add_to_1(self):
        """<_ArgumentDecls>.add_to(11,12,13) should invoke <_ArgumentDecls>._safe_add_to(ns,...) for ns in [ENV, VAR, OPT]"""
        decls = SConsArguments._ArgumentDecls()
        decls._safe_add_to = mock.Mock(name = '_safe_add_to')
        with mock.patch.object(SConsArguments._ArgumentDecls, '_ArgumentDecls__ensure_committed', return_value = True) as __ensure_committed:
            decls.add_to(10, 11, 12)
        try:
            __ensure_committed.assert_called_once_with()
            calls = [ mock.call(SConsArguments.ENV, 10),
                      mock.call(SConsArguments.VAR, 11),
                      mock.call(SConsArguments.OPT, 12) ]
            decls._safe_add_to.assert_has_calls(calls)
        except AssertionError as e:
            self.fail(str(e))

#############################################################################
class Test_ArgumentDecl(unittest.TestCase):
    def test_gvar_decl_1(self):
        """ArgumentDecl() should be an instance of SConsArguments._ArgumentDecl()"""
        self.assertIsInstance(SConsArguments.ArgumentDecl(), SConsArguments._ArgumentDecl)
    def test_gvar_decl_2(self):
        """if decl = ArgumentDecl() then ArgumentDecl(decl) should be decl"""
        decl = SConsArguments.ArgumentDecl()
        self.assertIs(SConsArguments.ArgumentDecl(decl), decl)
    def test_gvar_decl_3(self):
        """ArgumentDecl() should not be same as ArgumentDecl()"""
        self.assertIsNot(SConsArguments.ArgumentDecl(), SConsArguments.ArgumentDecl())

    def test_user_doc_example_1(self):
        """example 1 from user documentation should work"""
        decl = SConsArguments.ArgumentDecl( {'xvar' : None}, None, ('--xvar', {'dest' : 'xvar', 'type' : 'string'}) )
        self.assertIsInstance(decl, SConsArguments._ArgumentDecl)

#############################################################################
class Test_DeclareArgument(unittest.TestCase):
    def test_DeclareArgument_1(self):
        """DeclareArgument(<_ArgumentDecl>) should return same <_ArgumentDecl> object"""
        decl1 = SConsArguments._ArgumentDecl()
        decl2 = SConsArguments.DeclareArgument(decl1)
        self.assertIs(decl2, decl1)

    def test_user_doc_example_2(self):
        """example 2 from user documentation should work"""
        decl = SConsArguments.DeclareArgument(env_key = 'xvar', opt_key = 'xvar', option = '--xvar', type = 'string')
        self.assertIsInstance(decl, SConsArguments._ArgumentDecl)

#############################################################################
class Test_ArgumentDecls(unittest.TestCase):
    def test_user_doc_example_3(self):
        """example 3 from user documentation should work"""
        # create single declarations
        foodecl = SConsArguments.ArgumentDecl( {'ENV_FOO' : 'default ENV_FOO'},                  # ENV
                                               ('var_foo', 'var_foo help', ),                    # VAR
                                               ('--foo', {'dest' : "opt_foo"}) )                 # OPT
        bardecl = SConsArguments.ArgumentDecl( {'ENV_BAR' : None},                               # ENV
                                               ('var_bar', 'var_bar help', 'default var_bar'),   # VAR
                                               ('--bar', {'dest':"opt_bar", "type":"string"}))   # OPT
        # put them all together
        decls = SConsArguments.ArgumentDecls({ 'foo' : foodecl, 'bar' : bardecl })
        self.assertIsInstance(decls, dict)
        self.assertIsInstance(decls, SConsArguments._ArgumentDecls)
        self.assertIsInstance(decls['foo'], SConsArguments._ArgumentDecl)
        self.assertIsInstance(decls['bar'], SConsArguments._ArgumentDecl)

    def test_user_doc_example_4(self):
        """example 4 from user documentation should work"""
        # create multiple declarations at once
        decls = SConsArguments.ArgumentDecls({
          # Argument 'foo'
          'foo' : ( {'ENV_FOO' : 'default ENV_FOO'},                 # ENV
                    ('var_foo', 'var_foo help', ),                   # VAR
                    ('--foo', {'dest' : "opt_foo"}) ),               # OPT
          # Argument 'bar'
          'bar' : ( {'ENV_BAR' : None},                              # ENV
                    ('var_bar', 'var_bar help', 'default var_bar'),  # VAR
                    ('--bar', {'dest':"opt_bar", "type":"string"}) ) # OPT
        })
        self.assertIsInstance(decls, dict)
        self.assertIsInstance(decls, SConsArguments._ArgumentDecls)
        self.assertIsInstance(decls['foo'], SConsArguments._ArgumentDecl)
        self.assertIsInstance(decls['bar'], SConsArguments._ArgumentDecl)

    def test_user_doc_example_5(self):
        """example 5 from user documentation should work"""
        decls = SConsArguments.ArgumentDecls([
          # Argument 'foo'
          ('foo',  ( {'ENV_FOO' : 'default ENV_FOO'},                  # ENV
                     ('var_foo', 'var_foo help', ),                    # VAR
                     ('--foo', {'dest' : "opt_foo"}) )),               # OPT
          # Argument 'bar'
          ('bar',  ( {'ENV_BAR' : None},                               # ENV
                     ('var_bar', 'var_bar help', 'default var_bar'),   # VAR
                     ('--bar', {'dest':"opt_bar", "type":"string"}) )) # OPT
        ])
        self.assertIsInstance(decls, dict)
        self.assertIsInstance(decls, SConsArguments._ArgumentDecls)
        self.assertIsInstance(decls['foo'], SConsArguments._ArgumentDecl)
        self.assertIsInstance(decls['bar'], SConsArguments._ArgumentDecl)

    def test_user_doc_example_6(self):
        """example 6 from user documentation should work"""
        decls = SConsArguments.ArgumentDecls(
          # Argument 'foo'
          foo =  ( {'ENV_FOO' : 'default ENV_FOO'},                  # ENV
                   ('var_foo', 'var_foo help', ),                    # VAR
                   ('--foo', {'dest' : "opt_foo"}) ),                # OPT
          # Argument 'bar'
          bar =  ( {'ENV_BAR' : None},                               # ENV
                   ('var_bar', 'var_bar help', 'default var_bar'),   # VAR
                   ('--bar', {'dest':"opt_bar", "type":"string"}) )  # OPT
        )
        self.assertIsInstance(decls, dict)
        self.assertIsInstance(decls, SConsArguments._ArgumentDecls)
        self.assertIsInstance(decls['foo'], SConsArguments._ArgumentDecl)
        self.assertIsInstance(decls['bar'], SConsArguments._ArgumentDecl)

    def test_user_doc_example_7(self):
        """example 7 from user documentation should work"""
        decls = SConsArguments.ArgumentDecls(
           # Argument 'foo'
           [('foo',(  {'ENV_FOO' : 'ENV default FOO'},                    # ENV
                      ('FOO',         'FOO variable help', ),             # VAR
                      ('--foo',       {'dest' : "opt_foo"})         ))],  # OPT
           # Argument 'geez'
           geez  = (  {'ENV_GEEZ' : None},                                # ENV
                      ('GEEZ', 'GEEZ variable help', 'VAR default GEEZ'), # VAR
                      ('--geez', {'dest':"opt_geez", "type":"string"}))   # OPT
        )
        self.assertIsInstance(decls, dict)
        self.assertIsInstance(decls, SConsArguments._ArgumentDecls)
        self.assertIsInstance(decls['foo'], SConsArguments._ArgumentDecl)
        self.assertIsInstance(decls['geez'], SConsArguments._ArgumentDecl)

    # It's not a mistake, example 8 is found in Test_DeclareArguments.
    def test_user_doc_example_9(self):
        """example 9 from user documentation should work"""
        decls = SConsArguments.ArgumentDecls(
           foo = ( { 'ENV_FOO' : None }, ('VAR_FOO', 'Help for VAR_FOO', '$VAR_BAR'), None),
           bar = ( { 'ENV_BAR' : None }, ('VAR_BAR', 'Help for VAR_BAR', 'BAR'), None),
        )
        self.assertIsInstance(decls, dict)
        self.assertIsInstance(decls, SConsArguments._ArgumentDecls)
        self.assertIsInstance(decls['foo'], SConsArguments._ArgumentDecl)
        self.assertIsInstance(decls['bar'], SConsArguments._ArgumentDecl)

#############################################################################
class Test_DeclareArguments(unittest.TestCase):
    def test_user_doc_example_8(self):
        """example 8 from user documentation should work"""
        decls = SConsArguments.DeclareArguments(
          foo = { 'env_key': 'ENV_FOO', 'var_key' : 'var_foo', 'opt_key' : 'opt_foo',
                  'option' : '--foo', 'default' : 'Default FOO',
                  'help' : 'foo help' },
          bar = { 'env_key': 'ENV_BAR', 'var_key' : 'var_bar', 'opt_key' : 'opt_bar',
                  'option' : '--bar', 'default' : 'Default VAR',  'type' : 'string',
                  'help' : 'bar help' }
        )
        self.assertIsInstance(decls, dict)
        self.assertIsInstance(decls, SConsArguments._ArgumentDecls)
        self.assertIsInstance(decls['foo'], SConsArguments._ArgumentDecl)
        self.assertIsInstance(decls['bar'], SConsArguments._ArgumentDecl)

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
               , Test__ArgumentsProxy
               , Test__VariablesWrapper
               , Test__Arguments
               , Test__ArgumentDecl
               , Test__ArgumentDecls
               , Test_ArgumentDecl
               , Test_DeclareArgument
               , Test_ArgumentDecls
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
