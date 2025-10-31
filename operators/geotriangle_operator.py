# ============================================================================
# Operator: Import geotriangle
# ============================================================================

import bpy
import os
from pathlib import Path

def get_addon_directory():
    """Get the directory where this addon is installed"""
    return Path(__file__).parent

def get_geodreieck_blend_path():
    """Get the path to the geodreieck.blend file"""
    addon_dir = get_addon_directory()
    blend_path = addon_dir / "../assets" / "geotriangle_w_num.blend"
    return str(blend_path)

class FOT_OT_Importgeotriangle(bpy.types.Operator):
    """Import geotriangle from .blend file"""
    bl_idname = "object.import_geotriangle"
    bl_label = "Import geotriangle"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        blend_path = get_geodreieck_blend_path()
        
        if not os.path.exists(blend_path):
            self.report({'ERROR'}, f"geotriangle file not found: {blend_path}")
            return {'CANCELLED'}
        
        cursor_location = context.scene.cursor.location.copy()
        
        with bpy.data.libraries.load(blend_path, link=False) as (data_from, data_to):
            data_to.objects = [name for name in data_from.objects if name == "geotriangle"]
        
        imported_objects = []
        for obj in data_to.objects:
            if obj is not None:
                context.collection.objects.link(obj)
                obj.location = cursor_location
                imported_objects.append(obj)
        
        if not imported_objects:
            self.report({'WARNING'}, "No 'geotriangle' object found in the .blend file")
            return {'CANCELLED'}
        
        bpy.ops.object.select_all(action='DESELECT')
        for obj in imported_objects:
            obj.select_set(True)
        context.view_layer.objects.active = imported_objects[0]
        
        self.report({'INFO'}, f"Imported {len(imported_objects)} geotriangle object(s)")
        return {'FINISHED'}
    