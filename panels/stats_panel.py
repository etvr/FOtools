'''
FO-Tools: Mesh Statistics Panel

Contains the UI Panel for displaying mesh statistics.
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
'''
import bpy
from . import stats_operator

class FOTOOLS_PT_mesh_info(bpy.types.Panel):
    """Creates a Panel in the 3D View N-Panel to display mesh info"""
    bl_label = "Mesh Info"
    bl_idname = "FOTOOLS_PT_mesh_info"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'FOtools'

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj and obj.type == 'MESH'

    def draw(self, context):
        layout = self.layout
        obj = context.active_object

        stats = stats_operator.get_mesh_stats(obj, context)
        
        col = layout.column(align=True)

        row = col.row()
        row.label(text="Surface Area:")
        row.label(text=f"{stats['area']:.4f} m²")

        row = col.row()
        row.label(text="Volume:")
        row.label(text=f"{stats['volume']:.4f} m³")