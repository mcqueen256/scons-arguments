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
        "SConsArguments.ENV should == 0"
        self.assertEqual(SConsArguments.ENV,0)
    def test_VAR(self):
        "SConsArguments.VAR should == 1"
        self.assertEqual(SConsArguments.VAR,1)
    def test_OPT(self):
        "SConsArguments.OPT should == 2"
        self.assertEqual(SConsArguments.OPT,2)
    def test_ALL(self):
        "SConsArguments.ALL should == 3"
        self.assertEqual(SConsArguments.ALL,3)
    def test__missing(self):
        "SConsArguments._missing should be a class"
        self.assertTrue(isinstance(SConsArguments._missing,type))
    def test__undef(self):
        "SConsArguments._undef should be a class"
        self.assertTrue(isinstance(SConsArguments._undef,type))
    def test__notfound(self):
        "SConsArguments._notfound should be a class"
        self.assertTrue(isinstance(SConsArguments._notfound,type))

#############################################################################
class Test__resubst(unittest.TestCase):
    """Test SConsArguments._resubst() function"""
    def test__resubst_1(self):
        """SConsArguments._resubst('foo bar') should be 'foo bar'"""
        self.assertEqual(SConsArguments._resubst('foo bar'), 'foo bar')
    def test__resubst_2(self):
        """SConsArguments._resubst('foo bar', {'foo' : 'XFOO'}) should be 'foo bar'"""
        self.assertEqual(SConsArguments._resubst('foo bar', {'foo' : 'XFOO'}), 'foo bar')
    def test__resubst_3(self):
        """SConsArguments._resubst('foo $bar', {'bar' : 'XBAR'}) should be 'foo XBAR'"""
        self.assertEqual(SConsArguments._resubst('foo $bar', {'bar' : 'XBAR'}), 'foo XBAR')
    def test__resubst_4(self):
        """SConsArguments._resubst('$foo $bar', {'foo' : 'XFOO', 'bar' : 'XBAR'}) should be 'XFOO XBAR'"""
        self.assertEqual(SConsArguments._resubst('$foo $bar', {'foo' : 'XFOO', 'bar' : 'XBAR'}), 'XFOO XBAR')
    def test__resubst_5(self):
        """SConsArguments._resubst('$foo $bar', {'foo' : '$bar', 'bar' : 'XBAR'}) should be '$bar XBAR'"""
        self.assertEqual(SConsArguments._resubst('$foo $bar', {'foo' : '$bar', 'bar' : 'XBAR'}), '$bar XBAR')
    def test__resubst_6(self):
        """SConsArguments._resubst('foo ${bar}', {'bar' : 'XBAR'}) should be 'foo XBAR'"""
        self.assertEqual(SConsArguments._resubst('foo ${bar}', {'bar' : 'XBAR'}), 'foo XBAR')
    def test__resubst_7(self):
        """SConsArguments._resubst('${foo} ${bar}', {'foo' : 'XFOO', 'bar' : 'XBAR'}) should be 'XFOO XBAR'"""
        self.assertEqual(SConsArguments._resubst('${foo} ${bar}', {'foo' : 'XFOO', 'bar' : 'XBAR'}), 'XFOO XBAR')
    def test__resubst_8(self):
        """SConsArguments._resubst('${foo} ${bar}', {'foo' : '${bar}', 'bar' : 'XBAR'}) should be '${bar} XBAR'"""
        self.assertEqual(SConsArguments._resubst('${foo} ${bar}', {'foo' : '${bar}', 'bar' : 'XBAR'}), '${bar} XBAR')

#############################################################################
class Test__build_resubst_dict(unittest.TestCase):
    """Test SConsArguments._build_resubst_dict() function"""
    def test__build_resubst_dict_1(self):
        """SConsArguments._build_resubst_dict({}) should == {}"""
        self.assertEqual(SConsArguments._build_resubst_dict({}),{})
    def test__build_resubst_dict_2(self):
        """SConsArguments._build_resubst_dict({'xxx' : 'yyy', 'vvv' : 'www'}) should == {'xxx' : '${yyy}', 'vvv' : '${www}'}"""
        self.assertEqual(SConsArguments._build_resubst_dict({'xxx' : 'yyy', 'vvv' : 'www'}), {'xxx' : '${yyy}', 'vvv' : '${www}'})

#############################################################################
class Test__build_iresubst_dict(unittest.TestCase):
    """Test SConsArguments._build_iresubst_dict() function"""
    def test__build_iresubst_dict_1(self):
        """SConsArguments._build_iresubst_dict({}) should == {}"""
        self.assertEqual(SConsArguments._build_iresubst_dict({}),{})
    def test__build_iresubst_dict_2(self):
        """SConsArguments._build_iresubst_dict({'xxx' : 'yyy', 'vvv' : 'www'}) should == {'yyy' : '${xxx}', 'www' : '${vvv}'}"""
        self.assertEqual(SConsArguments._build_iresubst_dict({'xxx' : 'yyy', 'vvv' : 'www'}), {'yyy' : '${xxx}', 'www' : '${vvv}'})

