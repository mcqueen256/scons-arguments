"""`SConsArguments.Declarations`

Provides `_ArgumentDeclarations` class and factory methods
`ArgumentDeclarations` and `DeclareArguments`.
"""

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

__docformat__ = "restructuredText"

from .Util import ENV, VAR, OPT, ALL, MISSING, NOTFOUND
from .Util import _build_resubst_dict, _build_iresubst_dict, _resubst
from .Declaration import _ArgumentDeclaration, ArgumentDeclaration, DeclareArgument
from .Arguments import _Arguments

#############################################################################
class _ArgumentDeclarations(dict):
    #========================================================================
    """Dict-like object with *argument* declarations as values.

    The `_ArgumentDeclarations` object is a subclass of ``dict`` with keys being
    *argument* names and values being instances of `_ArgumentDeclaration` objects. The
    `_ArgumentDeclarations` dictionary also maintains *supplementary dictionaries*
    used internally to map names of *arguments* and their *endpoints*.

    The usage of `_ArgumentDeclarations` may be split into three stages:

        - declaring *arguments*; this may be done during object
          creation, see `__init__()`; further declarations may be added or
          existing ones may be modified via dictionary interface, see
          `__setitem__()`, `update()` and others,
        - committing declared variables, see `commit()`; after commit,
          any attempts to modify contents of `_ArgumentDeclarations` ends with a
          `RuntimeError` exception being raised,
        - creating related construction variables (``env["VARIABLE"]=VALUE``),
          command-line variables (``variable=value``) and command-line options
          (``--option=value``) according to committed `_ArgumentDeclarations`
          declarations, see `add_to()`; this may be performed by `commit()` as
          well.

    After that, an instance of `_Arguments` should be created from
    `_ArgumentDeclarations` to keep track of created *arguments* (and corresponding
    construction variables, command-line variables and command-line options).
    The dictionary `_ArgumentDeclarations` may be then disposed.

    **Note**:

        In several places we use ``ns`` as placeholder for one of the `ENV`,
        `VAR` or `OPT` selectors.
    """
    #========================================================================



    #========================================================================
    def __init__(self, *args, **kw):
        #--------------------------------------------------------------------
        """Constructor for `_ArgumentDeclarations`.

        ``__init__()`` initializes an empty `_ArgumentDeclarations` dictionary,

        ``__init__(mapping)`` initializes `_ArgumentDeclarations` dictionary from a
        mapping object's ``(key,value)`` pairs, each ``value`` must be
        instance of `_ArgumentDeclaration`,

        ``__init__(iterable)`` initializes the `_ArgumentDeclarations` dictionary as if
        via ``d = { }`` followed by ``for k, v in iterable: d[k] = v``.
        Each value ``v`` from ``iterable`` must be an instance of `_ArgumentDeclaration`,

        ``__init__(**kw)`` initializes the `_ArgumentDeclarations` dictionary with
        ``name=value`` pairs in the keyword argument list ``**kw``, each
        ``value`` must be an instance of `_ArgumentDeclaration`,
        """
        #--------------------------------------------------------------------
        self.__committed = False
        _ArgumentDeclarations.__validate_values(*args,**kw)
        super(_ArgumentDeclarations, self).__init__(*args,**kw)
        self.__update_supp_dicts()

    #========================================================================
    def __reset_supp_dicts(self):
        """Reset supplementary dictionaries to empty state. This method is for
        internal use, it IS **NOT a part of public API**."""
        self.__rename = [{} for n in range(0,ALL)]
        self.__irename = [{} for n in range(0,ALL)]
        self.__resubst = [{} for n in range(0,ALL)]
        self.__iresubst = [{} for n in range(0,ALL)]

    #========================================================================
    def __update_supp_dicts(self):
        """Update supplementary dictionaries to be in sync with the
        declarations contained in main dictionary. This method is for internal
        use, it IS **NOT a part of public API**."""
        self.__reset_supp_dicts()
        for x in self.iteritems(): self.__append_decl_to_supp_dicts(*x)

    #========================================================================
    def __replace_key_in_supp_dicts(self, ns, key, ns_key):
        #--------------------------------------------------------------------
        """Replace in the supplementary dicts the key identifying corresponding
        `ns` variable (where `ns` is one of `ENV`, `VAR` or `OPT`). This method
        is for internal use, it IS **NOT a part of public API**.

        **Note**: This only alters rename/irename dictionaries, the
        resubst/iresubst dicts are not altered.

        If the corresponding `ns` variable identified by ``ns_key`` already
        exists in the supplementary dictionaries, the supplementary
        dictionaries are left unaltered.

        :Parameters:
            ns : int
                selector of the corresponding variable being renamed; one of
                `ENV`, `VAR` or `OPT`,
            key : string
                the key identifying *argument* declared within this
                `_ArgumentDeclarations` dictionary, which subject to modification,
            ns_key : string
                new name for the corresponding `ns` variable.
        """
        #--------------------------------------------------------------------
        old_key = self.__rename[ns].get(key,NOTFOUND)
        if ns_key != old_key:
            self.__append_key_to_supp_dicts(ns, key, ns_key)
            try: del self.__irename[ns][old_key]
            except KeyError: pass

    #========================================================================
    def __append_key_to_supp_dicts(self, ns, key, ns_key):
        #--------------------------------------------------------------------
        """Add to supplementary dictionaries the new `ns` variable
        corresponding to *argument* identified by `key`. This method is for
        internal use, it IS **NOT a part of public API**.

        If the corresponding `ns` variable identified by ``ns_key`` already
        exists in the supplementary dictionaries, a ``RuntimeError`` is raised.

        :Parameters:
            ns : int
                selector of the corresponding variable being renamed; one of
                `ENV`, `VAR` or `OPT`,
            key : string
                the key identifying *argument* within this `_ArgumentDeclarations`
                dictionary, which subject to modification,
            ns_key : string
                new name for the corresponding `ns` variable.
        """
        #--------------------------------------------------------------------
        if ns_key in self.__irename[ns]:
            raise RuntimeError("variable %r is already declared" % ns_key)
        self.__rename[ns][key] = ns_key
        self.__irename[ns][ns_key] = key

    #========================================================================
    def __append_decl_to_supp_dicts(self, key, decl):
        for ns in range(0,ALL):
            if decl.has_decl(ns):
                ns_key = decl.get_key(ns)
                self.__append_key_to_supp_dicts(ns, key, ns_key)
        return decl

    #========================================================================
    def __del_from_supp_dicts(self, key):
        for ns in range(0,ALL):
            if key in self.__rename[ns]:
                ns_key = self.__rename[ns][key]
                del self.__rename[ns][key]
                del self.__irename[ns][ns_key]

    #========================================================================
    @staticmethod
    def __validate_values(initializer=MISSING,**kw):
        if initializer is not MISSING:
            try: keys = initializer.keys()
            except AttributeError:
                for (k,v) in iter(initializer): _ArgumentDeclarations.__validate_value(v)
            else:
                for k in keys: _ArgumentDeclarations.__validate_value(initializer[k])
        for k in kw: _ArgumentDeclarations.__validate_value(kw[k])

    #========================================================================
    @staticmethod
    def __validate_value(value):
        if not isinstance(value, _ArgumentDeclaration):
            raise TypeError("value must be an instance of _ArgumentDeclaration, %r is not allowed"  % value)

    #========================================================================
    def setdefault(self, key, value = MISSING):
        if value is MISSING:
            return super(_ArgumentDeclarations,self).setdefault(key)
        else:
            self.__ensure_not_committed()
            _ArgumentDeclarations.__validate_value(value)
            return super(_ArgumentDeclarations,self).setdefault(key, value)

    #========================================================================
    def update(self, *args, **kw):
        self.__ensure_not_committed()
        _ArgumentDeclarations.__validate_values(*args,**kw)
        super(_ArgumentDeclarations,self).update(*args,**kw)
        self.__update_supp_dicts()

    #========================================================================
    def clear(self, *args, **kw):
        self.__ensure_not_committed()
        super(_ArgumentDeclarations,self).clear(*args,**kw)
        self.__update_supp_dicts()

    #========================================================================
    def pop(self, key, *args, **kw):
        self.__ensure_not_committed()
        self.__del_from_supp_dicts(key)
        return super(_ArgumentDeclarations,self).pop(key,*args,**kw)

    #========================================================================
    def popitem(self, *args, **kw):
        self.__ensure_not_committed()
        (k,v) = super(_ArgumentDeclarations,self).popitem(*args,**kw)
        self.__del_from_supp_dicts(k)
        return (k,v)

    #========================================================================
    def copy(self):
        return _ArgumentDeclarations(self)

    #========================================================================
    def __setitem__(self, key, value):
        self.__ensure_not_committed()
        _ArgumentDeclarations.__validate_value(value)
        self.__append_decl_to_supp_dicts(key, value)
        return super(_ArgumentDeclarations,self).__setitem__(key, value)

    #========================================================================
    def __delitem__(self, key):
        self.__ensure_not_committed()
        self.__del_from_supp_dicts(key)
        return super(_ArgumentDeclarations,self).__delitem__(key)

    #========================================================================
    def get_rename_dict(self, ns):
        #--------------------------------------------------------------------
        """Get the dictionary mapping variable names from *argument* namespace
        to `ns` (where `ns` is one of `ENV`, `VAR` or `OPT`).

        :Parameters:
            ns : int
                selector of the corresponding namespace; one of `ENV`, `VAR` or
                `OPT`,
        :Returns:
            dictionary with items ``(key, ns_key)``, where ``key`` is the key
            from *argument* namespace and ``ns_key`` is variable name in the
            `ns` (`ENV`, `VAR` or `OPT`) namespace
        """
        #--------------------------------------------------------------------
        return self.__rename[ns].copy()

    #========================================================================
    def get_irename_dict(self, ns):
        #--------------------------------------------------------------------
        """Get the dictionary mapping variable names from `ns` namespace to
        *argument* namespace (where `ns` is one of `ENV`, `VAR` or `OPT`).

        :Parameters:
            ns : int
                selector of the corresponding namespace; one of `ENV`, `VAR` or
                `OPT`,
        :Returns:
            dictionary with items ``(ns_key, key)``, where ``key`` is the key
            from *argument* namespace and ``ns_key`` is variable name in the
            `ns` (`ENV`, `VAR` or `OPT`) namespace

        """
        #--------------------------------------------------------------------
        return self.__irename[ns].copy()

    #========================================================================
    def get_resubst_dict(self,ns):
        #--------------------------------------------------------------------
        """Get the dictionary mapping variable names from *argument* namespace
        to placeholders for variable values from `ns` namespace (where `ns`
        is one of `ENV`, `VAR` or `OPT`).

        **Note**:

            The declarations must be committed before this function may be
            called.

        :Parameters:
            ns : int
                selector of the corresponding namespace; one of `ENV`, `VAR` or
                `OPT`,
        :Returns:
            dictionary with items ``(key, "${" + ns_key + "}")``, where
            ``key`` is the key from *argument* namespace and ``ns_key`` is
            variable name in the `ns` (`ENV`, `VAR` or `OPT`) namespace

        """
        #--------------------------------------------------------------------
        self.__ensure_committed()
        return self.__resubst[ns].copy()

    #========================================================================
    def get_iresubst_dict(self, ns):
        #--------------------------------------------------------------------
        """Get the dictionary mapping variable names from `ns` namespace to
        placeholders for variable values from *argument* namespace (where `ns`
        is one of `ENV`, `VAR` or `OPT`).

        **Note**:

            The declarations must be committed before this function may be
            called.

        :Parameters:
            ns : int
                selector of the corresponding namespace; one of `ENV`, `VAR` or
                `OPT`,
        :Returns:
            dictionary with items ``(ns_key, "${" + key + "}")``, where
            ``key`` is the key from *argument* namespace and ``ns_key`` is
            variable name in the `ns` (`ENV`, `VAR` or `OPT`) namespace

        """
        #--------------------------------------------------------------------
        self.__ensure_committed()
        return self.__iresubst[ns].copy()

    #========================================================================
    def get_key(self, ns, key):
        #--------------------------------------------------------------------
        """Get the key identifying corresponding `ns` variable  (where `ns`
        is one of `ENV`, `VAR` or `OPT`).

        If the corresponding `ns` variable is not declared, the function
        raises an exception.

        :Parameters:
            ns : int
                selector of the corresponding namespace; one of `ENV`, `VAR` or
                `OPT`,
            key : string
                key identifying an already declared *argument* variable to which
                the queried `ns` variable corresponds,

        :Returns:
            the key (name) identifying `ns` variable corresponding to our
            *argument* identified by `key`

        """
        #--------------------------------------------------------------------
        return self[key].get_key(ns)

    #========================================================================
    def set_key(self, ns, key, ns_key):
        #--------------------------------------------------------------------
        """Change the key identifying a corresponding `ns` variable (where
        `ns` is one of `ENV`, `VAR` or `OPT`).

        If the corresponding `ns` variable is not declared, the function
        raises an exception.

        :Parameters:
            ns : int
                selector of the corresponding namespace; one of `ENV`, `VAR` or
                `OPT`,
            key : string
                key identifying an already declared *argument* to which
                the queried `ns` variable corresponds,

        :Returns:
            the key (name) identifying `ns` variable corresponding to our
            *argument* identified by `key`

        """
        #--------------------------------------------------------------------
        self.__ensure_not_committed()
        self[key].set_key(ns, ns_key)
        self.__replace_key_in_supp_dicts(ns, key, ns_key)

    #========================================================================
    def _add_to(self, ns, *args):
        """Invoke `_ArgumentDeclaration.add_to()` for each *argument* declared
        in this dictionary. This method is for internal use, it IS **NOT
        a part of public API**."""
        for (k,v) in self.iteritems(): v.add_to(ns,*args)

    #========================================================================
    def _safe_add_to(self, ns, *args):
        """Invoke `_ArgumentDeclaration.safe_add_to()` for each *argument*
        declared in this dictionary. This method is for internal use, it IS
        **NOT a part of public API**."""
        for (k,v) in self.iteritems(): v.safe_add_to(ns, *args)

    #========================================================================
    def _build_resubst_dicts(self):
        """Build supplementary dictionaries used to rename placeholders in
        values (forward, from *argument* namespace to ``ns`` namespaces).
        This method is for internal use, it IS **NOT a part of public API**."""
        for ns in range(0,ALL):
            self.__resubst[ns] = _build_resubst_dict(self.__rename[ns])

    #========================================================================
    def _build_iresubst_dicts(self):
        """Build supplementary dictionaries used to rename placeholders in
        values (inverse, from ``ns`` namespaces to *argument* namespace).
        This method is for internal use, it IS **NOT a part of public API**."""
        for ns in range(0,ALL):
            self.__iresubst[ns] = _build_iresubst_dict(self.__rename[ns])

    #========================================================================
    def _resubst_decl_defaults(self, decl):
        """Rename placeholders found in the declarations of default values of
        ``ns`` corresponding variables for the given declaration ``decl``.
        This method is for internal use, it IS **NOT a part of public API**.

        :Parameters:
            decl : _ArgumentDeclaration
                the *argument* declaration to modify
        """
        for ns in range(0,ALL):
            if decl.has_decl(ns):
                val = _resubst(decl.get_default(ns), self.__resubst[ns])
                decl.set_default(ns,val)

    #========================================================================
    def __resubst_defaults(self):
        """Rename placeholders found in the declarations of default values of
        ``ns`` corresponding variables for all declared *arguments*. This
        method is for internal use, it IS **NOT a part of public API**.
        """
        for (k,v) in self.iteritems():
            self._resubst_decl_defaults(v)

    #========================================================================
    def __ensure_not_committed(self):
        """Raise exception if the object was already committed. This method
        is for internal use, it IS **NOT a part of public API**."""
        if self.__committed:
            raise RuntimeError("declarations are already committed, can't " \
                               "be modified")
    #========================================================================
    def __ensure_committed(self):
        """Raise exception if the object was not jet committed. This method is
        for internal use, it IS **NOT a part of public API**"""
        if not self.__committed:
            raise RuntimeError("declarations must be committed before " \
                               "performing this operation")

    #========================================================================
    def commit(self, *args):
        #--------------------------------------------------------------------
        """Commit the declaration and optionally add appropriate variables to a
        SCons construction environment, command-line variables and command-line
        options.

        The function finishes declaration stage, freezes the dictionary and
        makes call to `add_to()` with ``*args`` passed verbatim to it.

        :Parameters:
            args
                positional arguments passed verbatim do `add_to()`.
        """
        #--------------------------------------------------------------------
        if not self.__committed:
            self._build_resubst_dicts()
            self._build_iresubst_dicts()
            self.__resubst_defaults()
            self.__committed = True
            self.add_to(*args)

    #========================================================================
    def add_to(self, *args):
        #--------------------------------------------------------------------
        """Create and initialize the corresponding ``ns`` variables (where
        ``ns`` is one of `ENV`, `VAR` or `OPT`).

        This function calls `_safe_add_to()` for each ``ns`` from ``(ENV,
        VAR, OPT)``.

        :Parameters:
            args
                positional arguments interpreted in order as ``env``,
                ``variables``, ``options`` where:

                    - ``env`` is a SCons environment object to be updated with
                      *arguments* defined here and their defaults,
                    - ``variables`` is a SCons Variables object for which new
                      command-line variables will be defined,
                    - ``options`` is a Boolean deciding whether the
                      corresponding command-line options should be created or
                      not (default ``False`` means 'do not create').

                All the arguments are optional. ``None`` may be used to
                represent missing argument and skip the creation of certain
                variables/options.
        """
        #--------------------------------------------------------------------
        self.__ensure_committed()
        for ns in range(0,min(len(args),ALL)):
            if args[ns]: self._safe_add_to(ns, args[ns])

    #========================================================================
    def Commit(self, env=None, variables=None, create_options=False, create_args=True, *args):
        """User interface to `commit()`, optionally returns newly created
        `_Arguments` object.

        :Parameters:
            env
                a SCons environment object to be populated with default values
                of construction variables defined by *arguments* declared here,
            variables
                a `SCons.Variables.Variables`_ object to be populated with new
                variables defined by *arguments* declared here,
            create_options : Boolean
                if ``True``, the command-line create_options declared by *arguments*
                are created,
            create_args
                if ``True`` (default) create and return a `_Arguments` object for
                further operation on variables and their values,

        :Returns:
            if `create_args` is ``True``, returns newly created `_Arguments` object,
            otherwise returns ``None``.

        .. _SCons.Variables.Variables: http://www.scons.org/doc/latest/HTML/scons-api/SCons.Variables.Variables-class.html
        """
        self.commit(env, variables, create_options, *args)
        if create_args:   return _Arguments(self)
        else:       return None

