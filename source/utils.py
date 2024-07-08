import bpy
import os

def has_lower_upper_pair(s):
    for i in range(len(s) - 1):
        if s[i].islower() and s[i + 1].isupper():
            return True
    return False


def get_addon_path():
    addon_name = __package__

    scripts_path = bpy.utils.user_resource("EXTENSIONS")
    addon_path = os.path.join(scripts_path, "user_default", addon_name)
    
    if os.path.exists(addon_path):
        return addon_path
    return None
