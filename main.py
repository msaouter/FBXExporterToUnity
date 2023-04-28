bl_info = {
    "name": "FBX Exporter to Unity",
    "description": "Setup an object and export it to use it in Unity",
    "author": "Marion Saouter",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "3D View > Tools",
    "warning": "",  # used for warning icon and text in addons panel
    "wiki_url": "",
    "tracker_url": "",
    "category": "Development"
}

import bpy
from math import radians

from bpy.types import (Panel,
                       Operator,
                       )


# ------------------------------------------------------------------------
#    Scene Properties
# ------------------------------------------------------------------------

# ------------------------------------------------------------------------
#    Operators
# ------------------------------------------------------------------------

class PrepareObject(Operator):
    bl_label = "Prepare Object"
    bl_idname = "object.prepare_for_export"

    def execute(self, context):
        current_obj = bpy.context.selected_objects[0]

        # Set origin to center of mass
        bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')

        # Move obj at (0,0,0)
        current_obj.location[0] = 0
        current_obj.location[1] = 0
        current_obj.location[2] = 0

        # Check transform affect only rotation
        if current_obj.rotation_euler.x < 1.57:
            bpy.context.scene.tool_settings.use_transform_data_origin = True

            # Rotate obj
            bpy.ops.transform.rotate(value=radians(-90), orient_axis='X')
            bpy.context.scene.tool_settings.use_transform_data_origin = False

        return {'FINISHED'}


# ------------------------------------------------------------------------
#    Menus
# ------------------------------------------------------------------------


# ------------------------------------------------------------------------
#    Panel in Object Mode
# ------------------------------------------------------------------------

class OBJECT_PT_FBXExporterPanel(Panel):
    bl_label = "FBX Unity Exporter"
    bl_idname = "OBJECT_PT_FBXExporterPanel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_category = "Tools"
    bl_context = "object"

    @classmethod
    def poll(self, context):
        return context.object is not None

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.operator("object.prepare_for_export", text="Prepare for export")
        op = layout.operator("export_scene.fbx", text="Export")
        op.filepath = bpy.path.abspath("//{}.fbx".format(bpy.context.selected_objects[0].name))
        op.batch_mode = 'OFF'
        op.use_selection = True
        op.use_active_collection = True
        op.object_types = {"MESH"}
        op.apply_scale_options = 'FBX_SCALE_UNITS'
        op.axis_forward = 'Z'
        op.bake_space_transform = False
        op.add_leaf_bones = False
        op.bake_anim = False


# ------------------------------------------------------------------------
#    Registration
# ------------------------------------------------------------------------

classes = (
    PrepareObject,
    OBJECT_PT_FBXExporterPanel
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)


if __name__ == "__main__":
    register()