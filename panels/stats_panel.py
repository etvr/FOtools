'''
FO-Tools: Mesh Statistics Panel

Contains the UI Panel for displaying mesh statistics.
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
'''
import bpy
from ..operators.stats_operator import get_mesh_stats

class FOTOOLS_PT_mesh_info(bpy.types.Panel):
    """Creates a Panel in the 3D View N-Panel to display mesh info"""
    bl_label = "Mesh Info"
    bl_idname = "FOTOOLS_PT_mesh_info"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'FOtools'

    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        layout = self.layout
        obj = context.active_object

        stats = get_mesh_stats(obj, context)

        col = layout.column(align=True)

        row = col.row()
        row.label(text="Surface Area:")
        row.label(text=f"{stats['area']:.6f} m²")

        row = col.row()
        row.label(text="Volume:")
        row.label(text=f"{stats['volume']:.6f} m³")

        row = col.row()
        row.label(text=" ")

        row = col.row()
        row.label(text="Delta X")
        row.label(text=f"{stats['delta_X']:.6f} m")


        row = col.row()
        row.label(text="Delta Y")
        row.label(text=f"{stats['delta_Y']:.6f} m")

        row = col.row()
        row.label(text="Delta Z")
        row.label(text=f"{stats['delta_Z']:.6f} m")

        row = col.row()
        row.label(text="Distance")
        row.label(text=f"{stats['distance_v1_v2']:.6f} m")