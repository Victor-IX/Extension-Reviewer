import bpy
from bpy.types import Operator, Panel
from .get_addons import get_addons, get_toml_data


class EXTENSIONREVIEW_OT_ToggleTextbox(Operator):
    bl_idname = "extensionreview.toggle_textbox"
    bl_label = "Toggle Text Box"

    def execute(self, context):
        # Placeholder for any future operation needed
        return {"FINISHED"}


class EXTENSIONREVIEW_PT_Panel(Panel):
    bl_label = "Get Addons List"
    bl_idname = "GETADDONSLIST_PT_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Get Addons List"

    def draw(self, context):
        layout = self.layout
        addon_list = get_addons()

        for addon_name in addon_list:
            row = layout.row()
            row.prop(context.scene, addon_name, toggle=True, text=addon_name)

            if getattr(context.scene, addon_name):
                toml_content = get_toml_data(addon_name)
                
                for content in toml_content:
                    layout.label(text=content)