#############################################################################
def __dict_converted(convert, initializer=MISSING, **kw):
    """Generic algorithm for dict initialization while converting the values
    provided within initializers. This function is for internal use, it IS
    **NOT a part of public API**"""
    if initializer is MISSING:
        decls = {}
    else:
        try: keys = initializer.keys()
        except AttributeError:
            decls = dict([ (k, convert(v)) for (k,v) in iter(initializer) ])
        else:
            decls = dict([ (k, convert(initializer[k])) for k in keys ])
    decls.update(dict([ (k, convert(kw[k])) for k in kw ]))
    return decls

#############################################################################
def ArgumentDeclarations(*args, **kw):
    """Create `_ArgumentDeclarations` dictionary with *argument* declarations.

    The function supports several forms of invocation, see the section
    **Returns** to find systematic description. Here we give just a couple of
    examples.

    If the first positional argument is a mapping (a dictionary for example)
    then values from the dictionary are passed through `ArgumentDeclaration()` and the
    resultant dictionary is used as initializer to `ArgumentDeclaration`. You may for
    example pass a dictionary of the form ``{ 'foo' : (env, var, opt)}``,
    where ``env``, ``var`` and ``opt`` are parameters accepted by
    `_ArgumentDeclaration.set_env_decl()`, `_ArgumentDeclaration.set_var_decl()` and
    `_ArgumentDeclaration.set_opt_decl()` respectively.

    **Example**

    .. python::

        decls = {
           # Argument 'foo'
          'foo' : (   {'ENV_FOO' : 'default ENV_FOO'},                  # ENV
                      ('VAR_FOO', 'VAR_FOO help', ),                    # VAR
                      ('--foo', {'dest' : "opt_foo"})               ),  # OPT

           # Argument 'bar'
          'bar' : (   {'ENV_BAR' : None},                               # ENV
                      ('VAR_BAR', 'VAR_BAR help', 'default VAR_BAR'),   # VAR
                      ('--bar', {'dest':"opt_bar", "type":"string"}))   # OPT
        }
        decls = ArgumentDeclarations(decls)

    The first positional argument may be iterable as well, in which case it
    should yield tuples in form ``(key, value)``, where ``value`` is any value
    convertible to `_ArgumentDeclaration`.

    **Example**

    .. python::

        decls = [
           # Argument 'foo'
          'foo' , (   {'ENV_FOO' : 'default ENV_FOO'},                  # ENV
                      ('VAR_FOO', 'VAR_FOO help', ),                    # VAR
                      ('--foo', {'dest' : "opt_foo"})               ),  # OPT

           # Argument 'bar'
          'bar' , (   {'ENV_BAR' : None},                               # ENV
                      ('VAR_BAR', 'VAR_BAR help', 'default VAR_BAR'),   # VAR
                      ('--bar', {'dest':"opt_bar", "type":"string"}))   # OPT
        ]
        decls = ArgumentDeclarations(decls)

    You may also define variables via keyword arguments to `ArgumentDeclarations()`.

    **Example**

    .. python::

        decls = ArgumentDeclarations(
           # Argument 'foo'
           foo  = (   {'ENV_FOO' : 'ENV default FOO'},                  # ENV
                      ('FOO',         'FOO variable help', ),           # VAR
                      ('--foo',       {'dest' : "opt_foo"})         ),  # OPT

           # Argument 'bar'
           bar  = (   {'ENV_BAR' : None},                               # ENV
                      ('BAR', 'BAR variable help', 'VAR default BAR'),  # VAR
                      ('--bar', {'dest':"opt_bar", "type":"string"}))   # OPT
        )

    You may of course append keyword arguments to normal arguments to pass
    extra declarations.

    **Example**

    .. python::

        decls = ArgumentDeclarations(
           # Argument 'foo'
           [('foo',(   {'ENV_FOO' : 'ENV default FOO'},                 # ENV
                      ('FOO',         'FOO variable help', ),           # VAR
                      ('--foo',       {'dest' : "opt_foo"})         ))],# OPT
           # Argument 'geez'
           geez  = (   {'ENV_GEEZ' : None},                             # ENV
                      ('GEEZ', 'GEEZ variable help', 'VAR default GEEZ'),# VAR
                      ('--geez', {'dest':"opt_geez", "type":"string"})) # OPT
        )

    or

    **Example**

    .. python::

        decls = ArgumentDeclarations(
           # Argument 'bar'
           {'bar':(   {'ENV_BAR' : None},                               # ENV
                      ('BAR', 'BAR variable help', 'VAR default BAR'),  # VAR
                      ('--bar', {'dest':"opt_bar", "type":"string"}))}, # OPT
           # Argument 'geez'
           geez  = (   {'ENV_GEEZ' : None},                             # ENV
                      ('GEEZ', 'GEEZ variable help', 'VAR default GEEZ'),# VAR
                      ('--geez', {'dest':"opt_geez", "type":"string"})) # OPT
        )

    This function

    :Returns:

        - `ArgumentDeclarations()` returns an empty `_ArgumentDeclarations` dictionary ``{}``,
        - `ArgumentDeclarations(mapping)` returns `_ArgumentDeclarations` dictionary initialized
          with ``{k : ArgumentDeclaration(mapping[k]) for k in mapping.keys()}``
        - `ArgumentDeclarations(iterable)` returns `_ArgumentDeclarations` dictionary initialized
          with ``{k : ArgumentDeclaration(v) for (k,v) in iter(initializer)}``

        In any case, the keyword arguments ``**kw`` are appended to the
        initializer.

    """
    convert = lambda x : x if isinstance(x, _ArgumentDeclaration)  \
                           else ArgumentDeclaration(**x) if hasattr(x, 'keys') \
                           else ArgumentDeclaration(*tuple(x))
    return _ArgumentDeclarations(__dict_converted(convert, *args, **kw))

#############################################################################
def DeclareArguments(*args, **kw):
    """Declare multiple *arguments* at once

    This function may be used to declare multiple *arguments* at once while
    using same parameters as `DeclareArgument()` for each individual
    *argument*.

    **Example**

    .. python::

        decls = DeclareArguments(
            foo = ('ENV_FOO', 'VAR_FOO', 'OPT_FOO', 'default foo', 'help for argument foo'),
            bar = ('ENV_BAR', 'VAR_BAR', 'OPT_BAR', 'default bar', 'help for argument bar'),
            gez = {'env_key' : 'ENV_GEZ', 'var_key' : 'VAR_GEZ', 'default' : 'default GEEZ' }
        )

    """
    convert = lambda x : x if isinstance(x, _ArgumentDeclaration) \
                           else DeclareArgument(**x) if hasattr(x, 'keys') \
                           else DeclareArgument(*tuple(x))
    return _ArgumentDeclarations(__dict_converted(convert, *args, **kw))


# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
