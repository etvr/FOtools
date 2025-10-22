bl_info = {
    "name": "Camera Ray Caster",
    "author": "Alexander de Bruijn",
    "version": (1, 0),
    "blender": (2, 93, 0),
    "location": "View3D > Sidebar > Ray Cast",
    "description": "Cast rays from camera and visualize them as cylinders",
    "category": "3D View",
}

import bpy
import gpu
import bgl
import numpy as np
from bpy_extras import view3d_utils
from mathutils import Vector, Matrix
from gpu_extras.batch import batch_for_shader

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

class CameraRayCaster(bpy.types.Operator):
    bl_idname = "view3d.camera_ray_caster"
    bl_label = "Cast Ray from Camera"
    bl_options = {'REGISTER', 'UNDO'}
    
    def modal(self, context, event):
        if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
            # Get the active camera
            scene = context.scene
            camera = scene.camera
            
            if not camera:
                self.report({'ERROR'}, "No active camera in the scene")
                return {'CANCELLED'}
            
            # Get mouse coordinates
            x, y = event.mouse_region_x, event.mouse_region_y
            
            # Get ray from camera view
            region = context.region
            rv3d = context.region_data
            
            # Convert 2D mouse position to 3D ray
            view_vector = view3d_utils.region_2d_to_vector_3d(region, rv3d, (x, y))
            ray_origin = view3d_utils.region_2d_to_origin_3d(region, rv3d, (x, y))
            
            # If we're in camera view, use the camera position as origin
            if rv3d.view_perspective == 'CAMERA':
                ray_origin = camera.matrix_world.translation
            
            # Calculate ray end point
            ray_length = context.scene.ray_cast_props.ray_length
            ray_end = ray_origin + view_vector * ray_length
            
            # Create a cylinder mesh to represent the ray
            bpy.ops.mesh.primitive_cylinder_add(
                radius=context.scene.ray_cast_props.cylinder_radius,
                depth=ray_length,
                enter_editmode=False,
                location=(0, 0, 0)
            )
            
            cylinder = context.active_object
            cylinder.name = "Camera_Ray"
            
            # Position and orient the cylinder to match the ray
            direction = ray_end - ray_origin
            direction.normalize()
            
            # Calculate rotation to align cylinder with ray direction
            up_vector = Vector((0, 0, 1))
            if abs(direction.dot(up_vector)) > 0.99:
                # If ray is nearly parallel to Z-axis, use X as reference
                reference = Vector((1, 0, 0))
            else:
                reference = up_vector
            
            # Create rotation matrix
            z_axis = direction
            x_axis = reference.cross(z_axis)
            x_axis.normalize()
            y_axis = z_axis.cross(x_axis)
            
            rotation_matrix = Matrix((
                (x_axis.x, y_axis.x, z_axis.x, 0),
                (x_axis.y, y_axis.y, z_axis.y, 0),
                (x_axis.z, y_axis.z, z_axis.z, 0),
                (0, 0, 0, 1)
            ))
            
            # By default, Blender's cylinder is aligned along Z
            # Set cylinder's position to ray_origin + half ray length in the ray direction
            mid_point = ray_origin + direction * (ray_length / 2)
            cylinder.location = mid_point
            cylinder.rotation_euler = rotation_matrix.to_euler()
            
            # Add origin and endpoint empties for reference
            bpy.ops.object.empty_add(type='PLAIN_AXES', location=ray_origin)
            origin_empty = context.active_object
            origin_empty.name = "Ray_Origin"
            origin_empty.empty_display_size = 0.2
            
            bpy.ops.object.empty_add(type='PLAIN_AXES', location=ray_end)
            end_empty = context.active_object
            end_empty.name = "Ray_End"
            end_empty.empty_display_size = 0.2
            
            # Group the objects
            cylinder.select_set(True)
            origin_empty.select_set(True)
            bpy.context.view_layer.objects.active = cylinder
            bpy.ops.object.parent_set(type='OBJECT')
            
            return {'FINISHED'}
        
        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            return {'CANCELLED'}
        
        return {'RUNNING_MODAL'}
    
    def invoke(self, context, event):
        if context.area.type == 'VIEW_3D':
            # Check if we're in camera view
            rv3d = context.region_data
            if rv3d.view_perspective != 'CAMERA':
                self.report({'WARNING'}, "This operator works best in camera view")
            
            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "View3D not found, cannot run operator")
            return {'CANCELLED'}

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
    

classes = (
    RayCastProperties,
    CameraRayCaster,
    VIEW3D_PT_camera_ray_caster,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.ray_cast_props = bpy.props.PointerProperty(type=RayCastProperties)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.ray_cast_props

if __name__ == "__main__":
    register()