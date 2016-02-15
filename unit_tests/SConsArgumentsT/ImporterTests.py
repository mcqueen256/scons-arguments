""" `SConsArgumentsT.ImporterTests`

Unit tests for SConsArguments.Importer
"""

__docformat__ = "restructuredText"

#
# Copyright (c) 2015-2016 by Pawel Tomulik
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

import SConsArguments.Importer as tested
import SConsArguments.Declaration
import SConsArguments.Declarations
import SCons.Tool
import importlib
import sys
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
class Test_GetDefaultArgpath(unittest.TestCase):
    def test_GetDefaultArgpath_0(self):
        """Test SConsArguments.Importer.GetDefaultArgpath()"""
        tested._defaultArgpath = None
        self.assertIsInstance(tested.GetDefaultArgpath(), list)

    def test_GetDefaultArgpath_1(self):
        """Test SConsArguments.Importer.GetDefaultArgpath()"""
        tested._defaultArgpath = 'asd'
        self.assertEqual(tested.GetDefaultArgpath(), 'asd')

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_GetDefaultArgpath_2(self):
        """Test SConsArguments.Importer.GetDefaultArgpath() using mocks"""
        with mock.patch('SCons.Tool.DefaultToolpath', new = [ 'foo', 'bar/site_tools', 'geez/site_tools/droom' ]), \
             mock.patch('SConsArguments.Importer._initDefaultArgpath', side_effect = tested._initDefaultArgpath) as init_mock:
            tested._defaultArgpath = None
            self.assertEqual(tested.GetDefaultArgpath(),[])
            self.assertTrue(init_mock.called)

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_GetDefaultArgpath_3(self):
        """Test SConsArguments.Importer.GetDefaultArgpath() using mocks"""
        with mock.patch('SConsArguments.Importer._initDefaultArgpath', side_effect = tested._initDefaultArgpath) as init_mock:
            tested._defaultArgpath = ['foo', 'bar']
            self.assertEqual(tested.GetDefaultArgpath(), ['foo', 'bar'])
            self.assertFalse(init_mock.called)

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_GetDefaultArgpath_4(self):
        """Test SConsArguments.Importer.GetDefaultArgpath() using mocks"""
        with mock.patch('SCons.Tool.DefaultToolpath', new = [ 'foo/site_tools', 'bar/site_tools', 'geez/bleah' ]), \
             mock.patch('SConsArguments.Importer._initDefaultArgpath', side_effect = tested._initDefaultArgpath) as init_mock, \
             mock.patch('os.path.exists', side_effect = lambda x : (x in (['bar/site_arguments', 'geez/bleah'])) ):
            tested._defaultArgpath = None
            self.assertEqual(tested.GetDefaultArgpath(), ['bar/site_arguments', 'geez/bleah'])
            self.assertTrue(init_mock.called)