#############################################################################
class Test__compose_dicts(unittest.TestCase):
    """Test SConsArguments._compose_dicts() function"""
    def test__compose_dicts_1(self):
        """SConsArguments._compose_dicts({},{}) should == {}"""
        self.assertEqual(SConsArguments._compose_dicts({},{}),{})
    def test__compose_dicts_2(self):
        """SConsArguments._compose_dicts({'uuu' : 'vvv', 'xxx' : 'yyy'} ,{ 'vvv' : 'VVV', 'yyy' : 'YYY'}) should == {'uuu' : 'VVV'}"""
        self.assertEqual(SConsArguments._compose_dicts({'uuu' : 'vvv', 'xxx' : 'yyy'}, { 'vvv' : 'VVV', 'yyy' : 'YYY'}), {'uuu' : 'VVV', 'xxx' : 'YYY'})

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
class Test__ArgumentsEnvProxy(unittest.TestCase):
    def test___init___1(self):
        """_ArgumentsEnvProxy.__init__(env) should set default attributes"""
        env = 'env'
        proxy = SConsArguments._ArgumentsEnvProxy(env)
        self.assertIs(proxy.env, env)
        self.assertEqual(proxy._ArgumentsEnvProxy__rename, {})
        self.assertEqual(proxy._ArgumentsEnvProxy__irename, {})
        self.assertEqual(proxy._ArgumentsEnvProxy__resubst, {})
        self.assertEqual(proxy._ArgumentsEnvProxy__iresubst, {})
        self.assertEqual(proxy.is_strict(), False)

    def test___init___2(self):
        """_ArgumentsEnvProxy.__init__(env, arg1, arg2, arg3, arg4, True) should set attributes"""
        env = 'env'
        arg1, arg2, arg3, arg4 = 'arg1', 'arg2', 'arg3', 'arg4'
        proxy = SConsArguments._ArgumentsEnvProxy(env, arg1, arg2, arg3, arg4, True)
        self.assertIs(proxy.env, env)
        self.assertIs(proxy._ArgumentsEnvProxy__rename,   arg1)
        self.assertIs(proxy._ArgumentsEnvProxy__resubst,  arg2)
        self.assertIs(proxy._ArgumentsEnvProxy__irename,  arg3)
        self.assertIs(proxy._ArgumentsEnvProxy__iresubst, arg4)
        self.assertIs(proxy.is_strict(), True)

    def test_is_strict(self):
        """Test _ArgumentsEnvProxy.is_strict()"""
        self.assertIs(SConsArguments._ArgumentsEnvProxy('env', strict = False).is_strict(), False)
        self.assertIs(SConsArguments._ArgumentsEnvProxy('env', strict = True).is_strict(), True)

    def test_set_strict_False_calls__setup_methods_False(self):
        """_ArgumentsEnvProxy.set_strict(False) should call _ArgumentsEnvProxy.__setup_methods(False)"""
        proxy = SConsArguments._ArgumentsEnvProxy('env')
        proxy._ArgumentsEnvProxy__setup_methods = mock.Mock(name = '__setup_methods')
        proxy.set_strict(False)
        try:
            proxy._ArgumentsEnvProxy__setup_methods.assert_called_with(False)
        except AssertionError as e:
            self.fail(str(e))

    def test_set_strict_True_calls__setup_methods_True(self):
        """_ArgumentsEnvProxy.set_strict(True) should call _ArgumentsEnvProxy.__setup_methods(True)"""
        proxy = SConsArguments._ArgumentsEnvProxy('env')
        proxy._ArgumentsEnvProxy__setup_methods = mock.Mock(name = '__setup_methods')
        proxy.set_strict(True)
        try:
            proxy._ArgumentsEnvProxy__setup_methods.assert_called_with(True)
        except AssertionError as e:
            self.fail(str(e))

    def test_set_strict_False(self):
        """_ArgumentsEnvProxy.is_strict() should be False after _ArgumentsEnvProxy.set_strict(False)"""
        proxy = SConsArguments._ArgumentsEnvProxy('env')
        proxy.set_strict(False)
        self.assertIs(proxy.is_strict(), False)

    def test_set_strict_True(self):
        """_ArgumentsEnvProxy.is_strict() should be True after _ArgumentsEnvProxy.set_strict(True)"""
        proxy = SConsArguments._ArgumentsEnvProxy('env')
        proxy.set_strict(True)
        self.assertIs(proxy.is_strict(), True)

    def test___setup_methods_True(self):
        """_ArgumentsEnvProxy.__setup_methods(True) should setup appropriate methods"""
        proxy = SConsArguments._ArgumentsEnvProxy('env', strict = False)
        proxy._ArgumentsEnvProxy__setup_methods(True)
        self.assertEqual(proxy._ArgumentsEnvProxy__delitem__impl, proxy._ArgumentsEnvProxy__delitem__strict)
        self.assertEqual(proxy._ArgumentsEnvProxy__getitem__impl, proxy._ArgumentsEnvProxy__getitem__strict)
        self.assertEqual(proxy._ArgumentsEnvProxy__setitem__impl, proxy._ArgumentsEnvProxy__setitem__strict)
        self.assertEqual(proxy.get, proxy._get_strict)
        self.assertEqual(proxy.has_key, proxy._has_key_strict)
        self.assertEqual(proxy._ArgumentsEnvProxy__contains__impl, proxy._ArgumentsEnvProxy__contains__strict)
        self.assertEqual(proxy.items, proxy._items_strict)

    def test___setup_methods_False(self):
        """_ArgumentsEnvProxy.__setup_methods(False) should setup appropriate methods"""
        proxy = SConsArguments._ArgumentsEnvProxy('env', strict = True)
        proxy._ArgumentsEnvProxy__setup_methods(False)
        self.assertEqual(proxy._ArgumentsEnvProxy__delitem__impl, proxy._ArgumentsEnvProxy__delitem__nonstrict)
        self.assertEqual(proxy._ArgumentsEnvProxy__getitem__impl, proxy._ArgumentsEnvProxy__getitem__nonstrict)
        self.assertEqual(proxy._ArgumentsEnvProxy__setitem__impl, proxy._ArgumentsEnvProxy__setitem__nonstrict)
        self.assertEqual(proxy.get, proxy._get_nonstrict)
        self.assertEqual(proxy.has_key, proxy._has_key_nonstrict)
        self.assertEqual(proxy._ArgumentsEnvProxy__contains__impl, proxy._ArgumentsEnvProxy__contains__nonstrict)
        self.assertEqual(proxy.items, proxy._items_nonstrict)

    def test___delitem___1(self):
        """_ArgumentsEnvProxy({'a' : 'A'}).__delitem__('a') should delete item 'a'"""
        env = { 'a' : 'A' }
        SConsArguments._ArgumentsEnvProxy(env).__delitem__('a')
        self.assertEqual(env, {})

    def test___delitem___2(self):
        """_ArgumentsEnvProxy({'a' : 'A'}, strict = True).__delitem__('a') should raise KeyError"""
        with self.assertRaises(KeyError):
            SConsArguments._ArgumentsEnvProxy({'a' : 'A'}, strict = True).__delitem__('a')

    def test___delitem___3(self):
        """_ArgumentsEnvProxy({'b' : 'B'}, rename = {'a' : 'b'}).__delitem__('a') should delete item 'b'"""
        env = { 'b' : 'B' }
        SConsArguments._ArgumentsEnvProxy(env, rename = { 'a' : 'b'}).__delitem__('a')
        self.assertEqual(env, {})

    def test___delitem___4(self):
        """_ArgumentsEnvProxy({'b' : 'B'}, rename = {'a' : 'b'}, strict = True).__delitem__('a') should delete item 'b'"""
        env = { 'b' : 'B' }
        SConsArguments._ArgumentsEnvProxy(env, rename = { 'a' : 'b'}, strict = True).__delitem__('a')
        self.assertEqual(env, {})

    def test___getitem___1(self):
        """_ArgumentsEnvProxy({'a' : 'A'}).__getitem__('a') should return 'A'"""
        env = { 'a' : 'A' }
        self.assertEqual(SConsArguments._ArgumentsEnvProxy({'a' : 'A'}).__getitem__('a'), 'A')

    def test___getitem___2(self):
        """_ArgumentsEnvProxy({'a' : 'A'}, strict = True).__getitem__('a') should raise KeyError"""
        with self.assertRaises(KeyError):
            SConsArguments._ArgumentsEnvProxy({'a' : 'A'}, strict = True).__getitem__('a')

    def test__getitem___3(self):
        """_ArgumentsEnvProxy({'b' : 'B'}, rename = {'a' : 'b'}).__getitem__('a') should return 'B'"""
        self.assertEqual(SConsArguments._ArgumentsEnvProxy({'b' : 'B'}, rename = {'a' : 'b'}).__getitem__('a'), 'B')

    def test___getitem___4(self):
        """_ArgumentsEnvProxy({'b' : 'B'}, rename = {'a' : 'b'}, strict = True).__getitem__('a') should return 'B'"""
        self.assertEqual(SConsArguments._ArgumentsEnvProxy({'b' : 'B'}, rename = {'a' : 'b'}, strict = True).__getitem__('a'), 'B')

    def test__setitem___1(self):
        """_ArgumentsEnvProxy({}).__setitem__('a', 'A') should set item 'a' to 'A'"""
        proxy = SConsArguments._ArgumentsEnvProxy({})
        proxy.__setitem__('a', 'A')
        self.assertEqual(proxy['a'], 'A')

    def test___setitem___2(self):
        """_ArgumentsEnvProxy({'a' : 'B'}).__setitem__('a', 'A') should set item 'a' to 'A'"""
        env = {'a' : 'B'}
        proxy = SConsArguments._ArgumentsEnvProxy(env)
        proxy.__setitem__('a', 'A')
        self.assertEqual(env['a'], 'A')

    def test__setitem___3(self):
        """_ArgumentsEnvProxy({'a' : 'B'}, rename = { 'a' : 'a' }, strict = True).__setitem__('a', 'A') should set item 'a' to 'A'"""
        env = {'a' : 'B'}
        proxy = SConsArguments._ArgumentsEnvProxy(env, rename = { 'a' : 'a' }, strict = True)
        proxy.__setitem__('a', 'A')
        self.assertEqual(env['a'], 'A')

    def test___setitem___4(self):
        """_ArgumentsEnvProxy({'a' : 'B'}, strict = True).__setitem__('a', 'A') should raise KeyError"""
        env = {'a' : 'B'}
        proxy = SConsArguments._ArgumentsEnvProxy(env, strict = True)
        with self.assertRaises(KeyError):
            proxy.__setitem__('a', 'A')
        self.assertEqual(env['a'], 'B')

    def test_get_1(self):
        """_ArgumentsEnvProxy({'a' : 'A'}).get('a') should return 'A'"""
        self.assertEqual(SConsArguments._ArgumentsEnvProxy({'a' : 'A'}).get('a'), 'A')

    def test_get_2(self):
        """_ArgumentsEnvProxy({'a' : 'A'}).get('b') should return None"""
        self.assertEqual(SConsArguments._ArgumentsEnvProxy({'a' : 'A'}).get('b'), None)

    def test_get_3(self):
        """_ArgumentsEnvProxy({'a' : 'A'}, rename = { 'b' : 'a' }).get('b') should return 'A'"""
        self.assertEqual(SConsArguments._ArgumentsEnvProxy({'a' : 'A'}, rename = { 'b' : 'a'}).get('b'), 'A')

    def test_get_4(self):
        """_ArgumentsEnvProxy({'a' : 'A'}, rename = { 'b' : 'a' }).get('a') should return 'A'"""
        self.assertEqual(SConsArguments._ArgumentsEnvProxy({'a' : 'A'}, rename = { 'b' : 'a'}).get('a'), 'A')

    def test_get_5(self):
        """_ArgumentsEnvProxy({'a' : 'A'}, strict = True).get('a') should raise KeyError"""
        with self.assertRaises(KeyError):
            SConsArguments._ArgumentsEnvProxy({'a' : 'A'}, strict = True).get('a')

    def test_get_6(self):
        """_ArgumentsEnvProxy({'a' : 'A'}, rename = { 'b' : 'a' }, strict = True).get('b') should return 'A'"""
        self.assertEqual(SConsArguments._ArgumentsEnvProxy({'a' : 'A'}, rename = { 'b' : 'a' }, strict = True).get('b'), 'A')

    def test_has_key_1(self):
        """_ArgumentsEnvProxy({'a' : 'A'}).has_key('a') should return True"""
        self.assertTrue(SConsArguments._ArgumentsEnvProxy({'a' : 'A'}).has_key('a'))

    def test_has_key_2(self):
        """_ArgumentsEnvProxy({'a' : 'A'}).has_key('b') should return False"""
        self.assertFalse(SConsArguments._ArgumentsEnvProxy({'a' : 'A'}).has_key('b'))

    def test_has_key_3(self):
        """_ArgumentsEnvProxy({'a' : 'A'}, rename = {'b' : 'a'}).has_key('a') should return True"""
        self.assertTrue(SConsArguments._ArgumentsEnvProxy({'a' : 'A'}, rename = {'b' : 'a'}).has_key('a'))

    def test_has_key_4(self):
        """_ArgumentsEnvProxy({'a' : 'A'}, rename = {'b' : 'a'}).has_key('b') should return True"""
        self.assertTrue(SConsArguments._ArgumentsEnvProxy({'a' : 'A'}, rename = {'b' : 'a'}).has_key('b'))

    def test_has_key_5(self):
        """_ArgumentsEnvProxy({'a' : 'A'}, rename = {'b' : 'a'}, strict = True).has_key('a') should return False"""
        self.assertFalse(SConsArguments._ArgumentsEnvProxy({'a' : 'A'}, rename = {'b' : 'a'}, strict = True).has_key('a'))

    def test_has_key_6(self):
        """_ArgumentsEnvProxy({'a' : 'A'}, rename = {'b' : 'a'}, strict = True).has_key('b') should return True"""
        self.assertTrue(SConsArguments._ArgumentsEnvProxy({'a' : 'A'}, rename = {'b' : 'a'}, strict = True).has_key('b'))

    def test_has_key_7(self):
        """_ArgumentsEnvProxy({'a' : 'A'}, rename = {'b' : 'c'}, strict = True).has_key('b') should return False"""
        self.assertFalse(SConsArguments._ArgumentsEnvProxy({'a' : 'A'}, rename = {'b' : 'c'}, strict = True).has_key('b'))

    def test___contains___1(self):
        """_ArgumentsEnvProxy({'a' : 'A'}).__contains__('a') should return True"""
        self.assertTrue(SConsArguments._ArgumentsEnvProxy({'a' : 'A'}).__contains__('a'))

    def test___contains___2(self):
        """_ArgumentsEnvProxy({'a' : 'A'}).__contains__('b') should return False"""
        self.assertFalse(SConsArguments._ArgumentsEnvProxy({'a' : 'A'}).__contains__('b'))

    def test___contains___3(self):
        """_ArgumentsEnvProxy({'a' : 'A'}, rename = {'b' : 'a'}).__contains__('a') should return True"""
        self.assertTrue(SConsArguments._ArgumentsEnvProxy({'a' : 'A'}, rename = {'b' : 'a'}).__contains__('a'))

    def test___contains___4(self):
        """_ArgumentsEnvProxy({'a' : 'A'}, rename = {'b' : 'a'}).__contains__('b') should return True"""
        self.assertTrue(SConsArguments._ArgumentsEnvProxy({'a' : 'A'}, rename = {'b' : 'a'}).__contains__('b'))

    def test___contains___5(self):
        """_ArgumentsEnvProxy({'a' : 'A'}, rename = {'b' : 'a'}, strict = True).__contains__('a') should return False"""
        self.assertFalse(SConsArguments._ArgumentsEnvProxy({'a' : 'A'}, rename = {'b' : 'a'}, strict = True).__contains__('a'))

    def test___contains___6(self):
        """_ArgumentsEnvProxy({'a' : 'A'}, rename = {'b' : 'a'}, strict = True).__contains__('b') should return True"""
        self.assertTrue(SConsArguments._ArgumentsEnvProxy({'a' : 'A'}, rename = {'b' : 'a'}, strict = True).__contains__('b'))

    def test___contains___7(self):
        """_ArgumentsEnvProxy({'a' : 'A'}, rename = {'b' : 'c'}, strict = True).__contains__('b') should return False"""
        self.assertFalse(SConsArguments._ArgumentsEnvProxy({'a' : 'A'}, rename = {'b' : 'c'}, strict = True).__contains__('b'))

    def test_items_1(self):
        """_ArgumentsEnvProxy({'a' : 'A', 'b' : 'B'}).items() should be [('a', 'A'), ('b', 'B')]"""
        self.assertEqual(SConsArguments._ArgumentsEnvProxy({'a' : 'A', 'b' : 'B'}).items(), ([('a', 'A'), ('b', 'B')]))

    def test_items_2(self):
        """_ArgumentsEnvProxy({'a' : 'A', 'b' : 'B'}, irename = {'a' : 'c'}).items() should be [('c', 'A'), ('b', 'B')]"""
        self.assertEqual(SConsArguments._ArgumentsEnvProxy({'a' : 'A', 'b' : 'B'}, irename = { 'a' : 'c'}).items(), ([('c', 'A'), ('b', 'B')]))

    def test_items_3(self):
        """_ArgumentsEnvProxy({'a' : 'A', 'b' : 'B'}, rename = {'c' : 'a'}, strict = True).items() should be [('c', 'A')]"""
        self.assertEqual(SConsArguments._ArgumentsEnvProxy({'a' : 'A', 'b' : 'B'}, rename = { 'c' : 'a'}, strict = True).items(), ([('c', 'A')]))

    def test_items_4(self):
        """_ArgumentsEnvProxy({'a' : '${a}'}, irename = {'a' : 'b'}, iresubst = {'a' : '${b}'}).items() should be [('b', '${b}')]"""
        self.assertEqual(SConsArguments._ArgumentsEnvProxy({'a' : '${a}'}, irename = {'a' : 'b'}, iresubst = {'a' : '${b}'}).items(), [('b', '${b}')])

    def test_items_5(self):
        """_ArgumentsEnvProxy({'a' : 'a'}, irename = {'a' : 'b'}, iresubst = {'a' : '${b}'}).items() should be [('b', 'a')]"""
        self.assertEqual(SConsArguments._ArgumentsEnvProxy({'a' : 'a'}, irename = {'a' : 'b'}, iresubst = {'a' : '${b}'}).items(), [('b', 'a')])

    def test_subst_1(self):
        """_ArgumentsEnvProxy(env).subst('${a} ${b}') should call env.subst('${a} ${b}')"""
        env = mock.Mock(name = 'env')
        env.subst = mock.Mock(name = 'env.subst')
        SConsArguments._ArgumentsEnvProxy(env).subst('${a} ${b}')
        try:
            env.subst.assert_called_with('${a} ${b}')
        except AssertionError as e:
            self.fail(str(e))

    def test_subst_2(self):
        """_ArgumentsEnvProxy(env, resubst = {'b' : '${c}}).subst('${a} ${b}') should call env.subst('${a} ${c}')"""
        env = mock.Mock(name = 'env')
        env.subst = mock.Mock(name = 'env.subst')
        SConsArguments._ArgumentsEnvProxy(env, resubst = {'b' : '${c}'}).subst('${a} ${b}')
        try:
            env.subst.assert_called_with('${a} ${c}')
        except AssertionError as e:
            self.fail(str(e))

