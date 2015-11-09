"""`SConsArguments.VariablesWrapper`

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

from .Util import UNDEFINED

#############################################################################
class _VariablesWrapper(object):
    """Wrapper class used to overcome several issues with original
    implementation of SCons Variables."""

    #========================================================================
    def __init__(self, variables):
        self.variables = variables

    #========================================================================
    def __getattr__(self, attr):
        return getattr(self.variables, attr)

    #========================================================================
    def Update(self, env, args):
        # One reason why it's reimplemented here is to get rid of env.subst(...)
        # substitutions that are present in the original SCons implementation
        # of Variables.Update(). The other is handling of the special UNDEFINED
        # value. If a variable's value is UNDEFINED, the corresponding construction
        # variable will not be created (env[varname] will raise keyerror,
        # unless it was created by someone else).
        import os
        import sys

        variables = self.variables
        values = {}

        # first set the defaults:
        for option in variables.options:
            if not option.default is None:
                values[option.key] = option.default

        # next set the value specified in the options file
        for filename in variables.files:
            if os.path.exists(filename):
                dir = os.path.split(os.path.abspath(filename))[0]
                if dir:
                    sys.path.insert(0, dir)
                try:
                    values['__name__'] = filename
                    exec(open(filename, 'rU').read(), {}, values)
                finally:
                    if dir:
                        del sys.path[0]
                    del values['__name__']

        # set the values specified on the command line
        if args is None: # pragma: no cover
            args = variables.args

        for arg, value in args.items():
            added = False
            for option in variables.options:
                if arg in list(option.aliases) + [ option.key ]:
                    values[option.key] = value
                    added = True
            if not added:
                variables.unknown[arg] = value

        # put the variables in the environment:
        # (don't copy over variables that are not declared as options)
        for option in variables.options:
            try:
                if values[option.key] is not UNDEFINED:
                    env[option.key] = values[option.key]
            except KeyError: # pragma: no cover
                pass

        # Call the convert functions:
        for option in variables.options:
            if option.converter and option.key in values and values[option.key] is not UNDEFINED:
                value = env.get(option.key)
                try:
                    try:
                        env[option.key] = option.converter(value)
                    except TypeError: # pragma: no cover
                        env[option.key] = option.converter(value, env)
                except ValueError as x: # pragma: no cover
                    raise SCons.Errors.UserError('Error converting option: %s\n%s'%(option.key, x))


        # Finally validate the values:
        for option in variables.options:
            if option.validator and option.key in values:
                option.validator(option.key, env.get(option.key), env)

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
