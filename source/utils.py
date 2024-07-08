from email.mime import base
import bpy
import os
from . import __package__ as base_package


def has_lower_upper_pair(s):
    for i in range(len(s) - 1):
        if s[i].islower() and s[i + 1].isupper():
            return True
    return False


def get_addon_path():
    # Need this to work with the Blender Development VSCode extension
    if base_package == "source":
        scripts_path = bpy.utils.user_resource("SCRIPTS")
        addon_path = os.path.join(scripts_path, "addons", base_package)
    else:
        scripts_path = bpy.utils.user_resource("EXTENSIONS")
        addon_path = os.path.join(scripts_path, "user_default", base_package)

    print(addon_path)
    if os.path.exists(addon_path):
        print("Path exists")
        return addon_path
    return None
