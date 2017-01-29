"""`SConsArguments.Importer`

Importing SCons arguments (declarations) from module files. The idea of
importing argument declarations from python modules is similar to that of
loading SCons tools from python modules. A python file placed in appropriate
directory can act as a source of arguments' declarations. The default list of
directories that are looked up for arguments' modules is called ``argpath``
and is returned by `GetDefaultArgpath()`. The list is derived from the
SCons tools search path stored in ``SCons.Tool.DefaultToolpath``. To generate
default ``argpath`` we just replace ``"site_tools"`` with ``"site_arguments"``
in the last component of each directory name. This means that, in typical
situation, argument modules will be placed in ``"site_scons/site_arguments/"``.
Only existing directories get included in the default ``argpath``.

A module containing argument declarations is a python module with the
following function defined::

    def arguments(**kw)

This function shall return a dict with argument names as keys and argument
declarations as values. Each declaration should have a form of dict with keys
and values specified by the documentation of
`SConsArguments.Declaration.DeclareArgument`. For example::

    # site_scons/site_arguments/mine.py
    def arguments(**kw):
        return {
            'arg1' : { 'help' : 'This is arg1' },
            'arg2' : { 'help' : 'This is arg2' }
        }

Modules may be imported with `ImportArguments()` function, which takes a
module name(s) as firsta argument (so, `ImportArguments("mine")` for the above
example).
"""

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

__docformat__ = "restructuredText"

from SConsArguments.Declarations import ArgumentDeclarations, DeclareArgument
from SConsArguments.NameConv import _ArgumentNameConv
import SCons.Util
import SCons.Tool
import SCons.Script.Main
import SCons.Node.FS
import SCons.Platform
import SCons.Errors
import types
import os.path
import sys

def _load_module_file(name, path):
    if sys.version_info < (3,4):
        import imp
        file, path, desc = imp.find_module(name, path)
        try:
            return imp.load_module(name, file, path, desc)
        finally:
            if file:
                file.close()
    else:
        import importlib.util
        spec = None
        for finder in sys.meta_path:
            spec = finder.find_spec(name, path)
            if spec is not None:
                break
        if spec is None:
            raise ImportError("No module named '%s'" % name)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod

#############################################################################
# This shall be initialized with _initDefaultArgpath(). It has to be a list.
_defaultArgpath = None
"""Default search path for arguments modules, see `GetDefaultArgpath()`."""

#############################################################################
def _handle_site_scons_dir(topdir, site_dir_name=None):
    global _defaultArgpath

    if site_dir_name:
        err_if_not_found = True # user specified: err if missing
    else:
        site_dir_name = "site_scons"
        err_if_not_found = False

    site_dir = os.path.join(topdir, site_dir_name)
    if not os.path.exists(site_dir):
        if err_if_not_found:
            raise SCons.Errors.UserError("site dir %s not found." % site_dir)
        return

    site_arguments_dirname = "site_arguments"
    site_arguments_dir = os.path.join(site_dir, site_arguments_dirname)
    if os.path.exists(site_arguments_dir):
        _defaultArgpath.insert(0, os.path.abspath(site_arguments_dir))

#############################################################################
def _handle_all_site_scons_dirs(topdir):
    platform = SCons.Platform.platform_default()
    homedir = lambda d : os.path.expanduser('~/' + d)

    if platform == 'win32' or platform == 'cygwin':
        sysdirs = [ os.path.expandvars('$ALLUSERSPROFILE\\Application Data\\scons'),
                    os.path.expandvars('$USERPROFILE\\Local Settings\\Application Data\\scons') ]
        appdatadir = os.path.expandvars('$APPDATA\\scons')
        if appdatadir not in sysdirs:
            sysdirs.append(appdatadir)
        sysdirs.append(homedir('.scons'))

    elif platform == 'darwin': # MacOS X
        sysdirs = [ '/Library/Application Support/SCons',
                    '/opt/local/share/scons', # (for MacPorts)
                    '/sw/share/scons', # (for Fink)
                    homedir('Library/Application Support/SCons'),
                    homedir('.scons') ]
    elif platform == 'sunos': # Solaris
        sysdirs = [ '/opt/sfw/scons',
                    '/usr/share/scons',
                    homedir('.scons') ]
    else:
        # assume posix-like, i.e. platform == 'posix'
        sysdirs = [ '/usr/share/scons',
                    homedir('.scons') ]

    dirs = sysdirs + [topdir]
    for d in dirs:
        _handle_site_scons_dir(d)

#############################################################################
def _initDefaultArgpath():
    global _defaultArgpath

    _defaultArgpath = []

    site_dir = SCons.Script.Main.GetOption('site_dir')
    no_site_dir = SCons.Script.Main.GetOption('no_site_dir')
    topdir = SCons.Node.FS.get_default_fs().SConstruct_dir

    if 'get_internal_path' in dir(topdir): # SCons >= 2.4.0
        toppath = topdir.get_internal_path()
    else:
        toppath = topdir.path

    if site_dir:
        _handle_site_scons_dir(toppath, site_dir)
    elif not no_site_dir:
        _handle_all_site_scons_dirs(toppath)

