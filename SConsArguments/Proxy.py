"""`SConsArguments.Proxy`

Provides the `_ArgumentsProxy` class
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
import string
from . import Util

#############################################################################
class _ArgumentsProxy(object):
    #========================================================================
    """Proxy object used to access indirectly variables stored in a **target**
    dictionary. The indirection layer automatically maps variable names between
    two namespaces (**user** and **target**).

    **Example**::

        user@host:$ scons -Q -f -

        import SConsArguments._ArgumentsProxy
        env = Environment()
        proxy = SConsArguments._ArgumentsProxy(env,
                                     { 'foo'     : 'ENV_FOO'     }, # rename
                                     { 'foo'     : '${ENV_FOO}'  }, # resubst
                                     { 'ENV_FOO' : 'foo'         }, # inverse rename
                                     { 'ENV_FOO' : '${foo}'      }) # inverse resubst
        proxy['foo'] = "FOO"
        print "proxy['foo'] is %r" % proxy['foo']
        print "env['ENV_FOO'] is %r" % env['ENV_FOO']
        <Ctl+D>
        proxy['foo'] is 'FOO'
        env['ENV_FOO'] is 'FOO'
        scons: `.' is up to date.
    """
    #========================================================================
    def __init__(self, target, rename={}, resubst={}, irename={}, iresubst={},
                 strict=False):
        # -------------------------------------------------------------------
        """Initializes `_ArgumentsProxy` object.

        :Parameters:
            target
                the **target** dictionary to be accessed via proxy,
            rename
                dictionary used for mapping variable names from **user**
                namespace to **target** namespace (used by `__setitem__()` and
                `__getitem__()`),
            resubst
                dictionary used by to rename placeholders in values passed
                from **user** to **target** (used by `__setitem__()` and
                `subst()`)
            irename
                dictionary used for mapping variable names from **target**
                to **user** namespace (used by ``items()``),
            iresubst
                dictionary used to rename placeholders in values passed
                back from **target** to **user** namespace (used by
                `__getitem__()` for example)
            strict
                if ``True`` only the keys defined in rename/resubst
                dictionaries are allowed, otherwise the original variables
                from ``target`` are also accessible via their keys
        """
        # -------------------------------------------------------------------
        self.target = target
        self._rename_dict = rename
        self._resubst_dict = resubst
        self._irename_dict = irename
        self._iresubst_dict = iresubst
        self.set_strict(strict)

    #========================================================================
    def is_strict(self):
        """Whether the proxy is in "strict" mode

        A "strict" mode proxy allows to access only these variables for which
        entries exist in rename/resubst dictionaries. If some variable is
        missing from dictionaries, a ``KeyError`` is raised.

        A "non-strict" proxy bypasses the rename/resubst dictionaries for
        variables that are not present therein and accesses the corresponding
        variable/option using Argument's name directly (without mapping).

        :Return:
            ``True``, if "strict" mode is enabled or ``False`` otherwise.
        """
        return self.__strict

    #========================================================================
    def set_strict(self, strict):
        """Set the proxy to "strict" or "non-strict" mode

        A "strict" mode proxy allows to access only these variables for which
        entries exist in rename/resubst dictionaries (for which mapping is
        defined). If some variable is not present in dictionaries, a KeyError
        is raised.

        A "non-strict" proxy bypasses the rename/resubst dictionaries for
        variables that are not present therein and accesses the corresponding
        variable/option using Argument's name directly (without mapping).

        :Parameters:
            strict
                determines whether to enable (``True``) or disable (``False``)
                the "strict" mode
        """
        self.__setup_methods(strict)
        self.__strict = strict

    #========================================================================
    def __setup_methods(self, strict):
        # switch between "strict" and "non-strict" mode by replacing certain
        # methods (accessors)
        if strict:
            self.__delitem__impl = self.__delitem__strict
            self.__getitem__impl = self.__getitem__strict
            self.__setitem__impl = self.__setitem__strict
            self.get = self._get_strict
            self.has_key = self._has_key_strict
            self.__contains__impl = self.__contains__strict
            self.items = self._items_strict
        else:
            self.__delitem__impl = self.__delitem__nonstrict
            self.__getitem__impl = self.__getitem__nonstrict
            self.__setitem__impl = self.__setitem__nonstrict
            self.get = self._get_nonstrict
            self.has_key = self._has_key_nonstrict
            self.__contains__impl = self.__contains__nonstrict
            self.items = self._items_nonstrict

    #========================================================================
    def __delitem__(self, key):
        self.__delitem__impl(key)

    #========================================================================
    def __delitem__strict(self, key):
        self.target.__delitem__(self._rename_dict[key])

    #========================================================================
    def __delitem__nonstrict(self, key):
        self.target.__delitem__(self._rename_dict.get(key,key))

    #========================================================================
    def __getitem__(self, key):
        return self.__getitem__impl(key)

    #========================================================================
    def __getitem__strict(self, key):
        target_key = self._rename_dict[key]
        return Util._resubst(self.target[target_key], self._iresubst_dict)

    #========================================================================
    def __getitem__nonstrict(self, key):
        target_key = self._rename_dict.get(key,key)
        return Util._resubst(self.target[target_key], self._iresubst_dict)

    #========================================================================
    def __setitem__(self, key, value):
        return self.__setitem__impl(key, value)

    #========================================================================
    def __setitem__strict(self, key, value):
        # FIXME: What may seem to be irrational is that we actually can't
        # insert to target items that are not already covered by _rename_dict hash.
        # Maybe we should provide some default way of extending _rename_dict when
        # setting new items in strict mode?
        target_key = self._rename_dict[key]
        target_val = Util._resubst(value, self._resubst_dict)
        self.target[target_key] = target_val

    #========================================================================
    def __setitem__nonstrict(self, key, value):
        target_key = self._rename_dict.get(key,key)
        target_val = Util._resubst(value, self._resubst_dict)
        self.target[target_key] = target_val

    #========================================================================
    def _get_strict(self, key, default=None):
        target_key = self._rename_dict[key]
        return Util._resubst(self.target.get(target_key, default), self._iresubst_dict)

    #========================================================================
    def _get_nonstrict(self, key, default=None):
        target_key = self._rename_dict.get(key,key)
        return Util._resubst(self.target.get(target_key, default), self._iresubst_dict)

    #========================================================================
    def _has_key_strict(self, key):
        return self._rename_dict.has_key(key) and self.target.has_key(self._rename_dict[key])

    #========================================================================
    def _has_key_nonstrict(self, key):
        return self.target.has_key(self._rename_dict.get(key,key))

    #========================================================================
    def __contains__(self, key):
        return self.__contains__impl(key)

    #========================================================================
    def __contains__strict(self, key):
        return self._rename_dict.has_key(key) and self.target.__contains__(self._rename_dict[key])

    #========================================================================
    def __contains__nonstrict(self, key):
        return self.target.__contains__(self._rename_dict.get(key,key))

    #========================================================================
    def _items_strict(self):
        iresubst = lambda v : Util._resubst(v, self._iresubst_dict)
        return [ (k, self[k]) for k in self._rename_dict ]

    #========================================================================
    def _items_nonstrict(self):
        iresubst = lambda v : Util._resubst(v, self._iresubst_dict)
        irename = lambda k : self._irename_dict.get(k,k)
        return [ (irename(k), iresubst(v)) for (k,v) in self.target.items() ]

    #========================================================================
    def subst(self, string, *args):
        """Interpolates variables from the **target** dictionary into the
        specific `string`, returning expanded result. This method is only
        guaranteed to work when the **target** dict is a SCons
        ``SubstitutionEnvironment``.

        This is merely same as

        .. python::

            self.target.subst(SConsArguments.Util._resubst(string, self._resubst_dict), *args)


        The core job of interpolating the variables is left to the
        ``target.subst()``. What this method does is to rename placeholders in
        `string` from **user** to **target** namespace before passing it to
        ``target.subst()``.
        """
        return self.target.subst(Util._resubst(string, self._resubst_dict), *args)

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
