import bpy
from .panel import *

bl_info = {
    "name": "Extension Reviewer",
    "description": "",
    "author": "Victor Chedeville",
    "version": (0, 0, 1),
    "blender": (4, 2, 0),
    "location": "View3D",
}

classes = (EXTENSIONREVIEW_PT_Panel,EXTENSIONREVIEW_OT_ToggleTextbox)

        
def register():
    for cls in classes:
        bpy.utils.register_class(cls)




def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