#############################################################################
def GetDefaultArgpath():
    """Default list of directories searched for modules containing argument
    declarations.

    The `_defaultArgpath` list returned by this function is constructed in way
    similar to that of default tool path. We just use ``"site_arguments"``
    instead of ``"site_tools"`` in the last component, and ``"SConsArguments"``
    instead of ``"SCons.Tool"``.
    """
    global _defaultArgpath
    if _defaultArgpath is None:
        _initDefaultArgpath()
    return _defaultArgpath

#############################################################################
def _import_argmod(name, argpath = None, **kw):
    if isinstance(name, types.ModuleType):
        return name

    newpath = (argpath or []) + GetDefaultArgpath()

    try:
        return _load_module_file(name, newpath)
    except ImportError as e:
        pass

    full_name = 'SConsArguments.' + name

    try:
        return sys.modules[full_name]
    except KeyError:
        try:
            return _load_module_file(name, sys.modules['SConsArguments'].__path__)
        except ImportError as e:
            raise RuntimeError("No module named %s : %s" % (name, e))

#############################################################################
def _load_dict_decl(name, decl, **kw):
    try:
        nameconv = kw['nameconv']
        if not isinstance(nameconv, _ArgumentNameConv):
            raise TypeError("The nameconv must be an instance of _ArgumentNameConv, not %r" % nameconv)
        forcenameconv = True
    except KeyError:
        # initially kw2 contains defaults
        kw2 = { 'env_key_transform' : True,     # generate construction variable
                'var_key_transform' : True,     # generate CLI variable
                'opt_key_transform' : False,    # but skip CLI option
                'option_transform'  : False }   # ...
        kws = { 'env_key_prefix', 'env_key_suffix', 'env_key_transform',
                'var_key_prefix', 'var_key_suffix', 'var_key_transform',
                'opt_key_prefix', 'opt_key_suffix', 'opt_key_transform',
                'opt_prefix', 'opt_name_prefix', 'opt_name_suffix',
                'option_transform' }
        kw2.update({ k : v for (k,v) in kw.items() if k in kws })
        nameconv = _ArgumentNameConv(**kw2)
        forcenameconv = False

    if forcenameconv:
        # nameconv provided by user, so we ignore *_prefix/*_suffix/*_transform
        # keywords and let the nameconv to override some entries provided in
        # decl (env_key, var_key, opt_key, option)
        decl2 = decl.copy()
        decl2.update(nameconv.name2dict(name))
    else:
        decl2 = nameconv.name2dict(name)
        decl2.update(decl)
    return decl2

#############################################################################
def _load_decl(name, decl, **kw):
    preprocessor = kw.get('preprocessor', lambda d : d)
    kw.pop('preprocessor', None) # delete kw['preprocessor'], if exists
    if SCons.Util.is_Dict(decl):
        return DeclareArgument(**_load_dict_decl(name, preprocessor(decl), **kw))
    else:
        raise TypeError("Unsupported decl type %s" % type(decl))

#############################################################################
def _load_decls(args, **kw):
    name_filter = kw.get('name_filter', lambda x : True)
    if SCons.Util.is_Sequence(name_filter) or isinstance(name_filter, set):
        allowed_names = name_filter
        name_filter = lambda x : x in allowed_names
    decls = ArgumentDeclarations()
    if SCons.Util.is_Dict(args):
        for name, decl in args.items():
            if name_filter(name):
                decls[name] = _load_decl(name, decl, **kw)
    else:
        raise TypeError("Can not load arguments from %r object" % type(args))
    return decls


