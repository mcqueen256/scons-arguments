"""`SConsArguments.NameConv`

This module provides the `_ArgumentNameConv` class.
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

#############################################################################
class _ArgumentNameConv(object):
    """Provides a systematic way to transform *argument* names into keys
    identifying their *endpoints*.

    This object may be helpful when generating multiple *arguments* where
    the *endpoint* names may have to be derived from *argument* names in
    a systematic way. The object provides four lambdas, which may be used
    to transform *argument* names to *endpoint* names. By default, these
    lambdas prepend preset prefixes and append preset suffixes to the name.
    For option keys and names, the original key is lowercased. These prefixes,
    as well as lambdas may be overwritten by user.

    :Ivar env_key_prefix:
        a prefix that is by default prepended to ENV key by the
        `env_key_transform` lambda, default: ``''``
    :Ivar env_key_suffix:
        a suffix that is by default prepended to ENV key by the
        `env_key_transform` lambda, default: ``''``
    :Ivar var_key_prefix:
        a prefix that is by default prepended to VAR key by the
        `var_key_transform` lambda, default: ``''``
    :Ivar var_key_suffix:
        a suffix that is by default prepended to VAR key by the
        `var_key_transform` lambda, default: ``''``
    :Ivar opt_key_prefix:
        a prefix that is by default prepended to OPT key by the
        `opt_key_transform` lambda, default: ``''``
    :Ivar opt_key_suffix:
        a suffix that is by default prepended to OPT key by the
        `opt_key_transform` lambda, default: ``''``
    :Ivar opt_prefix:
        a prefix that is by default used when composing option names,
        usually a single or double dash, default: ``'--'``
    :Ivar opt_name_prefix:
        additional prefix used when composing option names, inserted
        between `opt_prefix` and the *argument* name, default: ``''``
    :Ivar opt_name_suffix:
        a suffix that is by default used when composing option names,
        default: ``''``

    **Example**

    .. python::
        import SConsArguments
        tr = SConsArguments._ArgumentNameConv(env_key_prefix = 'ENV_', env_key_suffix = '_VNE',
                                                var_key_prefix = 'VAR_', var_key_suffix = '_RAV',
                                                opt_key_prefix = 'Opt_', opt_key_suffix = '_tpO',
                                                opt_prefix     = '-',
                                                opt_name_prefix = 'on_', opt_name_suffix = '_no')
        assert(tr.env_key_transform('FOO') == 'ENV_FOO_VNE')
        assert(tr.var_key_transform('FOO') == 'VAR_FOO_RAV')
        assert(tr.opt_key_transform('FOO') == 'Opt_foo_tpO')
        assert(tr.option_transform('FOO')  == '-on-foo-no')
    """
    def __init__(self, **kw):
        """Initializes `_ArgumentNameConv` object.

        :Keywords:
            env_key_prefix : str
                a prefix that is by default prepended to ENV key by the
                **env_key_transform** lambda, default: ``''``
            env_key_suffix : str
                a suffix that is by default prepended to ENV key by the
                **env_key_transform** lambda, default: ``''``
            var_key_prefix : str
                a prefix that is by default prepended to VAR key by the
                **var_key_transform** lambda, default: ``''``
            var_key_suffix : str
                a suffix that is by default prepended to VAR key by the
                **var_key_transform** lambda, default: ``''``
            opt_key_prefix : str
                a prefix that is by default prepended to OPT key by the
                **opt_key_transform** lambda, default: ``''``
            opt_key_suffix : str
                a suffix that is by default prepended to OPT key by the
                **opt_key_transform** lambda, default: ``''``
            opt_prefix : str
                a prefix that is by default used when composing option names,
                usually a single or double dash, default: ``'--'``
            opt_name_prefix : str
                additional prefix used when composing option names, inserted
                between **opt_prefix** and the *argument* name, default: ``''``
            opt_name_suffix : str
                a suffix that is by default used when composing option names,
                default: ``''``
            env_key_transform : callable | bool
                a lambda used to transform *argument* names to construction variables,
                may be customized to completely redefine the way ENV keys are
                transformed, if `env_key_transform` is not callable, then if
                evaluates to ``True`` a default transform is used, or if it
                evaluates to ``False`` a ``lambda x : None`` is used
            var_key_transform : callable | bool
                a lambda used to transform *argument* names to command-line variables,
                may be customized to completely redefine the way VAR keys are
                transformed,  if `env_key_transform` is not callable, then if
                evaluates to ``True`` a default transform is used, or if it
                evaluates to ``False`` a ``lambda x : None`` is used
            opt_key_transform : callable | bool
                a lambda used to transform *argument* names to command-line option keys,
                may be customized to completely redefine the way OPT keys are
                transformed, if `env_key_transform` is not callable, then if
                evaluates to ``True`` a default transform is used, or if it
                evaluates to ``False`` a ``lambda x : None`` is used
            option_transform : callable | bool
                a lambda used to transform *argument* names to command-line options,
                may be customized to completely redefine the way option names are
                transformed, if `env_key_transform` is not callable, then if
                evaluates to ``True`` a default transform is used, or if it
                evaluates to ``False`` a ``lambda x : None`` is used
        """
        def get_lambda(name, default, kw2):
            fcn = kw2.get(name, default)
            if not callable(fcn):
                if fcn:
                    fcn = default
                else:
                    fcn = lambda x : None
            return fcn

        self.env_key_prefix     = kw.get('env_key_prefix', '')
        self.env_key_suffix     = kw.get('env_key_suffix', '')
        self.var_key_prefix     = kw.get('var_key_prefix', '')
        self.var_key_suffix     = kw.get('var_key_suffix', '')
        self.opt_key_prefix     = kw.get('opt_key_prefix', '')
        self.opt_key_suffix     = kw.get('opt_key_suffix', '')
        self.opt_prefix         = kw.get('opt_prefix', '--')
        self.opt_name_prefix    = kw.get('opt_name_prefix', '')
        self.opt_name_suffix    = kw.get('opt_name_suffix', '')

        self._env_key_fcn  = get_lambda('env_key_transform', lambda x : x, kw)
        self._var_key_fcn  = get_lambda('var_key_transform', lambda x : x, kw)
        self._opt_key_fcn  = get_lambda('opt_key_transform', lambda x : x.lower(), kw)
        self._opt_name_fcn = get_lambda('opt_name_transform', lambda x : x.lower(), kw)
        self._option_fcn   = get_lambda('option_transform', lambda x : x.replace('_', '-'), kw)

    def name2env(self, name):
        """Transform *argument* name to corresponding construction variable name.

        :Parameters:
            name : str
                the string to be transformed

        Usage example: ``env_key = NameConv().name2env('foo')``
        """
        s = self._env_key_fcn(name)
        if not s:
            return None
        return self.env_key_prefix + s + self.env_key_suffix

    def name2var(self, name):
        """Transform *argument* name to corresponding command-line variable name.

        :Parameters:
            name : str
                the string to be transformed

        Usage example: ``var_key = NameConv().name2var('foo')``
        """
        s = self._var_key_fcn(name)
        if not s:
            return None
        return self.var_key_prefix + s + self.var_key_suffix

    def name2opt(self, name):
        """Transform *argument* name to corresponding command-line option key.

        :Parameters:
            name : str
                the string to be transformed

        Usage example: ``opt_key = NameConv().name2opt('foo')``
        """
        s = self._opt_key_fcn(name)
        if not s:
            return None
        return self.opt_key_prefix + s + self.opt_key_suffix

    def name2optname(self, name):
        """Transform *argument* name to corresponding command-line option name (without ``--`` prefix).

        :Parameters:
            name : str
                the string to be transformed

        Usage example: ``opt_key = NameConv().name2optname('foo')``
        """
        s = self._opt_name_fcn(name)
        if not s:
            return None
        return self.opt_name_prefix + s + self.opt_name_suffix

    def name2option(self, name):
        """Transform *argument* name to corresponding command-line option name (with ``--`` prefix).

        :Parameters:
            name : str
                the string to be transformed

        Usage example: ``opt_key = NameConv().name2option('foo')``
        """
        s = self.name2optname(name)
        if not s:
            return None
        s = self._option_fcn(s)
        if not s:
            return None
        return self.opt_prefix + s

    def name2dict(self, name):
        """Transform *argument* name to a dictionary possibly containing
        env_key, var_key, opt_key and option.

        :Parameters:
            name : str
                the string to be transformed

        Usage example: ``d = NameConv().name2dict('foo')``
        """
        d = dict()
        env = self.name2env(name)
        var = self.name2var(name)
        opt = self.name2opt(name)
        option  = self.name2option(name)
        if env:     d['env_key'] = env
        if var:     d['var_key'] = var
        if opt:     d['opt_key'] = opt
        if option:  d['option']  = option
        return d

    env_key_transform = name2env
    """Alias for `name2env`"""
    var_key_transform = name2var
    """Alias for `name2var`"""
    opt_key_transform = name2opt
    """Alias for `name2opt`"""
    option_transform = name2option
    """Alias for `name2option`"""

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
