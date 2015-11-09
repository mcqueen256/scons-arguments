""" SConsArguments.ProxyTests

Unit tests for SConsArguments.Proxy
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

import SConsArguments.Proxy
import unittest

# The mock module does not come as a part of python 2.x stdlib, it has to be
# installed separatelly. Here we detect whether mock is present and if not,
# we skip all the tests that use mock.
_mock_missing = True
try:
    # Try unittest.mock first (python 3.x) ...
    import unittest.mock as mock
    _mock_missing = False
except ImportError:
    try:
        # ... then try mock (python 2.x)
        import mock
        _mock_missing = False
    except ImportError:
        # mock not installed
        pass

#############################################################################
class Test__ArgumentsProxy(unittest.TestCase):
    def test___init___1(self):
        """_ArgumentsProxy.__init__(target) should set default attributes"""
        target = 'target'
        proxy = SConsArguments.Proxy._ArgumentsProxy(target)
        self.assertIs(proxy.target, target)
        self.assertEqual(proxy._rename_dict, {})
        self.assertEqual(proxy._irename_dict, {})
        self.assertEqual(proxy._resubst_dict, {})
        self.assertEqual(proxy._iresubst_dict, {})
        self.assertEqual(proxy.is_strict(), False)

    def test___init___2(self):
        """_ArgumentsProxy.__init__(target, arg1, arg2, arg3, arg4, True) should set attributes"""
        target = 'target'
        arg1, arg2, arg3, arg4 = 'arg1', 'arg2', 'arg3', 'arg4'
        proxy = SConsArguments.Proxy._ArgumentsProxy(target, arg1, arg2, arg3, arg4, True)
        self.assertIs(proxy.target, target)
        self.assertIs(proxy._rename_dict,   arg1)
        self.assertIs(proxy._resubst_dict,  arg2)
        self.assertIs(proxy._irename_dict,  arg3)
        self.assertIs(proxy._iresubst_dict, arg4)
        self.assertIs(proxy.is_strict(), True)

    def test_is_strict(self):
        """Test <_ArgumentsProxy>.is_strict()"""
        self.assertIs(SConsArguments.Proxy._ArgumentsProxy('tgt', strict = False).is_strict(), False)
        self.assertIs(SConsArguments.Proxy._ArgumentsProxy('tgt', strict = True).is_strict(), True)

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_set_strict_False_calls__setup_methods_False(self):
        """<_ArgumentsProxy>.set_strict(False) should call <_ArgumentsProxy>.__setup_methods(False)"""
        proxy = SConsArguments.Proxy._ArgumentsProxy('tgt')
        proxy._ArgumentsProxy__setup_methods = mock.Mock(name = '__setup_methods')
        proxy.set_strict(False)
        try:
            proxy._ArgumentsProxy__setup_methods.assert_called_with(False)
        except AssertionError as e:
            self.fail(str(e))

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_set_strict_True_calls__setup_methods_True(self):
        """<_ArgumentsProxy>.set_strict(True) should call <_ArgumentsProxy>.__setup_methods(True)"""
        proxy = SConsArguments.Proxy._ArgumentsProxy('tgt')
        proxy._ArgumentsProxy__setup_methods = mock.Mock(name = '__setup_methods')
        proxy.set_strict(True)
        try:
            proxy._ArgumentsProxy__setup_methods.assert_called_with(True)
        except AssertionError as e:
            self.fail(str(e))

    def test_set_strict_False(self):
        """<_ArgumentsProxy>.is_strict() should be False after <_ArgumentsProxy>.set_strict(False)"""
        proxy = SConsArguments.Proxy._ArgumentsProxy('tgt')
        proxy.set_strict(False)
        self.assertIs(proxy.is_strict(), False)

    def test_set_strict_True(self):
        """<_ArgumentsProxy>.is_strict() should be True after <_ArgumentsProxy>.set_strict(True)"""
        proxy = SConsArguments.Proxy._ArgumentsProxy('tgt')
        proxy.set_strict(True)
        self.assertIs(proxy.is_strict(), True)

    def test___setup_methods_True(self):
        """<_ArgumentsProxy>.__setup_methods(True) should setup appropriate methods"""
        proxy = SConsArguments.Proxy._ArgumentsProxy('tgt', strict = False)
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
        proxy = SConsArguments.Proxy._ArgumentsProxy('tgt', strict = True)
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
        SConsArguments.Proxy._ArgumentsProxy(tgt).__delitem__('a')
        self.assertEqual(tgt, {})

    def test___delitem___2(self):
        """_ArgumentsProxy({'a' : 'A'}, strict = True).__delitem__('a') should raise KeyError"""
        with self.assertRaises(KeyError):
            SConsArguments.Proxy._ArgumentsProxy({'a' : 'A'}, strict = True).__delitem__('a')

    def test___delitem___3(self):
        """_ArgumentsProxy({'b' : 'B'}, rename = {'a' : 'b'}).__delitem__('a') should delete item 'b'"""
        tgt = { 'b' : 'B' }
        SConsArguments.Proxy._ArgumentsProxy(tgt, rename = { 'a' : 'b'}).__delitem__('a')
        self.assertEqual(tgt, {})

    def test___delitem___4(self):
        """_ArgumentsProxy({'b' : 'B'}, rename = {'a' : 'b'}, strict = True).__delitem__('a') should delete item 'b'"""
        tgt = { 'b' : 'B' }
        SConsArguments.Proxy._ArgumentsProxy(tgt, rename = { 'a' : 'b'}, strict = True).__delitem__('a')
        self.assertEqual(tgt, {})

    def test___getitem___1(self):
        """_ArgumentsProxy({'a' : 'A'}).__getitem__('a') should return 'A'"""
        tgt = { 'a' : 'A' }
        self.assertEqual(SConsArguments.Proxy._ArgumentsProxy({'a' : 'A'}).__getitem__('a'), 'A')

    def test___getitem___2(self):
        """_ArgumentsProxy({'a' : 'A'}, strict = True).__getitem__('a') should raise KeyError"""
        with self.assertRaises(KeyError):
            SConsArguments.Proxy._ArgumentsProxy({'a' : 'A'}, strict = True).__getitem__('a')

    def test__getitem___3(self):
        """_ArgumentsProxy({'b' : 'B'}, rename = {'a' : 'b'}).__getitem__('a') should return 'B'"""
        self.assertEqual(SConsArguments.Proxy._ArgumentsProxy({'b' : 'B'}, rename = {'a' : 'b'}).__getitem__('a'), 'B')

    def test___getitem___4(self):
        """_ArgumentsProxy({'b' : 'B'}, rename = {'a' : 'b'}, strict = True).__getitem__('a') should return 'B'"""
        self.assertEqual(SConsArguments.Proxy._ArgumentsProxy({'b' : 'B'}, rename = {'a' : 'b'}, strict = True).__getitem__('a'), 'B')

    def test__setitem___1(self):
        """_ArgumentsProxy({}).__setitem__('a', 'A') should set item 'a' to 'A'"""
        proxy = SConsArguments.Proxy._ArgumentsProxy({})
        proxy.__setitem__('a', 'A')
        self.assertEqual(proxy['a'], 'A')

    def test___setitem___2(self):
        """_ArgumentsProxy({'a' : 'B'}).__setitem__('a', 'A') should set item 'a' to 'A'"""
        tgt = {'a' : 'B'}
        proxy = SConsArguments.Proxy._ArgumentsProxy(tgt)
        proxy.__setitem__('a', 'A')
        self.assertEqual(tgt['a'], 'A')

    def test__setitem___3(self):
        """_ArgumentsProxy({'a' : 'B'}, rename = { 'a' : 'a' }, strict = True).__setitem__('a', 'A') should set item 'a' to 'A'"""
        tgt = {'a' : 'B'}
        proxy = SConsArguments.Proxy._ArgumentsProxy(tgt, rename = { 'a' : 'a' }, strict = True)
        proxy.__setitem__('a', 'A')
        self.assertEqual(tgt['a'], 'A')

    def test___setitem___4(self):
        """_ArgumentsProxy({'a' : 'B'}, strict = True).__setitem__('a', 'A') should raise KeyError"""
        tgt = {'a' : 'B'}
        proxy = SConsArguments.Proxy._ArgumentsProxy(tgt, strict = True)
        with self.assertRaises(KeyError):
            proxy.__setitem__('a', 'A')
        self.assertEqual(tgt['a'], 'B')

    def test_get_1(self):
        """_ArgumentsProxy({'a' : 'A'}).get('a') should return 'A'"""
        self.assertEqual(SConsArguments.Proxy._ArgumentsProxy({'a' : 'A'}).get('a'), 'A')

    def test_get_2(self):
        """_ArgumentsProxy({'a' : 'A'}).get('b') should return None"""
        self.assertEqual(SConsArguments.Proxy._ArgumentsProxy({'a' : 'A'}).get('b'), None)

    def test_get_3(self):
        """_ArgumentsProxy({'a' : 'A'}, rename = { 'b' : 'a' }).get('b') should return 'A'"""
        self.assertEqual(SConsArguments.Proxy._ArgumentsProxy({'a' : 'A'}, rename = { 'b' : 'a'}).get('b'), 'A')

    def test_get_4(self):
        """_ArgumentsProxy({'a' : 'A'}, rename = { 'b' : 'a' }).get('a') should return 'A'"""
        self.assertEqual(SConsArguments.Proxy._ArgumentsProxy({'a' : 'A'}, rename = { 'b' : 'a'}).get('a'), 'A')

    def test_get_5(self):
        """_ArgumentsProxy({'a' : 'A'}, strict = True).get('a') should raise KeyError"""
        with self.assertRaises(KeyError):
            SConsArguments.Proxy._ArgumentsProxy({'a' : 'A'}, strict = True).get('a')

    def test_get_6(self):
        """_ArgumentsProxy({'a' : 'A'}, rename = { 'b' : 'a' }, strict = True).get('b') should return 'A'"""
        self.assertEqual(SConsArguments.Proxy._ArgumentsProxy({'a' : 'A'}, rename = { 'b' : 'a' }, strict = True).get('b'), 'A')

    def test_has_key_1(self):
        """_ArgumentsProxy({'a' : 'A'}).has_key('a') should return True"""
        self.assertTrue(SConsArguments.Proxy._ArgumentsProxy({'a' : 'A'}).has_key('a'))

    def test_has_key_2(self):
        """_ArgumentsProxy({'a' : 'A'}).has_key('b') should return False"""
        self.assertFalse(SConsArguments.Proxy._ArgumentsProxy({'a' : 'A'}).has_key('b'))

    def test_has_key_3(self):
        """_ArgumentsProxy({'a' : 'A'}, rename = {'b' : 'a'}).has_key('a') should return True"""
        self.assertTrue(SConsArguments.Proxy._ArgumentsProxy({'a' : 'A'}, rename = {'b' : 'a'}).has_key('a'))

    def test_has_key_4(self):
        """_ArgumentsProxy({'a' : 'A'}, rename = {'b' : 'a'}).has_key('b') should return True"""
        self.assertTrue(SConsArguments.Proxy._ArgumentsProxy({'a' : 'A'}, rename = {'b' : 'a'}).has_key('b'))

    def test_has_key_5(self):
        """_ArgumentsProxy({'a' : 'A'}, rename = {'b' : 'a'}, strict = True).has_key('a') should return False"""
        self.assertFalse(SConsArguments.Proxy._ArgumentsProxy({'a' : 'A'}, rename = {'b' : 'a'}, strict = True).has_key('a'))

    def test_has_key_6(self):
        """_ArgumentsProxy({'a' : 'A'}, rename = {'b' : 'a'}, strict = True).has_key('b') should return True"""
        self.assertTrue(SConsArguments.Proxy._ArgumentsProxy({'a' : 'A'}, rename = {'b' : 'a'}, strict = True).has_key('b'))

    def test_has_key_7(self):
        """_ArgumentsProxy({'a' : 'A'}, rename = {'b' : 'c'}, strict = True).has_key('b') should return False"""
        self.assertFalse(SConsArguments.Proxy._ArgumentsProxy({'a' : 'A'}, rename = {'b' : 'c'}, strict = True).has_key('b'))

    def test___contains___1(self):
        """_ArgumentsProxy({'a' : 'A'}).__contains__('a') should return True"""
        self.assertTrue(SConsArguments.Proxy._ArgumentsProxy({'a' : 'A'}).__contains__('a'))

    def test___contains___2(self):
        """_ArgumentsProxy({'a' : 'A'}).__contains__('b') should return False"""
        self.assertFalse(SConsArguments.Proxy._ArgumentsProxy({'a' : 'A'}).__contains__('b'))

    def test___contains___3(self):
        """_ArgumentsProxy({'a' : 'A'}, rename = {'b' : 'a'}).__contains__('a') should return True"""
        self.assertTrue(SConsArguments.Proxy._ArgumentsProxy({'a' : 'A'}, rename = {'b' : 'a'}).__contains__('a'))

    def test___contains___4(self):
        """_ArgumentsProxy({'a' : 'A'}, rename = {'b' : 'a'}).__contains__('b') should return True"""
        self.assertTrue(SConsArguments.Proxy._ArgumentsProxy({'a' : 'A'}, rename = {'b' : 'a'}).__contains__('b'))

    def test___contains___5(self):
        """_ArgumentsProxy({'a' : 'A'}, rename = {'b' : 'a'}, strict = True).__contains__('a') should return False"""
        self.assertFalse(SConsArguments.Proxy._ArgumentsProxy({'a' : 'A'}, rename = {'b' : 'a'}, strict = True).__contains__('a'))

    def test___contains___6(self):
        """_ArgumentsProxy({'a' : 'A'}, rename = {'b' : 'a'}, strict = True).__contains__('b') should return True"""
        self.assertTrue(SConsArguments.Proxy._ArgumentsProxy({'a' : 'A'}, rename = {'b' : 'a'}, strict = True).__contains__('b'))

    def test___contains___7(self):
        """_ArgumentsProxy({'a' : 'A'}, rename = {'b' : 'c'}, strict = True).__contains__('b') should return False"""
        self.assertFalse(SConsArguments.Proxy._ArgumentsProxy({'a' : 'A'}, rename = {'b' : 'c'}, strict = True).__contains__('b'))

    def test_items_1(self):
        """_ArgumentsProxy({'a' : 'A', 'b' : 'B'}).items() should be [('a', 'A'), ('b', 'B')]"""
        self.assertEqual(SConsArguments.Proxy._ArgumentsProxy({'a' : 'A', 'b' : 'B'}).items(), ([('a', 'A'), ('b', 'B')]))

    def test_items_2(self):
        """_ArgumentsProxy({'a' : 'A', 'b' : 'B'}, irename = {'a' : 'c'}).items() should be [('c', 'A'), ('b', 'B')]"""
        self.assertEqual(SConsArguments.Proxy._ArgumentsProxy({'a' : 'A', 'b' : 'B'}, irename = { 'a' : 'c'}).items(), ([('c', 'A'), ('b', 'B')]))

    def test_items_3(self):
        """_ArgumentsProxy({'a' : 'A', 'b' : 'B'}, rename = {'c' : 'a'}, strict = True).items() should be [('c', 'A')]"""
        self.assertEqual(SConsArguments.Proxy._ArgumentsProxy({'a' : 'A', 'b' : 'B'}, rename = { 'c' : 'a'}, strict = True).items(), ([('c', 'A')]))

    def test_items_4(self):
        """_ArgumentsProxy({'a' : '${a}'}, irename = {'a' : 'b'}, iresubst = {'a' : '${b}'}).items() should be [('b', '${b}')]"""
        self.assertEqual(SConsArguments.Proxy._ArgumentsProxy({'a' : '${a}'}, irename = {'a' : 'b'}, iresubst = {'a' : '${b}'}).items(), [('b', '${b}')])

    def test_items_5(self):
        """_ArgumentsProxy({'a' : 'a'}, irename = {'a' : 'b'}, iresubst = {'a' : '${b}'}).items() should be [('b', 'a')]"""
        self.assertEqual(SConsArguments.Proxy._ArgumentsProxy({'a' : 'a'}, irename = {'a' : 'b'}, iresubst = {'a' : '${b}'}).items(), [('b', 'a')])

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_subst_1(self):
        """_ArgumentsProxy(tgt).subst('${a} ${b}') should call tgt.subst('${a} ${b}')"""
        tgt = mock.Mock(name = 'tgt')
        tgt.subst = mock.Mock(name = 'tgt.subst')
        SConsArguments.Proxy._ArgumentsProxy(tgt).subst('${a} ${b}')
        try:
            tgt.subst.assert_called_with('${a} ${b}')
        except AssertionError as e:
            self.fail(str(e))

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_subst_2(self):
        """_ArgumentsProxy(tgt, resubst = {'b' : '${c}}).subst('${a} ${b}') should call tgt.subst('${a} ${c}')"""
        tgt = mock.Mock(name = 'tgt')
        tgt.subst = mock.Mock(name = 'tgt.subst')
        SConsArguments.Proxy._ArgumentsProxy(tgt, resubst = {'b' : '${c}'}).subst('${a} ${b}')
        try:
            tgt.subst.assert_called_with('${a} ${c}')
        except AssertionError as e:
            self.fail(str(e))

#############################################################################
if __name__ == "__main__":
    ldr = unittest.TestLoader()
    suite = unittest.TestSuite()
    # Load tests to test suite
    tclasses = [ Test__ArgumentsProxy ]

    for tclass in tclasses:
        suite.addTests(ldr.loadTestsFromTestCase(tclass))

    if not unittest.TextTestRunner(verbosity = 2).run(suite).wasSuccessful():
        sys.exit(1)

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
