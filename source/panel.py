import bpy
import os
import toml
import subprocess
from bpy.types import Operator, Panel
from .get_addons import get_addons, get_toml_data
from .utils import has_lower_upper_pair, get_addon_path


activated_addon_name = ""
errors = []


class EXTENSIONREVIEW_OT_toggle_textbox(Operator):
    bl_idname = "extensionreview.toggle"
    bl_label = "Get Extension Review"

    def execute(self, context):
        message_file = os.path.join(get_addon_path(), "message.toml")

        with open(message_file, "r") as file:
            messages = toml.load(file)

        messages_list = []
        separator = True
        error_intro_message = False
        warning_intro_message = False

        builder_messages = {
            "intro_message": messages["intro_message"],
            "separator": messages["separator"],
            "error_list": messages["error_list"],
            "warning_list": messages["warning_list"],
        }

        error_messages = {
            "blender_name": messages["blender_name"],
            "blender_logo": messages["blender_logo"],
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
            messages_list.append(builder_messages["intro_message"])
            messages_list.append(builder_messages["separator"])
            for error in errors:
                if error in error_messages:
                    if not error_intro_message:
                        messages_list.append(builder_messages["error_list"])
                        error_intro_message = False

                    separator = False
                    messages_list.append(error_messages[error])
                    self.report({"ERROR"}, error_messages[error])
                elif error in warning_messages:
                    if not separator:
                        messages_list.append(builder_messages["separator"])
                        separator = True
                    if not warning_intro_message:
                        messages_list.append(builder_messages["warning_list"])
                        warning_intro_message = True
                    messages_list.append(warning_messages[error])
                    self.report({"WARNING"}, warning_messages[error])
        else:
            self.report({"INFO"}, "No errors found.")

        for message in messages_list:
            print(message)

        final_message = "\n".join(messages_list)
        subprocess.run("clip", universal_newlines=True, input=final_message)

        return {"FINISHED"}


class WorkSpaceButtonsPanel:
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Get Addons List"


class EXTENSIONREVIEW_PT_panel(WorkSpaceButtonsPanel, Panel):
    bl_label = "Get Addons List"

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


class EXTENSIONREVIEW_PT_review(WorkSpaceButtonsPanel, Panel):
    bl_label = "Review Addon"

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

            # Manual Validation Warning
            col.label(text="Add Warning:")

            box = layout.box()
            row = box.row()
            row.prop(
                context.scene,
                "error_instal_precess_description",
                toggle=False,
                text="Installation Process in Description",
            )

            row = box.row()
            row.prop(
                context.scene,
                "error_license_description",
                toggle=False,
                text="License in Description",
            )

            row = layout.row()
            col = row.column()

            # Warning Validation
            col.label(text="Error:")

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


class EXTENSIONREVIEW_PT_review_error(WorkSpaceButtonsPanel, Panel):
    bl_label = "Review Addon Manual Error"
    bl_parent_id = "EXTENSIONREVIEW_PT_review"
    owner_ids = set()

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        col = row.column()

        # Manual Validation Error
        col.label(text="Add Error:")

        box = layout.box()
        row = box.row()
        row.prop(context.scene, "error_blender_logo", toggle=False, text="Blender Icon")

        row = box.row()
        row.prop(
            context.scene,
            "error_missing_files_permission",
            toggle=False,
            text="Files Permission",
        )

        row = box.row()
        row.prop(
            context.scene,
            "error_missing_network_permission",
            toggle=False,
            text="Network Permission",
        )

        row = box.row()
        row.prop(
            context.scene,
            "error_missing_clipboard_permission",
            toggle=False,
            text="Clipboard Permission",
        )

        row = box.row()
        row.prop(context.scene, "error_missing_tag", toggle=False, text="No Tag")

        row = box.row()
        row.prop(context.scene, "error_wrong_tag", toggle=False, text="Wrong Tag")

        row = box.row()
        row.prop(
            context.scene,
            "error_unclear_description",
            toggle=False,
            text="Unclear Description",
        )

        row = box.row()
        row.prop(
            context.scene,
            "error_missing_documentation",
            toggle=False,
            text="Missing Documentation",
        )

        row = box.row()
        row.prop(
            context.scene,
            "error_image_not_english",
            toggle=False,
            text="Image not in English",
        )

        row = box.row()
        row.prop(
            context.scene,
            "error_description_not_english",
            toggle=False,
            text="Description not in English",
        )

        row = box.row()
        row.prop(
            context.scene,
            "error_updater",
            toggle=False,
            text="Updater in the Add-on",
        )
