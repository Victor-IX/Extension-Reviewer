import bpy
from bpy.props import BoolProperty
from bpy.types import Operator
from .get_addons import get_addons, get_toml_data


def iniSceneProperties(scn):
    bpy.types.Scene.show_textbox = BoolProperty(
        name="Show Text Box", description="A boolean property", default=False
    )
    scn["show_textbox"] = False


class EXTENSIONREVIEW_OT_ToggleTextbox(Operator):
    bl_idname = "extensionreview.toggle_textbox"
    bl_label = "Toggle Text Box"

    def execute(self, context):
        scn = context.scene
        scn["show_textbox"] = not scn.get("show_textbox", False)
        self.report(
            {"INFO"}, f"Text box {'shown' if scn['show_textbox'] else 'hidden'}"
        )

        return {"FINISHED"}


class EXTENSIONREVIEW_PT_Panel(bpy.types.Panel):
    bl_label = "Get Addons List"
    bl_idname = "GETADDONSLIST_PT_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Get Addons List"

    def draw(self, context):
        layout = self.layout
        scn = context.scene

        addon_list = get_addons()

        for addon_name in addon_list:
            layout.operator("extensionreview.toggle_textbox", text=addon_name)

        if scn.get("show_textbox", False):
            toml_content = get_toml_data(addon_name)

            for content in toml_content:
                layout.label(text=content)
