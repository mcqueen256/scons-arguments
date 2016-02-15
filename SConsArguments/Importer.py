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

from .Declarations import ArgumentDeclarations, DeclareArgument
from .NameConv import _ArgumentNameConv
import SCons.Util
import SCons.Tool
import importlib
import types
import os.path
import sys

#############################################################################
# This shall be initialized with _initDefaultArgpath(). It has to be a list.
_defaultArgpath = None
"""Default search path for arguments modules, see `GetDefaultArgpath()`."""

#############################################################################
def _initDefaultArgpath():
    global _defaultArgpath
    def tool_to_arg(path):
        # Convert Toolpath to corresponding Argpath
        parts = list(os.path.split(path))
        if parts[-1] == 'site_tools':
            parts[-1] = 'site_arguments'
        return os.path.join(*parts)
    _defaultArgpath = filter(os.path.exists, map(tool_to_arg, SCons.Tool.DefaultToolpath))

#############################################################################
def GetDefaultArgpath():
    """Default list of directories searched for modules containing argument
    declarations.

    The `_defaultArgpath` list returned by this function is constructed based
    on default path used for SCons tools. If, for example,
    ``SCons.Tool.DefaultToolpath`` contains path
    ``'/foo/bar/site_scons/site_tools'``, then ``GetDefaultArgpath()`` will
    return a list containing corresponding entry
    ``'/foo/bar/site_scons/site_arguments'`` if such directory exists.
    """
    global _defaultArgpath
    if _defaultArgpath is None:
        _initDefaultArgpath()
    return _defaultArgpath

#############################################################################
def _import_argmod(name, argpath = None, **kw):
    if isinstance(name, types.ModuleType):
        return name

    oldpath = sys.path
    sys.path = (argpath or []) + GetDefaultArgpath()

    try:
        return importlib.import_module(name)
    except ImportError:
        pass
    finally:
        sys.path = oldpath

    full_name = 'SConsArguments.' + name

    try:
        return sys.modules[full_name]
    except KeyError:
        smpath = sys.modules['SConsArguments'].__path__
        oldpath = sys.path
        sys.path = smpath
        try:
            return importlib.import_module(full_name)
        except ImportError, e:
            raise RuntimeError("No module named %s : %s" % (name, e))
        finally:
            sys.path = oldpath

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
        kw2.update({ k : v for (k,v) in kw.iteritems() if k in kws })
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
        for name, decl in args.iteritems():
            if name_filter(name):
                decls[name] = _load_decl(name, decl, **kw)
    else:
        raise TypeError("Can not load arguments from %r object" % type(args))
    return decls


#############################################################################
def ImportArguments(modules, argpath = None, kwpass = None, **kw):
    """Import argument declarations from modules

    :Parameters:
        modules : str|list
            Modules to be imported (names).
        argpath : list
            A list of directories to be searched for arguments' modules prior
            to default ones (returned by `GetDefaultArgpath()`).
        kwpass : dict
            A dict passed as keyword arguments to the ``arguments(**kw)``
            function of every imported module.

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
    if kwpass is None:
        kwpass = dict()
    if SCons.Util.is_String(modules):
        modules = [ modules ]
    for modname in modules:
        mod = _import_argmod(modname, argpath)
        decls.update(_load_decls(mod.arguments(**kwpass), **kw))
    return decls


# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
