""" `SConsArgumentsT.ImporterTests`

Unit tests for `SConsArguments.Importer`
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
import SCons.Script.Main
import SCons.Node.FS
import SCons.Platform
import contextlib
import sys
import unittest
import os.path

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
class Test__load_module_file(unittest.TestCase):
    @unittest.skipIf(_mock_missing, "requires mock module")
    @unittest.skipIf(sys.version_info >= (3,4), "only for py < 3.4")
    def test__load_module_file_py27(self):
        "Test SConsArguments.Importer._load_module_file() with python 2.7"
        m_file = mock.MagicMock()
        with mock.patch('sys.version_info', new = (2,7)), \
             mock.patch('imp.find_module', return_value = (m_file, 'p', 'd')) as m_find_module, \
             mock.patch('imp.load_module', return_value = 'mod') as m_load_module:
            self.assertEqual(tested._load_module_file('mymod', 'my/path'), 'mod')
            m_find_module.assert_called_once_with('mymod', 'my/path')
            m_load_module.assert_called_once_with('mymod', m_file, 'p', 'd')
            m_file.close.assert_called_once_with()

    @unittest.skipIf(_mock_missing, "requires mock module")
    @unittest.skipIf(sys.version_info >= (3,4), "only for py < 3.4")
    def test__load_module_file_py33(self):
        "Test SConsArguments.Importer._load_module_file() with python 3.3"
        m_file = mock.MagicMock()
        with mock.patch('sys.version_info', new = (3,3)), \
             mock.patch('imp.find_module', return_value = (m_file, 'p', 'd')) as m_find_module, \
             mock.patch('imp.load_module', return_value = 'mod') as m_load_module:
            self.assertEqual(tested._load_module_file('mymod', 'my/path'), 'mod')
            m_find_module.assert_called_once_with('mymod', 'my/path')
            m_load_module.assert_called_once_with('mymod', m_file, 'p', 'd')
            m_file.close.assert_called_once_with()

    @unittest.skipIf(_mock_missing, "requires mock module")
    @unittest.skipIf(sys.version_info < (3,4), "only for py >= 3.4")
    def test__load_module_file_py34(self):
        "Test SConsArguments.Importer._load_module_file() with python 3.4"

        find_spec0 = mock.MagicMock(return_value = None)
        finder0 = mock.MagicMock(find_spec = find_spec0, loader = mock.MagicMock())

        spec1 = mock.MagicMock(loader = mock.MagicMock(), __str__ = 'spec1')
        find_spec1 = mock.MagicMock(return_value = spec1)
        finder1 = mock.MagicMock(find_spec = find_spec1)

        with mock.patch('sys.version_info', new = (3,4)), \
             mock.patch('sys.meta_path', new = [ finder0, finder1, finder0 ]), \
             mock.patch('importlib.util.module_from_spec', side_effect = lambda x : 'mod_%s' % x) as m_module_from_spec:
            self.assertEqual(tested._load_module_file('mymod', 'my/path'), 'mod_spec1')
            m_module_from_spec.assert_called_once_with('spec1')
            finder1.loader.exec_module.assert_called_once_with('mod_spec1')

#############################################################################
class Test__handle_site_scons_dir(unittest.TestCase):
    @unittest.skipIf(_mock_missing, "requires mock module")
    def test__handle_site_scons_dir_1(self):
        """Test SConsArguments.Importer._handle_site_scons_dir()"""
        with mock.patch('os.path.exists', return_value = False):
            tested._defaultArgpath = ['initial']
            tested._handle_site_scons_dir('top/dir')
            self.assertEqual(tested._defaultArgpath, ['initial'])

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test__handle_site_scons_dir_2(self):
        """Test SConsArguments.Importer._handle_site_scons_dir()"""
        with mock.patch('os.path.exists', return_value = True):
            tested._defaultArgpath = ['initial']
            tested._handle_site_scons_dir('top/dir')
            self.assertEqual(tested._defaultArgpath, [os.path.abspath('top/dir/site_scons/site_arguments'), 'initial'])

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test__handle_site_scons_dir_3(self):
        """Test SConsArguments.Importer._handle_site_scons_dir()"""
        with mock.patch('os.path.exists', return_value = True):
            tested._defaultArgpath = ['initial']
            tested._handle_site_scons_dir('top/dir', 'mysite')
            self.assertEqual(tested._defaultArgpath, [os.path.abspath('top/dir/mysite/site_arguments'), 'initial'])

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test__handle_site_scons_dir_4(self):
        """Test SConsArguments.Importer._handle_site_scons_dir()"""
        with mock.patch('os.path.exists', return_value = False), \
             mock.patch('os.path.join', side_effect = lambda *args : '/'.join(args)):
            with self.assertRaisesRegexp(SCons.Errors.UserError, "site dir top/dir/mysite not found"):
                tested._defaultArgpath = ['initial']
                tested._handle_site_scons_dir('top/dir', 'mysite')

#############################################################################
class Test__handle_all_site_scons_dirs(unittest.TestCase):
    def fakeEnv(self, platform):
        if platform == 'win32' or platform == 'cygwin':
            return { '$ALLUSERSPROFILE' : 'C:\\ProgramData',
                     '$USERPROFILE' : 'C:\\Users\\ptomulik',
                     '$APPDATA' : 'C:\\Users\\ptomulik\\AppData' }
        else:
            return dict()


    def expandvars(self, platform, arg):
        env = self.fakeEnv(platform)
        for (key,val) in env.items():
            arg = arg.replace(key, val)
        return arg

    def expanduser(self, platform, arg):
        if platform == 'win32':
            arg = arg.replace('~/', 'C:\\Users\\ptomulik\\home\\')
        else:
            arg = arg.replace('~/', '/home/ptomulik/')
        return arg

    def pathjoin(self, platform, *args):
        if platform == 'win32':
            return '\\'.join(args)
        else:
            return '/'.join(args)


    @unittest.skipIf(_mock_missing, "requires mock module")
    def test__handle_all_site_scons_dirs_win32(self):

        _defaultArgpath = []

        def _handle_site_scons_dir(topdir):
            _defaultArgpath.insert(0, os.path.join(topdir, 'site_scons', 'site_arguments'))

        env = self.fakeEnv('win32')
        with mock.patch('SCons.Platform.platform_default', return_value='win32'), \
             mock.patch('os.path.expandvars', side_effect = lambda x : self.expandvars('win32', x)), \
             mock.patch('os.path.expanduser', side_effect = lambda x : self.expanduser('win32', x)), \
             mock.patch('os.path.join', side_effect = lambda *x : self.pathjoin('win32', *x)), \
             mock.patch('SConsArguments.Importer._handle_site_scons_dir', side_effect = _handle_site_scons_dir):

            tested._handle_all_site_scons_dirs('C:\\Users\\ptomulik\\foo')
            self.assertEqual(_defaultArgpath, [
                'C:\\Users\\ptomulik\\foo\\site_scons\\site_arguments',
                'C:\\Users\\ptomulik\\home\\.scons\\site_scons\\site_arguments',
                '%s\\scons\\site_scons\\site_arguments' % env['$APPDATA'],
                '%s\\Local Settings\\Application Data\\scons\\site_scons\\site_arguments' % env['$USERPROFILE'],
                '%s\\Application Data\\scons\\site_scons\\site_arguments' % env['$ALLUSERSPROFILE']
             ])

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test__handle_all_site_scons_dirs_darwin(self):

        _defaultArgpath = []

        def _handle_site_scons_dir(topdir):
            _defaultArgpath.insert(0, os.path.join(topdir, 'site_scons', 'site_arguments'))

        env = self.fakeEnv('darwin')
        with mock.patch('SCons.Platform.platform_default', return_value='darwin'), \
             mock.patch('os.path.expandvars', side_effect = lambda x : self.expandvars('darwin', x)), \
             mock.patch('os.path.expanduser', side_effect = lambda x : self.expanduser('darwin', x)), \
             mock.patch('os.path.join', side_effect = lambda *x : self.pathjoin('darwin', *x)), \
             mock.patch('SConsArguments.Importer._handle_site_scons_dir', side_effect = _handle_site_scons_dir):

            tested._handle_all_site_scons_dirs('/home/ptomulik/foo')
            self.assertEqual(_defaultArgpath, [
                '/home/ptomulik/foo/site_scons/site_arguments',
                '/home/ptomulik/.scons/site_scons/site_arguments',
                '/home/ptomulik/Library/Application Support/SCons/site_scons/site_arguments',
                '/sw/share/scons/site_scons/site_arguments',
                '/opt/local/share/scons/site_scons/site_arguments',
                '/Library/Application Support/SCons/site_scons/site_arguments'
             ])

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test__handle_all_site_scons_dirs_sunos(self):

        _defaultArgpath = []

        def _handle_site_scons_dir(topdir):
            _defaultArgpath.insert(0, os.path.join(topdir, 'site_scons', 'site_arguments'))

        env = self.fakeEnv('sunos')
        with mock.patch('SCons.Platform.platform_default', return_value='sunos'), \
             mock.patch('os.path.expandvars', side_effect = lambda x : self.expandvars('sunos', x)), \
             mock.patch('os.path.expanduser', side_effect = lambda x : self.expanduser('sunos', x)), \
             mock.patch('os.path.join', side_effect = lambda *x : self.pathjoin('sunos', *x)), \
             mock.patch('SConsArguments.Importer._handle_site_scons_dir', side_effect = _handle_site_scons_dir):

            tested._handle_all_site_scons_dirs('/home/ptomulik/foo')
            self.assertEqual(_defaultArgpath, [
                '/home/ptomulik/foo/site_scons/site_arguments',
                '/home/ptomulik/.scons/site_scons/site_arguments',
                '/usr/share/scons/site_scons/site_arguments',
                '/opt/sfw/scons/site_scons/site_arguments'
             ])

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test__handle_all_site_scons_dirs_other(self):

        _defaultArgpath = []

        def _handle_site_scons_dir(topdir):
            _defaultArgpath.insert(0, os.path.join(topdir, 'site_scons', 'site_arguments'))

        env = self.fakeEnv('other')
        with mock.patch('SCons.Platform.platform_default', return_value='other'), \
             mock.patch('os.path.expandvars', side_effect = lambda x : self.expandvars('other', x)), \
             mock.patch('os.path.expanduser', side_effect = lambda x : self.expanduser('other', x)), \
             mock.patch('os.path.join', side_effect = lambda *x : self.pathjoin('other', *x)), \
             mock.patch('SConsArguments.Importer._handle_site_scons_dir', side_effect = _handle_site_scons_dir):

            tested._handle_all_site_scons_dirs('/home/ptomulik/foo')
            self.assertEqual(_defaultArgpath, [
                '/home/ptomulik/foo/site_scons/site_arguments',
                '/home/ptomulik/.scons/site_scons/site_arguments',
                '/usr/share/scons/site_scons/site_arguments'
             ])


#############################################################################
class Test__initDefaultArgpath(unittest.TestCase):
    @contextlib.contextmanager
    def mocks1(self):
        with mock.MagicMock() as m:
            with mock.patch("SCons.Script.Main.GetOption") as m.GetOption, \
                 mock.patch("SCons.Node.FS.get_default_fs") as m.get_default_fs, \
                 mock.patch("SConsArguments.Importer._handle_site_scons_dir") as m._handle_site_scons_dir, \
                 mock.patch("SConsArguments.Importer._handle_all_site_scons_dirs") as m._handle_all_site_scons_dirs:

                m.get_abspath = mock.MagicMock(return_value = 'topdir/path')
                m.SConstruct_dir = mock.MagicMock(get_abspath = m.get_abspath)
                m.default_fs = mock.MagicMock(SConstruct_dir = m.SConstruct_dir)
                m.get_default_fs.return_value = m.default_fs

                yield m

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test__initDefaultArgpath_1(self):
        """Test SConsArguments.Importer._initDefaultArgpath()"""
        with self.mocks1() as m:

            m.GetOption.return_value = None

            tested._defaultArgpath = None
            tested._initDefaultArgpath()

            m._handle_site_scons_dir.assert_not_called()
            m._handle_all_site_scons_dirs.assert_called_once_with('topdir/path')

            self.assertIsInstance(tested._defaultArgpath, list)
            self.assertEqual(tested._defaultArgpath, [])

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test__initDefaultArgpath_2(self):
        """Test SConsArguments.Importer._initDefaultArgpath()"""
        def get_option(name):
            if name == 'no_site_dir':
                return True
            else:
                return None

        with self.mocks1() as m:

            m.GetOption.side_effect = get_option

            tested._defaultArgpath = None
            tested._initDefaultArgpath()

            m._handle_site_scons_dir.assert_not_called()
            m._handle_all_site_scons_dirs.assert_not_called()

            self.assertIsInstance(tested._defaultArgpath, list)
            self.assertEqual(tested._defaultArgpath, [])

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test__initDefaultArgpath_3(self):
        """Test SConsArguments.Importer._initDefaultArgpath()"""
        def get_option(name):
            if name == 'site_dir':
                return 'site_scons'
            else:
                return None

        def handle_dir(topdir, site_dir):
            tested._defaultArgpath.append(topdir + '/' + site_dir)

        with self.mocks1() as m:

            m.GetOption.side_effect = get_option
            m._handle_site_scons_dir.side_effect = handle_dir

            tested._defaultArgpath = None
            tested._initDefaultArgpath()

            m._handle_site_scons_dir.assert_called_once_with('topdir/path', 'site_scons')
            m._handle_all_site_scons_dirs.assert_not_called()

            self.assertIsInstance(tested._defaultArgpath, list)
            self.assertEqual(tested._defaultArgpath, ['topdir/path/site_scons'])

#############################################################################
class Test_GetDefaultArgpath(unittest.TestCase):
    def test_GetDefaultArgpath_1(self):
        """Test SConsArguments.Importer.GetDefaultArgpath()"""
        tested._defaultArgpath = 'asd'
        self.assertEqual(tested.GetDefaultArgpath(), 'asd')

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test_GetDefaultArgpath_2(self):
        """Test SConsArguments.Importer.GetDefaultArgpath() using mocks"""
        def init_argpath():
            tested._defaultArgpath = ['bar']
        with mock.patch('SConsArguments.Importer._initDefaultArgpath', side_effect = init_argpath) as m:
            tested._defaultArgpath = None
            self.assertEqual(tested.GetDefaultArgpath(),['bar'])
            m.assert_called_once_with()

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
             mock.patch('SConsArguments.Importer._load_module_file') as mock_load_module_file:
            mock_GetDefaultArgpath.return_value = ['site_scons/site_arguments']
            mock_load_module_file.return_value = 'xyz'
            oldpath = sys.path
            mod = tested._import_argmod('foo')
            self.assertEqual(mod, 'xyz')
            self.assertEqual(sys.path, oldpath)

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test__import_argmod_3(self):
        """Test SConsArguments.Importer._import_argmod('foo')"""
        with mock.patch('SConsArguments.Importer.GetDefaultArgpath') as mock_GetDefaultArgpath, \
             mock.patch('SConsArguments.Importer._load_module_file') as mock_load_module_file:
            mock_GetDefaultArgpath.return_value = ['site_scons/site_arguments']
            mock_load_module_file.side_effect = ImportError
            oldpath = sys.path
            with self.assertRaisesRegexp(RuntimeError, "No module named %s :" % 'foo'):
                tested._import_argmod('foo')
            self.assertEqual(sys.path, oldpath)

    @unittest.skipIf(_mock_missing, "requires mock module")
    def test__import_argmod_4(self):
        """Test SConsArguments.Importer._import_argmod(...)"""
        def fake_load_module_file(modname, path=None):
            if path == ['SConsArguments'] and modname == 'foo':
                return 'SConsArguments.foo'
            else:
                raise ImportError("bleah")
        with mock.patch('SConsArguments.Importer.GetDefaultArgpath') as mock_GetDefaultArgpath, \
             mock.patch('SConsArguments.Importer._load_module_file') as mock_load_module_file:
            mock_GetDefaultArgpath.return_value = ['site_scons/site_arguments']
            mock_load_module_file.side_effect = fake_load_module_file
            oldpath = sys.path
            with self.assertRaisesRegexp(RuntimeError, "No module named %s : %s" % ('bar', 'bleah')):
                tested._import_argmod('bar')
            self.assertEqual(sys.path, oldpath)
            oldpath = sys.path
            self.assertEqual(tested._import_argmod('foo'), 'SConsArguments.foo')
            self.assertEqual(sys.path, oldpath)

## FIXME: reimplement the test
##    def test__import_argmod_5(self):
##        """Test SConsArguments.Importer._import_argmod('Declaration')"""
##        self.assertEqual(tested._import_argmod('Declarations'), SConsArguments.Declarations)

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
            declo = tested.ImportArguments('foomod', ['foo/bar'], name_filter = ['arg1','baaz'], foo = 'FOO')
            self.assertEqual(declo['arg1'].get_var_decl()['help'], 'This is arg1')
            mock_import_argmod.assert_called_once_with('foomod', ['foo/bar'])
            mock_load_decls.assert_called_once_with({'arg1' : {'help' : 'This is arg1'}}, name_filter = ['arg1', 'baaz'], foo = 'FOO')
            mock_mod.arguments.assert_called_once_with(name_filter = ['arg1', 'baaz'], foo = 'FOO')

#############################################################################
class Test_export_arguments(unittest.TestCase):
    """Test case for SConsArguments.Importer.export_arguments()"""
    def setUp(self):
        self.argsFixture = {
            'VAR1' : { 'help' : 'This is VAR1' },
            'VAR2' : { 'help' : 'This is VAR2' },
            'VAR3' : { 'help' : 'This is VAR3' },
            'VAR4' : { 'help' : 'This is VAR4' },
            'VAR5' : { 'help' : 'This is VAR4' },
            'VAR6' : { 'help' : 'This is VAR4' }
        }
        self.groupsFixture = {
            'g1' : ['VAR1', 'VAR2'],
            'g2' : ['VAR3', 'VAR4'],
            'g3' : ['VAR5', 'VAR6']
        }

    def test_export_arguments_1(self):
        arguments = self.argsFixture
        expected = self.argsFixture
        result = tested.export_arguments('foomod', arguments)
        self.assertEqual(result, expected)

    def test_export_arguments_2(self):
        groups = self.groupsFixture
        arguments = self.argsFixture
        expected = dict()
        result = tested.export_arguments('foomod', arguments, groups, include_groups = [])
        self.assertEqual(result, expected)

    def test_export_arguments_3(self):
        groups = self.groupsFixture
        arguments = self.argsFixture
        expected = { k : arguments[k] for k in groups['g1'] }
        result = tested.export_arguments('foomod', arguments, groups, include_groups = 'g1')
        self.assertEqual(result, expected)
        result = tested.export_arguments('foomod', arguments, groups, foomod_include_groups = 'g1', include_groups = 'g2')
        self.assertEqual(result, expected)

    def test_export_arguments_4(self):
        groups = self.groupsFixture
        arguments = self.argsFixture
        expected = { k : arguments[k] for k in groups['g2'] }
        result = tested.export_arguments('foomod', arguments, groups, include_groups = 'g2')
        self.assertEqual(result, expected)
        result = tested.export_arguments('foomod', arguments, groups, foomod_include_groups = 'g2', include_groups = 'g1')
        self.assertEqual(result, expected)

    def test_export_arguments_5(self):
        groups = self.groupsFixture
        arguments = self.argsFixture
        expected = { k : arguments[k] for k in (groups['g1'] + groups['g2']) }
        result = tested.export_arguments('foomod', arguments, groups, include_groups = ['g1', 'g2'])
        self.assertEqual(result, expected)
        result = tested.export_arguments('foomod', arguments, groups, foomod_include_groups = ['g1', 'g2'], include_groups = 'g3')
        self.assertEqual(result, expected)

    def test_export_arguments_6(self):
        groups = self.groupsFixture
        arguments = self.argsFixture
        expected = { k : arguments[k] for k in (set(arguments.keys()) - set(groups['g1'])) }
        result = tested.export_arguments('foomod', arguments, groups, exclude_groups = 'g1')
        self.assertEqual(result, expected)
        result = tested.export_arguments('foomod', arguments, groups, foomod_exclude_groups = 'g1', exclude_groups = 'g2')
        self.assertEqual(result, expected)

    def test_export_arguments_7(self):
        groups = self.groupsFixture
        arguments = self.argsFixture
        expected = { k : arguments[k] for k in (set(arguments.keys()) - set(groups['g2'])) }
        result = tested.export_arguments('foomod', arguments, groups, exclude_groups = 'g2')
        self.assertEqual(result, expected)
        result = tested.export_arguments('foomod', arguments, groups, foomod_exclude_groups = 'g2', exclude_groups = 'g1')
        self.assertEqual(result, expected)

    def test_export_arguments_8(self):
        groups = self.groupsFixture
        arguments = self.argsFixture
        expected = { k : arguments[k] for k in (set(arguments.keys()) - set(groups['g1'] + groups['g2'])) }
        result = tested.export_arguments('foomod', arguments, groups, exclude_groups = ['g1', 'g2'])
        self.assertEqual(result, expected)
        result = tested.export_arguments('foomod', arguments, groups, foomod_exclude_groups = ['g1', 'g2'], exclude_groups = 'g3')
        self.assertEqual(result, expected)

    def test_export_arguments_9(self):
        groups = self.groupsFixture
        arguments = self.argsFixture
        expected = dict()
        result = tested.export_arguments('foomod', arguments, groups, include_groups = ['inexistent'])
        self.assertEqual(result, expected)
        result = tested.export_arguments('foomod', arguments, groups, foomod_include_groups = ['inexistent'])
        self.assertEqual(result, expected)

    def test_export_arguments_10(self):
        groups = self.groupsFixture
        arguments = self.argsFixture
        expected = arguments
        result = tested.export_arguments('foomod', arguments, groups, exclude_groups = ['inexistent'])
        self.assertEqual(result, expected)
        result = tested.export_arguments('foomod', arguments, groups, foomod_exclude_groups = ['inexistent'])
        self.assertEqual(result, expected)


#############################################################################
if __name__ == "__main__":
    ldr = unittest.TestLoader()
    suite = unittest.TestSuite()
    # Load tests to test suite
    tclasses = [ Test__load_module_file
               , Test__handle_site_scons_dir
               , Test__handle_all_site_scons_dirs
               , Test__initDefaultArgpath
               , Test_GetDefaultArgpath
               , Test__load_dict_decl
               , Test__load_decl
               , Test__load_decls
               , Test__import_argmod
               , Test_ImportArguments
               , Test_export_arguments
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