#############################################################################
class Test__load_dict_decl(unittest.TestCase):
    def test__load_dict_decl_1(self):
        """Test SConsArguments.Importer._load_dict_decl('foo',{})"""
        decl = tested._load_dict_decl('foo',{})
        xpct = { 'env_key' : 'foo', 'var_key' : 'foo' }
        self.assertEqual(xpct, decl)

    def test__load_dict_decl_2(self):
        """Test SConsArguments.Importer._load_dict_decl('foo',{'help' :'Argument foo'})"""
        decl = tested._load_dict_decl('foo',{'help' : 'Argument foo'})
        xpct = { 'env_key' : 'foo', 'var_key' : 'foo', 'help' : 'Argument foo' }
        self.assertEqual(xpct, decl)

    def test__load_dict_decl_3(self):
        """Test SConsArguments.Importer._load_dict_decl('foo',{'help' : 'Argument foo'}, nameconv = nc)"""
        nc =  tested._ArgumentNameConv()
        decl = tested._load_dict_decl('foo',{'help' : 'Argument foo'}, nameconv = nc)
        xpct = { 'env_key' : 'foo', 'var_key' : 'foo', 'opt_key' : 'foo', 'option' : '--foo', 'help' : 'Argument foo' }
        self.assertEqual(xpct, decl)
        #
        nc =  tested._ArgumentNameConv(env_key_prefix = 'env_', var_key_prefix = 'var_', opt_key_prefix = 'opt_')
        decl = tested._load_dict_decl('foo',{'help' : 'Argument foo'}, nameconv = nc)
        xpct = { 'env_key' : 'env_foo', 'var_key' : 'var_foo', 'opt_key' : 'opt_foo', 'option' : '--foo', 'help' : 'Argument foo' }
        self.assertEqual(xpct, decl)
        # NameConv shall override some entries preset in decli...
        nc =  tested._ArgumentNameConv(env_key_prefix = 'env_', var_key_prefix = 'var_', opt_key_prefix = 'opt_')
        decli = { 'env_key' : 'foo_env', 'var_key' : 'foo_var', 'opt_key' : 'foo_opt', 'help' : 'Argument foo'}
        declo = tested._load_dict_decl('foo', decli, nameconv = nc)
        xpct = { 'env_key' : 'env_foo', 'var_key' : 'var_foo', 'opt_key' : 'opt_foo', 'option' : '--foo', 'help' : 'Argument foo' }
        self.assertEqual(xpct, declo)

    def test__load_dict_decl_4(self):
        """Test SConsArguments.Importer._load_dict_decl('foo', decli)"""
        decli = {'env_key' : 'env_foo', 'var_key' : 'var_foo', 'opt_key' : 'opt_foo', 'option' : '--option-foo'}
        declo = tested._load_dict_decl('foo', decli)
        self.assertEqual(decli, declo)

    def test__load_dict_decl_5(self):
        """Test SConsArguments.Importer._load_dict_decl('foo', decli, nameconv = nc)"""
        nc =  tested._ArgumentNameConv()
        decli = {'env_key' : 'env_foo', 'var_key' : 'var_foo', 'opt_key' : 'opt_foo', 'option' : '--option-foo'}
        declo = tested._load_dict_decl('foo', decli, nameconv = nc)
        xpct =  {'env_key' : 'foo', 'var_key' : 'foo', 'opt_key' : 'foo', 'option' : '--foo'}
        self.assertEqual(xpct, declo)

    def test__load_dict_decl_6(self):
        """Test SConsArguments.Importer._load_dict_decl('foo', decli, env_key_transform = True)"""
        decli = {'env_key' : 'env_foo', 'var_key' : 'var_foo', 'opt_key' : 'opt_foo', 'option' : '--option-foo'}
        declo = tested._load_dict_decl('foo', decli, env_key_transform = True)
        xpct = {'env_key' : 'env_foo', 'var_key' : 'var_foo', 'opt_key' : 'opt_foo', 'option' : '--option-foo'}
        self.assertEqual(xpct, declo)
        #
        decli = {'var_key' : 'var_foo', 'opt_key' : 'opt_foo', 'option' : '--option-foo'}
        declo = tested._load_dict_decl('foo', decli, env_key_transform = True)
        xpct = {'env_key' : 'foo', 'var_key' : 'var_foo', 'opt_key' : 'opt_foo', 'option' : '--option-foo'}
        self.assertEqual(xpct, declo)

    def test__load_dict_decl_7(self):
        """Test SConsArguments.Importer._load_dict_decl('foo', decli, var_key_transform = True)"""
        decli = {'env_key' : 'env_foo', 'var_key' : 'var_foo', 'opt_key' : 'opt_foo', 'option' : '--option-foo'}
        declo = tested._load_dict_decl('foo', decli, var_key_transform = True)
        xpct = {'env_key' : 'env_foo', 'var_key' : 'var_foo', 'opt_key' : 'opt_foo', 'option' : '--option-foo'}
        self.assertEqual(xpct, declo)
        #
        decli = {'env_key' : 'env_foo', 'opt_key' : 'opt_foo', 'option' : '--option-foo'}
        declo = tested._load_dict_decl('foo', decli, var_key_transform = True)
        xpct = {'env_key' : 'env_foo', 'var_key' : 'foo', 'opt_key' : 'opt_foo', 'option' : '--option-foo'}
        self.assertEqual(xpct, declo)

    def test__load_dict_decl_8(self):
        """Test SConsArguments.Importer._load_dict_decl('foo', decli, opt_key_transform = True)"""
        decli = {'env_key' : 'env_foo', 'var_key' : 'var_foo', 'opt_key' : 'opt_foo', 'option' : '--option-foo'}
        declo = tested._load_dict_decl('foo', decli, opt_key_transform = True)
        xpct = {'env_key' : 'env_foo', 'var_key' : 'var_foo', 'opt_key' : 'opt_foo', 'option' : '--option-foo'}
        self.assertEqual(xpct, declo)
        #
        decli = {'env_key' : 'env_foo', 'var_key' : 'var_foo', 'option' : '--option-foo'}
        declo = tested._load_dict_decl('foo', decli, opt_key_transform = True)
        xpct = {'env_key' : 'env_foo', 'var_key' : 'var_foo', 'opt_key' : 'foo', 'option' : '--option-foo'}
        self.assertEqual(xpct, declo)

    def test__load_dict_decl_9(self):
        """Test SConsArguments.Importer._load_dict_decl('foo', decli, option_transform = True)"""
        decli = {'env_key' : 'env_foo', 'var_key' : 'var_foo', 'opt_key' : 'opt_foo', 'option' : '--option-foo'}
        declo = tested._load_dict_decl('foo', decli, option_transform = True)
        xpct = {'env_key' : 'env_foo', 'var_key' : 'var_foo', 'opt_key' : 'opt_foo', 'option' : '--option-foo'}
        self.assertEqual(xpct, declo)
        #
        decli = {'env_key' : 'env_foo', 'var_key' : 'var_foo', 'opt_key' : 'opt_foo'}
        declo = tested._load_dict_decl('foo', decli, option_transform = True)
        xpct = {'env_key' : 'env_foo', 'var_key' : 'var_foo', 'opt_key' : 'opt_foo', 'option' : '--foo'}
        self.assertEqual(xpct, declo)

    def test__load_dict_decl_10(self):
        """Test SConsArguments.Importer._load_dict_decl('foo', decli, env_key_transform = False)"""
        decli = {'env_key' : 'env_foo', 'var_key' : 'var_foo', 'opt_key' : 'opt_foo', 'option' : '--option-foo'}
        declo = tested._load_dict_decl('foo', decli, env_key_transform = False)
        xpct = {'env_key' : 'env_foo', 'var_key' : 'var_foo', 'opt_key' : 'opt_foo', 'option' : '--option-foo'}
        self.assertEqual(xpct, declo)
        #
        decli = {'var_key' : 'var_foo', 'opt_key' : 'opt_foo', 'option' : '--option-foo'}
        declo = tested._load_dict_decl('foo', decli, env_key_transform = False)
        xpct = {'var_key' : 'var_foo', 'opt_key' : 'opt_foo', 'option' : '--option-foo'}
        self.assertEqual(xpct, declo)

    def test__load_dict_decl_11(self):
        """Test SConsArguments.Importer._load_dict_decl('foo', decli, var_key_transform = False)"""
        decli = {'env_key' : 'env_foo', 'var_key' : 'var_foo', 'opt_key' : 'opt_foo', 'option' : '--option-foo'}
        declo = tested._load_dict_decl('foo', decli, var_key_transform = False)
        xpct = {'env_key' : 'env_foo', 'var_key' : 'var_foo', 'opt_key' : 'opt_foo', 'option' : '--option-foo'}
        self.assertEqual(xpct, declo)
        #
        decli = {'env_key' : 'env_foo', 'opt_key' : 'opt_foo', 'option' : '--option-foo'}
        declo = tested._load_dict_decl('foo', decli, var_key_transform = False)
        xpct = {'env_key' : 'env_foo', 'opt_key' : 'opt_foo', 'option' : '--option-foo'}
        self.assertEqual(xpct, declo)

    def test__load_dict_decl_12(self):
        """Test SConsArguments.Importer._load_dict_decl('foo', decli, opt_key_transform = False)"""
        decli = {'env_key' : 'env_foo', 'var_key' : 'var_foo', 'opt_key' : 'opt_foo', 'option' : '--option-foo'}
        declo = tested._load_dict_decl('foo', decli, opt_key_transform = False)
        xpct = {'env_key' : 'env_foo', 'var_key' : 'var_foo', 'opt_key' : 'opt_foo', 'option' : '--option-foo'}
        self.assertEqual(xpct, declo)
        #
        decli = {'env_key' : 'env_foo', 'var_key' : 'var_foo', 'option' : '--option-foo'}
        declo = tested._load_dict_decl('foo', decli, opt_key_transform = False)
        xpct = {'env_key' : 'env_foo', 'var_key' : 'var_foo', 'option' : '--option-foo'}
        self.assertEqual(xpct, declo)

    def test__load_dict_decl_13(self):
        """Test SConsArguments.Importer._load_dict_decl('foo', decli, option_transform = False)"""
        decli = {'env_key' : 'env_foo', 'var_key' : 'var_foo', 'opt_key' : 'opt_foo', 'option' : '--option-foo'}
        declo = tested._load_dict_decl('foo', decli, option_transform = False)
        xpct = {'env_key' : 'env_foo', 'var_key' : 'var_foo', 'opt_key' : 'opt_foo', 'option' : '--option-foo'}
        self.assertEqual(xpct, declo)
        #
        decli = {'env_key' : 'env_foo', 'var_key' : 'var_foo', 'opt_key' : 'opt_foo'}
        declo = tested._load_dict_decl('foo', decli, option_transform = False)
        xpct = {'env_key' : 'env_foo', 'var_key' : 'var_foo', 'opt_key' : 'opt_foo'}
        self.assertEqual(xpct, declo)

    def test__load_dict_decl_14(self):
        """Test SConsArguments.Importer._load_dict_decl('foo', {}, nameconv = 'bleah')"""
        with self.assertRaisesRegexp(TypeError, "The nameconv must be an instance of _ArgumentNameConv, not %r" % 'bleah'):
            tested._load_dict_decl('foo', {}, nameconv = 'bleah')

