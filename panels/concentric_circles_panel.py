'''
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

FOtools: a set of blender tools to assist in 3D-Forensic analysis Alexander de Bruijn 2025
'''

import bpy

class FOTOOLS_PT_concentric_circles(bpy.types.Panel):
    """Creates a Panel in the FO-Tools Tab"""
    bl_label = "Circular Distance Grid"
    bl_idname = "FOTOOLS_PT_concentric_circles"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "FOtools"

    # Define properties on the scene so they are persistent and accessible
    bpy.types.Scene.concentric_num_circles = bpy.props.IntProperty(
        name="Circles",
        description="How many concentric circles to create",
        default=10,
        min=1,
        max=100
    )
    bpy.types.Scene.concentric_start_radius = bpy.props.FloatProperty(
        name="Start Radius",
        description="The radius of the first circle",
        default=1.0,
        min=0.01,
        unit='LENGTH'
    )
    bpy.types.Scene.concentric_radius_step = bpy.props.FloatProperty(
        name="Radius Step",
        description="The increase in radius for each subsequent circle",
        default=1.0,
        min=0.01,
        unit='LENGTH'
    )
    bpy.types.Scene.concentric_align_to_object = bpy.props.BoolProperty(
        name="Align to Object",
        description="Align the circles to the selected object's orientation",
        default=False
    )
    bpy.types.Scene.concentric_label_size = bpy.props.FloatProperty(
        name="Label Size",
        description="The font size of the radius labels",
        default=0.2,
        min=0.01,
        unit='LENGTH'
    )

    bpy.types.Scene.label_orientation = bpy.props.FloatProperty(
        name="Label orientation",
        description="The direction of the radius labels",
        default=0.0,
        unit='ROTATION'
    )


    def draw(self, context):
        layout = self.layout
        scene = context.scene
        layout.label(text="Select an object as the center:")

        col = layout.column(align=True)
        col.prop(scene, "concentric_num_circles")
        col.prop(scene, "concentric_start_radius")
        col.prop(scene, "concentric_radius_step")

        layout.prop(scene, "concentric_align_to_object")
        layout.prop(scene, "concentric_label_size")
        layout.prop(scene, "label_orientation")

        layout.separator()
        layout.operator("fotools.create_concentric_circles", text="Create Circles", icon="MESH_CIRCLE")