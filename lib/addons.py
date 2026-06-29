# ███╗   ██╗██████╗
# ████╗  ██║██╔══██╗
# ██╔██╗ ██║██║  ██║
# ██║╚██╗██║██║  ██║
# ██║ ╚████║██████╔╝
# ╚═╝  ╚═══╝╚═════╝
#
# ND (Non-Destructive) Blender Add-on
# Copyright (C) 2024 Tristan S. & Ian J. (HugeMenace)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# ---
# Contributors: Tristo (HM)
# ---

import bpy


def get_registered_addon_name():
    path = __name__.split('.')

    # Extensions are registered under a 'bl_ext.<repo>.<id>' module path, whereas
    # legacy add-ons (installed from a .zip) use a single top-level module name.
    if __name__.startswith('bl_ext.'):
        return '.'.join(path[0:3])

    return path[0]


def is_addon_enabled(addon):
    for key in bpy.context.preferences.addons.keys():
        if addon == key:
            return True

    return False