#############################################################################
class Test__load_decl(unittest.TestCase):
    def test__load_decl_0(self):
        """Test _load_decl('foo', 'bleah') raises an exception"""
        with self.assertRaisesRegexp(TypeError, "Unsupported decl type"):
            tested._load_decl('foo', 'bleah')

    def test__load_decl__dict_1(self):
        """Test _load_decl('foo', {'help' : 'This is foo'})"""
        declo = tested._load_decl('foo', {'help' : 'This is foo'})
        self.assertIsInstance(declo, SConsArguments.Declaration._ArgumentDeclaration)
        self.assertEqual(declo.get_var_decl()['help'], 'This is foo')

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test__load_decl__dict_2(self):
        """Test _load_decl('foo', {'help' : 'This is foo'}) using mocks"""
        with mock.patch('SConsArguments.Importer.DeclareArgument', side_effect = SConsArguments.Declaration.DeclareArgument) as mock_DeclareArgument, \
             mock.patch('SConsArguments.Importer._load_dict_decl', side_effect = tested._load_dict_decl) as mock_load_dict_decl:
            tested._load_decl('foo', {'help' : 'This is foo'})
            mock_load_dict_decl.assert_called_once_with('foo', {'help' : 'This is foo'})
            mock_DeclareArgument.assert_called_once_with(env_key='foo', help='This is foo', var_key='foo')

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test__load_decl__dict_3(self):
        """Test _load_decl('foo', {'help' : 'This is foo'}, preprocessor = ...) using mocks"""
        with mock.patch('SConsArguments.Importer.DeclareArgument', side_effect = SConsArguments.Declaration.DeclareArgument) as mock_DeclareArgument, \
             mock.patch('SConsArguments.Importer._load_dict_decl', side_effect = tested._load_dict_decl) as mock_load_dict_decl:
            tested._load_decl('foo', {'help' : 'This is foo'}, preprocessor = lambda x : dict(x.items() + {'env_key' : 'env_foo'}.items()))
            mock_load_dict_decl.assert_called_once_with('foo', {'help' : 'This is foo', 'env_key' : 'env_foo'})
            mock_DeclareArgument.assert_called_once_with(env_key='env_foo', help='This is foo', var_key='foo')

