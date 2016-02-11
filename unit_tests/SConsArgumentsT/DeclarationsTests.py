""" SConsArguments.DeclarationsTests

Unit tests for SConsArguments.Declarations
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

import SConsArguments.Declarations
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
class Test__ArgumentDeclarations(unittest.TestCase):
    @unittest.skipIf(_mock_missing, "requires mock module")
    def test___init___mock_1(self):
        """Test, using mock, _ArgumentDeclarations.__init__() with no arguments"""
        with mock.patch.object(SConsArguments.Declarations._ArgumentDeclarations, '_ArgumentDeclarations__validate_values') as __validate_values, \
             mock.patch.object(SConsArguments.Declarations._ArgumentDeclarations, '_ArgumentDeclarations__update_supp_dicts') as __update_supp_dicts:
            decls = SConsArguments.Declarations._ArgumentDeclarations()
            self.assertFalse(decls._ArgumentDeclarations__committed)
            try:
                __validate_values.assert_called_once_with()
                __update_supp_dicts.assert_called_once_with()
            except AssertionError as e:
                self.fail(str(e))

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test___init___mock_2(self):
        """Test, using mocks, _ArgumentDeclarations.__init__() with mixed arguments"""
        with mock.patch.object(SConsArguments.Declarations._ArgumentDeclarations, '_ArgumentDeclarations__validate_values') as __validate_values, \
             mock.patch.object(SConsArguments.Declarations._ArgumentDeclarations, '_ArgumentDeclarations__update_supp_dicts') as __update_supp_dicts:
            decls = SConsArguments.Declarations._ArgumentDeclarations([('a','A'),('b','B')], d = 'D')
        self.assertFalse(decls._ArgumentDeclarations__committed)
        try:
            __validate_values.assert_called_once_with([('a','A'),('b','B')], d = 'D')
            __update_supp_dicts.assert_called_once_with()
        except AssertionError as e:
            self.fail(str(e))

    def test___init___noargs_1(self):
        """Test _ArgumentDeclarations.__init__() without arguments"""
        decls = SConsArguments.Declarations._ArgumentDeclarations()
        self.assertFalse(decls._ArgumentDeclarations__committed)
        self.assertEqual(decls, dict())

    def test___init___dict_1(self):
        """Test _ArgumentDeclarations.__init__() with dict argument"""
        a = SConsArguments.DeclareArgument()
        b = SConsArguments.DeclareArgument()
        decls = SConsArguments.Declarations._ArgumentDeclarations({'a' : a, 'b' : b})
        self.assertFalse(decls._ArgumentDeclarations__committed)
        self.assertEqual(decls, {'a' : a, 'b' : b})

    def test___init___list_1(self):
        """Test _ArgumentDeclarations.__init__() with list argument"""
        a = SConsArguments.DeclareArgument()
        b = SConsArguments.DeclareArgument()
        decls = SConsArguments.Declarations._ArgumentDeclarations([('a' , a), ('b' , b)])
        self.assertFalse(decls._ArgumentDeclarations__committed)
        self.assertEqual(decls, {'a' : a, 'b' : b})

    def test___init___kwargs_1(self):
        """Test _ArgumentDeclarations.__init__() with keyword arguments"""
        a = SConsArguments.DeclareArgument()
        b = SConsArguments.DeclareArgument()
        decls = SConsArguments.Declarations._ArgumentDeclarations(a = a, b = b)
        self.assertFalse(decls._ArgumentDeclarations__committed)
        self.assertEqual(decls, {'a' : a, 'b' : b})

    def test___init___mix_2(self):
        """Test _ArgumentDeclarations.__init__() with mix of arguments and keywords"""
        a = SConsArguments.DeclareArgument()
        b = SConsArguments.DeclareArgument()
        decls = SConsArguments.Declarations._ArgumentDeclarations({'a' : a}, b = b)
        self.assertFalse(decls._ArgumentDeclarations__committed)
        self.assertEqual(decls, {'a' : a, 'b' : b})

    def test___init___TypeError_1(self):
        """_ArgumentDeclarations.__init__({'a': 'b'}) should raise TypeError"""
        with self.assertRaises(TypeError) as cm:
            SConsArguments.Declarations._ArgumentDeclarations({'a' : 'A'})
        self.assertEqual(str(cm.exception), "value must be an instance of _ArgumentDeclaration, %r is not allowed" % 'A')

    def test___init___error_ENV_already_declared(self):
        """_ArgumentDeclarations.__init__() should raise RuntimeError when two declarations refer to same construction variable"""
        a1 = SConsArguments.Declarations._ArgumentDeclaration(('a', None))
        a2 = SConsArguments.Declarations._ArgumentDeclaration(('a', None))
        with self.assertRaises(RuntimeError) as cm:
            decls = SConsArguments.Declarations._ArgumentDeclarations(a1 = a1, a2 = a2)
        self.assertEqual(str(cm.exception), "variable 'a' is already declared")

    def test___init___error_VAR_already_declared(self):
        """_ArgumentDeclarations.__init__() should raise RuntimeError when two declarations refer to same command-line variable"""
        a1 = SConsArguments.Declarations._ArgumentDeclaration(None, ('a',))
        a2 = SConsArguments.Declarations._ArgumentDeclaration(None, ('a',))
        with self.assertRaises(RuntimeError) as cm:
            decls = SConsArguments.Declarations._ArgumentDeclarations(a1 = a1, a2 = a2)
        self.assertEqual(str(cm.exception), "variable 'a' is already declared")

    def test___init___error_OPT_already_declared(self):
        """_ArgumentDeclarations.__init__() should raise RuntimeError when two declarations refer to command-line option with same 'dest'"""
        a1 = SConsArguments.Declarations._ArgumentDeclaration(None, None, ('--a1', {'dest' : 'a'}))
        a2 = SConsArguments.Declarations._ArgumentDeclaration(None, None, ('--a2', {'dest' : 'a'}))
        with self.assertRaises(RuntimeError) as cm:
            decls = SConsArguments.Declarations._ArgumentDeclarations(a1 = a1, a2 = a2)
        self.assertEqual(str(cm.exception), "variable 'a' is already declared")

    def test___reset_supp_dicts_1(self):
        """<_ArgumentDeclarations>.__reset_supp_dicts() should reset all supplementary dictionaries, including resubst dicts"""
        a = SConsArguments.Declarations._ArgumentDeclaration(('ENV_a',None), ('VAR_a',), ('--a', {'dest' : 'OPT_a'}))
        b = SConsArguments.Declarations._ArgumentDeclaration(('ENV_b',None), ('VAR_b',), ('--b', {'dest' : 'OPT_b'}))
        decls = SConsArguments.Declarations._ArgumentDeclarations(a = a, b = b)
        decls.commit() # to generate resubst/iresubst dicts
        decls._ArgumentDeclarations__reset_supp_dicts()
        self.assertEqual(decls._ArgumentDeclarations__rename,   [dict(),dict(),dict()])
        self.assertEqual(decls._ArgumentDeclarations__irename,  [dict(),dict(),dict()])
        self.assertEqual(decls._ArgumentDeclarations__resubst,  [dict(),dict(),dict()])
        self.assertEqual(decls._ArgumentDeclarations__iresubst, [dict(),dict(),dict()])

    def test___replace_key_in_supp_dicts__ENV_1(self):
        """<_ArgumentDeclarations>.__replace_key_in_supp_dicts(ENV,'a','ENX_a') should replace 'ENV_a' with 'ENX_a' in rename/irename dicts"""
        a = SConsArguments.Declarations._ArgumentDeclaration(('ENV_a',None), ('VAR_a',), ('--a', {'dest' : 'OPT_a'}))
        b = SConsArguments.Declarations._ArgumentDeclaration(('ENV_b',None), ('VAR_b',), ('--b', {'dest' : 'OPT_b'}))
        decls = SConsArguments.Declarations._ArgumentDeclarations(a = a, b = b)
        decls._ArgumentDeclarations__replace_key_in_supp_dicts(SConsArguments.ENV, 'a', 'ENX_a')
        self.assertEqual(decls._ArgumentDeclarations__rename,   [  {'a' : 'ENX_a', 'b' : 'ENV_b'},
                                                            {'a' : 'VAR_a', 'b' : 'VAR_b'},
                                                            {'a' : 'OPT_a', 'b' : 'OPT_b'} ])
        self.assertEqual(decls._ArgumentDeclarations__irename,  [  {'ENX_a' : 'a', 'ENV_b' : 'b'},
                                                            {'VAR_a' : 'a', 'VAR_b' : 'b'},
                                                            {'OPT_a' : 'a', 'OPT_b' : 'b'} ])

    def test___replace_key_in_supp_dicts__VAR_1(self):
        """<_ArgumentDeclarations>.__replace_key_in_supp_dicts(VAR,'a','VAX_a') should replace 'VAR_a' with 'VAX_a' in rename/irename dicts"""
        a = SConsArguments.Declarations._ArgumentDeclaration(('ENV_a',None), ('VAR_a',), ('--a', {'dest' : 'OPT_a'}))
        b = SConsArguments.Declarations._ArgumentDeclaration(('ENV_b',None), ('VAR_b',), ('--b', {'dest' : 'OPT_b'}))
        decls = SConsArguments.Declarations._ArgumentDeclarations(a = a, b = b)
        decls._ArgumentDeclarations__replace_key_in_supp_dicts(SConsArguments.VAR, 'a', 'VAX_a')
        self.assertEqual(decls._ArgumentDeclarations__rename,   [  {'a' : 'ENV_a', 'b' : 'ENV_b'},
                                                            {'a' : 'VAX_a', 'b' : 'VAR_b'},
                                                            {'a' : 'OPT_a', 'b' : 'OPT_b'} ])
        self.assertEqual(decls._ArgumentDeclarations__irename,  [  {'ENV_a' : 'a', 'ENV_b' : 'b'},
                                                            {'VAX_a' : 'a', 'VAR_b' : 'b'},
                                                            {'OPT_a' : 'a', 'OPT_b' : 'b'} ])

    def test___replace_key_in_supp_dicts__OPT_1(self):
        """<_ArgumentDeclarations>.__replace_key_in_supp_dicts(OPT,'a','OPX_a') should replace 'OPT_a' with 'OPX_a' in rename/irename dicts"""
        a = SConsArguments.Declarations._ArgumentDeclaration(('ENV_a',None), ('VAR_a',), ('--a', {'dest' : 'OPT_a'}))
        b = SConsArguments.Declarations._ArgumentDeclaration(('ENV_b',None), ('VAR_b',), ('--b', {'dest' : 'OPT_b'}))
        decls = SConsArguments.Declarations._ArgumentDeclarations(a = a, b = b)
        decls._ArgumentDeclarations__replace_key_in_supp_dicts(SConsArguments.OPT, 'a', 'OPX_a')
        self.assertEqual(decls._ArgumentDeclarations__rename,   [  {'a' : 'ENV_a', 'b' : 'ENV_b'},
                                                            {'a' : 'VAR_a', 'b' : 'VAR_b'},
                                                            {'a' : 'OPX_a', 'b' : 'OPT_b'} ])
        self.assertEqual(decls._ArgumentDeclarations__irename,  [  {'ENV_a' : 'a', 'ENV_b' : 'b'},
                                                            {'VAR_a' : 'a', 'VAR_b' : 'b'},
                                                            {'OPX_a' : 'a', 'OPT_b' : 'b'} ])
    def test___replace_key_in_supp_dicts__nokey_1(self):
        """<_ArgumentDeclarations>.__replace_key_in_supp_dicts(ENV,'inexistent', 'foo') should add new name mapping"""
        a = SConsArguments.Declarations._ArgumentDeclaration(('ENV_a',None), ('VAR_a',), ('--a', {'dest' : 'OPT_a'}))
        b = SConsArguments.Declarations._ArgumentDeclaration(('ENV_b',None), ('VAR_b',), ('--b', {'dest' : 'OPT_b'}))
        decls = SConsArguments.Declarations._ArgumentDeclarations(a = a, b = b)
        decls._ArgumentDeclarations__replace_key_in_supp_dicts(SConsArguments.ENV, 'inexistent', 'foo')
        self.assertEqual(decls._ArgumentDeclarations__rename,   [  {'a' : 'ENV_a', 'b' : 'ENV_b', 'inexistent' : 'foo'},
                                                            {'a' : 'VAR_a', 'b' : 'VAR_b'},
                                                            {'a' : 'OPT_a', 'b' : 'OPT_b'} ])
        self.assertEqual(decls._ArgumentDeclarations__irename,  [  {'ENV_a' : 'a', 'ENV_b' : 'b', 'foo': 'inexistent'},
                                                            {'VAR_a' : 'a', 'VAR_b' : 'b'},
                                                            {'OPT_a' : 'a', 'OPT_b' : 'b'} ])

    def test___del_from_supp_dicts_1(self):
        """<_ArgumentDeclarations>.__del_from_supp_dicts('a') should delete 'a' from rename/irename dictionaries"""
        a = SConsArguments.Declarations._ArgumentDeclaration(('ENV_a',None), ('VAR_a',), ('--a', {'dest' : 'OPT_a'}))
        b = SConsArguments.Declarations._ArgumentDeclaration(('ENV_b',None), ('VAR_b',), ('--b', {'dest' : 'OPT_b'}))
        decls = SConsArguments.Declarations._ArgumentDeclarations(a = a, b = b)
        decls._ArgumentDeclarations__del_from_supp_dicts('a')
        self.assertEqual(decls._ArgumentDeclarations__rename,   [  {'b' : 'ENV_b'},
                                                            {'b' : 'VAR_b'},
                                                            {'b' : 'OPT_b'} ])
        self.assertEqual(decls._ArgumentDeclarations__irename,  [  {'ENV_b' : 'b'},
                                                            {'VAR_b' : 'b'},
                                                            {'OPT_b' : 'b'} ])

    def test___del_from_supp_dicts_2(self):
        """<_ArgumentDeclarations>.__del_from_supp_dicts('b') should delete 'a' from rename/irename dictionaries"""
        a = SConsArguments.Declarations._ArgumentDeclaration(('ENV_a',None), ('VAR_a',), ('--a', {'dest' : 'OPT_a'}))
        b = SConsArguments.Declarations._ArgumentDeclaration(('ENV_b',None), ('VAR_b',), ('--b', {'dest' : 'OPT_b'}))
        decls = SConsArguments.Declarations._ArgumentDeclarations(a = a, b = b)
        decls._ArgumentDeclarations__del_from_supp_dicts('b')
        self.assertEqual(decls._ArgumentDeclarations__rename,   [  {'a' : 'ENV_a'},
                                                            {'a' : 'VAR_a'},
                                                            {'a' : 'OPT_a'} ])
        self.assertEqual(decls._ArgumentDeclarations__irename,  [  {'ENV_a' : 'a'},
                                                            {'VAR_a' : 'a'},
                                                            {'OPT_a' : 'a'} ])

    def test___ensure_not_committed_1(self):
        """<_ArgumetnDecls>.__ensure_not_committed() should not raise on a committed <_ArgumentDeclarations>"""
        decls = SConsArguments.Declarations._ArgumentDeclarations()
        try:
            decls._ArgumentDeclarations__ensure_not_committed()
        except RuntimeError:
            self.fail("__ensure_not_committed() raised RuntimeError unexpectedly")

    def test___ensure_not_committed_2(self):
        """<_ArgumetnDecls>.__ensure_not_committed() should raise RuntimeError on an uncommitted <_ArgumentDeclarations>"""
        decls = SConsArguments.Declarations._ArgumentDeclarations()
        decls.commit()
        with self.assertRaises(RuntimeError) as cm:
           decls._ArgumentDeclarations__ensure_not_committed()
        self.assertEqual(str(cm.exception), "declarations are already committed, can't be modified")

    def test___ensure_committed_1(self):
        """<_ArgumetnDecls>.__ensure_committed() should not raise on a committed <_ArgumentDeclarations>"""
        decls = SConsArguments.Declarations._ArgumentDeclarations()
        decls.commit()
        try:
            decls._ArgumentDeclarations__ensure_committed()
        except RuntimeError:
            self.fail("__ensure_committed() raised RuntimeError unexpectedly")

    def test___ensure_committed_2(self):
        """<_ArgumetnDecls>.__ensure_committed() should raise RuntimeError on an uncommitted <_ArgumentDeclarations>"""
        decls = SConsArguments.Declarations._ArgumentDeclarations()
        with self.assertRaises(RuntimeError) as cm:
           decls._ArgumentDeclarations__ensure_committed()
        self.assertEqual(str(cm.exception), "declarations must be committed before performing this operation")

    def test_setdefault__TypeError_1(self):
        """<_ArgumentDeclarations>.setdefault('foo', None) should raise TypeError"""
        decls = SConsArguments.Declarations._ArgumentDeclarations()
        with self.assertRaises(TypeError) as cm:
            decls.setdefault('foo', None)
        self.assertEqual(str(cm.exception), "value must be an instance of _ArgumentDeclaration, None is not allowed")

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_setdefault__0(self):
        """<_ArgumentDeclarations>.setdefault('foo', 'bar') does not invoke __ensure_not_committed() nor __validate_value()"""
        decls = SConsArguments.Declarations._ArgumentDeclarations()
        decls._ArgumentDeclarations__ensure_not_committed = mock.Mock(name = '__ensure_not_commited')
        with mock.patch.object(SConsArguments.Declarations._ArgumentDeclarations, '_ArgumentDeclarations__validate_value') as __validate_value:
            decls.setdefault('foo')
        try:
            decls._ArgumentDeclarations__ensure_not_committed.assert_not_called()
            __validate_value.assert_not_called()
        except AssertionError as e:
            self.fail(str(e))
        foo = decls['foo']
        self.assertIs(foo, None)

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_setdefault__1(self):
        """<_ArgumentDeclarations>.setdefault('foo', 'bar') invokes __ensure_not_committed() and __validate_value()"""
        decls = SConsArguments.Declarations._ArgumentDeclarations()
        decls._ArgumentDeclarations__ensure_not_committed = mock.Mock(name = '__ensure_not_commited')
        with mock.patch.object(SConsArguments.Declarations._ArgumentDeclarations, '_ArgumentDeclarations__validate_value') as __validate_value:
            decls.setdefault('foo', 'bar')
        try:
            decls._ArgumentDeclarations__ensure_not_committed.assert_called_once_with()
            __validate_value.assert_called_once_with('bar')
        except AssertionError as e:
            self.fail(str(e))
        foo = decls['foo']
        self.assertEqual(foo, 'bar')

    def test_setdefault__2(self):
        """<_ArgumentDeclarations>.setdefault('a', <_ArgumentDeclaration>) should set default value appropriatelly"""
        a1 = SConsArguments.Declarations._ArgumentDeclaration(('ENV_a1','A1'), ('VAR_a1',), ('--a1', {'dest' : 'OPT_a1'}))
        a2 = SConsArguments.Declarations._ArgumentDeclaration(('ENV_a2','A2'), ('VAR_a2',), ('--a2', {'dest' : 'OPT_a2'}))
        decls = SConsArguments.Declarations._ArgumentDeclarations()
        decls.setdefault('a', a1)
        self.assertIs(decls['a'], a1)
        decls.update(a = a2)
        self.assertIs(decls['a'], a2)

    def test_setdefault__3(self):
        """<_ArgumentDeclarations>.setdefault('a', <_ArgumentDeclaration>) should not oeverwrite existing values"""
        a1 = SConsArguments.Declarations._ArgumentDeclaration(('ENV_a1','A1'), ('VAR_a1',), ('--a1', {'dest' : 'OPT_a1'}))
        a2 = SConsArguments.Declarations._ArgumentDeclaration(('ENV_a2','A2'), ('VAR_a2',), ('--a2', {'dest' : 'OPT_a2'}))
        decls = SConsArguments.Declarations._ArgumentDeclarations(a = a1)
        decls.setdefault('a', a2)
        self.assertIs(decls['a'], a1)

    def test_setdefault__4(self):
        """<_ArgumentDeclarations>.setdefault('a', <_ArgumentDeclaration>) should raise RuntimeError on committed object"""
        a = SConsArguments.Declarations._ArgumentDeclaration(('ENV_a1','A1'), ('VAR_a1',), ('--a1', {'dest' : 'OPT_a1'}))
        decls = SConsArguments.Declarations._ArgumentDeclarations()
        decls.commit()
        with self.assertRaises(RuntimeError) as cm:
            decls.setdefault('a', a)
        self.assertEqual(str(cm.exception), "declarations are already committed, can't be modified")

    def test_update__TypeError_1(self):
        """<_ArgumentDeclarations>.update({'foo' : 'bar'}) should raise TypeError"""
        decls = SConsArguments.Declarations._ArgumentDeclarations()
        with self.assertRaises(TypeError) as cm:
            decls.update({'a' : 'b'})
        self.assertEqual(str(cm.exception), "value must be an instance of _ArgumentDeclaration, %r is not allowed" % 'b')

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_update__1(self):
        """<_ArgumentDeclarations>.update(*args, **kw) invokes __ensure_not_committed(), __validate_values() and __update_supp_dicts()"""
        decls = SConsArguments.Declarations._ArgumentDeclarations()
        decls._ArgumentDeclarations__ensure_not_committed = mock.Mock(name = '__ensure_not_commited')
        decls._ArgumentDeclarations__update_supp_dicts = mock.Mock(name = '__update_supp_dicts')
        with mock.patch.object(SConsArguments.Declarations._ArgumentDeclarations, '_ArgumentDeclarations__validate_values') as __validate_values:
            decls.update({'foo' : 'bar'}, geez = 123)
        try:
            __validate_values.assert_called_once_with({'foo' : 'bar'}, geez = 123)
            decls._ArgumentDeclarations__ensure_not_committed.assert_called_once_with()
            decls._ArgumentDeclarations__update_supp_dicts.assert_called_once_with()
        except AssertionError as e:
            self.fail(str(e))
        self.assertEqual(decls['foo'], 'bar')
        self.assertEqual(decls['geez'], 123)

    def test_update__2(self):
        """<_ArgumentDeclarations>.update() should perform dict update appropriately"""
        a = SConsArguments.Declarations._ArgumentDeclaration()
        b1 = SConsArguments.Declarations._ArgumentDeclaration()
        b2 = SConsArguments.Declarations._ArgumentDeclaration()
        c = SConsArguments.Declarations._ArgumentDeclaration()
        decls = SConsArguments.Declarations._ArgumentDeclarations(a = a, b = b1)
        decls.update({'b' : b2, 'c' : c})
        self.assertIs(decls['a'], a)
        self.assertIs(decls['b'], b2)
        self.assertIs(decls['c'], c)

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_clear__1(self):
        """<_ArgumentDeclarations>.clear() should invoke __ensure_not_committed() and __update_supp_dicts()"""
        a = SConsArguments.Declarations._ArgumentDeclaration()
        b = SConsArguments.Declarations._ArgumentDeclaration()
        decls = SConsArguments.Declarations._ArgumentDeclarations(a = a, b = b)
        decls._ArgumentDeclarations__ensure_not_committed = mock.Mock(name = '__ensure_not_committed')
        decls._ArgumentDeclarations__update_supp_dicts = mock.Mock(name = '__update_supp_dicts')
        decls.clear()
        try:
            decls._ArgumentDeclarations__ensure_not_committed.assert_called_once_with()
            decls._ArgumentDeclarations__update_supp_dicts.assert_called_once_with()
        except AssertionError as e:
            self.fail(str(e))
        # BTW, it should also clear the dictionary, so...
        self.assertFalse(decls) # is empty


    def test_clear__2(self):
        """<_ArgumentDeclarations>.clear() should clear the dict"""
        a = SConsArguments.Declarations._ArgumentDeclaration()
        b = SConsArguments.Declarations._ArgumentDeclaration()
        decls = SConsArguments.Declarations._ArgumentDeclarations(a = a, b = b)
        decls.clear()
        self.assertFalse(decls) # is empty

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_pop__1(self):
        """<_ArgumentDeclarations>.pop('a') should invoke __ensure_not_committed() and __del_from_supp_dicts()"""
        a = SConsArguments.Declarations._ArgumentDeclaration()
        b = SConsArguments.Declarations._ArgumentDeclaration()
        decls = SConsArguments.Declarations._ArgumentDeclarations(a = a, b = b)
        decls._ArgumentDeclarations__ensure_not_committed = mock.Mock(name = '__ensure_not_committed')
        decls._ArgumentDeclarations__del_from_supp_dicts = mock.Mock(name = '__del_from_supp_dicts')
        ret = decls.pop('a')
        try:
            decls._ArgumentDeclarations__ensure_not_committed.assert_called_once_with()
            decls._ArgumentDeclarations__del_from_supp_dicts.assert_called_once_with('a')
        except AssertionError as e:
            self.fail(str(e))
        # BTW, it should return the value
        self.assertIs(ret, a)

    def test_pop__2(self):
        """<_ArgumentDeclarations>.pop('a') should pop key 'a' from dict and return it's value"""
        a = SConsArguments.Declarations._ArgumentDeclaration()
        b = SConsArguments.Declarations._ArgumentDeclaration()
        decls = SConsArguments.Declarations._ArgumentDeclarations(a = a, b = b)
        ret = decls.pop('a')
        self.assertIs(ret, a)
        self.assertEqual(decls, {'b': b})

    def test_pop__3(self):
        """<_ArgumentDeclarations>.pop('inexistent', 'default') should return 'default'"""
        a = SConsArguments.Declarations._ArgumentDeclaration()
        b = SConsArguments.Declarations._ArgumentDeclaration()
        decls = SConsArguments.Declarations._ArgumentDeclarations(a = a, b = b)
        ret = decls.pop('inexistent', 'default')
        self.assertIs(ret, 'default')
        # The operation should not touch anything
        self.assertEqual(decls, {'a' : a, 'b': b})

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_popitem__1(self):
        """<_ArgumentDeclarations>.popitem() should invoke __ensure_not_committed() and __del_from_supp_dicts()"""
        a = SConsArguments.Declarations._ArgumentDeclaration()
        b = SConsArguments.Declarations._ArgumentDeclaration()
        decls = SConsArguments.Declarations._ArgumentDeclarations(a = a, b = b)
        decls._ArgumentDeclarations__ensure_not_committed = mock.Mock(name = '__ensure_not_committed')
        decls._ArgumentDeclarations__del_from_supp_dicts = mock.Mock(name = '__del_from_supp_dicts')
        ret = decls.popitem()
        try:
            decls._ArgumentDeclarations__ensure_not_committed.assert_called_once_with()
            decls._ArgumentDeclarations__del_from_supp_dicts.assert_called_once_with(ret[0])
        except AssertionError as e:
            self.fail(str(e))
        # BTW, it should return the value
        self.assertTrue(ret == ('a', a) or ret == ('b', b))

    def test_popitem__2(self):
        """<_ArgumentDeclarations>.popitem() should remove item from dict and return it"""
        a = SConsArguments.Declarations._ArgumentDeclaration()
        b = SConsArguments.Declarations._ArgumentDeclaration()
        decls = SConsArguments.Declarations._ArgumentDeclarations(a = a, b = b)
        ret = decls.popitem()
        self.assertTrue(ret == ('a', a) or ret == ('b', b))
        if ret == ('a', a):
            self.assertEqual(decls, {'b' : b})
        else:
            self.assertEqual(decls, {'a' : a})

    def test_copy(self):
        """<_ArgumentDeclarations>.copy() should return a copy of the dict"""
        a = SConsArguments.Declarations._ArgumentDeclaration()
        b = SConsArguments.Declarations._ArgumentDeclaration()
        decls = SConsArguments.Declarations._ArgumentDeclarations(a = a, b = b)
        dcopy = decls.copy()
        self.assertEqual(decls, dcopy) # equal objects,
        self.assertIsNot(decls, dcopy) # but not same object...
        self.assertIs(type(dcopy), SConsArguments.Declarations._ArgumentDeclarations)

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test___setitem___1(self):
        """<_ArgumentDeclarations>.__setitem__() should invoke __ensure_not_committed(), __validate_value() and __append_decl_to_supp_dicts()"""
        a = SConsArguments.Declarations._ArgumentDeclaration()
        b1 = SConsArguments.Declarations._ArgumentDeclaration()
        b2 = SConsArguments.Declarations._ArgumentDeclaration()
        decls = SConsArguments.Declarations._ArgumentDeclarations(a = a, b = b1)
        decls._ArgumentDeclarations__ensure_not_committed = mock.Mock(name = '__ensure_not_committed')
        decls._ArgumentDeclarations__append_decl_to_supp_dicts = mock.Mock(name = '__append_decl_to_supp_dicts')
        with mock.patch.object(SConsArguments.Declarations._ArgumentDeclarations, '_ArgumentDeclarations__validate_value') as __validate_value:
            decls.__setitem__('b',b2)
        try:
            decls._ArgumentDeclarations__ensure_not_committed.assert_called_once_with()
            __validate_value.assert_called_once_with(b2)
            decls._ArgumentDeclarations__append_decl_to_supp_dicts.assert_called_once_with('b', b2)
        except AssertionError as e:
            self.fail(str(e))
        self.assertEqual(decls, {'a' : a, 'b' : b2 })

    def test___setitem___2(self):
        """<_ArgumentDeclarations>.__setitem__() should invoke __ensure_not_committed(), __validate_value() and __append_decl_to_supp_dicts()"""
        a = SConsArguments.Declarations._ArgumentDeclaration()
        b1 = SConsArguments.Declarations._ArgumentDeclaration()
        b2 = SConsArguments.Declarations._ArgumentDeclaration()
        decls = SConsArguments.Declarations._ArgumentDeclarations(a = a, b = b1)
        decls.__setitem__('b',b2)
        self.assertEqual(decls, {'a' : a, 'b' : b2 })

    def test___setitem___3(self):
        """<_ArgumentDeclarations>.__setitem__() should replace existing entry"""
        a = SConsArguments.Declarations._ArgumentDeclaration()
        b1 = SConsArguments.Declarations._ArgumentDeclaration()
        b2 = SConsArguments.Declarations._ArgumentDeclaration()
        decls = SConsArguments.Declarations._ArgumentDeclarations(a = a, b = b1)
        decls['b'] = b2
        self.assertEqual(decls, {'a' : a, 'b' : b2 })

    def test___setitem___4(self):
        """<_ArgumentDeclarations>.__setitem__() should add non-existing entry"""
        a = SConsArguments.Declarations._ArgumentDeclaration()
        b = SConsArguments.Declarations._ArgumentDeclaration()
        decls = SConsArguments.Declarations._ArgumentDeclarations(a = a)
        decls['b'] = b
        self.assertEqual(decls, {'a' : a, 'b' : b })

    def test___setitem___5(self):
        """<_ArgumentDeclarations>.__setitem__() should work on empty dict"""
        b = SConsArguments.Declarations._ArgumentDeclaration()
        decls = SConsArguments.Declarations._ArgumentDeclarations()
        decls['b'] = b
        self.assertEqual(decls, { 'b' : b })

    def test___setitem___6(self):
        """<_ArgumentDeclarations>.__setitem__() should work on an entry with default value set"""
        b1 = SConsArguments.Declarations._ArgumentDeclaration()
        b2 = SConsArguments.Declarations._ArgumentDeclaration()
        decls = SConsArguments.Declarations._ArgumentDeclarations()
        decls.setdefault('b', b1)
        decls['b'] = b2
        self.assertEqual(decls, { 'b' : b2 })

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test___delitem___1(self):
        """<_ArgumentDeclarations>.__delitem__() should invoke __ensure_not_committed(), and __del_from_supp_dicts()"""
        a = SConsArguments.Declarations._ArgumentDeclaration()
        b = SConsArguments.Declarations._ArgumentDeclaration()
        decls = SConsArguments.Declarations._ArgumentDeclarations(a = a, b = b)
        decls._ArgumentDeclarations__ensure_not_committed = mock.Mock(name = '__ensure_not_committed')
        decls._ArgumentDeclarations__del_from_supp_dicts = mock.Mock(name = '__del_from_supp_dicts')
        decls.__delitem__('b')
        try:
            decls._ArgumentDeclarations__ensure_not_committed.assert_called_once_with()
            decls._ArgumentDeclarations__del_from_supp_dicts.assert_called_once_with('b')
        except AssertionError as e:
            self.fail(str(e))
        self.assertEqual(decls, {'a' : a })

    def test___delitem___2(self):
        """<_ArgumentDeclarations>.__delitem__() should delete requested key"""
        a = SConsArguments.Declarations._ArgumentDeclaration()
        b = SConsArguments.Declarations._ArgumentDeclaration()
        decls = SConsArguments.Declarations._ArgumentDeclarations(a = a, b = b)
        decls.__delitem__('b')
        self.assertEqual(decls, {'a' : a })

    def test___delitem___KeyError_1(self):
        """<_ArgumentDeclarations>.__delitem__('inexistent') should raise KeyError"""
        a = SConsArguments.Declarations._ArgumentDeclaration()
        b = SConsArguments.Declarations._ArgumentDeclaration()
        decls = SConsArguments.Declarations._ArgumentDeclarations(a = a, b = b)
        with self.assertRaises(KeyError):
            decls.__delitem__('inexistent')
        self.assertEqual(decls, {'a' : a, 'b' : b })

    def test_get_rename_dict__ENV_1(self):
        """_ArgumentDeclarations().get_rename_dict(ENV) should return empty dict"""
        self.assertEqual(SConsArguments.Declarations._ArgumentDeclarations().get_rename_dict(SConsArguments.ENV), dict())

    def test_get_rename_dict__ENV_2(self):
        """Test <_ArgumentDeclarations>.get_rename_dict(ENV) with trivial name mapping"""
        a = SConsArguments.Declarations._ArgumentDeclaration(('a','A'))
        b = SConsArguments.Declarations._ArgumentDeclaration(('b','B'))
        decls = SConsArguments.Declarations._ArgumentDeclarations(a = a, b = b)
        self.assertEqual(decls.get_rename_dict(SConsArguments.ENV), {'a' : 'a', 'b' : 'b'})

    def test_get_rename_dict__ENV_3(self):
        """Test <_ArgumentDeclarations>.get_rename_dict(ENV) with non-trivial name mappint"""
        a = SConsArguments.Declarations._ArgumentDeclaration(('ENV_a','A'))
        b = SConsArguments.Declarations._ArgumentDeclaration(('ENV_b','B'))
        decls = SConsArguments.Declarations._ArgumentDeclarations(a = a, b = b)
        self.assertEqual(decls.get_rename_dict(SConsArguments.ENV), {'a' : 'ENV_a', 'b' : 'ENV_b'})

    def test_get_irename_dict__ENV_1(self):
        """_ArgumentDeclarations().get_irename_dict(ENV) should return empty dict"""
        self.assertEqual(SConsArguments.Declarations._ArgumentDeclarations().get_irename_dict(SConsArguments.ENV), dict())

    def test_get_irename_dict__ENV_2(self):
        """Test <_ArgumentDeclarations>.get_irename_dict(ENV) with trivial name mapping"""
        a = SConsArguments.Declarations._ArgumentDeclaration(('a','A'))
        b = SConsArguments.Declarations._ArgumentDeclaration(('b','B'))
        decls = SConsArguments.Declarations._ArgumentDeclarations(a = a, b = b)
        self.assertEqual(decls.get_irename_dict(SConsArguments.ENV), {'a' : 'a', 'b' : 'b'})

    def test_get_irename_dict__ENV_3(self):
        """Test <_ArgumentDeclarations>.get_irename_dict(ENV) with non-trivial name mappint"""
        a = SConsArguments.Declarations._ArgumentDeclaration(('ENV_a','A'))
        b = SConsArguments.Declarations._ArgumentDeclaration(('ENV_b','B'))
        decls = SConsArguments.Declarations._ArgumentDeclarations(a = a, b = b)
        self.assertEqual(decls.get_irename_dict(SConsArguments.ENV), {'ENV_a' : 'a', 'ENV_b' : 'b'})

    def test_get_rename_dict__VAR_1(self):
        """_ArgumentDeclarations().get_rename_dict(VAR) should return empty dict"""
        self.assertEqual(SConsArguments.Declarations._ArgumentDeclarations().get_rename_dict(SConsArguments.VAR), dict())

    def test_get_rename_dict__VAR_2(self):
        """Test <_ArgumentDeclarations>.get_rename_dict(VAR) with trivial name mapping"""
        a = SConsArguments.Declarations._ArgumentDeclaration(None, ('a',))
        b = SConsArguments.Declarations._ArgumentDeclaration(None, ('b',))
        decls = SConsArguments.Declarations._ArgumentDeclarations(a = a, b = b)
        self.assertEqual(decls.get_rename_dict(SConsArguments.VAR), {'a' : 'a', 'b' : 'b'})

    def test_get_rename_dict__VAR_3(self):
        """Test <_ArgumentDeclarations>.get_rename_dict(VAR) with non-trivial name mappint"""
        a = SConsArguments.Declarations._ArgumentDeclaration(None, ('VAR_a',))
        b = SConsArguments.Declarations._ArgumentDeclaration(None, ('VAR_b',))
        decls = SConsArguments.Declarations._ArgumentDeclarations(a = a, b = b)
        self.assertEqual(decls.get_rename_dict(SConsArguments.VAR), {'a' : 'VAR_a', 'b' : 'VAR_b'})

    def test_get_irename_dict__VAR_1(self):
        """_ArgumentDeclarations().get_irename_dict(VAR) should return empty dict"""
        self.assertEqual(SConsArguments.Declarations._ArgumentDeclarations().get_irename_dict(SConsArguments.VAR), dict())

    def test_get_irename_dict__VAR_2(self):
        """Test <_ArgumentDeclarations>.get_irename_dict(VAR) with trivial name mapping"""
        a = SConsArguments.Declarations._ArgumentDeclaration(None, ('a',))
        b = SConsArguments.Declarations._ArgumentDeclaration(None, ('b',))
        decls = SConsArguments.Declarations._ArgumentDeclarations(a = a, b = b)
        self.assertEqual(decls.get_irename_dict(SConsArguments.VAR), {'a' : 'a', 'b' : 'b'})

    def test_get_irename_dict__VAR_3(self):
        """Test <_ArgumentDeclarations>.get_irename_dict(VAR) with non-trivial name mappint"""
        a = SConsArguments.Declarations._ArgumentDeclaration(None, ('VAR_a',))
        b = SConsArguments.Declarations._ArgumentDeclaration(None, ('VAR_b',))
        decls = SConsArguments.Declarations._ArgumentDeclarations(a = a, b = b)
        self.assertEqual(decls.get_irename_dict(SConsArguments.VAR), {'VAR_a' : 'a', 'VAR_b' : 'b'})

    def test_get_rename_dict__OPT_1(self):
        """_ArgumentDeclarations().get_rename_dict(OPT) should return empty dict"""
        self.assertEqual(SConsArguments.Declarations._ArgumentDeclarations().get_rename_dict(SConsArguments.OPT), dict())

    def test_get_rename_dict__OPT_2(self):
        """Test <_ArgumentDeclarations>.get_rename_dict(OPT) with trivial name mapping"""
        a = SConsArguments.Declarations._ArgumentDeclaration(None, None, ('--a', {'dest' : 'a'}))
        b = SConsArguments.Declarations._ArgumentDeclaration(None, None, ('--b', {'dest' : 'b'}))
        decls = SConsArguments.Declarations._ArgumentDeclarations(a = a, b = b)
        self.assertEqual(decls.get_rename_dict(SConsArguments.OPT), {'a' : 'a', 'b' : 'b'})

    def test_get_rename_dict__OPT_3(self):
        """Test <_ArgumentDeclarations>.get_rename_dict(OPT) with non-trivial name mappint"""
        a = SConsArguments.Declarations._ArgumentDeclaration(None, None, ('--a', {'dest' : 'OPT_a'}))
        b = SConsArguments.Declarations._ArgumentDeclaration(None, None, ('--b', {'dest' : 'OPT_b'}))
        decls = SConsArguments.Declarations._ArgumentDeclarations(a = a, b = b)
        self.assertEqual(decls.get_rename_dict(SConsArguments.OPT), {'a' : 'OPT_a', 'b' : 'OPT_b'})

    def test_get_irename_dict__OPT_1(self):
        """_ArgumentDeclarations().get_irename_dict(OPT) should return empty dict"""
        self.assertEqual(SConsArguments.Declarations._ArgumentDeclarations().get_irename_dict(SConsArguments.OPT), dict())

    def test_get_irename_dict__OPT_2(self):
        """Test <_ArgumentDeclarations>.get_irename_dict(OPT) with trivial name mapping"""
        a = SConsArguments.Declarations._ArgumentDeclaration(None, None, ('--a', {'dest' : 'a'}))
        b = SConsArguments.Declarations._ArgumentDeclaration(None, None, ('--b', {'dest' : 'b'}))
        decls = SConsArguments.Declarations._ArgumentDeclarations(a = a, b = b)
        self.assertEqual(decls.get_irename_dict(SConsArguments.OPT), {'a' : 'a', 'b' : 'b'})

    def test_get_irename_dict__OPT_3(self):
        """Test <_ArgumentDeclarations>.get_irename_dict(OPT) with non-trivial name mappint"""
        a = SConsArguments.Declarations._ArgumentDeclaration(None, None, ('--a', {'dest' : 'OPT_a'}))
        b = SConsArguments.Declarations._ArgumentDeclaration(None, None, ('--b', {'dest' : 'OPT_b'}))
        decls = SConsArguments.Declarations._ArgumentDeclarations(a = a, b = b)
        self.assertEqual(decls.get_irename_dict(SConsArguments.OPT), {'OPT_a' : 'a', 'OPT_b' : 'b'})

    def test_get_resubst_dict__ENV_1(self):
        """_ArgumentDeclarations().get_resubst_dict(ENV) should return empty dict"""
        decls = SConsArguments.Declarations._ArgumentDeclarations()
        decls.commit()
        self.assertEqual(decls.get_resubst_dict(SConsArguments.ENV), dict())

    def test_get_resubst_dict__ENV_2(self):
        """Test <_ArgumentDeclarations>.get_resubst_dict(ENV) with trivial name mapping"""
        a = SConsArguments.Declarations._ArgumentDeclaration(('a','A'))
        b = SConsArguments.Declarations._ArgumentDeclaration(('b','B'))
        decls = SConsArguments.Declarations._ArgumentDeclarations(a = a, b = b)
        decls.commit()
        self.assertEqual(decls.get_resubst_dict(SConsArguments.ENV), dict())

    def test_get_resubst_dict__ENV_3(self):
        """Test <_ArgumentDeclarations>.get_resubst_dict(ENV) with non-trivial name mappint"""
        a = SConsArguments.Declarations._ArgumentDeclaration(('ENV_a','A'))
        b = SConsArguments.Declarations._ArgumentDeclaration(('ENV_b','B'))
        decls = SConsArguments.Declarations._ArgumentDeclarations(a = a, b = b)
        decls.commit()
        self.assertEqual(decls.get_resubst_dict(SConsArguments.ENV), {'a' : '${ENV_a}', 'b' : '${ENV_b}'})

    def test_get_iresubst_dict__ENV_1(self):
        """_ArgumentDeclarations().get_iresubst_dict(ENV) should return empty dict"""
        decls = SConsArguments.Declarations._ArgumentDeclarations()
        decls.commit()
        self.assertEqual(decls.get_iresubst_dict(SConsArguments.ENV), dict())

    def test_get_iresubst_dict__ENV_2(self):
        """Test <_ArgumentDeclarations>.get_iresubst_dict(ENV) with trivial name mapping"""
        a = SConsArguments.Declarations._ArgumentDeclaration(('a','A'))
        b = SConsArguments.Declarations._ArgumentDeclaration(('b','B'))
        decls = SConsArguments.Declarations._ArgumentDeclarations(a = a, b = b)
        decls.commit()
        self.assertEqual(decls.get_iresubst_dict(SConsArguments.ENV), dict())

    def test_get_iresubst_dict__ENV_3(self):
        """Test <_ArgumentDeclarations>.get_iresubst_dict(ENV) with non-trivial name mappint"""
        a = SConsArguments.Declarations._ArgumentDeclaration(('ENV_a','A'))
        b = SConsArguments.Declarations._ArgumentDeclaration(('ENV_b','B'))
        decls = SConsArguments.Declarations._ArgumentDeclarations(a = a, b = b)
        decls.commit()
        self.assertEqual(decls.get_iresubst_dict(SConsArguments.ENV), {'ENV_a' : '${a}', 'ENV_b' : '${b}'})

    def test_get_resubst_dict__VAR_1(self):
        """_ArgumentDeclarations().get_resubst_dict(VAR) should return empty dict"""
        decls = SConsArguments.Declarations._ArgumentDeclarations()
        decls.commit()
        self.assertEqual(decls.get_resubst_dict(SConsArguments.VAR), dict())

    def test_get_resubst_dict__VAR_2(self):
        """Test <_ArgumentDeclarations>.get_resubst_dict(VAR) with trivial name mapping"""
        a = SConsArguments.Declarations._ArgumentDeclaration(None, ('a',))
        b = SConsArguments.Declarations._ArgumentDeclaration(None, ('b',))
        decls = SConsArguments.Declarations._ArgumentDeclarations(a = a, b = b)
        decls.commit()
        self.assertEqual(decls.get_resubst_dict(SConsArguments.VAR), {})

    def test_get_resubst_dict__VAR_3(self):
        """Test <_ArgumentDeclarations>.get_resubst_dict(VAR) with non-trivial name mappint"""
        a = SConsArguments.Declarations._ArgumentDeclaration(None, ('VAR_a',))
        b = SConsArguments.Declarations._ArgumentDeclaration(None, ('VAR_b',))
        decls = SConsArguments.Declarations._ArgumentDeclarations(a = a, b = b)
        decls.commit()
        self.assertEqual(decls.get_resubst_dict(SConsArguments.VAR), {'a' : '${VAR_a}', 'b' : '${VAR_b}'})

    def test_get_iresubst_dict__VAR_1(self):
        """_ArgumentDeclarations().get_iresubst_dict(VAR) should return empty dict"""
        decls = SConsArguments.Declarations._ArgumentDeclarations()
        decls.commit()
        self.assertEqual(decls.get_iresubst_dict(SConsArguments.VAR), dict())

    def test_get_iresubst_dict__VAR_2(self):
        """Test <_ArgumentDeclarations>.get_iresubst_dict(VAR) with trivial name mapping"""
        a = SConsArguments.Declarations._ArgumentDeclaration(None, ('a',))
        b = SConsArguments.Declarations._ArgumentDeclaration(None, ('b',))
        decls = SConsArguments.Declarations._ArgumentDeclarations(a = a, b = b)
        decls.commit()
        self.assertEqual(decls.get_iresubst_dict(SConsArguments.VAR), {})

    def test_get_iresubst_dict__VAR_3(self):
        """Test <_ArgumentDeclarations>.get_iresubst_dict(VAR) with non-trivial name mappint"""
        a = SConsArguments.Declarations._ArgumentDeclaration(None, ('VAR_a',))
        b = SConsArguments.Declarations._ArgumentDeclaration(None, ('VAR_b',))
        decls = SConsArguments.Declarations._ArgumentDeclarations(a = a, b = b)
        decls.commit()
        self.assertEqual(decls.get_iresubst_dict(SConsArguments.VAR), {'VAR_a' : '${a}', 'VAR_b' : '${b}'})

    def test_get_resubst_dict__OPT_1(self):
        """_ArgumentDeclarations().get_resubst_dict(OPT) should return empty dict"""
        decls = SConsArguments.Declarations._ArgumentDeclarations()
        decls.commit()
        self.assertEqual(decls.get_resubst_dict(SConsArguments.OPT), dict())

    def test_get_resubst_dict__OPT_2(self):
        """Test <_ArgumentDeclarations>.get_resubst_dict(OPT) with trivial name mapping"""
        a = SConsArguments.Declarations._ArgumentDeclaration(None, None, ('--a', {'dest' : 'a'}))
        b = SConsArguments.Declarations._ArgumentDeclaration(None, None, ('--b', {'dest' : 'b'}))
        decls = SConsArguments.Declarations._ArgumentDeclarations(a = a, b = b)
        decls.commit()
        self.assertEqual(decls.get_resubst_dict(SConsArguments.OPT), {})

    def test_get_resubst_dict__OPT_3(self):
        """Test <_ArgumentDeclarations>.get_resubst_dict(OPT) with non-trivial name mappint"""
        a = SConsArguments.Declarations._ArgumentDeclaration(None, None, ('--a', {'dest' : 'OPT_a'}))
        b = SConsArguments.Declarations._ArgumentDeclaration(None, None, ('--b', {'dest' : 'OPT_b'}))
        decls = SConsArguments.Declarations._ArgumentDeclarations(a = a, b = b)
        decls.commit()
        self.assertEqual(decls.get_resubst_dict(SConsArguments.OPT), {'a' : '${OPT_a}', 'b' : '${OPT_b}'})

    def test_get_iresubst_dict__OPT_1(self):
        """_ArgumentDeclarations().get_iresubst_dict(OPT) should return empty dict"""
        decls = SConsArguments.Declarations._ArgumentDeclarations()
        decls.commit()
        self.assertEqual(decls.get_iresubst_dict(SConsArguments.OPT), dict())

    def test_get_iresubst_dict__OPT_2(self):
        """Test <_ArgumentDeclarations>.get_iresubst_dict(OPT) with trivial name mapping"""
        a = SConsArguments.Declarations._ArgumentDeclaration(None, None, ('--a', {'dest' : 'a'}))
        b = SConsArguments.Declarations._ArgumentDeclaration(None, None, ('--b', {'dest' : 'b'}))
        decls = SConsArguments.Declarations._ArgumentDeclarations(a = a, b = b)
        decls.commit()
        self.assertEqual(decls.get_iresubst_dict(SConsArguments.OPT), {})

    def test_get_iresubst_dict__OPT_3(self):
        """Test <_ArgumentDeclarations>.get_iresubst_dict(OPT) with non-trivial name mappint"""
        a = SConsArguments.Declarations._ArgumentDeclaration(None, None, ('--a', {'dest' : 'OPT_a'}))
        b = SConsArguments.Declarations._ArgumentDeclaration(None, None, ('--b', {'dest' : 'OPT_b'}))
        decls = SConsArguments.Declarations._ArgumentDeclarations(a = a, b = b)
        decls.commit()
        self.assertEqual(decls.get_iresubst_dict(SConsArguments.OPT), {'OPT_a' : '${a}', 'OPT_b' : '${b}'})

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_get_key_1(self):
        """<_ArgumentDeclarations>.get_key('ns','a') should return self[key].get_key(ENV)"""
        class _test_key: pass
        a = SConsArguments.Declarations._ArgumentDeclaration()
        a.get_key = mock.Mock(name = 'get_key', return_value = _test_key)
        decls = SConsArguments.Declarations._ArgumentDeclarations(a = a)
        key = decls.get_key('ns','a')
        self.assertIs(key, _test_key)
        try:
            a.get_key.assert_called_once_with('ns')
        except AssertionError as e:
            self.fail(str(e))

    def test_get_key_ENV_1(self):
        """<_ArgumentDeclarations>.get_key(ENV,'a') returns appropriate key"""
        a = SConsArguments.Declarations._ArgumentDeclaration(('ENV_a','A'))
        b = SConsArguments.Declarations._ArgumentDeclaration(('ENV_b','B'))
        decls = SConsArguments.Declarations._ArgumentDeclarations(a = a, b = b)
        self.assertEqual(decls.get_key(SConsArguments.ENV, 'a'), 'ENV_a')
        self.assertEqual(decls.get_key(SConsArguments.ENV, 'b'), 'ENV_b')

    def test_get_key_VAR_1(self):
        """<_ArgumentDeclarations>.get_key(VAR,'a') returns appropriate key"""
        a = SConsArguments.Declarations._ArgumentDeclaration(None, ('VAR_a',))
        b = SConsArguments.Declarations._ArgumentDeclaration(None, ('VAR_b',))
        decls = SConsArguments.Declarations._ArgumentDeclarations(a = a, b = b)
        self.assertEqual(decls.get_key(SConsArguments.VAR, 'a'), 'VAR_a')
        self.assertEqual(decls.get_key(SConsArguments.VAR, 'b'), 'VAR_b')

    def test_get_key_OPT_1(self):
        """<_ArgumentDeclarations>.get_key(OPT,'a') returns appropriate key"""
        a = SConsArguments.Declarations._ArgumentDeclaration(None, None, ('--a', {'dest' : 'OPT_a'}))
        b = SConsArguments.Declarations._ArgumentDeclaration(None, None, ('--b', {'dest' : 'OPT_b'}))
        decls = SConsArguments.Declarations._ArgumentDeclarations(a = a, b = b)
        self.assertEqual(decls.get_key(SConsArguments.OPT, 'a'), 'OPT_a')
        self.assertEqual(decls.get_key(SConsArguments.OPT, 'b'), 'OPT_b')

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_set_key_1(self):
        """<_ArgumentDeclarations>.set_key('ns', 'a', 'ns_a') should invoke __ensure_not_committed(), self['a'].set_key('ns', 'ns_a') and __replace_key_in_supp_dicts('ns', 'a', 'ns_a')"""
        a = SConsArguments.Declarations._ArgumentDeclaration()
        decls = SConsArguments.Declarations._ArgumentDeclarations(a = a)
        decls._ArgumentDeclarations__ensure_not_committed = mock.Mock(name = '__ensure_not_committed')
        decls['a'].set_key = mock.Mock(name = 'set_key')
        decls._ArgumentDeclarations__replace_key_in_supp_dicts = mock.Mock(name = '__replace_key_in_supp_dicts')
        decls.set_key('ns', 'a', 'ns_a')
        try:
            decls._ArgumentDeclarations__ensure_not_committed.assert_called_once_with()
            a.set_key.ensure_called_once_with('ns', 'ns_a')
            decls._ArgumentDeclarations__replace_key_in_supp_dicts.assert_called_once_with('ns', 'a', 'ns_a')
        except AssertionError as e:
            self.fail(str(e))

    def test_set_key_ENV_1(self):
        """<_ArgumentDeclarations>.set_key(ENV, 'a', 'ENV_a') should replace the old key and update supplementary dicts"""
        a = SConsArguments.Declarations._ArgumentDeclaration({'a' : 'A'})
        decls = SConsArguments.Declarations._ArgumentDeclarations(a = a)
        decls.set_key(SConsArguments.ENV, 'a', 'ENV_a')
        self.assertEqual(a.get_key(SConsArguments.ENV), 'ENV_a')
        self.assertEqual(decls.get_rename_dict(SConsArguments.ENV), {'a' : 'ENV_a'})
        self.assertEqual(decls.get_irename_dict(SConsArguments.ENV), {'ENV_a' : 'a'})

    def test_set_key_VAR_1(self):
        """<_ArgumentDeclarations>.set_key(VAR, 'a', 'VAR_a') should replace the old key and update supplementary dicts"""
        a = SConsArguments.Declarations._ArgumentDeclaration(None, ('a',))
        decls = SConsArguments.Declarations._ArgumentDeclarations(a = a)
        decls.set_key(SConsArguments.VAR, 'a', 'VAR_a')
        self.assertEqual(a.get_key(SConsArguments.VAR), 'VAR_a')
        self.assertEqual(decls.get_rename_dict(SConsArguments.VAR), {'a' : 'VAR_a'})
        self.assertEqual(decls.get_irename_dict(SConsArguments.VAR), {'VAR_a' : 'a'})

    def test_set_key_OPT_1(self):
        """<_ArgumentDeclarations>.set_key(OPT, 'a', 'OPT_a') should replace the old key and update supplementary dicts"""
        a = SConsArguments.Declarations._ArgumentDeclaration(None, None, ('--a', {'dest' : 'a'}))
        decls = SConsArguments.Declarations._ArgumentDeclarations(a = a)
        decls.set_key(SConsArguments.OPT, 'a', 'OPT_a')
        self.assertEqual(a.get_key(SConsArguments.OPT), 'OPT_a')
        self.assertEqual(decls.get_rename_dict(SConsArguments.OPT), {'a' : 'OPT_a'})
        self.assertEqual(decls.get_irename_dict(SConsArguments.OPT), {'OPT_a' : 'a'})

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test__add_to_1(self):
        """<_ArgumentDeclarations>._add_to(ns,*args) should invoke v.add_to(ns,*args) for each (k,v) in <_ArgumentDeclarations>.iteritems()"""
        a = SConsArguments.Declarations._ArgumentDeclaration()
        b = SConsArguments.Declarations._ArgumentDeclaration()
        a.add_to = mock.Mock(name = 'a.add_to')
        b.add_to = mock.Mock(name = 'b.add_to')
        decls = SConsArguments.Declarations._ArgumentDeclarations(a = a, b = b)
        decls._add_to('ns', 'arg1', 'arg2')
        try:
            a.add_to.assert_called_once_with('ns','arg1','arg2')
            b.add_to.assert_called_once_with('ns','arg1','arg2')
        except AssertionError as e:
            self.fail(str(e))

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test__safe_add_to_1(self):
        """<_ArgumentDeclarations>._add_to(ns,*args) should invoke v.add_to(ns,*args) for each (k,v) in <_ArgumentDeclarations>.iteritems()"""
        a = SConsArguments.Declarations._ArgumentDeclaration()
        b = SConsArguments.Declarations._ArgumentDeclaration()
        a.safe_add_to = mock.Mock(name = 'a.add_to')
        b.safe_add_to = mock.Mock(name = 'b.add_to')
        decls = SConsArguments.Declarations._ArgumentDeclarations(a = a, b = b)
        decls._safe_add_to('ns', 'arg1', 'arg2')
        try:
            a.safe_add_to.assert_called_once_with('ns','arg1','arg2')
            b.safe_add_to.assert_called_once_with('ns','arg1','arg2')
        except AssertionError as e:
            self.fail(str(e))

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_commit_1(self):
        """<_ArgumentDeclarations>.commit(*args) should do nothing on already committed object"""
        decls = SConsArguments.Declarations._ArgumentDeclarations()
        decls._build_resubst_dicts = mock.Mock(name = '_build_resubst_dict')
        decls._build_iresubst_dicts = mock.Mock(name = '_build_iresubst_dict')
        decls._ArgumentDeclarations__resubst_defaults = mock.Mock(name = '__resubst_defaults')
        decls.add_to = mock.Mock(name = 'add_to')
        decls._ArgumentDeclarations__committed = True # mark it already committed
        decls.commit(10,11,12)
        try:
            decls._build_resubst_dicts.assert_not_called()
            decls._build_iresubst_dicts.assert_not_called()
            decls._ArgumentDeclarations__resubst_defaults.assert_not_called()
            decls.add_to.assert_not_called()
        except AssertionError as e:
            self.fail(str(e))

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_commit_2(self):
        """<_ArgumentDeclarations>.commit(*args) should invoke appropriate methods"""
        decls = SConsArguments.Declarations._ArgumentDeclarations()
        decls._build_resubst_dicts = mock.Mock(name = '_build_resubst_dict')
        decls._build_iresubst_dicts = mock.Mock(name = '_build_iresubst_dict')
        decls._ArgumentDeclarations__resubst_defaults = mock.Mock(name = '__resubst_defaults')
        decls.add_to = mock.Mock(name = 'add_to')
        decls.commit(10,11,12)
        try:
            decls._build_resubst_dicts.assert_called_once_with()
            decls._build_iresubst_dicts.assert_called_once_with()
            decls._ArgumentDeclarations__resubst_defaults.called_once_with()
            decls.add_to.assert_called_once_with(10,11,12)
        except AssertionError as e:
            self.fail(str(e))
        self.assertTrue(decls._ArgumentDeclarations__committed)

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_Commit_1(self):
        """<_ArgumentDeclarations>.Commit('env', 'variables', 'create_options') should invoke <_ArgumentDeclarations>.commit() and return <_Arguments>"""
        decls = SConsArguments.Declarations._ArgumentDeclarations()
        decls.commit = mock.Mock(name = 'commit')
        with mock.patch('SConsArguments.Declarations._Arguments', return_value = '_Arguments') as _Arguments:
            ret = decls.Commit('env', 'variables', 'create_options')
        try:
            decls.commit.assert_called_once_with('env','variables','create_options')
        except AssertionError as e:
            self.fail(str(e))
        self.assertIs(ret, '_Arguments')

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_Commit_2(self):
        """<_ArgumentDeclarations>.Commit('env', 'variables', 'create_options', True) should invoke <_ArgumentDeclarations>.commit() and return None"""
        decls = SConsArguments.Declarations._ArgumentDeclarations()
        decls.commit = mock.Mock(name = 'commit')
        with mock.patch('SConsArguments.Declarations._Arguments', return_value = '_Arguments') as _Arguments:
            ret = decls.Commit('env', 'variables', 'create_options', True)
        try:
            decls.commit.assert_called_once_with('env','variables','create_options')
        except AssertionError as e:
            self.fail(str(e))
        self.assertIs(ret, '_Arguments')

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_Commit_3(self):
        """<_ArgumentDeclarations>.Commit('env', 'variables', 'create_options', True, 'arg1', 'arg2') should invoke <_ArgumentDeclarations>.commit() and return None"""
        decls = SConsArguments.Declarations._ArgumentDeclarations()
        decls.commit = mock.Mock(name = 'commit')
        with mock.patch('SConsArguments.Declarations._Arguments', return_value = '_Arguments') as _Arguments:
            ret = decls.Commit('env', 'variables', 'create_options', True, 'arg1', 'arg2')
        try:
            decls.commit.assert_called_once_with('env','variables','create_options', 'arg1', 'arg2')
        except AssertionError as e:
            self.fail(str(e))
        self.assertIs(ret, '_Arguments')

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_Commit_4(self):
        """<_ArgumentDeclarations>.Commit('env', 'variables', 'create_options', False) should invoke <_ArgumentDeclarations>.commit() and return None"""
        decls = SConsArguments.Declarations._ArgumentDeclarations()
        decls.commit = mock.Mock(name = 'commit')
        with mock.patch('SConsArguments.Declarations._Arguments', return_value = '_Arguments') as _Arguments:
            ret = decls.Commit('env', 'variables', 'create_options', False)
        try:
            decls.commit.assert_called_once_with('env','variables','create_options')
        except AssertionError as e:
            self.fail(str(e))
        self.assertIs(ret, None)


    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_Commit_5(self):
        """<_ArgumentDeclarations>.Commit('env', 'variables', 'create_options', False, 'arg1', 'arg2') should invoke <_ArgumentDeclarations>.commit() and return None"""
        decls = SConsArguments.Declarations._ArgumentDeclarations()
        decls.commit = mock.Mock(name = 'commit')
        with mock.patch('SConsArguments.Declarations._Arguments', return_value = '_Arguments') as _Arguments:
            ret = decls.Commit('env', 'variables', 'create_options', False, 'arg1', 'arg2')
        try:
            decls.commit.assert_called_once_with('env','variables','create_options', 'arg1', 'arg2')
        except AssertionError as e:
            self.fail(str(e))
        self.assertIs(ret, None)


    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_add_to_1(self):
        """<_ArgumentDeclarations>.add_to(11,12,13) should invoke <_ArgumentDeclarations>._safe_add_to(ns,...) for ns in [ENV, VAR, OPT]"""
        decls = SConsArguments.Declarations._ArgumentDeclarations()
        decls._safe_add_to = mock.Mock(name = '_safe_add_to')
        with mock.patch.object(SConsArguments.Declarations._ArgumentDeclarations, '_ArgumentDeclarations__ensure_committed', return_value = True) as __ensure_committed:
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
class Test_ArgumentDeclarations(unittest.TestCase):
    def test_user_doc_example_3(self):
        """example 3 from user documentation should work"""
        # create single declarations
        foodecl = SConsArguments.Declarations.ArgumentDeclaration( {'ENV_FOO' : 'default ENV_FOO'},      # ENV
                                                      ('var_foo', 'var_foo help', ),                    # VAR
                                                      ('--foo', {'dest' : "opt_foo"}) )                 # OPT
        bardecl = SConsArguments.Declarations.ArgumentDeclaration( {'ENV_BAR' : None},                   # ENV
                                                      ('var_bar', 'var_bar help', 'default var_bar'),   # VAR
                                                      ('--bar', {'dest':"opt_bar", "type":"string"}))   # OPT
        # put them all together
        decls = SConsArguments.Declarations.ArgumentDeclarations({ 'foo' : foodecl, 'bar' : bardecl })
        self.assertIsInstance(decls, dict)
        self.assertIsInstance(decls, SConsArguments.Declarations._ArgumentDeclarations)
        self.assertIsInstance(decls['foo'], SConsArguments.Declarations._ArgumentDeclaration)
        self.assertIsInstance(decls['bar'], SConsArguments.Declarations._ArgumentDeclaration)

    def test_user_doc_example_4(self):
        """example 4 from user documentation should work"""
        # create multiple declarations at once
        decls = SConsArguments.Declarations.ArgumentDeclarations({
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
        self.assertIsInstance(decls, SConsArguments.Declarations._ArgumentDeclarations)
        self.assertIsInstance(decls['foo'], SConsArguments.Declarations._ArgumentDeclaration)
        self.assertIsInstance(decls['bar'], SConsArguments.Declarations._ArgumentDeclaration)

    def test_user_doc_example_5(self):
        """example 5 from user documentation should work"""
        decls = SConsArguments.Declarations.ArgumentDeclarations([
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
        self.assertIsInstance(decls, SConsArguments.Declarations._ArgumentDeclarations)
        self.assertIsInstance(decls['foo'], SConsArguments.Declarations._ArgumentDeclaration)
        self.assertIsInstance(decls['bar'], SConsArguments.Declarations._ArgumentDeclaration)

    def test_user_doc_example_6(self):
        """example 6 from user documentation should work"""
        decls = SConsArguments.Declarations.ArgumentDeclarations(
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
        self.assertIsInstance(decls, SConsArguments.Declarations._ArgumentDeclarations)
        self.assertIsInstance(decls['foo'], SConsArguments.Declarations._ArgumentDeclaration)
        self.assertIsInstance(decls['bar'], SConsArguments.Declarations._ArgumentDeclaration)

    def test_user_doc_example_7(self):
        """example 7 from user documentation should work"""
        decls = SConsArguments.Declarations.ArgumentDeclarations(
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
        self.assertIsInstance(decls, SConsArguments.Declarations._ArgumentDeclarations)
        self.assertIsInstance(decls['foo'], SConsArguments.Declarations._ArgumentDeclaration)
        self.assertIsInstance(decls['geez'], SConsArguments.Declarations._ArgumentDeclaration)

    # It's not a mistake, example 8 is found in Test_DeclareArguments.
    def test_user_doc_example_9(self):
        """example 9 from user documentation should work"""
        decls = SConsArguments.Declarations.ArgumentDeclarations(
           foo = ( { 'ENV_FOO' : None }, ('VAR_FOO', 'Help for VAR_FOO', '$VAR_BAR'), None),
           bar = ( { 'ENV_BAR' : None }, ('VAR_BAR', 'Help for VAR_BAR', 'BAR'), None),
        )
        self.assertIsInstance(decls, dict)
        self.assertIsInstance(decls, SConsArguments.Declarations._ArgumentDeclarations)
        self.assertIsInstance(decls['foo'], SConsArguments.Declarations._ArgumentDeclaration)
        self.assertIsInstance(decls['bar'], SConsArguments.Declarations._ArgumentDeclaration)

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
        self.assertIsInstance(decls, SConsArguments.Declarations._ArgumentDeclarations)
        self.assertIsInstance(decls['foo'], SConsArguments.Declarations._ArgumentDeclaration)
        self.assertIsInstance(decls['bar'], SConsArguments.Declarations._ArgumentDeclaration)

#############################################################################
if __name__ == "__main__":
    ldr = unittest.TestLoader()
    suite = unittest.TestSuite()
    # Load tests to test suite
    tclasses = [ Test__ArgumentDeclarations
               , Test_ArgumentDeclarations
               , Test_DeclareArguments ]

    for tclass in tclasses:
        suite.addTests(ldr.loadTestsFromTestCase(tclass))

    if not unittest.TextTestRunner(verbosity = 2).run(suite).wasSuccessful():
        sys.exit(1)

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
