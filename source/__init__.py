import bpy
from .panel import *
from .get_addons import get_addons

bl_info = {
    "name": "Extension Reviewer",
    "description": "",
    "author": "Victor Chedeville",
    "version": (0, 0, 1),
    "blender": (4, 2, 0),
    "location": "View3D",
}

classes = (EXTENSIONREVIEW_PT_Panel, EXTENSIONREVIEW_OT_ToggleTextbox)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    addon_list = get_addons()
    for addon in addon_list:
        setattr(bpy.types.Scene, addon, bpy.props.BoolProperty(name=addon, default=False))

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    
    addon_list = get_addons()
    for addon in addon_list:
        delattr(bpy.types.Scene, addon)

if __name__ == "__main__":
    register()