#############################################################################
class Test__load_decls(unittest.TestCase):
    def test__load_decls_1(self):
        """SConsArguments.Importer._load_decls('foo') should raise TypeError"""
        with self.assertRaisesRegexp(TypeError, "Can not load arguments from %r object" % type('foo')):
            tested._load_decls('foo')

    def test__load_decls_2(self):
        """Test SConsArguments.Importer._load_decls({'arg1' : {...}})"""
        declo = tested._load_decls({ 'arg1' : {'help' : 'This is arg1'}, 'arg2' : {'help' : 'This is arg2' }})
        self.assertIsInstance(declo, SConsArguments.Declarations._ArgumentDeclarations)
        self.assertEqual(declo['arg1'].get_var_decl()['help'], 'This is arg1')
        self.assertEqual(declo['arg2'].get_var_decl()['help'], 'This is arg2')

    def test__load_decls_3(self):
        """Test SConsArguments.Importer._load_decls({'arg1' : {...}}, name_filter = lambda x : ...)"""
        declo = tested._load_decls({ 'arg1' : {'help' : 'This is arg1'}, 'arg2' : {'help' : 'This is arg2' }}, name_filter = lambda x : (x == 'arg1'))
        self.assertIsInstance(declo, SConsArguments.Declarations._ArgumentDeclarations)
        self.assertEqual(declo['arg1'].get_var_decl()['help'], 'This is arg1')
        self.assertFalse('arg2' in declo)

    def test__load_decls_4(self):
        """Test SConsArguments.Importer._load_decls({'arg1' : {...}}, name_filter = [...])"""
        decli = { 'arg1' : {'help' : 'This is arg1'}, 'arg2' : {'help' : 'This is arg2' } }
        declo = tested._load_decls(decli, name_filter = ['arg1','foo'])
        self.assertIsInstance(declo, SConsArguments.Declarations._ArgumentDeclarations)
        self.assertEqual(declo['arg1'].get_var_decl()['help'], 'This is arg1')
        self.assertFalse('arg2' in declo)

    def test__load_decls_5(self):
        """Test SConsArguments.Importer._load_decls({'arg1' : {...}}, name_filter = (...,))"""
        decli = { 'arg1' : {'help' : 'This is arg1'}, 'arg2' : {'help' : 'This is arg2' } }
        declo = tested._load_decls(decli, name_filter = ('arg1','foo'))
        self.assertIsInstance(declo, SConsArguments.Declarations._ArgumentDeclarations)
        self.assertEqual(declo['arg1'].get_var_decl()['help'], 'This is arg1')
        self.assertFalse('arg2' in declo)

    def test__load_decls_6(self):
        """Test SConsArguments.Importer._load_decls({'arg1' : {...}}, name_filter = set(...))"""
        decli = { 'arg1' : {'help' : 'This is arg1'}, 'arg2' : {'help' : 'This is arg2' } }
        declo = tested._load_decls(decli, name_filter = {'arg1','foo'})
        self.assertIsInstance(declo, SConsArguments.Declarations._ArgumentDeclarations)
        self.assertEqual(declo['arg1'].get_var_decl()['help'], 'This is arg1')
        self.assertFalse('arg2' in declo)

