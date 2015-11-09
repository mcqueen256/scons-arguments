"""`SConsArguments.Declaration`

TODO: Write documentation
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

import SCons.Util
from .Util import ENV, VAR, OPT, ALL, UNDEFINED

#############################################################################
class _ArgumentDeclaration(object):
    #========================================================================
    """Declaration of single *argument*.

    This object holds information necessary to create construction variable in
    SCons Environment, SCons command-line variable (``variable=value``) and
    SCons command-line option (``--option=value``) corresponding to a given
    *argument* (it for example holds the names and default values of
    these variables/options before they get created).

    **Note**:

        In several places we use ``ns`` as placeholder for one of the ``ENV``,
        ``VAR`` or ``OPT`` constants which represent selection of
        "corresponding Environment construction variable", "corresponding SCons
        command-line variable" or "corresponding SCons command-line option"
        respectively.  So, for example the call ``decl.set_decl(ENV,decl)``
        stores the declaration of corresponding construction variable in a
        SCons environment (``ENV``).
    """
    #========================================================================


    #========================================================================
    def __init__(self, env_decl=None, var_decl=None, opt_decl=None):
        #--------------------------------------------------------------------
        """Constructor for the `_ArgumentDeclaration` object

        :Parameters:
            env_decl
                parameters used later to create related construction variable
                in `SCons environment`_, same as ``decl`` argument to
                `set_env_decl()`,
            var_decl
                parameters used later to create related `SCons command-line
                variable`_, same as ``decl`` argument to `set_var_decl()`,
            opt_decl
                parameters used later to create related `SCons command-line
                option`_, same as  ``decl`` argument to `set_opt_decl()`.

        .. _SCons environment:  http://www.scons.org/doc/HTML/scons-user.html#chap-environments
        .. _SCons command-line option: http://www.scons.org/doc/HTML/scons-user.html#sect-command-line-options
        .. _SCons command-line variable: http://www.scons.org/doc/HTML/scons-user.html#sect-command-line-variables
        """
        #--------------------------------------------------------------------
        # __decl_tab is an internal 3-element list and holds argument info
        #            for ENV, VAR and OPT endpoints.
        self.__decl_tab = [None,None,None]
        if env_decl: self.set_env_decl(env_decl)
        if var_decl: self.set_var_decl(var_decl)
        if opt_decl: self.set_opt_decl(opt_decl)

    #========================================================================
    def set_decl(self, ns, decl):
        #--------------------------------------------------------------------
        """Declare related *endpoint* in `ns` namespace. `ns` is one of `ENV`,
        `VAR` or `OPT`.

        This functions just dispatches the job between `set_env_decl()`,
        `set_var_decl()` and `set_opt_decl()` according to `ns` argument.

        :Parameters:
            ns : int
                one of `ENV`, `VAR` or `OPT`,
            decl
                declaration parameters passed to particular setter method
                (`set_env_decl()`, `set_var_decl()`, or `set_opt_decl()`).
        """
        #--------------------------------------------------------------------
        if ns == ENV:     self.set_env_decl(decl)
        elif ns == VAR:   self.set_var_decl(decl)
        elif ns == OPT:   self.set_opt_decl(decl)
        else:               raise IndexError("index out of range")

    #========================================================================
    def set_env_decl(self, decl):
        #--------------------------------------------------------------------
        """Set parameters for later creation of the related construction
        variable in `SCons environment`_.

        :Parameters:
            decl : tuple | dict | str
                may be a tuple in form ``("name", default)``, one-entry
                dictionary ``{"name": default}`` or just a string ``"name"``;
                later, when requested, this data is used to create construction
                variable for user-provided `SCons environment`_ ``env`` with
                ``env.SetDefault(name = default)``

        .. _SCons environment:  http://www.scons.org/doc/HTML/scons-user.html#chap-environments
        """
        #--------------------------------------------------------------------
        if SCons.Util.is_Tuple(decl):
            if not len(decl) == 2:
                raise ValueError("tuple 'decl' must have 2 elements but " \
                                 "has %d" % len(decl))
            decl = { 'key' : decl[0], 'default' : decl[1] }
        elif SCons.Util.is_Dict(decl):
            if not len(decl) == 1:
                raise ValueError("dictionary 'decl' must have 1 item but " \
                                 "has %d" % len(decl))
            first = decl.items()[0]
            decl = { 'key' : first[0], 'default' : first[1] }
        elif SCons.Util.is_String(decl):
            decl = { 'key' : decl,  'default' : UNDEFINED }
        else:
            raise TypeError("'decl' must be tuple, dictionary or string, %r " \
                            "is not allowed" % type(decl).__name__)
        self.__decl_tab[ENV] = decl

    #========================================================================
    def set_var_decl(self, decl):
        #--------------------------------------------------------------------
        """Set parameters for later creation of the related `SCons command-line
        variable`_.

        :Parameters:
            decl : tuple | dict
                declaration parameters used later to add the related `SCons
                command-line variable`_; if `decl` is a tuple, it must have
                the form::

                    ( key [, help, default, validator, converter, kw] ),

                where entries in square brackets are optional; the consecutive
                elements  are interpreted in order shown above as ``key``,
                ``help``, ``default``, ``validator``, ``converter``, ``kw``;
                the meaning of these arguments is same as for
                `SCons.Variables.Variables.Add()`_; the ``kw``, if present,
                must be a dictionary;

                if `decl` is a dictionary, it should have the form::

                    { 'key'         : "file_name",
                      'help'        : "File name to read", ...  }

                the ``'kw'`` entry, if present, must be a dictionary; the
                arguments enclosed in the dictionary are later passed verbatim
                to `SCons.Variables.Variables.Add()`_.

        .. _SCons.Variables.Variables.Add(): http://www.scons.org/doc/latest/HTML/scons-api/SCons.Variables.Variables-class.html#Add
        .. _SCons command-line variable: http://www.scons.org/doc/HTML/scons-user.html#sect-command-line-variables
        """
        #--------------------------------------------------------------------
        if SCons.Util.is_Tuple(decl) or SCons.Util.is_List(decl):
            keys = [ 'key', 'help', 'default', 'validator', 'converter', 'kw' ]
            if len(decl) > len(keys):
                raise ValueError('len(decl) should be less or greater than ' \
                                 '%d, but is %d' % (len(keys),len(decl) ))
            args = dict(zip(keys, decl))
        elif SCons.Util.is_Dict(decl):
            args = decl.copy()
        else:
            raise TypeError("'decl' must be a list, tuple or dict, %r " \
                            "is not allowed" % type(decl).__name__)
        try:
            kw = args['kw']
            del args['kw']
        except KeyError:
            kw = {}
        if not SCons.Util.is_Dict(kw):
            raise TypeError("decl['kw'] must be a dictionary, %r is not " \
                            "allowed" % type(kw).__name__)
        kw.update(args)
        self.__decl_tab[VAR] = kw

    #========================================================================
    def set_opt_decl(self, decl):
        #--------------------------------------------------------------------
        """Set parameters for later creation of the related `SCons command-line
        option`_.

        :Parameters:
            decl : tuple | list | dict
                declaration parameters used later when creating the related
                `SCons command-line option`_; if it is a tuple or list, it
                should have the form::

                        (names, args) or [names, args]

                where ``names`` is a string or tuple of option names (e.g.
                ``"-f --file"`` or ``('-f', '--file')``) and ``args`` is a
                dictionary defining the remaining `option attributes`_; the
                entire `decl` may be for example::

                    ( ('-f','--file-name'),
                      { 'action'         : "store",
                        'dest'           : "file_name" } )

                if `decl` is a dictionary, it should have following form
                (keys are important, values are just examples)::

                    { 'names'          : ("-f", "--file-name")
                      'action'         : "store",
                      'type'           : "string",
                      'dest'           : "file_name", ... }

                or::

                    { 'names'          : ("-f", "--file-name")
                      'kw' : { 'action'         : "store",
                               'type'           : "string",
                               'dest'           : "file_name", ... } }

                the parameters enclosed in ``decl`` dictionary are later
                passed verbatim to `SCons.Script.Main.AddOption()`_.
                Note, that we require the ``dest`` parameter.

        .. _SCons.Script.Main.AddOption(): http://www.scons.org/doc/latest/HTML/scons-api/SCons.Script.Main-module.html#AddOption
        .. _SCons command-line option: http://www.scons.org/doc/HTML/scons-user.html#sect-command-line-options
        .. _option attributes: http://docs.python.org/2/library/optparse.html#option-attributes
        """
        #--------------------------------------------------------------------
        if SCons.Util.is_Tuple(decl) or SCons.Util.is_List(decl):
            try:
                if SCons.Util.is_String(decl[0]):
                    names = tuple(decl[0].split())
                elif SCons.Util.is_Tuple(decl[0]):
                    names = decl[0]
                elif SCons.Util.is_List(decl[0]):
                    names = tuple(decl[0])
                else:
                    raise TypeError("decl[0] must be a string, tuple or list, %s "\
                                    "is not allowed" % type(decl[0]).__name__)
            except IndexError:
                raise ValueError("'decl' must not be empty, got %(decl)r" % locals())
            try:
                kw  = decl[1]
            except IndexError:
                kw = {}
        elif SCons.Util.is_Dict(decl):
            if SCons.Util.is_String(decl['names']):
                names = tuple(decl['names'].split())
            elif SCons.Util.is_Tuple(decl['names']):
                names = decl['names']
            elif SCons.Util.is_List(decl['names']):
                names = tuple(decl['names'])
            else:
                raise TypeError("decl['names'] must be a string, tuple or list, %s "\
                                "is not allowed" % type(decl['names']).__name__)
            try:
                kw = decl['kw']
            except KeyError:
                kw = decl.copy()
                del(kw['names'])
        else:
            raise TypeError("'decl' must be a tuple list or dictionary, %s " \
                            "is not allowed" % type(decl).__name__)
        if 'dest' not in kw:
            raise ValueError("missing parameter 'dest' in option specification")
        self.__decl_tab[OPT] = (names, kw)

    #========================================================================
    def has_decl(self, ns):
        #--------------------------------------------------------------------
        """Test if declaration of *endpoint* `ns` was provided. `ns` is one of
        `ENV`, `VAR` or `OPT`.

        :Parameters:
            ns : int
                one of `ENV`, `VAR` or `OPT`
        :Returns:
            ``True`` if the declaration exists, or ``False`` otherwise.
        """
        #--------------------------------------------------------------------
        return self.__decl_tab[ns] is not None

    #========================================================================
    def has_env_decl(self):
        """Same as `has_decl(ENV)`"""
        return self.has_decl(ENV)

    #========================================================================
    def has_var_decl(self):
        """Same as `has_decl(VAR)`"""
        return self.has_decl(VAR)

    #========================================================================
    def has_opt_decl(self):
        """Same as `has_decl(OPT)`"""
        return self.has_decl(OPT)

    #========================================================================
    def get_decl(self, ns):
        #--------------------------------------------------------------------
        """Return internal representation of declaration for *endpoint* `ns`.

        If the corresponding `ns` declaration does not exist, or `ns` is out of
        range, the method throws an IndexError.

        :Parameters:
            ns : int
                one of `ENV`, `VAR` or `OPT`
        :Returns:
            The corresponding declaration
        """
        #--------------------------------------------------------------------
        if (ns < 0) or ns > ALL:
            raise IndexError("index out of range")
        elif not self.has_decl(ns):
            nsstr = [ 'ENV', 'VAR', 'OPT' ]
            raise IndexError("there is no %s declaration in this _ArgumentDeclaration" % nsstr[ns])
        return self.__decl_tab[ns]

    #========================================================================
    def get_env_decl(self):
        """Same as `get_decl(ENV)`"""
        return self.get_decl(ENV)

    #========================================================================
    def get_var_decl(self):
        """Same as `get_decl(VAR)`"""
        return self.get_decl(VAR)

    #========================================================================
    def get_opt_decl(self):
        """Same as `get_decl(OPT)`"""
        return self.get_decl(OPT)

    #========================================================================
    def get_key(self, ns):
        #--------------------------------------------------------------------
        """Returns the key (variable name) identifying *endpoint* variable from
        namespace `ns`. `ns` is one of `ENV`, `VAR` or `OPT`.

        :Parameters:
            ns : int
                one of `ENV`, `VAR` or `OPT`
        :Returns:
            ``decl`` parameters stored by last call `set_decl(ns,decl)`.
        """
        #--------------------------------------------------------------------
        decl = self.get_decl(ns)
        if ns == ENV or ns == VAR:
            return decl['key']
        elif ns == OPT:
            return decl[1]['dest']
        else: # pragma: no cover
            raise IndexError("index out of range")

    #========================================================================
    def get_env_key(self):
        """Same as `get_key(ENV)`"""
        return self.get_key(ENV)

    #========================================================================
    def get_var_key(self):
        """Same as `get_key(VAR)`"""
        return self.get_key(VAR)

    #========================================================================
    def get_opt_key(self):
        """Same as `get_key(OPT)`"""
        return self.get_key(OPT)

    #========================================================================
    def set_key(self, ns, key):
        #--------------------------------------------------------------------
        """Rename the corresponding *endpoint* in `ns` namespace. `ns` is one
        of `ENV`, `VAR` or `OPT`.

        The corresponding declaration must exists, that is ``has_decl(ns)``
        must be ``True``. Otherwise, ``IndexError`` will be raised.

        **Warning**
            This method should not be used on `_ArgumentDeclaration` objects which
            belong to an `_ArgumentDeclarations` dictionary. To rename *endpoints* of
            such *arguments*, use `_ArgumentDeclarations.set_key()`. This limitation
            may be removed in future.

        :Parameters:
            ns : int
                one of `ENV`, `VAR` or `OPT`
            key : string
                new name for the *endpoint* `ns`.
        """
        #--------------------------------------------------------------------
        decl = self.get_decl(ns)
        if ns == ENV or ns == VAR:
            decl['key'] = key
        elif ns == OPT:
            decl[1]['dest'] = key
        else: # pragma: no cover
            raise IndexError("index out of range")

    #========================================================================
    def set_env_key(self, key):
        """Same as `set_key(ENV, key)`.

        **Warning**
            This method should not be used on `_ArgumentDeclaration` objects which
            belong to an `_ArgumentDeclarations` dictionary. To rename *endpoints* of
            such *arguments*, use `_ArgumentDeclarations.set_key()`. This limitation
            may be removed in future.
        """
        self.set_key(ENV,key)

    #========================================================================
    def set_var_key(self, key):
        """Same as `set_key(VAR, key)`.

        **Warning**
            This method should not be used on `_ArgumentDeclaration` objects which
            belong to an `_ArgumentDeclarations` dictionary. To rename *endpoints* of
            such *arguments*, use `_ArgumentDeclarations.set_key()`. This limitation
            may be removed in future.
        """
        self.set_key(VAR,key)

    #========================================================================
    def set_opt_key(self, key):
        """Same as `set_key(OPT, key)`.

        **Warning**
            This method should not be used on `_ArgumentDeclaration` objects which
            belong to an `_ArgumentDeclarations` dictionary. To rename *endpoints* of
            such *arguments*, use `_ArgumentDeclarations.set_key()`. This limitation
            may be removed in future.
        """
        self.set_key(OPT,key)

    #========================================================================
    def get_default(self, ns):
        #--------------------------------------------------------------------
        """Get the default value of `ns` *endpoint*. `ns` is one of `ENV`,
        `VAR`, `OPT`.

        :Parameters:
            ns : int
                one of `ENV`, `VAR` or `OPT`
        """
        #--------------------------------------------------------------------
        decl = self.get_decl(ns)
        if ns == ENV or ns == VAR:
            return decl.get('default', UNDEFINED)
        elif ns == OPT:
            return decl[1].get('default', UNDEFINED)
        else: # pragma: no cover
            raise IndexError("index out of range")

    #========================================================================
    def get_env_default(self):
        """Same as `get_default(ENV)`"""
        return self.get_default(ENV)

    #========================================================================
    def get_var_default(self):
        """Same as `get_default(VAR)`"""
        return self.get_default(VAR)

    #========================================================================
    def get_opt_default(self):
        """Same as `get_default(OPT)`"""
        return self.get_default(OPT)

    #========================================================================
    def set_default(self, ns, default):
        #--------------------------------------------------------------------
        """Define the default value of `ns` *endpoint*. `ns` is one of `ENV`,
        `VAR`, `OPT`.

        :Parameters:
            ns : int
                one of `ENV`, `VAR` or `OPT`
            default
                the new default value
        """
        #--------------------------------------------------------------------
        decl = self.get_decl(ns)
        if ns == ENV or ns == VAR:
            decl['default'] = default
        elif ns == OPT:
            decl[1]['default'] = default
        else: # pragma: no cover
            raise IndexError("index out of range")

    #========================================================================
    def set_env_default(self, default):
        """Same as `set_default(ENV, default)`"""
        self.set_default(ENV,default)

    #========================================================================
    def set_var_default(self, default):
        """Same as `set_default(VAR, default)`"""
        self.set_default(VAR,default)

    #========================================================================
    def set_opt_default(self, default):
        """Same as `set_default(OPT, default)`"""
        self.set_default(OPT,default)

    #========================================================================
    def add_to(self, ns, *args, **kw):
        #--------------------------------------------------------------------
        """Add new construction variable, command-line variable or command-line
        option (an *endpoint*) depending on the `ns` variable. The `ns` is one
        of `ENV`, `VAR` or `OPT`.

        The method actually dispatches the job between `add_to_env()`,
        `add_to_var()` and `add_to_opt()`.

        The method raises ``IndexError`` if there is no declaration for the
        given *endpoint* indicated with `ns`.

        **Examples**:

            - ``decl.add_to(ENV,env)`` creates new construction variable
              in `SCons environment`_ ``env``,
            - ``decl.add_to(VAR,vars)`` creates new command-line variable
              in `SCons variables`_ ``vars``
            - ``decl.add_to(OPT)`` creates a corresponding SCons
              `command-line option`_.

        :Parameters:
            ns : int
                one of `ENV`, `VAR` or `OPT`
            args, kw
                additional arguments and keywords, depend on `ns`:

                - if ``ns == ENV``, then ``env=args[0]`` is assumed to be
                  a `SCons environment`_ to create construction variable for,
                - if ``ns == VAR`, then ``vars=args[0]`` is assumed to be
                  a SCons `Variables`_ object, ``*args[1:]`` are used as
                  positional arguments to `vars.Add()`_ and ``**kw`` are
                  passed to `vars.Add()`_ as additional keywords,
                - if ``ns == OPT``, the arguments and keywords are not used.

        .. _SCons environment:  http://www.scons.org/doc/HTML/scons-user.html#chap-environments
        .. _SCons variables: http://www.scons.org/doc/HTML/scons-user.html#sect-command-line-variables
        .. _Variables: http://www.scons.org/doc/latest/HTML/scons-api/SCons.Variables.Variables-class.html
        .. _vars.Add(): http://www.scons.org/doc/latest/HTML/scons-api/SCons.Variables.Variables-class.html#Add
        .. _command-line option: http://www.scons.org/doc/HTML/scons-user.html#sect-command-line-options
        """
        #--------------------------------------------------------------------
        if ns == ENV:
            self.add_to_env(args[0])
        elif ns == VAR:
            self.add_to_var(args[0],*args[1:],**kw)
        elif ns == OPT:
            self.add_to_opt()
        else:
            raise IndexError("index out of range")

    #========================================================================
    def add_to_env(self, env):
        #--------------------------------------------------------------------
        """Add construction variable to `SCons environment`_ corresponding to
        this *argument* and set it do default value.

        The method raises ``IndexError`` if there is no declaration for
        construction variable in this `_ArgumentDeclaration` object.

        **Remarks**:

            - the construction variable is "created" with ``env.SetDefault()``;
              existing construction variables are NOT overwritten by this call,
            - the construction variable is not created if the default value
              of this *argument* for construction variable is `UNDEFINED`.

        :Parameters:
            env
                  a `SCons environment`_ to create construction variable for,

        .. _SCons environment:  http://www.scons.org/doc/HTML/scons-user.html#chap-environments
        """
        #--------------------------------------------------------------------
        decl = self.get_decl(ENV)
        default = decl.get('default', UNDEFINED)
        if default is not UNDEFINED:
            env.SetDefault(**{decl['key'] : default})

    #========================================================================
    def add_to_var(self, variables, *args, **kw):
        #--------------------------------------------------------------------
        """Add new SCons `command-line variable`_ corresponding to this *argument*.

        The method raises ``IndexError`` if there is no declaration for the
        corresponding command-line variable in this `_ArgumentDeclaration` object.

        :Parameters:
            variables
                SCons `Variables`_ object,

            args, kw
                additional arguments and keywords, ``*args`` are used as
                positional arguments to `variables.Add()`_ and ``**kw`` are
                passed to `variables.Add()`_ as additional keywords

        .. _command-line variable: http://www.scons.org/doc/HTML/scons-user.html#sect-command-line-variables
        .. _Variables: http://www.scons.org/doc/latest/HTML/scons-api/SCons.Variables.Variables-class.html
        .. _variables.Add(): http://www.scons.org/doc/latest/HTML/scons-api/SCons.Variables.Variables-class.html#Add
        """
        #--------------------------------------------------------------------
        decl = self.get_decl(VAR)
        kw2 = decl.copy()
        kw2.update(kw)
        return variables.Add(*args,**kw2)

    #========================================================================
    def add_to_opt(self):
        #--------------------------------------------------------------------
        """Add new SCons `command-line option`_ corresponding to this *argument*.

        The method raises ``IndexError`` if there is no declaration for the
        command-line option in this `_ArgumentDeclaration` object.

        .. _command-line option: http://www.scons.org/doc/HTML/scons-user.html#sect-command-line-options
        """
        #--------------------------------------------------------------------
        from SCons.Script.Main import AddOption
        decl = self.get_decl(OPT)
        AddOption(*decl[0], **decl[1])

    #========================================================================
    def safe_add_to(self, ns, *args):
        #--------------------------------------------------------------------
        """Same as `add_to()`, but does not raise exceptions when the
        corresponding `ns` *endpoint* is not found.

        :Parameters:
            ns : int
                one of `ENV`, `VAR` or `OPT`

        :Returns:
            returns ``True`` is new variable has been created or ``False`` if
            there is no declaration for corresponding `ns` variable in this
            object.
        """
        #--------------------------------------------------------------------
        if self.has_decl(ns):
            self.add_to(ns, *args)
            return True
        else:
            return False

#############################################################################
def ArgumentDeclaration(*args, **kw):
    #------------------------------------------------------------------------
    """Convert input arguments to `_ArgumentDeclaration` instance.

   :Returns:
        - if ``args[0]`` is an instance of `_ArgumentDeclaration`, then returns
          ``args[0]`` unaltered,
        - otherwise returns result of `_ArgumentDeclaration(*args,**kw)`
    """
    #------------------------------------------------------------------------
    if len(args) > 0 and isinstance(args[0], _ArgumentDeclaration):
        return args[0]
    else:
        return _ArgumentDeclaration(*args, **kw)

#############################################################################
def DeclareArgument(env_key=None, var_key=None, opt_key=None, default=UNDEFINED,
              help=None, validator=None, converter=None, option=None,
              type=None, opt_default=None, metavar=None, nargs=None,
              choices=None, action=None, const=None, callback=None,
              callback_args=None, callback_kwargs=None):
    #------------------------------------------------------------------------
    """Convert unified set of arguments to `_ArgumentDeclaration` instance.

    This function accepts minimal set of parameters to declare consistently an
    *argument* and its corresponding `ENV`, `VAR` and `OPT` counterparts.  If
    the first argument named `env_key` is an instance of `_ArgumentDeclaration`, then
    it is returned unaltered. Otherwise the arguments are mapped onto following
    attributes of corresponding `ENV`, `VAR` and `OPT` variables/options::

        ARG                 ENV         VAR         OPT
        ----------------+-----------------------------------------
        env_key         |   key         -           -
        var_key         |   -           key         -
        opt_key         |   -           -           dest
        default         |   default     default     -
        help            |   -           help        help
        validator       |   -           validator   -
        converter       |   -           converter   -
        option          |   -           -           option strings
        type            |   -           -           type
        opt_default     |   -           -           default
        metavar         |   -           -           metavar
        nargs           |   -           -           nargs
        choices         |   -           -           choices
        action          |   -           -           action
        const           |   -           -           const
        callback        |   -           -           callback
        callback_args   |   -           -           callback_args
        callback_kwargs |   -           -           callback_kwargs
        ----------------+------------------------------------------

    :Parameters:
        env_key : `_ArgumentDeclaration` | string | None
            if an instance of `_ArgumentDeclaration`, then this object is returned to the
            caller, key used to identify corresponding construction variable
            (`ENV`); if ``None`` the *argument* has no corresponding
            construction variable,
        var_key : string | None
            key used to identify corresponding command-line variable (`VAR`);
            if ``None``, the *argument* has no corresponding command-line
            variable,
        opt_key : string | None
            key used to identify corresponding command-line option (`OPT`);
            if ``None`` the *argument* variable  has no corresponding
            command-line option,
        default
            default value used to initialize corresponding construction
            variable (`ENV`) and command-line variable (`VAR`);
            note that there is separate `opt_default` argument for command-line
            option,
        help : string | None
            message used to initialize help in corresponding command-line
            variable (`VAR`) and command-line option (`OPT`),
        validator
            same as for `SCons.Variables.Variables.Add()`_,
        converter
            same as for `SCons.Variables.Variables.Add()`_,
        option
            option string, e.g. ``"--option"`` used for corresponding
            command-line option,
        type
            same as `type` in `optparse option attributes`_,
        opt_default
            same as `default` in `optparse option attributes`_,
        metavar
            same as `metavar` in `optparse option attributes`_,
        nargs
            same as `nargs` in `optparse option attributes`_,
        choices
            same as `choices` in `optparse option attributes`_,
        action
            same as `action` in `optparse option attributes`_,
        const
            same as `const` in `optparse option attributes`_,
        callback
            same as `callback` in `optparse option attributes`_,
        callback_args
            same as `callback_args` in `optparse option attributes`_,
        callback_kwargs
            same as `callback_kwargs` in `optparse option attributes`_,

    :Returns:
        - if `env_key` is present and it is an instance of `_ArgumentDeclaration`, then it
          is returned unaltered,
        - otherwise returns new `_ArgumentDeclaration` object initialized according to
          rules given above.

    .. _SCons.Variables.Variables.Add(): http://www.scons.org/doc/latest/HTML/scons-api/SCons.Variables.Variables-class.html#Add
    .. _optparse option attributes: http://docs.python.org/2/library/optparse.html#option-attributes
    """
    #------------------------------------------------------------------------
    if isinstance(env_key, _ArgumentDeclaration):
        return env_key
    else:
        # --- ENV ---
        if env_key is not None:
            env_decl = { env_key : default }
        else:
            env_decl = None
        # --- VAR ---
        if var_key is not None:
            items = [ (var_key, 'key'), (default, 'default'), (help, 'help'),
                      (validator, 'validator'), (converter, 'converter') ]
            var_decl = dict([ (k, v) for (v,k) in items if v is not None ])
        else:
            var_decl = None
        # --- OPT ---
        if opt_key and option is not None:
            items = [   (opt_key, 'dest'), (opt_default, 'default'),
                        (help, 'help'), (type, 'type'), (metavar, 'metavar'),
                        (nargs, 'nargs'), (choices, 'choices'),
                        (action, 'action'), (const, 'const'),
                        (callback, 'callback'),
                        (callback_args, 'callback_args'),
                        (callback_kwargs, 'callback_kwargs') ]
            opt_decl = (option, dict( [(k, v) for (v,k) in items if v is not None] ))
        else:
            opt_decl = None
        return _ArgumentDeclaration(env_decl, var_decl, opt_decl)

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
