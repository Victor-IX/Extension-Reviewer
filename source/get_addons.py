from logging import warn
from operator import contains
import os
import bpy
import toml 
       
def get_addons():
    scripts_path = bpy.utils.user_resource("EXTENSIONS")
    addon_list = []
    path = scripts_path + "/user_default/"

    try:
        addons_path = [os.path.join(path, item) for item in os.listdir(path)]

        for addon_folder in addons_path:
            manifest_path = os.path.join(addon_folder, "blender_manifest.toml")

            if os.path.isfile(manifest_path):
                with open(manifest_path, "r") as file:
                    manifest_data = toml.load(file)
                    addon_name = manifest_data.get("name")
                    
                    if addon_name:
                        addon_list.append(addon_name)

        return addon_list

    except FileNotFoundError:
        return f"The specified path '{path}' does not exist."
    except PermissionError:
        return f"Permission denied to access the specified path '{path}'."
    except Exception as e:
        return str(e)


def get_toml_data(addon_name, context):
    scripts_path = bpy.utils.user_resource("EXTENSIONS")
    path = os.path.join(scripts_path, "user_default")
    addon_folder = os.path.join(path, get_addon_folder(addon_name))
    manifest_path = os.path.join(addon_folder, "blender_manifest.toml")

    if os.path.isfile(manifest_path):
        with open(manifest_path, "r") as file:
            addon_toml = file.readlines()
            warn_line_comment = any(line.strip().startswith("#") for line in addon_toml)  
            if context.scene.show_original_manifest:
                addon_toml = [line for line in addon_toml if line.strip() and not line.strip().startswith("#")]
            return addon_toml, warn_line_comment

    return None, False


def get_addon_folder(addon_name):
    scripts_path = bpy.utils.user_resource("EXTENSIONS")
    path = os.path.join(scripts_path, "user_default")

    try:
        addons_path = [os.path.join(path, item) for item in os.listdir(path)]

        for addon_folder in addons_path:
            manifest_path = os.path.join(addon_folder, "blender_manifest.toml")

            if os.path.isfile(manifest_path):
                with open(manifest_path, "r") as file:
                    manifest_data = toml.load(file)
                    test_addon_name = manifest_data.get("name")

                    if test_addon_name == addon_name:
                        return addon_folder

    except FileNotFoundError:
        return f"The specified path '{path}' does not exist."
    except PermissionError:
        return f"Permission denied to access the specified path '{path}'."
    except Exception as e:
        return str(e)