#############################################################################
class Test__import_argmod(unittest.TestCase):
    def test__import_argmod_1(self):
        """Test SConsArguments.Importer._import_argmod(sys)"""
        oldpath = sys.path
        mod = tested._import_argmod(sys)
        self.assertEqual(mod, sys)

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test__import_argmod_2(self):
        """Test SConsArguments.Importer._import_argmod('foo')"""
        with mock.patch('SConsArguments.Importer.GetDefaultArgpath',) as mock_GetDefaultArgpath, \
             mock.patch('importlib.import_module') as mock_import_module:
            mock_GetDefaultArgpath.return_value = ['site_scons/site_arguments']
            mock_import_module.return_value = 'xyz'
            oldpath = sys.path
            mod = tested._import_argmod('foo')
            self.assertEqual(mod, 'xyz')
            self.assertEqual(sys.path, oldpath)

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test__import_argmod_3(self):
        """Test SConsArguments.Importer._import_argmod('foo')"""
        with mock.patch('SConsArguments.Importer.GetDefaultArgpath') as mock_GetDefaultArgpath, \
             mock.patch('importlib.import_module') as mock_import_module:
            mock_GetDefaultArgpath.return_value = ['site_scons/site_arguments']
            mock_import_module.side_effect = ImportError
            oldpath = sys.path
            with self.assertRaisesRegexp(RuntimeError, "No module named %s :" % 'foo'):
                tested._import_argmod('foo')
            self.assertEqual(sys.path, oldpath)

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test__import_argmod_4(self):
        """Test SConsArguments.Importer._import_argmod(...)"""
        def fake_import_module(modname):
            if modname == 'SConsArguments.foo':
                return 'SConsArguments.foo'
            else:
                raise ImportError("bleah")
        with mock.patch('SConsArguments.Importer.GetDefaultArgpath') as mock_GetDefaultArgpath, \
             mock.patch('importlib.import_module') as mock_import_module:
            mock_GetDefaultArgpath.return_value = ['site_scons/site_arguments']
            mock_import_module.side_effect = fake_import_module
            oldpath = sys.path
            with self.assertRaisesRegexp(RuntimeError, "No module named %s : %s" % ('bar', 'bleah')):
                tested._import_argmod('bar')
            self.assertEqual(sys.path, oldpath)
            oldpath = sys.path
            self.assertEqual(tested._import_argmod('foo'), 'SConsArguments.foo')
            self.assertEqual(sys.path, oldpath)

    def test__import_argmod_5(self):
        """Test SConsArguments.Importer._import_argmod('Declaration')"""
        self.assertEqual(tested._import_argmod('Declarations'), SConsArguments.Declarations)

