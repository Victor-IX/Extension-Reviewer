import bpy
import json
from bpy.types import Operator, Panel
from numpy import add
from .get_addons import get_addons, get_toml_data
from .utils import has_lower_upper_pair


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
        has_warnings = False
        has_error = False

        for addon_name in addon_list:
            if getattr(context.scene, addon_name):
                row = layout.row()
                col = row.column()
                col.label(text="Options:")

                col = row.column()
                row = layout.row()
                row.prop(
                    context.scene, "show_original_manifest", text="Manifest Processing"
                )

                toml_content, warn_line_comment = get_toml_data(addon_name, context)

                row = layout.row()
                col = row.column()
                col.label(text="Blender Manifest:")

                box = layout.box()

                for content in toml_content:
                    row = box.row()
                    row.scale_y = 0.5
                    row.label(text=content)

                row = layout.row()
                col = row.column()
                col.label(text="Warning:")

                box = layout.box()
                row = box.row()

                if warn_line_comment:
                    row.scale_y = 0.7
                    row.label(text="Commented in the Manifest", icon="ERROR")
                    has_warnings = True

                if "_" in addon_name:
                    row = box.row()
                    row.scale_y = 0.7
                    row.label(
                        text="Underscore in the Extension name", icon="ERROR"
                    )
                    has_warnings = True

                if has_lower_upper_pair(addon_name):
                    row = box.row()
                    row.scale_y = 0.7
                    row.label(
                        text="Lower/Upper pair in the Extension name",
                        icon="ERROR",
                    )
                    has_warnings = True

                if not has_warnings:
                    row.label(text="No Warnings", icon="INFO")

                row = layout.row()
                col = row.column()
                col.label(text="Error:")

                box = layout.box()
                row = box.row()

                if "blender" in addon_name.lower():
                    row = box.row()
                    row.scale_y = 0.7
                    row.label(
                        text="Blender in the Extension name", icon="CANCEL"
                    )
                    has_error = True

                if not has_error:
                    row.label(text="No Errors", icon="INFO")

                row = layout.row()
                col = row.column()
               
                col.scale_y = 2
                col.operator("extensionreview.toggle", text="Copy Extension Review")
