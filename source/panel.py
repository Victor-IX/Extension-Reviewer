import bpy
from bpy.types import Operator, Panel
from .get_addons import get_addons, get_toml_data


class EXTENSIONREVIEW_OT_ToggleTextbox(Operator):
    bl_idname = "extensionreview.toggle"
    bl_label = "Get Extension Review"

    def execute(self, context):
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


class EXTENSIONREVIEW_PT_Review(Panel):
    bl_label = "Review Addon"
    bl_idname = "REVIEWADDON_PT_review"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Get Addons List"

    def draw(self, context):
        layout = self.layout
        addon_list = get_addons()

        
        
        for addon_name in addon_list:
            if getattr(context.scene, addon_name):
                
                row = layout.row()
                col = row.column()
                col.label(text="Options:")
                
                col = row.column()
                row = layout.row()
                row.prop(context.scene, "show_original_manifest", text="Manifest Processing")
                
                
                toml_content, warn_line_comment = get_toml_data(addon_name, context)
                box = layout.box()
                for content in toml_content:
                    row = box.row()
                    row.scale_y = 0.5
                    row.label(text=content)

                row = layout.row()
                col = row.column()


                if warn_line_comment:
                    col.label(text="Warning: Commented line detected", icon="ERROR")

                col.scale_y = 2
                col.operator("extensionreview.toggle", text="Get Extension Review")