#############################################################################
class Test__Arguments(unittest.TestCase):

    @classmethod
    def _gdecls_mock_1(cls):
        # decls0 is a substitute of _ArgumentDecls instance, with only keys()
        # method defined
        gdecls = mock.Mock(name = 'gdecls0')
        gdecls.keys = mock.Mock(name = 'keys', return_value = ['k','e','y','s'])
        return gdecls

    @classmethod
    def _gdecls_mock_2(cls):
        gdecls = cls._gdecls_mock_1()
        return cls._mock_gdecls_supp_dicts_2(gdecls)

    @classmethod
    def _gdecls_mock_3(cls):
        gdecls = cls._gdecls_mock_1()
        return cls._mock_gdecls_supp_dicts_3(gdecls)

    @classmethod
    def _gdecls_mock_4(cls):
        gdecls = cls._gdecls_mock_1()
        return cls._mock_gdecls_supp_dicts_4(gdecls)

    @classmethod
    def _gdecls_mock_5(cls):
        gdecls = cls._gdecls_mock_1()
        return cls._mock_gdecls_supp_dicts_5(gdecls)

    @classmethod
    def _gvars_mock_4_UpdateEnvironment(cls):
        gv = SConsArguments._Arguments(cls._gdecls_mock_1())
        gv.update_env_from_vars = mock.Mock(name = 'update_env_from_vars')
        gv.update_env_from_opts = mock.Mock(name = 'update_env_from_opts')
        return gv

    @classmethod
    def _mock_gdecls_supp_dicts_2(cls, gdecls):
        def get_ns_rename_dict(xxx):   return "rename_dict[%d]" % xxx
        def get_ns_resubst_dict(xxx):  return "resubst_dict[%d]" % xxx
        def get_ns_irename_dict(xxx):  return "irename_dict[%d]" % xxx
        def get_ns_iresubst_dict(xxx): return "iresubst_dict[%d]" % xxx
        gdecls.get_ns_rename_dict = mock.Mock(name = 'get_ns_rename_dict', side_effect = get_ns_rename_dict)
        gdecls.get_ns_irename_dict = mock.Mock(name = 'get_ns_rename_dict', side_effect = get_ns_irename_dict)
        gdecls.get_ns_resubst_dict = mock.Mock(name = 'get_ns_rename_dict', side_effect = get_ns_resubst_dict)
        gdecls.get_ns_iresubst_dict = mock.Mock(name = 'get_ns_iresubst_dict',  side_effect = get_ns_iresubst_dict)
        return gdecls

    @classmethod
    def _mock_gdecls_supp_dicts_3(cls, gdecls):
        def get_ns_rename_dict(xxx):   return None
        def get_ns_resubst_dict(xxx):  return None
        def get_ns_irename_dict(xxx):  return None
        def get_ns_iresubst_dict(xxx): return None
        gdecls.get_ns_rename_dict = mock.Mock(name = 'get_ns_rename_dict', side_effect = get_ns_rename_dict)
        gdecls.get_ns_irename_dict = mock.Mock(name = 'get_ns_rename_dict', side_effect = get_ns_irename_dict)
        gdecls.get_ns_resubst_dict = mock.Mock(name = 'get_ns_rename_dict', side_effect = get_ns_resubst_dict)
        gdecls.get_ns_iresubst_dict = mock.Mock(name = 'get_ns_iresubst_dict',  side_effect = get_ns_iresubst_dict)
        return gdecls

    @classmethod
    def _mock_gdecls_supp_dicts_4(cls, gdecls):
        def get_ns_rename_dict(xxx):
            return  [ {'a' : 'env_a'},    {'a' : 'var_a'},    {'a' : 'opt_a'}    ][xxx]
        def get_ns_resubst_dict(xxx):
            return  [ {'a' : '${env_a}'}, {'a' : '${var_a}'}, {'a' : '${opt_a}'} ][xxx]
        def get_ns_irename_dict(xxx):
            return  [ {'env_a' : 'a'},    {'var_a' : 'a'},    {'opt_a' : 'a'}    ][xxx]
        def get_ns_iresubst_dict(xxx):
            return  [ {'env_a' : '${a}'}, {'var_a' : '${a}'}, {'opt_a' : '${a}'} ][xxx]
        gdecls.get_ns_rename_dict = mock.Mock(name = 'get_ns_rename_dict', side_effect = get_ns_rename_dict)
        gdecls.get_ns_irename_dict = mock.Mock(name = 'get_ns_rename_dict', side_effect = get_ns_irename_dict)
        gdecls.get_ns_resubst_dict = mock.Mock(name = 'get_ns_rename_dict', side_effect = get_ns_resubst_dict)
        gdecls.get_ns_iresubst_dict = mock.Mock(name = 'get_ns_iresubst_dict',  side_effect = get_ns_iresubst_dict)
        return gdecls

    @classmethod
    def _mock_gdecls_supp_dicts_5(cls, gdecls):
        def get_ns_rename_dict(xxx):
            return  [ 
                {'k' : 'env_k', 'e' : 'env_e', 'y' : 'env_y', 's' : 'env_s'}, 
                {'k' : 'var_k', 'e' : 'var_e', 'y' : 'var_y', 's' : 'var_s'},
                {'k' : 'opt_k', 'e' : 'opt_e', 'y' : 'opt_y', 's' : 'opt_s'}
            ][xxx]
        def get_ns_resubst_dict(xxx):
            return  [ 
                {'k' : '${env_k}', 'e' : '${env_e}', 'y' : '${env_y}', 's' : '${env_s}'},
                {'k' : '${var_k}', 'e' : '${var_e}', 'y' : '${var_y}', 's' : '${var_s}'},
                {'k' : '${opt_k}', 'e' : '${opt_e}', 'y' : '${opt_y}', 's' : '${opt_s}'}
            ][xxx]
        def get_ns_irename_dict(xxx):
            return  [
                {'env_k' : 'k', 'env_e' : 'e', 'env_y' : 'y', 'env_s' : 's' },
                {'var_k' : 'k', 'var_e' : 'e', 'var_y' : 'y', 'var_s' : 's' },
                {'opt_k' : 'k', 'opt_e' : 'e', 'opt_y' : 'y', 'opt_s' : 's' }
            ][xxx]
        def get_ns_iresubst_dict(xxx):
            return  [
                {'env_k' : '${k}','env_e' : '${e}',  'env_y' : '${y}', 'env_s' : '${s}' },
                {'var_k' : '${k}','var_e' : '${e}',  'var_y' : '${y}', 'var_s' : '${s}' },
                {'opt_k' : '${k}','opt_e' : '${e}',  'opt_y' : '${y}', 'opt_s' : '${s}' },
            ][xxx]
        gdecls.get_ns_rename_dict = mock.Mock(name = 'get_ns_rename_dict', side_effect = get_ns_rename_dict)
        gdecls.get_ns_irename_dict = mock.Mock(name = 'get_ns_rename_dict', side_effect = get_ns_irename_dict)
        gdecls.get_ns_resubst_dict = mock.Mock(name = 'get_ns_rename_dict', side_effect = get_ns_resubst_dict)
        gdecls.get_ns_iresubst_dict = mock.Mock(name = 'get_ns_iresubst_dict',  side_effect = get_ns_iresubst_dict)
        return gdecls

    def test___init___1(self):
        """_SConsArguments.__init__(gdecls) should call gdecls.keys() and self.__init_supp_dicts(gdecls)"""
        gdecls = self._gdecls_mock_1()
        with mock.patch.object(SConsArguments._Arguments, '_Arguments__init_supp_dicts', autospec=True) as m:
            gv = SConsArguments._Arguments(gdecls)
            try:
                m.assert_called_once_with(gv, gdecls)
                gdecls.keys.assert_called_once_with()
            except AssertionError as e:
                self.fail(str(e))
        self.assertIsInstance(gv, SConsArguments._Arguments)
        self.assertEqual(gv._Arguments__keys, ['k', 'e', 'y', 's'])

    def test___init___2(self):
        """_SConsArguments.__init__(gdecls) should initialize its iternal dicts"""
        gv = SConsArguments._Arguments(self._gdecls_mock_2())
        self.assertEqual(gv._Arguments__rename, ['rename_dict[0]', 'rename_dict[1]', 'rename_dict[2]'])
        self.assertEqual(gv._Arguments__resubst, ['resubst_dict[0]', 'resubst_dict[1]', 'resubst_dict[2]'])
        self.assertEqual(gv._Arguments__irename, ['irename_dict[0]', 'irename_dict[1]', 'irename_dict[2]'])
        self.assertEqual(gv._Arguments__iresubst, ['iresubst_dict[0]', 'iresubst_dict[1]', 'iresubst_dict[2]'])


    def test___reset_supp_dicts(self):
        """_SConsArguments.__reset_supp_dicts() should reset internal dicts to {}"""
        gv = SConsArguments._Arguments(self._gdecls_mock_2())
        gv._Arguments__reset_supp_dicts()
        self.assertEqual(gv._Arguments__rename, [{},{},{}])
        self.assertEqual(gv._Arguments__resubst, [{},{},{}])
        self.assertEqual(gv._Arguments__irename, [{},{},{}])
        self.assertEqual(gv._Arguments__iresubst, [{},{},{}])

    def test___init_supp_dicts(self):
        """_SConsArguments.__init_supp_dicts(gdecls) should initialize internal dicts appropriately"""
        gdecls = self._gdecls_mock_3()
        gv = SConsArguments._Arguments(gdecls)
        self.assertEqual(gv._Arguments__rename, [None, None, None])
        self.assertEqual(gv._Arguments__resubst, [None, None, None])
        self.assertEqual(gv._Arguments__irename, [None, None, None])
        self.assertEqual(gv._Arguments__iresubst, [None, None, None])
        self._mock_gdecls_supp_dicts_2(gdecls)
        gv._Arguments__init_supp_dicts(gdecls)
        self.assertEqual(gv._Arguments__rename, ['rename_dict[0]', 'rename_dict[1]', 'rename_dict[2]'])
        self.assertEqual(gv._Arguments__resubst, ['resubst_dict[0]', 'resubst_dict[1]', 'resubst_dict[2]'])
        self.assertEqual(gv._Arguments__irename, ['irename_dict[0]', 'irename_dict[1]', 'irename_dict[2]'])
        self.assertEqual(gv._Arguments__iresubst, ['iresubst_dict[0]', 'iresubst_dict[1]', 'iresubst_dict[2]'])

    def XxxEnvProxy_test(self, x):
        gv = SConsArguments._Arguments(self._gdecls_mock_4())
        env = { 'env_a' : 'A', 'env_b' : 'B'}
        with mock.patch('SConsArguments._ArgumentsEnvProxy', return_value = 'ok') as ProxyClass:
            if x == 'var_':
                proxy = gv.VarEnvProxy(env)
            elif x == 'opt_':
                proxy = gv.OptEnvProxy(env)
            else:
                proxy = gv.EnvProxy(env)

            try:
                ProxyClass.assert_called_once_with(env, { '%sa' % x : 'env_a' }, {'%sa' % x : '${env_a}'}, {'env_a' : '%sa' % x}, {'env_a' : '${%sa}' % x})
            except AssertionError as e:
                self.fail(str(e))
            self.assertEqual(proxy, 'ok')

    def test_VarEnvProxy(self):
        """_Arguments(gdecls).VarEnvProxy(env) should _ArgumentsEnvProxy() with appropriate arguments"""
        self.XxxEnvProxy_test('var_')

    def test_OptEnvProxy(self):
        """_Arguments(gdecls).OptEnvProxy(env) should _ArgumentsEnvProxy() with appropriate arguments"""
        self.XxxEnvProxy_test('opt_')

    def test_EnvProxy(self):
        """_Arguments(gdecls).EnvProxy(env) should _ArgumentsEnvProxy() with appropriate arguments"""
        self.XxxEnvProxy_test('')

    def test_get_keys(self):
        """_Arguments(gdecls).get_keys() should return attribute __keys"""
        gv = SConsArguments._Arguments(self._gdecls_mock_1())
        self.assertEqual(gv.get_keys(), ['k','e','y','s'])
        # expect a copy of __keys, not __keys
        self.assertIsNot(gv.get_keys(), gv._Arguments__keys)

    def test_get_ns_key_ENV_x(self):
        """_Arguments(gdecls).get_ns_key(ENV, 'x') should be raise KeyError"""
        gv = SConsArguments._Arguments(self._gdecls_mock_4())
        with self.assertRaises(KeyError):
            gv.get_ns_key(SConsArguments.ENV, 'x')

    def test_get_ns_key_VAR_x(self):
        """_Arguments(gdecls).get_ns_key(VAR, 'x') should be raise KeyError"""
        gv = SConsArguments._Arguments(self._gdecls_mock_4())
        with self.assertRaises(KeyError):
            gv.get_ns_key(SConsArguments.VAR, 'x')

    def test_get_ns_key_OPT_x(self):
        """_Arguments(gdecls).get_ns_key(OPT, 'x') should be raise KeyError"""
        gv = SConsArguments._Arguments(self._gdecls_mock_4())
        with self.assertRaises(KeyError):
            gv.get_ns_key(SConsArguments.OPT, 'x')

    def test_get_ns_key_123_a(self):
        """_Arguments(gdecls).get_ns_key(123, 'a') should be raise KeyError"""
        gv = SConsArguments._Arguments(self._gdecls_mock_4())
        with self.assertRaises(IndexError):
            gv.get_ns_key(123, 'a')

    def test_get_ns_key_ENV_a(self):
        """_Arguments(gdecls).get_ns_key(ENV, 'a') should == 'env_a'"""
        gv = SConsArguments._Arguments(self._gdecls_mock_4())
        self.assertEqual(gv.get_ns_key(SConsArguments.ENV, 'a'), 'env_a')

    def test_get_ns_key_VAR_a(self):
        """_Arguments(gdecls).get_ns_key(VAR, 'a') should == 'var_a'"""
        gv = SConsArguments._Arguments(self._gdecls_mock_4())
        self.assertEqual(gv.get_ns_key(SConsArguments.VAR, 'a'), 'var_a')

    def test_get_ns_key_OPT_a(self):
        """_Arguments(gdecls).get_ns_key(OPT, 'a') should == 'opt_a'"""
        gv = SConsArguments._Arguments(self._gdecls_mock_4())
        self.assertEqual(gv.get_ns_key(SConsArguments.OPT, 'a'), 'opt_a')

    def test_env_key_x(self):
        """_Arguments(gdecls).env_key('x') should raise KeyError"""
        gv = SConsArguments._Arguments(self._gdecls_mock_4())
        with self.assertRaises(KeyError):
            gv.env_key('x')

    def test_env_key_a(self):
        """_Arguments(gdecls).env_key('a') should == 'env_a'"""
        gv = SConsArguments._Arguments(self._gdecls_mock_4())
        self.assertEqual(gv.env_key('a'), 'env_a')

    def test_var_key_x(self):
        """_Arguments(gdecls).var_key('x') should raise KeyError"""
        gv = SConsArguments._Arguments(self._gdecls_mock_4())
        with self.assertRaises(KeyError):
            gv.var_key('x')

    def test_var_key_a(self):
        """_Arguments(gdecls).var_key('a') should == 'var_a'"""
        gv = SConsArguments._Arguments(self._gdecls_mock_4())
        self.assertEqual(gv.var_key('a'), 'var_a')

    def test_opt_key_x(self):
        """_Arguments(gdecls).opt_key('x') should raise KeyError"""
        gv = SConsArguments._Arguments(self._gdecls_mock_4())
        with self.assertRaises(KeyError):
            gv.opt_key('x')

    def test_opt_key_a(self):
        """_Arguments(gdecls).opt_key('a') should == 'opt_a'"""
        gv = SConsArguments._Arguments(self._gdecls_mock_4())
        self.assertEqual(gv.opt_key('a'), 'opt_a')

    @unittest.skip("this test should be replaced with a working one")
    def test_update_env_from_vars_1(self):
        """_Arguments(gdecls).update_env_from_vars('env', variables)"""
        def VarEnvProxy(arg): return 'var_%s_proxy' % arg
        gv = SConsArguments._Arguments(self._gdecls_mock_1())
        gv.VarEnvProxy = mock.Mock(name = 'VarEnvProxy', side_effect = VarEnvProxy)
        variables = mock.Mock(name = 'variables')
        variables.Update = mock.Mock(name = 'Update')
        gv.update_env_from_vars('env', variables)
        try:
            variables.Update.assert_called_once_with('var_env_proxy', None)
        except AssertionError as e:
            self.fail(str(e))

    @unittest.skip("this test should be replaced with a working one")
    def test_update_env_from_vars_2(self):
        """_Arguments(gdecls).update_env_from_vars('env', variables, 'arg')"""
        self.skip()
        def VarEnvProxy(arg): return 'var_%s_proxy' % arg
        gv = SConsArguments._Arguments(self._gdecls_mock_1())
        gv.VarEnvProxy = mock.Mock(name = 'VarEnvProxy', side_effect = VarEnvProxy)
        variables = mock.Mock('variables')
        variables.Update = mock.Mock(name = 'Update')
        gv.update_env_from_vars('env', variables, 'arg')
        try:
            variables.Update.assert_called_once_with('var_env_proxy', 'arg')
        except AssertionError as e:
            self.fail(str(e))

    def test_update_env_from_opts_1(self):
        """_Arguments(gdecls).update_env_from_opts('env')"""
        proxy = { 'env1' : {} }
        def OptEnvProxy(arg): return proxy[arg]
        gv = SConsArguments._Arguments(self._gdecls_mock_4())
        gv.OptEnvProxy = mock.Mock(name = 'OptEnvProxy', side_effect = OptEnvProxy)
        with mock.patch('SCons.Script.Main.GetOption', side_effect = lambda key : 'val_%s' % key) as GetOption:
            gv.update_env_from_opts('env1')
            try:
                GetOption.assert_called_once_with('opt_a')
            except AssertionError as e:
                self.fail(str(e))
            self.assertEqual(proxy['env1']['opt_a'], 'val_opt_a')

    def test_UpdateEnvironment_1(self):
        """_Arguments(gdecls).UpdateEnvironment('env') never calls update_env_from_{vars,opts}"""
        gv = self._gvars_mock_4_UpdateEnvironment()
        gv.UpdateEnvironment('env')
        try:
            gv.update_env_from_vars.assert_not_called()
            gv.update_env_from_opts.assert_not_called()
        except AssertionError as e:
            self.fail(str(e))

    def test_UpdateEnvironment_2(self):
        """_Arguments(gdecls).UpdateEnvironment('env','variables1') calls update_env_from_vars('env', 'variables1') once"""
        gv = self._gvars_mock_4_UpdateEnvironment()
        gv.UpdateEnvironment('env', 'variables1')
        try:
            gv.update_env_from_vars.assert_called_once_with('env', 'variables1', None)
            gv.update_env_from_opts.assert_not_called()
        except AssertionError as e:
            self.fail(str(e))

    def test_UpdateEnvironment_3(self):
        """_Arguments(gdecls).UpdateEnvironment('env',None,True) calls update_env_from_opts('env') once"""
        gv = self._gvars_mock_4_UpdateEnvironment()
        gv.UpdateEnvironment('env', None, True)
        try:
            gv.update_env_from_vars.assert_not_called()
            gv.update_env_from_opts.assert_called_once_with('env')
        except AssertionError as e:
            self.fail(str(e))

    def test_UpdateEnvironment_4(self):
        """_Arguments(gdecls).UpdateEnvironment('env','variables1',True) calls update_env_from_{opts,vars} once"""
        gv = self._gvars_mock_4_UpdateEnvironment()
        gv.UpdateEnvironment('env', 'variables1', True)
        try:
            gv.update_env_from_vars.assert_called_once_with('env', 'variables1', None)
            gv.update_env_from_opts.assert_called_once_with('env')
        except AssertionError as e:
            self.fail(str(e))

    def test_SaveVariables(self):
        """_Arguments(gdecls).SaveVariables(variables, 'filename1', 'env1')"""
        def VarEnvProxy(arg): return 'var_%s_proxy' % arg
        gv = SConsArguments._Arguments(self._gdecls_mock_1())
        gv.VarEnvProxy = mock.Mock(name = 'VarEnvProxy', side_effect = VarEnvProxy)
        variables = mock.Mock(name = 'variables')
        variables.Save = mock.Mock(name = 'Save')
        gv.SaveVariables(variables, 'filename1', 'env1')
        try:
            variables.Save.assert_called_once_with('filename1','var_env1_proxy')
        except AssertionError as e:
            self.fail(str(e))

    def test_GenerateVariablesHelpText_1(self):
        """_Arguments(gdecls).GenerateVariablesHelpText(variables, 'env1')"""
        def VarEnvProxy(arg): return 'var_%s_proxy' % arg
        gv = SConsArguments._Arguments(self._gdecls_mock_1())
        gv.VarEnvProxy = mock.Mock(name = 'VarEnvProxy', side_effect = VarEnvProxy)
        variables = mock.Mock(name = 'variables')
        variables.GenerateHelpText = mock.Mock(name = 'GenerateHelpText')
        gv.GenerateVariablesHelpText(variables, 'env1')
        try:
            variables.GenerateHelpText.assert_called_once_with('var_env1_proxy')
        except AssertionError as e:
            self.fail(str(e))

    def test_GenerateVariablesHelpText_2(self):
        """_Arguments(gdecls).GenerateVariablesHelpText(variables, 'env1', 'arg1', 'arg2')"""
        def VarEnvProxy(arg): return 'var_%s_proxy' % arg
        gv = SConsArguments._Arguments(self._gdecls_mock_1())
        gv.VarEnvProxy = mock.Mock(name = 'VarEnvProxy', side_effect = VarEnvProxy)
        variables = mock.Mock(name = 'variables')
        variables.GenerateHelpText = mock.Mock(name = 'GenerateHelpText')
        gv.GenerateVariablesHelpText(variables, 'env1', 'arg1', 'arg2')
        try:
            variables.GenerateHelpText.assert_called_once_with('var_env1_proxy', 'arg1', 'arg2')
        except AssertionError as e:
            self.fail(str(e))

    def test_GetCurrentValues_1(self):
        """_Arguments(gdecls).GetCurrentValues(env) works as expected"""
        gv = SConsArguments._Arguments(self._gdecls_mock_5())
        env = { 'env_k' : 'K', 'env_e' : 'E', 'env_x' : 'X' }
        current = gv.GetCurrentValues(env)
        self.assertIs(current['env_k'], env['env_k'])
        self.assertIs(current['env_e'], env['env_e'])
        self.assertEqual(current, {'env_k' : 'K', 'env_e' : 'E'})


