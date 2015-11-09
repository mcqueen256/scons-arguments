"""`SConsArguments`

**Intro**

This package implements SCons *arguments*. A SCons *argument* is an entity
which correlates up to three *endpoints*:

- single construction variable in SCons environment (``env['NAME'], env.subst('$NAME')``),
- single SCons command-line variable (``scons variable=value`` in command-line), and
- single SCons command-line option (``scons --option=value`` in command-line).

Some of the above may be missing in *argument*'s specification, so we may for
example correlate only a construction variable with a command-line option
without involving command-line variable. *Arguments* specify how information
shall flow from command-line to SCons environment.

**Endpoint names and data flow**

Each *argument* has up to three *endpoints*:

- ``ENV`` *endpoint*: a construction variable in SCons environment,
- ``VAR`` *endpoint*: a command line variable, and
- ``OPT`` *endpoint*: a command line option.

Separate "namespaces" are used to keep names of ``ENV``, ``VAR`` and ``OPT``
endpoints (i.e. construction variables, command-line variables and command-line
options). The user defines mappings between *endpoints* when specifying
*arguments*. *Arguments* also have their own names which may be independent of
their endpoint names. For example, one may create an *argument* named ``foo``
which correlates a construction variable named ``ENV_FOO``, command-line
variable named ``VAR_FOO`` and command-line option identified by key
``opt_foo`` (we use ``dest`` attribute of command line option as its
identifying key, see `option attributes`_ of python ``optparse``). At certain
point *arguments* get requested to update SCons environment ``env``, that is
to populate environment with values taken from command-line variables and/or
options.  At this point, value taken from command-line variable ``VAR_FOO`` or
value from command-line option ``opt_foo`` is passed to construction variable
``ENV_FOO``. If both,command-line variable and command-line option are set,
then command-line option takes precedence.

**Substitutions in Arguments**

If a command-line value is a string, it may contain placeholders (e.g.
``VAR_FOO`` may be a string in form ``"bleah bleah ${VAR_BAR}"``, which contains
placeholder ``${VAR_BAR}``). The placeholder is assumed to be the name of
*endpoint* from the same namespace where the placeholder appears. It means,
that if we have a command-line variable, and its value is a string containing
placeholder ``"$VVV"``, then ``VVV`` is assumed to be the name of another
command-line variable (and not, for example, construction variable). When
passing strings from command-line variables and options to a SCons environment,
the placeholders are renamed such that they refer to corresponding construction
variables in SCons environment. This is shown in the example below.

**Example**

Assume, we have the following three *arguments* defined::

    .               (1)         (2)         (3)
    Arguments:      foo         bar         geez
    Environment:    ENV_FOO     ENV_BAR     ENV_GEEZ
    Variables:      VAR_FOO     VAR_BAR     VAR_GEEZ
    Options:        opt_foo     opt_bar     opt_geez
    .             --opt-foo   --opt-bar   --opt-geez


and we invoked scons as follows::

    # Command line:
    scons VAR_FOO='${VAR_BAR}' VAR_BAR='${foo}' --opt-geez='${opt_foo}'

then, after updating a SCons environment ``env`` with *arguments*, the
environment shall have the following construction variables set::

    env['ENV_FOO'] = '${ENV_BAR}'   # VAR_FOO -> ENV_FOO,  VAR_BAR -> ENV_BAR
    env['ENV_BAR'] = '${foo}'       # VAR_BAR -> ENV_BAR,  foo -x-> foo
    env['ENV_GEEZ'] = '${ENV_FOO}'  # opt_geez-> ENV_GEEZ, opt_foo -> ENV_FOO

The arrow ``-x->`` denotes the fact, that there was no command-line variable
named ``foo``, so the ``"${foo}"`` placeholder was left unaltered.

**Example**

The following ``SConstruct`` file defines three *arguments*: ``foo``, ``bar``
and ``geez``. Corresponding construction variables (environment) are named
``ENV_FOO``, ``ENV_BAR`` and ``ENV_GEEZ`` respectively. Corresponding
command-line variables are: ``VAR_FOO``, ``VAR_BAR`` and ``VAR_GEEZ``. Finally,
the command-line options that correspond to our *arguments* are named
``opt_foo``, ``opt_bar`` and ``opt_geez`` (note: these are actually keys
identifying options within SCons script, they may be different from the option
names that user sees on his screen - here we have key ``opt_foo`` and
command-line option ``--foo``).

.. python::

    from SConsArguments import ArgumentDeclarations
    env = Environment()
    decls = ArgumentDeclarations(
       # Argument 'foo'
       foo = (   {'ENV_FOO' : 'ENV_FOO default'},                   # ENV
                 ('VAR_FOO',  'VAR_FOO help'),                      # VAR
                 ('--foo', {'dest' : "opt_foo"})         ),         # OPT
       # Argument 'bar'
       bar = (   {'ENV_BAR' : None},                                # ENV
                 ('VAR_BAR', 'VAR_BAR help', 'VAR_BAR default'),    # VAR
                 ('--bar',  {'dest':"opt_bar", "type":"string"})),  # OPT
       # Argument 'geez'
       geez =(   {'ENV_GEEZ' : None},                               # ENV
                 ('VAR_GEEZ', 'VAR_GEEZ help', 'VAR_GEEZ default'), # VAR
                 ('--geez', {'dest':"opt_geez", "type":"string"}))  # OPT
    )
    variables = Variables()
    args = decls.Commit(env, variables, True)
    args.UpdateEnvironment(env, variables, True)

    print "env['ENV_FOO']: %r" %  env['ENV_FOO']
    print "env['ENV_BAR']: %r" %  env['ENV_BAR']
    print "env['ENV_GEEZ']: %r" %  env['ENV_GEEZ']

Running scons several times for this example, different results may be obtained
depending on command-line variables and options provided. Let's do some
experiments, first show the help message to see available command-line options::

    user@host:$ scons -Q -h
    env['ENV_FOO']: 'ENV_FOO default'
    env['ENV_BAR']: 'VAR_BAR default'
    env['ENV_GEEZ']: 'VAR_GEEZ default'
    usage: scons [OPTION] [TARGET] ...

    SCons Options:
       <.... lot of output here ...>
    Local Options:
      --geez=OPT_GEEZ
      --foo=OPT_FOO
      --bar=OPT_BAR

then play with them a little bit (as well as with command-line variables)::

    user@host:$ scons -Q --foo='OPT FOO'
    env['ENV_FOO']: 'OPT FOO'
    env['ENV_BAR']: 'VAR_BAR default'
    env['ENV_GEEZ']: 'VAR_GEEZ default'
    scons: `.' is up to date.

    user@host:$ scons -Q VAR_FOO='VAR_FOO cmdline'
    env['ENV_FOO']: 'VAR_FOO cmdline'
    env['ENV_BAR']: 'VAR_BAR default'
    env['ENV_GEEZ']: 'VAR_GEEZ default'
    scons: `.' is up to date.

    user@host:$ scons -Q VAR_FOO='VAR_FOO cmdline' --foo='opt_foo cmdline'
    env['ENV_FOO']: 'opt_foo cmdline'
    env['ENV_BAR']: 'VAR_BAR default'
    env['ENV_GEEZ']: 'VAR_GEEZ default'
    scons: `.' is up to date.

    user@host:$ scons -Q VAR_FOO='VAR_FOO and ${VAR_BAR}'
    env['ENV_FOO']: 'VAR_FOO and ${ENV_BAR}'
    env['ENV_BAR']: 'VAR_BAR default'
    env['ENV_GEEZ']: 'VAR_GEEZ default'
    scons: `.' is up to date.

    user@host:$ scons -Q --foo='opt_foo with ${opt_geez}'
    env['ENV_FOO']: 'opt_foo with ${ENV_GEEZ}'
    env['ENV_BAR']: 'VAR_BAR default'
    env['ENV_GEEZ']: 'VAR_GEEZ default'
    scons: `.' is up to date.

*Arguments* are very flexible and provide much more than presented above. The
documentation of `ArgumentDeclarations()`, `ArgumentDeclaration()`, `DeclareArguments()`,
`DeclareArgument()`, `_ArgumentDeclarations`, `_Arguments`, and `_ArgumentDeclaration` shall
be a good starting point for developers and advanced users.

.. _option attributes: http://docs.python.org/2/library/optparse.html#option-attributes
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

from .Declaration import _ArgumentDeclaration, ArgumentDeclaration, DeclareArgument
from .Declarations import _ArgumentDeclarations, ArgumentDeclarations, DeclareArguments
from .Arguments import _Arguments
from .Proxy import  _ArgumentsProxy
from .NameConv import _ArgumentNameConv
from .Util import ENV, VAR, OPT, ALL
from .Util import _missing, MISSING, _undef, UNDEFINED, _notfound, NOTFOUND
from .Util import _resubst, _build_resubst_dict, _build_iresubst_dict, _compose_mappings, _invert_dict
from .VariablesWrapper import _VariablesWrapper

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