#############################################################################
class Test_ImportArguments(unittest.TestCase):
    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_ImportArguments_1(self):
        """Test ImportArguments()"""
        with mock.patch('SConsArguments.Importer._import_argmod') as mock_import_argmod, \
             mock.patch('SConsArguments.Importer._load_decls', side_effect = tested._load_decls) as mock_load_decls:
            mock_mod = mock.MagicMock()
            mock_mod.arguments = mock.MagicMock()
            mock_mod.arguments.return_value = {'arg1' : {'help' : 'This is arg1'}}
            mock_import_argmod.return_value = mock_mod
            declo = tested.ImportArguments('foomod')
            self.assertEqual(declo['arg1'].get_var_decl()['help'], 'This is arg1')
            mock_import_argmod.assert_called_once_with('foomod', None)
            mock_load_decls.assert_called_once_with({'arg1' : {'help' : 'This is arg1'}})
            mock_mod.arguments.assert_called_once_with()

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_ImportArguments_2(self):
        """Test ImportArguments()"""
        with mock.patch('SConsArguments.Importer._import_argmod') as mock_import_argmod, \
             mock.patch('SConsArguments.Importer._load_decls', side_effect = tested._load_decls) as mock_load_decls:
            mock_mod = mock.MagicMock()
            mock_mod.arguments = mock.MagicMock()
            mock_mod.arguments.return_value = {'arg1' : {'help' : 'This is arg1'}}
            mock_import_argmod.return_value = mock_mod
            declo = tested.ImportArguments('foomod', ['foo/bar'], {'foo' : 'FOO'}, name_filter = ['arg1','baaz'])
            self.assertEqual(declo['arg1'].get_var_decl()['help'], 'This is arg1')
            mock_import_argmod.assert_called_once_with('foomod', ['foo/bar'])
            mock_load_decls.assert_called_once_with({'arg1' : {'help' : 'This is arg1'}}, name_filter = ['arg1', 'baaz'])
            mock_mod.arguments.assert_called_once_with(foo = 'FOO')



#############################################################################
if __name__ == "__main__":
    ldr = unittest.TestLoader()
    suite = unittest.TestSuite()
    # Load tests to test suite
    tclasses = [ Test_GetDefaultArgpath
               , Test__load_dict_decl
               , Test__load_decl
               , Test__load_decls
               , Test__import_argmod
               , Test_ImportArguments
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