#############################################################################
def ImportArguments(modules, argpath = None, **kw):
    """Import argument declarations from modules

    Note, that all the keyword arguments get passed to module's
    ``argument(**kw)`` functions as ``**kw``. Not all meaningful keyword
    arguments are listed here.

    :Parameters:
        modules : str|list
            Modules to be imported (names).
        argpath : list
            A list of directories to be searched for arguments' modules prior
            to default ones (returned by `GetDefaultArgpath()`).

    :Keywords:
        preprocessor : callable
            A callable object used to preprocess every argument declaration
            when it's loaded from a module. This allows to customize arguments
            provided by third parties. It's used internally as follows:
            ``y = preprocessor(x)``, where ``x`` is the original argument
            declaration record from a module.
        name_filter : callable | list | set
            A callable object used to filter-out unwanted arguments based on
            their names. If **name_filter** is a list or set (a collection),
            only arguments listed in this collection will be imported.
        nameconv : `SConsArguments.NameConv._ArgumentNameConv`
            An instance of `SConsArguments.NameConv._ArgumentNameConv` that
            will be used internally to map argument names to their
            corresponding construction variables, command-line variables and/or
            options. If **nameconv** is present, then **env_key_prefix**,
            **env_key_suffix**, **env_key_transform**, **var_key_prefix**,
            **var_key_suffix**, **var_key_transform**, **opt_key_prefix**,
            **opt_key_suffix**, **opt_key_transform**, **opt_prefix**, 
            **opt_name_prefix**, **opt_name_suffix**, and **option_transform**
            are ignored.
        env_key_prefix : str
            A prefix to be prepended to ENV keys. See
            `SConsArguments.NameConv._ArgumentNameConv`.
        env_key_suffix : str
            A suffix to be appended to ENV keys. See
            `SConsArguments.NameConv._ArgumentNameConv`.
        env_key_transform : callable | bool
            A lambda used to transform *argument* names to construction
            variables, may be customized to completely redefine the way ENV
            keys are transformed. See
            `SConsArguments.NameConv._ArgumentNameConv`.
        var_key_prefix : str
            A prefix to be prepended to VAR keys. See
            `SConsArguments.NameConv._ArgumentNameConv`.
        var_key_suffix : str
            A suffix to be appended to VAR keys. See
            `SConsArguments.NameConv._ArgumentNameConv`.
        var_key_transform : callable | bool
            A lambda used to transform *argument* names to command-line
            variables, may be customized to completely redefine the way VAR
            keys are transformed. See
            `SConsArguments.NameConv._ArgumentNameConv`.
        opt_key_prefix : str
            A prefix to be prepended to OPT keys. See
            `SConsArguments.NameConv._ArgumentNameConv`.
        opt_key_suffix : str
            A suffix to be appended to OPT keys. See
            `SConsArguments.NameConv._ArgumentNameConv`.
        opt_key_transform : callable | bool
            A lambda used to transform *argument* names to command-line
            option keys, may be customized to completely redefine the way OPT
            keys are transformed. See
            `SConsArguments.NameConv._ArgumentNameConv`.
        opt_prefix : str
            a prefix that is by default used when composing option names,
            usually a single or double dash, see
            `SConsArguments.NameConv._ArgumentNameConv`.
        opt_name_prefix : str
            additional prefix used when composing option names, inserted
            between **opt_prefix** and the argument name, see
            `SConsArguments.NameConv._ArgumentNameConv`.
        opt_name_suffix : str
            additional suffix used when composing option names, see
            `SConsArguments.NameConv._ArgumentNameConv`.
        option_transform : callable | bool
            A lambda used to transform *argument* names to command-line
            options, may be customized to completely redefine the way option
            names are transformed. See
            `SConsArguments.NameConv._ArgumentNameConv`.

    :Returns:
       An instance of `SConsArguments.Declarations._ArgumentDeclarations`
       containing the imported argument declarations.
    """
    # Load modules possibly containing arguments
    decls = ArgumentDeclarations()
    if SCons.Util.is_String(modules):
        modules = [ modules ]
    for modname in modules:
        mod = _import_argmod(modname, argpath)
        decls.update(_load_decls(mod.arguments(**kw), **kw))
    return decls

#############################################################################
def export_arguments(modname, args, groups = None, **kw):
    """Helper function for arguments' module developers

    :Parameters:
        modname : str
            name of the module calling this function

        args : dict
            a dictionary with all argument definitions that may be potentially
            exported by the calling module.

        groups : dict
            argument groups (group names); the dictionary shall have group
            names as keys followed by lists of argument names belonging to
            these groups

    :Keywords:
        include_group : str | list
            only include arguments assigned to the listed groups
        ${modname}_include_group : str | list
            only include arguments assigned to the listed groups
        exclude_group : str | list
            exclude arguments assigned to the listed groups
        ${modname}_exclude_group : str | list
            exclude arguments assigned to the listed groups
        exclude_${group} : boolean
            whether to exclude arguments belonging to a given ${group}; for
            example, if there is a group named ``'progs'`` in **groups**,
            then arguments belonging to ``'progs'`` may be excluded with
            ``exclude_progs = True``,

        ${modname}_exclude_${group} : boolean
            works same way same as **exclude_${group}**, provided the
            ``${modname}`` prefix is same as the value of **modname** argument
            (so, if ``modname = 'foo'``, then ``foo_exclude_progs`` will
            exclude all arguments belonging to a group named ``progs``)
    """
    include_groups = kw.get("%s_include_groups" % modname, kw.get('include_groups', None))
    if SCons.Util.is_String(include_groups):
        include_groups = [ include_groups ]

    exclude_groups = kw.get("%s_exclude_groups" % modname, kw.get('exclude_groups', None))
    if SCons.Util.is_String(exclude_groups):
        exclude_groups = [ exclude_groups ]

    if include_groups is not None:
        include = set()
        for groupname in include_groups:
            include.update(groups.get(groupname,[]))
    else:
        include = set(args.keys())

    exclude = set()
    if exclude_groups is not None:
        for groupname in exclude_groups:
            exclude.update(groups.get(groupname,[]))

    return { k : args[k] for k in (include - exclude) }



# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
