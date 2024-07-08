import bpy
from .panel import *
from .get_addons import get_addons
from bpy.props import BoolProperty

bl_info = {
    "name": "Extension Reviewer",
    "description": "",
    "author": "Victor Chedeville",
    "version": (0, 0, 1),
    "blender": (4, 2, 0),
    "location": "View3D",
}

bl_idname = __package__


bpy.types.Scene.show_original_manifest = BoolProperty(
    name="Manifest Processing",
    default=True,
    description="Enable Manifest Processing",
)

bpy.types.Scene.error_blender_logo = BoolProperty(
    name="Blender Logo",
    default=False,
    description="Blender Logo is used in the Extension Icon or the Feature Images",
)

bpy.types.Scene.error_missing_files_permission = BoolProperty(
    name="Files Permission",
    default=False,
    description="Files Permission is missing in the Extension Manifest",
)

bpy.types.Scene.error_missing_network_permission = BoolProperty(
    name="Network Permission",
    default=False,
    description="Network Permission is missing in the Extension Manifest",
)

bpy.types.Scene.error_missing_clipboard_permission = BoolProperty(
    name="Clipboard Permission",
    default=False,
    description="Clipboard Permission is missing in the Extension Manifest",
)

bpy.types.Scene.error_missing_tag = BoolProperty(
    name="No Tag",
    default=False,
    description="No Tag is present in the Extension Manifest",
)

bpy.types.Scene.error_wrong_tag = BoolProperty(
    name="Wrong Tag",
    default=False,
    description="The Tag in the Extension Manifest is incorrect",
)

bpy.types.Scene.error_unclear_description = BoolProperty(
    name="Unclear Description",
    default=False,
    description="The Description in the Extension Manifest is unclear",
)

bpy.types.Scene.error_missing_version = BoolProperty(
    name="Missing Version",
    default=False,
    description="The Version in the Extension Manifest is missing",
)

bpy.types.Scene.error_missing_documentation = BoolProperty(
    name="Missing Documentation",
    default=False,
    description="The Documentation in the Extension Manifest is missing",
)

bpy.types.Scene.error_image_not_english = BoolProperty(
    name="Image not in English",
    default=False,
    description="The Image in the Extension Manifest is not in English",
)

bpy.types.Scene.error_description_not_english = BoolProperty(
    name="Description not in English",
    default=False,
    description="The Description in the Extension Manifest is not in English",
)

bpy.types.Scene.error_updater = BoolProperty(
    name="Updater",
    default=False,
    description="The Extension has an Updater",
)

bpy.types.Scene.error_instal_precess_description = BoolProperty(
    name="Installation Process in Description",
    default=False,
    description="The Installation Process is in the Description",
)

bpy.types.Scene.error_license_description = BoolProperty(
    name="License in Description",
    default=False,
    description="The License is in the Description",
)

classes = (
    EXTENSIONREVIEW_PT_Panel,
    EXTENSIONREVIEW_OT_ToggleTextbox,
    EXTENSIONREVIEW_PT_Review,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    addon_list = get_addons()
    for addon in addon_list:
        setattr(
            bpy.types.Scene, addon, bpy.props.BoolProperty(name=addon, default=False)
        )


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    addon_list = get_addons()
    for addon in addon_list:
        delattr(bpy.types.Scene, addon)


if __name__ == "__main__":
    register()
