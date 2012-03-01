# cerbero - a multi-platform build system for Open Source software
# Copyright (C) 2012 Andoni Morales Alastruey <ylatuya@gmail.com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.


from cerbero.commands import Command, register_command
from cerbero.cookbook import CookBook
from cerbero.errors import FatalError
from cerbero.utils import _, N_, ArgparseArgument


class Check(Command):
    doc = N_('Run checks on a given recipe')
    name = 'check'

    def __init__(self):
        Command.__init__(self,
            [ArgparseArgument('recipe', nargs=1,
                             help=_('name of the recipe to run checks on')),
            ])

    def run(self, config, args):
        cookbook = CookBook.load(config)
        recipe_name = args.recipe[0]

        recipe = cookbook.get_recipe(recipe_name)
        if recipe is None:
            raise FatalError(_("Recipe %s not found" % recipe_name))

        if cookbook.recipe_needs_build(recipe_name):
            raise FatalError(_("Recipe %s is not build yet" % recipe_name))

        # call step function
        stepfunc = None
        try:
            stepfunc = getattr(recipe, 'check')
        except:
            print 'no check step'

        if stepfunc:
            try:
                stepfunc()
            except FatalError, e:
                raise e
            except Exception, ex:
                raise FatalError(_("Error running checks: %s") % (ex))

register_command(Check)