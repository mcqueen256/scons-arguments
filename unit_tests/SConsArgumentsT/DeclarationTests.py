""" `SConsArgumentsT.DeclarationTests`

Unit tests for `SConsArguments.Declaration`
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

import SConsArguments.Declaration
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
class Test__ArgumentDeclaration(unittest.TestCase):
    @unittest.skipIf(_mock_missing, "requires mock module")
    def test___init___1(self):
        """_ArgumentDeclaration.__init__() should not call any of _set_XXX_decl()"""
        with mock.patch.object(SConsArguments.Declaration._ArgumentDeclaration, 'set_env_decl') as m_env, \
             mock.patch.object(SConsArguments.Declaration._ArgumentDeclaration, 'set_var_decl') as m_var, \
             mock.patch.object(SConsArguments.Declaration._ArgumentDeclaration, 'set_opt_decl') as m_opt:
            decl = SConsArguments.Declaration._ArgumentDeclaration()
            try:
                m_env.assert_not_called()
                m_var.assert_not_called()
                m_opt.assert_not_called()
            except AssertionError as e:
                self.fail(str(e))

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test___init___2(self):
        """_ArgumentDeclaration.__init__() should set __decl_tab to [None, None, None]"""
        with mock.patch.object(SConsArguments.Declaration._ArgumentDeclaration, '_ArgumentDeclaration__decl_tab', create=True) as m:
            decl = SConsArguments.Declaration._ArgumentDeclaration()
            self.assertEqual(len(decl._ArgumentDeclaration__decl_tab), SConsArguments.ALL)
            self.assertIs(decl._ArgumentDeclaration__decl_tab[SConsArguments.ENV], None)
            self.assertIs(decl._ArgumentDeclaration__decl_tab[SConsArguments.VAR], None)
            self.assertIs(decl._ArgumentDeclaration__decl_tab[SConsArguments.OPT], None)

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test___init___3(self):
        """_ArgumentDeclaration.__init__('a', 'b', 'c') should call of set_env_decl('a'), set_var_decl('b'), set_opt_decl('c')"""
        with mock.patch.object(SConsArguments.Declaration._ArgumentDeclaration, 'set_env_decl', autospec=True) as m_env, \
             mock.patch.object(SConsArguments.Declaration._ArgumentDeclaration, 'set_var_decl', autospec=True) as m_var, \
             mock.patch.object(SConsArguments.Declaration._ArgumentDeclaration, 'set_opt_decl', autospec=True) as m_opt:
            decl = SConsArguments.Declaration._ArgumentDeclaration('a', 'b', 'c')
            try:
                m_env.assert_called_once_with(decl,'a')
                m_var.assert_called_once_with(decl,'b')
                m_opt.assert_called_once_with(decl,'c')
            except AssertionError as e:
                self.fail(str(e))

    def test_set_decl_1(self):
        """<_ArgumentDeclaration>.set_decl(123,'a') should raise IndexError"""
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        with self.assertRaises(IndexError):
            decl.set_decl(123,'a')

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_set_decl__ENV(self):
        """<_ArgumentDeclaration>.set_decl(ENV,'a') should call set_env_decl('a')"""
        decl = SConsArguments.Declaration._ArgumentDeclaration()
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

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_set_decl__VAR(self):
        """<_ArgumentDeclaration>.set_decl(VAR,'b') should call set_var_decl('b')"""
        decl = SConsArguments.Declaration._ArgumentDeclaration()
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

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_set_decl__OPT(self):
        """<_ArgumentDeclaration>.set_decl(OPT,'a') should call set_opt_decl('a')"""
        decl = SConsArguments.Declaration._ArgumentDeclaration()
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
        """<_ArgumentDeclaration>.set_env_decl(tuple()) should raise ValueError"""
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        with self.assertRaises(ValueError):
            decl.set_env_decl(tuple())

    def test_set_env_decl__tuple_ValueError_2(self):
        """<_ArgumentDeclaration>.set_env_decl(('a',)) should raise ValueError"""
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        with self.assertRaises(ValueError):
            decl.set_env_decl(('a',))

    def test_set_env_decl__tuple_1(self):
        """<_ArgumentDeclaration>.set_env_decl(('A','B')) should set __decl_tab[ENV] to {'key' : 'A', 'default' : 'B'}"""
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        decl.set_env_decl(('A','B'))
        self.assertEqual(decl._ArgumentDeclaration__decl_tab[SConsArguments.ENV], {'key' : 'A', 'default' : 'B'})

    def test_set_env_decl__dict_ValueError_1(self):
        """<_ArgumentDeclaration>.set_env_decl(dict()) should raise ValueError"""
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        with self.assertRaises(ValueError):
            decl.set_env_decl(dict())

    def test_set_env_decl__dict_ValueError_2(self):
        """<_ArgumentDeclaration>.set_env_decl({'a' : 'A', 'b' : 'B'}) should raise ValueError"""
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        with self.assertRaises(ValueError):
            decl.set_env_decl({'a' : 'A', 'b' : 'B'})

    def test_set_env_decl__dict_TypeError_1(self):
        """<_ArgumentDeclaration>.set_env_decl(None) should raise TypeError"""
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        with self.assertRaises(TypeError):
            decl.set_env_decl(None)

    def test_set_env_decl__dict_TypeError_2(self):
        """<_ArgumentDeclaration>.set_env_decl(123) should raise TypeError"""
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        with self.assertRaises(TypeError):
            decl.set_env_decl(123)

    def test_set_env_decl__dict_1(self):
        """<_ArgumentDeclaration>.set_env_decl({'a':'A'}) should set __decl_tab[ENV] to {'key' : 'a', 'default' : 'A'}"""
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        decl.set_env_decl({'a':'A'})
        self.assertEqual(decl._ArgumentDeclaration__decl_tab[SConsArguments.ENV], {'key' : 'a', 'default' : 'A'})

    def test_set_env_decl__string_1(self):
        """<_ArgumentDeclaration>.set_env_decl('foo') should set __decl_tab[ENV] to {'key' : 'foo', 'default' : _undef}"""
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        decl.set_env_decl('foo')
        self.assertEqual(decl._ArgumentDeclaration__decl_tab[SConsArguments.ENV], {'key' : 'foo', 'default' : SConsArguments._undef})

    def test_set_var_decl__ValueError_1(self):
        """<_ArgumentDeclaration>.set_var_decl((1, 2, 3, 4, 5, 6, 7)) should raise ValueError"""
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        with self.assertRaises(ValueError):
            decl.set_var_decl((1,2,3,4,5,6,7))

    def test_set_var_decl__ValueError_2(self):
        """<_ArgumentDeclaration>.set_var_decl([1, 2, 3, 4, 5, 6, 7]) should raise ValueError"""
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        with self.assertRaises(ValueError):
            decl.set_var_decl([1,2,3,4,5,6,7])

    def test_set_var_decl__TypeError_1(self):
        """<_ArgumentDeclaration>.set_var_decl(None) should raise TypeError"""
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        with self.assertRaises(TypeError):
            decl.set_var_decl(None)

    def test_set_var_decl__TypeError_2(self):
        """<_ArgumentDeclaration>.set_var_decl("foo") should raise TypeError"""
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        with self.assertRaises(TypeError):
            decl.set_var_decl("foo")

    def test_set_var_decl__TypeError_3(self):
        """<_ArgumentDeclaration>.set_var_decl(123) should raise TypeError"""
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        with self.assertRaises(TypeError):
            decl.set_var_decl(123)

    def test_set_var_decl__TypeError_4(self):
        """<_ArgumentDeclaration>.set_var_decl({'kw' : None}) should raise TypeError"""
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        with self.assertRaises(TypeError):
            decl.set_var_decl({'kw' : None})

    def test_set_var_decl__TypeError_4(self):
        """<_ArgumentDeclaration>.set_var_decl({'kw' : 'foo'}) should raise TypeError"""
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        with self.assertRaises(TypeError):
            decl.set_var_decl({'kw' : 'foo'})

    def test_set_var_decl__TypeError_5(self):
        """<_ArgumentDeclaration>.set_var_decl({'kw' : 123}) should raise TypeError"""
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        with self.assertRaises(TypeError):
            decl.set_var_decl({'kw' : 123})

    def test_set_var_decl__tuple_0(self):
        """<_ArgumentDeclaration>.set_var_decl(tuple()) should set __decl_tab[VAR] = {}"""
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        decl.set_var_decl(tuple())
        self.assertEqual(decl._ArgumentDeclaration__decl_tab[SConsArguments.VAR], {})

    def test_set_var_decl__tuple_1(self):
        """<_ArgumentDeclaration>.set_var_decl(('K',)) should set __decl_tab[VAR] = {'key' : 'K'}"""
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        decl.set_var_decl(('K',))
        self.assertEqual(decl._ArgumentDeclaration__decl_tab[SConsArguments.VAR], {'key' : 'K'})

    def test_set_var_decl__tuple_2(self):
        """<_ArgumentDeclaration>.set_var_decl(('K','H')) should set __decl_tab[VAR] = {'key' : 'K', 'help' : 'H'}"""
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        decl.set_var_decl(('K','H'))
        self.assertEqual(decl._ArgumentDeclaration__decl_tab[SConsArguments.VAR], {'key' : 'K', 'help' : 'H'})

    def test_set_var_decl__tuple_3(self):
        """<_ArgumentDeclaration>.set_var_decl(('K','H','D')) should set __decl_tab[VAR] = {'key' : 'K', 'help' : 'H', 'default' : 'D'}"""
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        decl.set_var_decl(('K','H', 'D'))
        self.assertEqual(decl._ArgumentDeclaration__decl_tab[SConsArguments.VAR], {'key' : 'K', 'help' : 'H', 'default' : 'D'})

    def test_set_var_decl__tuple_4(self):
        """<_ArgumentDeclaration>.set_var_decl(('K','H','D','V')) should set __decl_tab[VAR] = {'key' : 'K', 'help' : 'H', 'default' : 'D', 'validator' : 'V'}"""
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        decl.set_var_decl(('K','H','D','V'))
        self.assertEqual(decl._ArgumentDeclaration__decl_tab[SConsArguments.VAR], {'key' : 'K', 'help' : 'H', 'default' : 'D', 'validator' : 'V'})

    def test_set_var_decl__tuple_5(self):
        """<_ArgumentDeclaration>.set_var_decl(('K','H','D','V','C')) should set __decl_tab[VAR] = {'key' : 'K', 'help' : 'H', 'default' : 'D', 'validator' : 'V', 'converter' : 'C'}"""
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        decl.set_var_decl(('K','H','D','V','C'))
        self.assertEqual(decl._ArgumentDeclaration__decl_tab[SConsArguments.VAR], {'key' : 'K', 'help' : 'H', 'default' : 'D', 'validator' : 'V', 'converter' : 'C'})

    def test_set_var_decl__tuple_6(self):
        """<_ArgumentDeclaration>.set_var_decl(('K','H','D','V','C',{'a':'A'})) should set __decl_tab[VAR] = {'key' : 'K', 'help' : 'H', 'default' : 'D', 'validator' : 'V', 'converter' : 'C', 'a' : 'A'}"""
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        decl.set_var_decl(('K','H','D','V','C',{'a':'A'}))
        self.assertEqual(decl._ArgumentDeclaration__decl_tab[SConsArguments.VAR], {'key' : 'K', 'help' : 'H', 'default' : 'D', 'validator' : 'V', 'converter' : 'C', 'a' : 'A'})

    def test_set_var_decl__list_0(self):
        """<_ArgumentDeclaration>.set_var_decl(list()) should set __decl_tab[VAR] = {}"""
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        decl.set_var_decl(list())
        self.assertEqual(decl._ArgumentDeclaration__decl_tab[SConsArguments.VAR], {})

    def test_set_var_decl__list_1(self):
        """<_ArgumentDeclaration>.set_var_decl(['K']) should set __decl_tab[VAR] = {'key' : 'K'}"""
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        decl.set_var_decl(['K'])
        self.assertEqual(decl._ArgumentDeclaration__decl_tab[SConsArguments.VAR], {'key' : 'K'})

    def test_set_var_decl__list_2(self):
        """<_ArgumentDeclaration>.set_var_decl(['K','H']) should set __decl_tab[VAR] = {'key' : 'K', 'help' : 'H'}"""
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        decl.set_var_decl(['K','H'])
        self.assertEqual(decl._ArgumentDeclaration__decl_tab[SConsArguments.VAR], {'key' : 'K', 'help' : 'H'})

    def test_set_var_decl__list_3(self):
        """<_ArgumentDeclaration>.set_var_decl(['K','H','D']) should set __decl_tab[VAR] = {'key' : 'K', 'help' : 'H', 'default' : 'D'}"""
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        decl.set_var_decl(['K','H', 'D'])
        self.assertEqual(decl._ArgumentDeclaration__decl_tab[SConsArguments.VAR], {'key' : 'K', 'help' : 'H', 'default' : 'D'})

    def test_set_var_decl__list_4(self):
        """<_ArgumentDeclaration>.set_var_decl(['K','H','D','V']) should set __decl_tab[VAR] = {'key' : 'K', 'help' : 'H', 'default' : 'D', 'validator' : 'V'}"""
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        decl.set_var_decl(['K','H','D','V'])
        self.assertEqual(decl._ArgumentDeclaration__decl_tab[SConsArguments.VAR], {'key' : 'K', 'help' : 'H', 'default' : 'D', 'validator' : 'V'})

    def test_set_var_decl__list_5(self):
        """<_ArgumentDeclaration>.set_var_decl(['K','H','D','V','C']) should set __decl_tab[VAR] = {'key' : 'K', 'help' : 'H', 'default' : 'D', 'validator' : 'V', 'converter' : 'C'}"""
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        decl.set_var_decl(['K','H','D','V','C'])
        self.assertEqual(decl._ArgumentDeclaration__decl_tab[SConsArguments.VAR], {'key' : 'K', 'help' : 'H', 'default' : 'D', 'validator' : 'V', 'converter' : 'C'})

    def test_set_var_decl__list_6(self):
        """<_ArgumentDeclaration>.set_var_decl(['K','H','D','V','C',{'a':'A'}]) should set __decl_tab[VAR] = {'key' : 'K', 'help' : 'H', 'default' : 'D', 'validator' : 'V', 'converter' : 'C', 'a' : 'A'}"""
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        decl.set_var_decl(['K','H','D','V','C',{'a':'A'}])
        self.assertEqual(decl._ArgumentDeclaration__decl_tab[SConsArguments.VAR], {'key' : 'K', 'help' : 'H', 'default' : 'D', 'validator' : 'V', 'converter' : 'C', 'a' : 'A'})

    def test_set_opt_decl__ValueError_1(self):
        """<_ArgumentDeclaration>.set_opt_decl(tuple()) should raise ValueError"""
        empty = tuple()
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        with self.assertRaises(ValueError) as cm:
            decl.set_opt_decl(empty)
        self.assertEqual(str(cm.exception), "'decl' must not be empty, got %(empty)r" % locals())

    def test_set_opt_decl__ValueError_2(self):
        """<_ArgumentDeclaration>.set_opt_decl(('--foo',)) should raise ValueError"""
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        with self.assertRaises(ValueError) as cm:
            decl.set_opt_decl(('-foo',))
        self.assertEqual(str(cm.exception), "missing parameter 'dest' in option specification")

    def test_set_opt_decl__ValueError_3(self):
        """<_ArgumentDeclaration>.set_opt_decl(['--foo']) should raise ValueError"""
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        with self.assertRaises(ValueError) as cm:
            decl.set_opt_decl(['-foo'])
        self.assertEqual(str(cm.exception), "missing parameter 'dest' in option specification")

    def test_set_opt_decl__ValueError_4(self):
        """<_ArgumentDeclaration>.set_opt_decl({'names' : '--foo'}) should raise ValueError (missing 'dest')"""
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        with self.assertRaises(ValueError) as cm:
            decl.set_opt_decl({'names' : '--foo'})
        self.assertEqual(str(cm.exception), "missing parameter 'dest' in option specification")

    def test_set_opt_decl__KeyError_1(self):
        """<_ArgumentDeclaration>.set_opt_decl(dict()) should raise KeyError"""
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        with self.assertRaises(KeyError):
            decl.set_opt_decl(dict())

    def test_set_opt_decl__TypeError_1(self):
        """<_ArgumentDeclaration>.set_opt_decl((None,)) should raise TypeError"""
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        with self.assertRaises(TypeError):
            decl.set_opt_decl((None,))

    def test_set_opt_decl__TypeError_2(self):
        """<_ArgumentDeclaration>.set_opt_decl((123,)) should raise TypeError"""
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        with self.assertRaises(TypeError):
            decl.set_opt_decl((123,))

    def test_set_opt_decl__TypeError_3(self):
        """<_ArgumentDeclaration>.set_opt_decl({'names' : None)) should raise TypeError"""
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        with self.assertRaises(TypeError):
            decl.set_opt_decl({'names' : None})

    def test_set_opt_decl__TypeError_4(self):
        """<_ArgumentDeclaration>.set_opt_decl({'names' : 123}) should raise TypeError"""
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        with self.assertRaises(TypeError):
            decl.set_opt_decl({'names' : 123})

    def test_set_opt_decl__TypeError_5(self):
        """<_ArgumentDeclaration>.set_opt_decl(None) should raise TypeError"""
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        with self.assertRaises(TypeError):
            decl.set_opt_decl(None)

    def test_set_opt_decl__TypeError_6(self):
        """<_ArgumentDeclaration>.set_opt_decl('foo') should raise TypeError"""
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        with self.assertRaises(TypeError):
            decl.set_opt_decl('foo')

    def test_set_opt_decl__TypeError_7(self):
        """<_ArgumentDeclaration>.set_opt_decl(123) should raise TypeError"""
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        with self.assertRaises(TypeError):
            decl.set_opt_decl(123)

    def test_set_opt_decl__tuple_1(self):
        """<_ArgumentDeclaration>.set_opt_decl(('--foo', {'dest' : 'foo'})) sets __decl_tab[OPT] = (('--foo',), {'dest' : 'foo'})"""
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        decl.set_opt_decl(('--foo', {'dest' : 'foo'}))
        self.assertEqual(decl._ArgumentDeclaration__decl_tab[SConsArguments.OPT], (('--foo',), {'dest' : 'foo'}))

    def test_set_opt_decl__tuple_2(self):
        """<_ArgumentDeclaration>.set_opt_decl(('--foo -f', {'dest' : 'foo'})) sets __decl_tab[OPT] = (('--foo','-f'), {'dest' : 'foo'})"""
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        decl.set_opt_decl(('--foo -f', {'dest' : 'foo'}))
        self.assertEqual(decl._ArgumentDeclaration__decl_tab[SConsArguments.OPT], (('--foo','-f'), {'dest' : 'foo'}))

    def test_set_opt_decl__tuple_3(self):
        """<_ArgumentDeclaration>.set_opt_decl((('--foo','-f'), {'dest' : 'foo'})) sets __decl_tab[OPT] = (('--foo','-f'), {'dest' : 'foo'})"""
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        decl.set_opt_decl((('--foo', '-f'), {'dest' : 'foo'}))
        self.assertEqual(decl._ArgumentDeclaration__decl_tab[SConsArguments.OPT], (('--foo','-f'), {'dest' : 'foo'}))

    def test_set_opt_decl__tuple_4(self):
        """<_ArgumentDeclaration>.set_opt_decl((['--foo','-f'], {'dest' : 'foo'})) sets __decl_tab[OPT] = (('--foo','-f'), {'dest' : 'foo'})"""
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        decl.set_opt_decl((['--foo', '-f'], {'dest' : 'foo'}))
        self.assertEqual(decl._ArgumentDeclaration__decl_tab[SConsArguments.OPT], (('--foo','-f'), {'dest' : 'foo'}))

    def test_set_opt_decl__list_1(self):
        """<_ArgumentDeclaration>.set_opt_decl(['--foo', {'dest' : 'foo'}]) sets __decl_tab[OPT] = (('--foo',), {'dest' : 'foo'})"""
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        decl.set_opt_decl(['--foo', {'dest' : 'foo'}])
        self.assertEqual(decl._ArgumentDeclaration__decl_tab[SConsArguments.OPT], (('--foo',), {'dest' : 'foo'}))

    def test_set_opt_decl__list_2(self):
        """<_ArgumentDeclaration>.set_opt_decl(['--foo -f', {'dest' : 'foo'}]) sets __decl_tab[OPT] = (('--foo','-f'), {'dest' : 'foo'})"""
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        decl.set_opt_decl(['--foo -f', {'dest' : 'foo'}])
        self.assertEqual(decl._ArgumentDeclaration__decl_tab[SConsArguments.OPT], (('--foo','-f'), {'dest' : 'foo'}))

    def test_set_opt_decl__list_3(self):
        """<_ArgumentDeclaration>.set_opt_decl([('--foo','-f'), {'dest' : 'foo'}]) sets __decl_tab[OPT] = (('--foo','-f'), {'dest' : 'foo'})"""
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        decl.set_opt_decl([('--foo', '-f'), {'dest' : 'foo'}])
        self.assertEqual(decl._ArgumentDeclaration__decl_tab[SConsArguments.OPT], (('--foo','-f'), {'dest' : 'foo'}))

    def test_set_opt_decl__list_4(self):
        """<_ArgumentDeclaration>.set_opt_decl([['--foo','-f'], {'dest' : 'foo'}]) sets __decl_tab[OPT] = (('--foo','-f'), {'dest' : 'foo'})"""
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        decl.set_opt_decl([['--foo', '-f'], {'dest' : 'foo'}])
        self.assertEqual(decl._ArgumentDeclaration__decl_tab[SConsArguments.OPT], (('--foo','-f'), {'dest' : 'foo'}))

    def test_set_opt_decl__dict_1(self):
        """<_ArgumentDeclaration>.set_opt_decl({'names' : '--foo', 'dest' : 'foo'}) sets __decl_tab[OPT] = (('--foo',), {'dest' : 'foo'})"""
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        decl.set_opt_decl({'names' : '--foo', 'dest' : 'foo'})
        self.assertEqual(decl._ArgumentDeclaration__decl_tab[SConsArguments.OPT], (('--foo',), {'dest' : 'foo'}))

    def test_set_opt_decl__dict_2(self):
        """<_ArgumentDeclaration>.set_opt_decl({'names' : '--foo -f', 'dest' : 'foo'}) sets __decl_tab[OPT] = (('--foo','-f'), {'dest' : 'foo'})"""
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        decl.set_opt_decl({'names' : '--foo -f', 'dest' : 'foo'})
        self.assertEqual(decl._ArgumentDeclaration__decl_tab[SConsArguments.OPT], (('--foo','-f'), {'dest' : 'foo'}))

    def test_set_opt_decl__dict_3(self):
        """<_ArgumentDeclaration>.set_opt_decl({'names' : ('--foo','-f'), 'dest' : 'foo'}) sets __decl_tab[OPT] = (('--foo','-f'), {'dest' : 'foo'})"""
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        decl.set_opt_decl({'names' : ('--foo', '-f'), 'dest' : 'foo'})
        self.assertEqual(decl._ArgumentDeclaration__decl_tab[SConsArguments.OPT], (('--foo','-f'), {'dest' : 'foo'}))

    def test_set_opt_decl__dict_4(self):
        """<_ArgumentDeclaration>.set_opt_decl({'names' : ['--foo','-f'], 'dest' : 'foo'}) sets __decl_tab[OPT] = (('--foo','-f'), {'dest' : 'foo'})"""
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        decl.set_opt_decl({'names' : ['--foo', '-f'], 'dest' : 'foo'})
        self.assertEqual(decl._ArgumentDeclaration__decl_tab[SConsArguments.OPT], (('--foo','-f'), {'dest' : 'foo'}))

    def test_has_decl_0(self):
        """_ArgumentDeclaration().has_decl(...) should always return False"""
        self.assertFalse(SConsArguments.Declaration._ArgumentDeclaration().has_decl(SConsArguments.ENV))
        self.assertFalse(SConsArguments.Declaration._ArgumentDeclaration().has_decl(SConsArguments.VAR))
        self.assertFalse(SConsArguments.Declaration._ArgumentDeclaration().has_decl(SConsArguments.OPT))

    def test_has_decl_ENV_1(self):
        """<_ArgumentDeclaration>.has_decl(EVN) should return true when ENV declaration was provided"""
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        decl.set_env_decl({'FOO' : 123})
        self.assertTrue(decl.has_decl(SConsArguments.ENV))
        self.assertFalse(decl.has_decl(SConsArguments.VAR))
        self.assertFalse(decl.has_decl(SConsArguments.OPT))

    def test_has_decl_VAR_1(self):
        """<_ArgumentDeclaration>.has_decl(VAR) should return true when VAR declaration was provided"""
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        decl.set_var_decl(('FOO',))
        self.assertFalse(decl.has_decl(SConsArguments.ENV))
        self.assertTrue(decl.has_decl(SConsArguments.VAR))
        self.assertFalse(decl.has_decl(SConsArguments.OPT))

    def test_has_decl_OPT_1(self):
        """<_ArgumentDeclaration>.has_decl(EVN) should return true when OPT declaration was provided"""
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        decl.set_opt_decl(('--foo', {'dest' : 'foo'}))
        self.assertFalse(decl.has_decl(SConsArguments.ENV))
        self.assertFalse(decl.has_decl(SConsArguments.VAR))
        self.assertTrue(decl.has_decl(SConsArguments.OPT))

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_has_env_decl_1(self):
        """<_ArgumentDeclaration>.has_env_decl() should invoke has_decl(ENV)"""
        class _test_val: pass
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        decl.has_decl = mock.Mock(name = 'has_decl', return_value = _test_val)
        ret = decl.has_env_decl()
        self.assertIs(ret, _test_val)
        try:
            decl.has_decl.assert_called_once_with(SConsArguments.ENV)
        except AssertionError as e:
            self.fail(str(e))

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_has_var_decl_1(self):
        """<_ArgumentDeclaration>.has_var_decl() should invoke has_decl(VAR)"""
        class _test_val: pass
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        decl.has_decl = mock.Mock(name = 'has_decl', return_value = _test_val)
        ret = decl.has_var_decl()
        self.assertIs(ret, _test_val)
        try:
            decl.has_decl.assert_called_once_with(SConsArguments.VAR)
        except AssertionError as e:
            self.fail(str(e))

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_has_opt_decl_1(self):
        """<_ArgumentDeclaration>.has_opt_decl() should invoke has_decl(OPT)"""
        class _test_val: pass
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        decl.has_decl = mock.Mock(name = 'has_decl', return_value = _test_val)
        ret = decl.has_opt_decl()
        self.assertIs(ret, _test_val)
        try:
            decl.has_decl.assert_called_once_with(SConsArguments.OPT)
        except AssertionError as e:
            self.fail(str(e))

    def test_get_decl__123_IndexError_1(self):
        """<_ArgumentDeclaration>.get_decl(123) should raise IndexError"""
        with self.assertRaises(IndexError):
            SConsArguments.Declaration._ArgumentDeclaration(env_decl = {'a' : 'A'}).get_decl(123)

    def test_get_decl__ENV_IndexError(self):
        """_ArgumentDeclaration().get_decl(ENV) should raise IndexError"""
        with self.assertRaises(IndexError):
            SConsArguments.Declaration._ArgumentDeclaration().get_decl(SConsArguments.ENV)

    def test_get_decl__VAR_IndexError(self):
        """_ArgumentDeclaration().get_decl(VAR) should raise IndexError"""
        with self.assertRaises(IndexError):
            SConsArguments.Declaration._ArgumentDeclaration().get_decl(SConsArguments.VAR)

    def test_get_decl__OPT_IndexError(self):
        """_ArgumentDeclaration().get_decl(OPT) should raise IndexError"""
        with self.assertRaises(IndexError):
            SConsArguments.Declaration._ArgumentDeclaration().get_decl(SConsArguments.OPT)

    def test_get_decl__ENV_1(self):
        """<_ArgumentDeclaration>.get_decl(ENV) should return __decl_tab[ENV]"""
        class _test_val: pass
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        decl._ArgumentDeclaration__decl_tab[SConsArguments.ENV] = _test_val
        self.assertIs(decl.get_decl(SConsArguments.ENV), _test_val)

    def test_get_decl__VAR_1(self):
        """<_ArgumentDeclaration>.get_decl(VAR) should return __decl_tab[VAR]"""
        class _test_val: pass
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        decl._ArgumentDeclaration__decl_tab[SConsArguments.VAR] = _test_val
        self.assertIs(decl.get_decl(SConsArguments.VAR), _test_val)

    def test_get_decl__OPT_1(self):
        """<_ArgumentDeclaration>.get_decl(OPT) should return __decl_tab[OPT]"""
        class _test_val: pass
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        decl._ArgumentDeclaration__decl_tab[SConsArguments.OPT] = _test_val
        self.assertIs(decl.get_decl(SConsArguments.OPT), _test_val)

    def test_get_key__123_IndexError_1(self):
        """<_ArgumentDeclaration>.get_key(123) should raise IndexError"""
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        with self.assertRaises(IndexError) as cm:
            decl.get_key(123)
        self.assertEqual(str(cm.exception), "index out of range")

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_get_env_decl_1(self):
        """<_ArgumentDeclaration>.get_env_decl() should invoke get_decl(ENV)"""
        class _test_val: pass
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        decl.get_decl = mock.Mock(name = 'get_decl', return_value = _test_val)
        ret = decl.get_env_decl()
        self.assertIs(ret, _test_val)
        try:
            decl.get_decl.assert_called_once_with(SConsArguments.ENV)
        except AssertionError as e:
            self.fail(str(e))

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_get_var_decl_1(self):
        """<_ArgumentDeclaration>.get_var_decl() should invoke get_decl(VAR)"""
        class _test_val: pass
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        decl.get_decl = mock.Mock(name = 'get_decl', return_value = _test_val)
        ret = decl.get_var_decl()
        self.assertIs(ret, _test_val)
        try:
            decl.get_decl.assert_called_once_with(SConsArguments.VAR)
        except AssertionError as e:
            self.fail(str(e))

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_get_opt_decl_1(self):
        """<_ArgumentDeclaration>.get_opt_decl() should invoke get_decl(OPT)"""
        class _test_val: pass
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        decl.get_decl = mock.Mock(name = 'get_decl', return_value = _test_val)
        ret = decl.get_opt_decl()
        self.assertIs(ret, _test_val)
        try:
            decl.get_decl.assert_called_once_with(SConsArguments.OPT)
        except AssertionError as e:
            self.fail(str(e))

    def test_get_key__ENV_IndexError_1(self):
        """_ArgumentDeclaration().get_key(ENV) should raise IndexError"""
        with self.assertRaises(IndexError):
            SConsArguments.Declaration._ArgumentDeclaration().get_key(SConsArguments.ENV)

    def test_get_key__VAR_IndexError_1(self):
        """_ArgumentDeclaration().get_key(VAR) should raise IndexError"""
        with self.assertRaises(IndexError):
            SConsArguments.Declaration._ArgumentDeclaration().get_key(SConsArguments.VAR)

    def test_get_key__OPT_IndexError_1(self):
        """_ArgumentDeclaration().get_key(OPT) should raise IndexError"""
        with self.assertRaises(IndexError):
            SConsArguments.Declaration._ArgumentDeclaration().get_key(SConsArguments.OPT)

    def test_get_key__ENV_1(self):
        """_ArgumentDeclaration({'ENV_FOO' : 1}).get_key(ENV) should return 'ENV_FOO'"""
        self.assertEqual(SConsArguments.Declaration._ArgumentDeclaration({'ENV_FOO' : 1}).get_key(SConsArguments.ENV), 'ENV_FOO')

    def test_get_key__VAR_1(self):
        """_ArgumentDeclaration(var_decl = ('VAR_FOO',)).get_key(VAR) should return 'VAR_FOO'"""
        self.assertEqual(SConsArguments.Declaration._ArgumentDeclaration(var_decl = ('VAR_FOO',)).get_key(SConsArguments.VAR), 'VAR_FOO')

    def test_get_key__OPT_1(self):
        """_ArgumentDeclaration(opt_decl = ('--foo', {'dest' : 'OPT_FOO'})).get_key(OPT) should return 'OPT_FOO'"""
        self.assertEqual(SConsArguments.Declaration._ArgumentDeclaration(opt_decl = ('--foo', {'dest' : 'OPT_FOO'})).get_key(SConsArguments.OPT), 'OPT_FOO')

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_get_env_key_1(self):
        """<_ArgumentDeclaration>.get_env_key() should invoke get_key(ENV)"""
        class _test_val: pass
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        decl.get_key = mock.Mock(name = 'get_key', return_value = _test_val)
        ret = decl.get_env_key()
        self.assertIs(ret, _test_val)
        try:
            decl.get_key.assert_called_once_with(SConsArguments.ENV)
        except AssertionError as e:
            self.fail(str(e))

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_get_var_key_1(self):
        """<_ArgumentDeclaration>.get_var_key() should invoke get_key(VAR)"""
        class _test_val: pass
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        decl.get_key = mock.Mock(name = 'get_key', return_value = _test_val)
        ret = decl.get_var_key()
        self.assertIs(ret, _test_val)
        try:
            decl.get_key.assert_called_once_with(SConsArguments.VAR)
        except AssertionError as e:
            self.fail(str(e))

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_get_opt_key_1(self):
        """<_ArgumentDeclaration>.get_opt_key() should invoke get_key(OPT)"""
        class _test_val: pass
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        decl.get_key = mock.Mock(name = 'get_key', return_value = _test_val)
        ret = decl.get_opt_key()
        self.assertIs(ret, _test_val)
        try:
            decl.get_key.assert_called_once_with(SConsArguments.OPT)
        except AssertionError as e:
            self.fail(str(e))

    def test_set_key__IndexError_1(self):
        """_ArgumentDeclaration().set_key(123,'a') should raise IndexError"""
        with self.assertRaises(IndexError):
            SConsArguments.Declaration._ArgumentDeclaration().set_key(123,'a')

    def test_set_key__ENV_IndexError_1(self):
        """_ArgumentDeclaration().set_key(ENV,'a') should raise IndexError"""
        with self.assertRaises(IndexError):
            SConsArguments.Declaration._ArgumentDeclaration().set_key(SConsArguments.ENV,'a')

    def test_set_key__VAR_IndexError_1(self):
        """_ArgumentDeclaration().set_key(VAR,'a') should raise IndexError"""
        with self.assertRaises(IndexError):
            SConsArguments.Declaration._ArgumentDeclaration().set_key(SConsArguments.VAR,'a')

    def test_set_key__OPT_IndexError_1(self):
        """_ArgumentDeclaration().set_key(OPT,'a') should raise IndexError"""
        with self.assertRaises(IndexError):
            SConsArguments.Declaration._ArgumentDeclaration().set_key(SConsArguments.OPT,'a')

    def test_set_key__ENV_1(self):
        """<_ArgumentDeclaration>.set_key(ENV,'BAR') should set new ENV key"""
        valu = {'xyz' : 'bobo'}
        decl = SConsArguments.Declaration._ArgumentDeclaration(env_decl = {'FOO' : valu})
        self.assertEqual(decl.get_key(SConsArguments.ENV), 'FOO')
        decl.set_key(SConsArguments.ENV,'BAR');
        self.assertEqual(decl.get_key(SConsArguments.ENV), 'BAR')
        self.assertIs(decl._ArgumentDeclaration__decl_tab[SConsArguments.ENV]['default'], valu)

    def test_set_key__VAR_1(self):
        """<_ArgumentDeclaration>.set_key(VAR,'BAR') should set new VAR key"""
        valu = {'xyz' : 'bobo'}
        decl = SConsArguments.Declaration._ArgumentDeclaration(var_decl = {'key' : 'FOO', 'default' : valu})
        self.assertEqual(decl.get_key(SConsArguments.VAR), 'FOO')
        decl.set_key(SConsArguments.VAR,'BAR');
        self.assertEqual(decl.get_key(SConsArguments.VAR), 'BAR')
        self.assertIs(decl._ArgumentDeclaration__decl_tab[SConsArguments.VAR]['key'], 'BAR')
        self.assertIs(decl._ArgumentDeclaration__decl_tab[SConsArguments.VAR]['default'], valu)

    def test_set_key__OPT_1(self):
        """<_ArgumentDeclaration>.set_key(OPT,'BAR') should set new OPT key"""
        valu = {'xyz' : 'bobo'}
        decl = SConsArguments.Declaration._ArgumentDeclaration(opt_decl = ('--foo', {'dest' : 'FOO', 'default' :  valu}))
        self.assertEqual(decl.get_key(SConsArguments.OPT), 'FOO')
        decl.set_key(SConsArguments.OPT,'BAR');
        self.assertEqual(decl.get_key(SConsArguments.OPT), 'BAR')
        self.assertIs(decl._ArgumentDeclaration__decl_tab[SConsArguments.OPT][1]['dest'], 'BAR')
        self.assertIs(decl._ArgumentDeclaration__decl_tab[SConsArguments.OPT][1]['default'], valu)

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_set_env_key_1(self):
        """<_ArgumentDeclaration>.set_env_key(key) should invoke set_key(ENV,key)"""
        class _test_key: pass
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        decl.set_key = mock.Mock(name = 'set_key')
        decl.set_env_key(_test_key)
        try:
            decl.set_key.assert_called_once_with(SConsArguments.ENV, _test_key)
        except AssertionError as e:
            self.fail(str(e))

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_set_var_key_1(self):
        """<_ArgumentDeclaration>.set_var_key(key) should invoke set_key(VAR,key)"""
        class _test_key: pass
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        decl.set_key = mock.Mock(name = 'set_key')
        decl.set_var_key(_test_key)
        try:
            decl.set_key.assert_called_once_with(SConsArguments.VAR, _test_key)
        except AssertionError as e:
            self.fail(str(e))

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_set_opt_key_1(self):
        """<_ArgumentDeclaration>.set_opt_key(key) should invoke set_key(OPT,key)"""
        class _test_key: pass
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        decl.set_key = mock.Mock(name = 'set_key')
        decl.set_opt_key(_test_key)
        try:
            decl.set_key.assert_called_once_with(SConsArguments.OPT, _test_key)
        except AssertionError as e:
            self.fail(str(e))

    def test_get_default__123_IndexError_1(self):
        """<_ArgumentDeclaration>.get_default(123) should raise IndexError"""
        decl = SConsArguments.Declaration._ArgumentDeclaration('FOO', ('FOO',1), ('-foo', {'dest' : 'FOO', 'default' : 1}))
        with self.assertRaises(IndexError):
            decl.get_default(123)

    def test_get_default__ENV_IndexError_1(self):
        """_ArgumentDeclaration().get_default(ENV) should raise IndexError"""
        with self.assertRaises(IndexError):
            SConsArguments.Declaration._ArgumentDeclaration().get_default(SConsArguments.ENV)

    def test_get_default__VAR_IndexError_1(self):
        """_ArgumentDeclaration().get_default(VAR) should raise IndexError"""
        with self.assertRaises(IndexError):
            SConsArguments.Declaration._ArgumentDeclaration().get_default(SConsArguments.VAR)

    def test_get_default__OPT_IndexError_1(self):
        """_ArgumentDeclaration().get_default(OPT) should raise IndexError"""
        with self.assertRaises(IndexError):
            SConsArguments.Declaration._ArgumentDeclaration().get_default(SConsArguments.OPT)

    def test_get_default__ENV_1(self):
        """_ArgumentDeclaration(env_decl = 'FOO').get_default(ENV) should return _undef"""
        decl = SConsArguments.Declaration._ArgumentDeclaration(env_decl = 'FOO')
        self.assertIs(decl.get_default(SConsArguments.ENV), SConsArguments._undef)

    def test_get_default__ENV_2(self):
        """_ArgumentDeclaration(env_decl = {'FOO': 123}).get_default(ENV) should return 123"""
        decl = SConsArguments.Declaration._ArgumentDeclaration(env_decl = {'FOO' : 123})
        self.assertEqual(decl.get_default(SConsArguments.ENV), 123)

    def test_get_default__VAR_1(self):
        """_ArgumentDeclaration(var_decl = ('FOO',)).get_default(VAR) should return _undef"""
        decl = SConsArguments.Declaration._ArgumentDeclaration(var_decl = ('FOO',))
        self.assertIs(decl.get_default(SConsArguments.VAR), SConsArguments._undef)

    def test_get_default__VAR_2(self):
        """_ArgumentDeclaration(var_decl = {'key': 'FOO', 'default': 123}).get_default(VAR) should return 123"""
        decl = SConsArguments.Declaration._ArgumentDeclaration(var_decl = {'key' : 'FOO', 'default' : 123})
        self.assertEqual(decl.get_default(SConsArguments.VAR), 123)

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_get_env_default_1(self):
        """<_ArgumentDeclaration>.get_env_default() should invoke get_default(ENV)"""
        class _test_val: pass
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        decl.get_default = mock.Mock(name = 'get_default', return_value = _test_val)
        ret = decl.get_env_default()
        self.assertIs(ret, _test_val)
        try:
            decl.get_default.assert_called_once_with(SConsArguments.ENV)
        except AssertionError as e:
            self.fail(str(e))

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_get_var_default_1(self):
        """<_ArgumentDeclaration>.get_var_default() should invoke get_default(VAR)"""
        class _test_val: pass
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        decl.get_default = mock.Mock(name = 'get_default', return_value = _test_val)
        ret = decl.get_var_default()
        self.assertIs(ret, _test_val)
        try:
            decl.get_default.assert_called_once_with(SConsArguments.VAR)
        except AssertionError as e:
            self.fail(str(e))

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_get_opt_default_1(self):
        """<_ArgumentDeclaration>.get_opt_default() should invoke get_default(OPT)"""
        class _test_val: pass
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        decl.get_default = mock.Mock(name = 'get_default', return_value = _test_val)
        ret = decl.get_opt_default()
        self.assertIs(ret, _test_val)
        try:
            decl.get_default.assert_called_once_with(SConsArguments.OPT)
        except AssertionError as e:
            self.fail(str(e))

    def test_set_default__123_IndexError_1(self):
        """<_ArgumentDeclaration>.set_default(123, 1) should raise IndexError"""
        decl = SConsArguments.Declaration._ArgumentDeclaration('FOO', ('FOO',), ('-foo', {'dest' : 'FOO'}))
        with self.assertRaises(IndexError):
            decl.set_default(123, 1)

    def test_set_default__ENV_IndexError_1(self):
        """_ArgumentDeclaration().set_default(ENV, 1) should raise IndexError"""
        with self.assertRaises(IndexError):
            SConsArguments.Declaration._ArgumentDeclaration().set_default(SConsArguments.ENV, 1)

    def test_set_default__VAR_IndexError_1(self):
        """_ArgumentDeclaration().set_default(VAR, 1) should raise IndexError"""
        with self.assertRaises(IndexError):
            SConsArguments.Declaration._ArgumentDeclaration().set_default(SConsArguments.VAR, 1)

    def test_set_default__OPT_IndexError_1(self):
        """_ArgumentDeclaration().set_default(OPT, 1) should raise IndexError"""
        with self.assertRaises(IndexError):
            SConsArguments.Declaration._ArgumentDeclaration().set_default(SConsArguments.OPT, 1)

    def test_set_default__ENV_1(self):
        """<_ArgumentDeclaration>.set_default(ENV, 123) should set ENV default to 123"""
        decl = SConsArguments.Declaration._ArgumentDeclaration(env_decl = 'FOO')
        decl.set_default(SConsArguments.ENV, 123)
        self.assertEqual(decl.get_default(SConsArguments.ENV), 123)

    def test_set_default__VAR_1(self):
        """<_ArgumentDeclaration>.set_default(VAR, 123) should set VAR default to 123"""
        decl = SConsArguments.Declaration._ArgumentDeclaration(var_decl = ('FOO',))
        decl.set_default(SConsArguments.VAR, 123)
        self.assertEqual(decl.get_default(SConsArguments.VAR), 123)

    def test_set_default__OPT_1(self):
        """<_ArgumentDeclaration>.set_default(OPT, 123) should set OPT default to 123"""
        decl = SConsArguments.Declaration._ArgumentDeclaration(opt_decl = ('--foo', {'dest' : 'FOO'}))
        decl.set_default(SConsArguments.OPT, 123)
        self.assertEqual(decl.get_default(SConsArguments.OPT), 123)

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_set_env_default_1(self):
        """<_ArgumentDeclaration>.set_env_default(default) should invoke set_default(ENV,default)"""
        class _test_default: pass
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        decl.set_default = mock.Mock(name = 'set_default')
        decl.set_env_default(_test_default)
        try:
            decl.set_default.assert_called_once_with(SConsArguments.ENV, _test_default)
        except AssertionError as e:
            self.fail(str(e))

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_set_var_default_1(self):
        """<_ArgumentDeclaration>.set_var_default(default) should invoke set_default(VAR,default)"""
        class _test_default: pass
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        decl.set_default = mock.Mock(name = 'set_default')
        decl.set_var_default(_test_default)
        try:
            decl.set_default.assert_called_once_with(SConsArguments.VAR, _test_default)
        except AssertionError as e:
            self.fail(str(e))

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_set_opt_default_1(self):
        """<_ArgumentDeclaration>.set_opt_default(default) should invoke set_default(OPT,default)"""
        class _test_default: pass
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        decl.set_default = mock.Mock(name = 'set_default')
        decl.set_opt_default(_test_default)
        try:
            decl.set_default.assert_called_once_with(SConsArguments.OPT, _test_default)
        except AssertionError as e:
            self.fail(str(e))

    def test_add_to__123_IndexError_1(self):
        """<_ArgumentDeclaration>.add_to(123) should raise IndexError"""
        decl = SConsArguments.Declaration._ArgumentDeclaration('FOO', ('FOO',), ('--foo', {'dest' : 'FOO'}))
        with self.assertRaises(IndexError):
            decl.add_to(123)

    def test_add_to__ENV_IndexError_1(self):
        """_ArgumentDeclaration().add_to(ENV) should raise IndexError"""
        with self.assertRaises(IndexError):
            SConsArguments.Declaration._ArgumentDeclaration().add_to(SConsArguments.ENV)

    def test_add_to__VAR_IndexError_1(self):
        """_ArgumentDeclaration().add_to(VAR) should raise IndexError"""
        with self.assertRaises(IndexError):
            SConsArguments.Declaration._ArgumentDeclaration().add_to(SConsArguments.VAR)

    def test_add_to__OPT_IndexError_1(self):
        """_ArgumentDeclaration().add_to(OPT) should raise IndexError"""
        with self.assertRaises(IndexError):
            SConsArguments.Declaration._ArgumentDeclaration().add_to(SConsArguments.OPT)

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_add_to__ENV_0(self):
        """_ArgumentDeclaration(env_decl = 'FOO').add_to(ENV,env) should not call env.SetDefault()"""
        env = mock.Mock(name = 'env')
        env.SetDefault = mock.Mock(name = 'SetDefault')
        decl1 = SConsArguments.Declaration._ArgumentDeclaration(env_decl = 'FOO')
        decl1.add_to(SConsArguments.ENV, env)
        try:
            env.SetDefault.assert_not_called()
        except AssertionError as e:
            self.fail(str(e))

        decl2 = SConsArguments.Declaration._ArgumentDeclaration(env_decl = {'FOO' : SConsArguments._undef})
        decl2.add_to(SConsArguments.ENV, env)
        try:
            env.SetDefault.assert_not_called()
        except AssertionError as e:
            self.fail(str(e))

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_add_to__ENV_1(self):
        """_ArgumentDeclaration(env_decl = {'FOO' : 123}).add_to(ENV,env) should call env.SetDefault(FOO = 123)"""
        env = mock.Mock(name = 'env')
        env.SetDefault = mock.Mock(name = 'SetDefault')
        decl = SConsArguments.Declaration._ArgumentDeclaration(env_decl = {'FOO' : 123})
        decl.add_to(SConsArguments.ENV, env)
        try:
            env.SetDefault.assert_called_once_with(FOO = 123)
        except AssertionError as e:
            self.fail(str(e))

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_add_to__VAR_1(self):
        """_ArgumentDeclaration(var_decl = ('FOO',)).add_to(VAR,var) should call var.Add(key='FOO')"""
        var = mock.Mock(name = 'var')
        var.Add = mock.Mock(name = 'Add')
        decl1 = SConsArguments.Declaration._ArgumentDeclaration(var_decl = ('FOO',))
        decl1.add_to(SConsArguments.VAR, var)
        try:
            var.Add.assert_called_once_with(key = 'FOO')
        except AssertionError as e:
            self.fail(str(e))

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_add_to__VAR_2(self):
        """_ArgumentDeclaration(var_decl = ('FOO', 'some help', 123)).add_to(VAR,var) should call var.Add(key = 'FOO', default = 123)"""
        var = mock.Mock(name = 'var')
        var.Add = mock.Mock(name = 'Add')
        decl = SConsArguments.Declaration._ArgumentDeclaration(var_decl = ('FOO', 'some help', 123))
        decl.add_to(SConsArguments.VAR, var)
        try:
            var.Add.assert_called_once_with(key = 'FOO', help = 'some help', default = 123)
        except AssertionError as e:
            self.fail(str(e))

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_add_to__OPT_1(self):
        """_ArgumentDeclaration(opt_decl = ('--foo',{'dest' : 'FOO'})).add_to(OPT,opt) should call SCons.Script.Main.AddOption('--foo', dest='FOO')"""
        with mock.patch('SCons.Script.Main.AddOption') as AddOption:
            decl1 = SConsArguments.Declaration._ArgumentDeclaration(opt_decl = ('--foo',{'dest' : 'FOO'}))
            decl1.add_to(SConsArguments.OPT)
            try:
                AddOption.assert_called_once_with('--foo', dest = 'FOO')
            except AssertionError as e:
                self.fail(str(e))

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_safe_add_to__ENV_0(self):
        """_ArgumentDeclaration().safe_add_to(ENV,env) should not call <_ArgumentDeclaration>.add_to()"""
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        decl.add_to = mock.Mock(name = 'add_to')
        env = mock.Mock(name = 'env')
        ret = decl.safe_add_to(SConsArguments.ENV, env)
        try:
            decl.add_to.assert_not_called()
        except AssertionError as e:
            self.fail(str(e))
        self.assertFalse(ret)

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_safe_add_to__VAR_0(self):
        """_ArgumentDeclaration().safe_add_to(VAR,var) should not call <_ArgumentDeclaration>.add_to()"""
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        decl.add_to = mock.Mock(name = 'add_to')
        var = mock.Mock(name = 'var')
        ret = decl.safe_add_to(SConsArguments.VAR, var)
        try:
            decl.add_to.assert_not_called()
        except AssertionError as e:
            self.fail(str(e))
        self.assertFalse(ret)

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_safe_add_to__OPT_0(self):
        """_ArgumentDeclaration().safe_add_to(OPT) should not call <_ArgumentDeclaration>.add_to()"""
        decl = SConsArguments.Declaration._ArgumentDeclaration()
        decl.add_to = mock.Mock(name = 'add_to')
        ret = decl.safe_add_to(SConsArguments.OPT)
        try:
            decl.add_to.assert_not_called()
        except AssertionError as e:
            self.fail(str(e))
        self.assertFalse(ret)

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_safe_add_to__ENV_1(self):
        """_ArgumentDeclaration(env_decl = 'FOO').safe_add_to(ENV,env) should call <_ArgumentDeclaration>.add_to(ENV,env)"""
        decl = SConsArguments.Declaration._ArgumentDeclaration(env_decl = 'FOO')
        decl.add_to = mock.Mock(name = 'add_to')
        env = mock.Mock(name = 'env')
        ret = decl.safe_add_to(SConsArguments.ENV, env)
        try:
            decl.add_to.assert_called_once_with(SConsArguments.ENV,env)
        except AssertionError as e:
            self.fail(str(e))
        self.assertTrue(ret)

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_safe_add_to__VAR_1(self):
        """_ArgumentDeclaration(var_decl = ('FOO',)).safe_add_to(VAR,var) should call <_ArgumentDeclaration>.add_to(VAR,var)"""
        decl = SConsArguments.Declaration._ArgumentDeclaration(var_decl = ('FOO',))
        decl.add_to = mock.Mock(name = 'add_to')
        var = mock.Mock(name = 'var')
        ret = decl.safe_add_to(SConsArguments.VAR, var)
        try:
            decl.add_to.assert_called_once_with(SConsArguments.VAR, var)
        except AssertionError as e:
            self.fail(str(e))
        self.assertTrue(ret)

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_safe_add_to__OPT_1(self):
        """_ArgumentDeclaration(opt_decl = ('--foo', {'dest' : 'FOO'})).safe_add_to(OPT) should call <_ArgumentDeclaration>.add_to(OPT)"""
        decl = SConsArguments.Declaration._ArgumentDeclaration(opt_decl = ('--foo', {'dest' : 'FOO'}))
        decl.add_to = mock.Mock(name = 'add_to')
        ret = decl.safe_add_to(SConsArguments.OPT)
        try:
            decl.add_to.assert_called_once_with(SConsArguments.OPT)
        except AssertionError as e:
            self.fail(str(e))
        self.assertTrue(ret)

#############################################################################
class Test_ArgumentDeclaration(unittest.TestCase):
    def test_gvar_decl_1(self):
        """ArgumentDeclaration() should be an instance of SConsArguments.Declaration._ArgumentDeclaration()"""
        self.assertIsInstance(SConsArguments.Declaration.ArgumentDeclaration(), SConsArguments.Declaration._ArgumentDeclaration)
    def test_gvar_decl_2(self):
        """if decl = ArgumentDeclaration() then ArgumentDeclaration(decl) should be decl"""
        decl = SConsArguments.Declaration.ArgumentDeclaration()
        self.assertIs(SConsArguments.Declaration.ArgumentDeclaration(decl), decl)
    def test_gvar_decl_3(self):
        """ArgumentDeclaration() should not be same as ArgumentDeclaration()"""
        self.assertIsNot(SConsArguments.Declaration.ArgumentDeclaration(), SConsArguments.Declaration.ArgumentDeclaration())

    def test_user_doc_example_1(self):
        """example 1 from user documentation should work"""
        decl = SConsArguments.Declaration.ArgumentDeclaration( {'xvar' : None}, None, ('--xvar', {'dest' : 'xvar', 'type' : 'string'}) )
        self.assertIsInstance(decl, SConsArguments.Declaration._ArgumentDeclaration)

#############################################################################
class Test_DeclareArgument(unittest.TestCase):
    def test_DeclareArgument_1(self):
        """DeclareArgument(<_ArgumentDeclaration>) should return same <_ArgumentDeclaration> object"""
        decl1 = SConsArguments.Declaration._ArgumentDeclaration()
        decl2 = SConsArguments.DeclareArgument(decl1)
        self.assertIs(decl2, decl1)

    def test_user_doc_example_2(self):
        """example 2 from user documentation should work"""
        decl = SConsArguments.DeclareArgument(env_key = 'xvar', opt_key = 'xvar', option = '--xvar', type = 'string')
        self.assertIsInstance(decl, SConsArguments.Declaration._ArgumentDeclaration)

#############################################################################
if __name__ == "__main__":
    ldr = unittest.TestLoader()
    suite = unittest.TestSuite()
    # Load tests to test suite
    tclasses = [ Test_module_constants
               , Test_Transformer
               , Test__resubst
               , Test__build_resubst_dict
               , Test__build_iresubst_dict
               , Test__compose_mappings
               , Test__invert_dict
##               , Test__ArgumentsProxy
               , Test__VariablesWrapper
               , Test__ArgumentDeclaration
               , Test_ArgumentDeclaration
               , Test_DeclareArgument
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