#############################################################################
class Test__ArgumentDecl(unittest.TestCase):
    # TODO: Write unit tests for _ArgumentDecl class (see GH issue #1)
    pass

#############################################################################
class Test__ArgumentDecls(unittest.TestCase):
    # TODO: Write unit tests for _ArgumentDecls class (see GH issue #1)
    pass

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
          # GVar 'foo'
          'foo' : ( {'ENV_FOO' : 'default ENV_FOO'},                 # ENV
                    ('var_foo', 'var_foo help', ),                   # VAR
                    ('--foo', {'dest' : "opt_foo"}) ),               # OPT
          # GVar 'bar'
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
          # GVar 'foo'
          ('foo',  ( {'ENV_FOO' : 'default ENV_FOO'},                  # ENV
                     ('var_foo', 'var_foo help', ),                    # VAR
                     ('--foo', {'dest' : "opt_foo"}) )),               # OPT
          # GVar 'bar'
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
          # GVar 'foo'
          foo =  ( {'ENV_FOO' : 'default ENV_FOO'},                  # ENV
                   ('var_foo', 'var_foo help', ),                    # VAR
                   ('--foo', {'dest' : "opt_foo"}) ),                # OPT
          # GVar 'bar'
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
           # GVar 'foo'
           [('foo',(  {'ENV_FOO' : 'ENV default FOO'},                    # ENV
                      ('FOO',         'FOO variable help', ),             # VAR
                      ('--foo',       {'dest' : "opt_foo"})         ))],  # OPT
           # GVar 'geez'
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
               , Test__compose_dicts
               , Test__invert_dict
               , Test__ArgumentsEnvProxy
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
