import bpy
import os
import toml
from bpy.types import Operator, Panel
from .get_addons import get_addons, get_toml_data
from .utils import has_lower_upper_pair, get_addon_path


activated_addon_name = ""
errors = []


class EXTENSIONREVIEW_OT_ToggleTextbox(Operator):
    bl_idname = "extensionreview.toggle"
    bl_label = "Get Extension Review"

    def execute(self, context):
        message_file = os.path.join(get_addon_path(), "message.toml")

        with open(message_file, "r") as file:
            messages = toml.load(file)

        messages_list = []

        error_messages = {
            "blender_name": messages["blender_name"],
            "remnant_files": messages["remnant_files"],
            "missing_permission_network": messages["missing_permission_network"],
            "missing_permission_file": messages["missing_permission_file"],
            "missing_permission_clipboard": messages["missing_permission_clipboard"],
        }

        warning_messages = {
            "commented_line": messages["commented_line"],
            "underscore_in_name": messages["underscore_in_name"],
            "missing_space_in_name": messages["missing_space_in_name"],
        }

        if errors:
            for error in errors:
                if error in error_messages:
                    messages_list.append(error_messages[error])
                    self.report({"ERROR"}, error_messages[error])
                elif error in warning_messages:
                    messages_list.append(warning_messages[error])
                    self.report({"WARNING"}, warning_messages[error])
        else:
            self.report({"INFO"}, "No errors found.")

        print(messages_list)

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
        global activated_addon_name
        activated_addon_name = ""

        for addon_name in addon_list:
            if getattr(context.scene, addon_name):
                activated_addon_name = addon_name

        for addon_name in addon_list:
            if activated_addon_name == "" or activated_addon_name == addon_name:
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
        has_warnings = False
        has_error = False
        global errors
        addon_name = activated_addon_name

        if addon_name != "" and getattr(context.scene, addon_name):
            errors = []
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

            # Warning Validation
            col.label(text="Warning:")

            box = layout.box()
            row = box.row()

            if warn_line_comment:
                row.scale_y = 0.7
                row.label(text="Commented in the Manifest", icon="ERROR")
                has_warnings = True
                errors.append("commented_line")

            if "_" in addon_name:
                row = box.row()
                row.scale_y = 0.7
                row.label(text="Underscore in the Extension name", icon="ERROR")
                has_warnings = True
                errors.append("underscore_in_name")

            if has_lower_upper_pair(addon_name):
                row = box.row()
                row.scale_y = 0.7
                row.label(
                    text="Lower/Upper pair in the Extension name",
                    icon="ERROR",
                )
                has_warnings = True
                errors.append("missing_space_in_name")

            if not has_warnings:
                row.label(text="No Warnings", icon="INFO")

            row = layout.row()
            col = row.column()

            # Error Validation
            col.label(text="Error:")

            box = layout.box()
            row = box.row()

            if "blender" in addon_name.lower():
                row = box.row()
                row.scale_y = 0.7
                row.label(text="Blender in the Extension name", icon="CANCEL")
                has_error = True
                errors.append("blender_name")

            if not has_error:
                row.label(text="No Errors", icon="INFO")

            row = layout.row()
            col = row.column()

            col.scale_y = 2
            col.operator("extensionreview.toggle", text="Copy Extension Review")
