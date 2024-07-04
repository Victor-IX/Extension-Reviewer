from math import e
import os
import bpy
from numpy import add
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

def get_toml_data(addon_name):
    scripts_path = bpy.utils.user_resource("EXTENSIONS")
    path = scripts_path + "/user_default/"
    addon_folder = os.path.join(path, get_addon_folder(addon_name))
    manifest_path = os.path.join(addon_folder, "blender_manifest.toml")
    
    
    print (addon_name)
    print (manifest_path)
    
    if os.path.isfile(manifest_path):
        print ("File exists")
        with open(manifest_path, "r") as file:
            addon_toml = file.readlines()
            return addon_toml
    
    return None

def get_addon_folder(addon_name):
    scripts_path = bpy.utils.user_resource("EXTENSIONS")
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
                        if addon_name == addon_name:
                            return addon_folder
    
    except FileNotFoundError:
        return f"The specified path '{path}' does not exist."
    except PermissionError:
        return f"Permission denied to access the specified path '{path}'."
    except Exception as e:
        return str(e)