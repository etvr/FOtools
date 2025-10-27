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

class RayCastProperties(bpy.types.PropertyGroup):
    ray_length: bpy.props.FloatProperty(
        name="Ray Length", 
        description="Length of the ray cylinder",
        default=10.0,
        min=0.1,
        max=100.0
    )
    
    cylinder_radius: bpy.props.FloatProperty(
        name="Cylinder Radius",
        description="Radius of the ray cylinder",
        default=0.05,
        min=0.01,
        max=1.0
    ) 

class VIEW3D_PT_camera_ray_caster(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Ray Cast'
    bl_label = "Camera Ray Caster"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        ray_cast_props = scene.ray_cast_props
        
        layout.prop(ray_cast_props, "ray_length")
        layout.prop(ray_cast_props, "cylinder_radius")
        layout.operator("view3d.camera_ray_caster", text="Click to Cast Ray")
        
        # Display information
        box = layout.box()
        box.label(text="- Switch to camera view")
        box.label(text="- Click 'Cast Ray and Click in viewport to cast")