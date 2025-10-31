import bpy
import os
from pathlib import Path

def get_addon_directory():
    return Path(__file__).parent

def get_geodreieck_blend_path():
    addon_dir = get_addon_directory()
    blend_path = addon_dir / "../assets" / "geotriangle_w_num.blend"
    return str(blend_path)


class FOT_PT_GeodreieckImporter(bpy.types.Panel):

    """Panel for importing geodreieck"""

    bl_label = "Geodreieck Importer"
   # bl_idname = "FOT_PT_geodreieck_importer"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'FOTools'
    
    def draw(self, context):
        layout = self.layout
        
        box = layout.box()
        box.label(text="Import Geodreieck:", icon='IMPORT')
        # box.operator(
        #     FOT_OT_ImportGeodreieck.bl_idname,
        #     text="Add Geodreieck",
        #     icon='MESH_DATA'
        # )
        box.operator(
            "object.import_geotriangle",
            text="Add Geodreieck"
        )
        
        box = layout.box()
        box.label(text="Info:", icon='INFO')
        blend_path = get_geodreieck_blend_path()
        
        if os.path.exists(blend_path):
            box.label(text="✓ geotriangle.blend found", icon='CHECKMARK')
        else:
            box.label(text="✗ geotriangle.blend not found", icon='ERROR')
            box.label(text="Expected location:")
            
            col = box.column(align=True)
            col.scale_y = 0.8
            col.label(text=blend_path)