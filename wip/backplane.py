bl_info = {
    "name": "Camera Backplane Creator",
    "author": "Your Name",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Sidebar > Backplane",
    "description": "Creates a plane that fills the camera view at a specified distance (2x size)",
    "category": "Camera",
}

import bpy
import math
from mathutils import Vector

class CAMERA_OT_create_backplane(bpy.types.Operator):
    """Create a plane that fills the camera view at a specified distance"""
    bl_idname = "camera.create_backplane"
    bl_label = "Create Camera Backplane"
    bl_options = {'REGISTER', 'UNDO'}
    
    distance: bpy.props.FloatProperty(
        name="Distance",
        description="Distance from camera",
        default=10.0,
        min=0.1,
        max=1000.0
    )
    
    def execute(self, context):
        camera = context.active_object
        
        if not camera or camera.type != 'CAMERA':
            self.report({'ERROR'}, "Please select a camera")
            return {'CANCELLED'}
        
        cam_data = camera.data
        scene = context.scene
        
        # Calculate render aspect ratio
        render_aspect = scene.render.resolution_x / scene.render.resolution_y
        
        # Get camera parameters and calculate plane dimensions
        if cam_data.type == 'PERSP':
            # Calculate field of view based on sensor fit
            if cam_data.sensor_fit == 'VERTICAL':
                fov_vertical = 2 * math.atan(cam_data.sensor_height / (2 * cam_data.lens))
                height = 2 * self.distance * math.tan(fov_vertical / 2)
                width = height * render_aspect
            elif cam_data.sensor_fit == 'HORIZONTAL':
                fov_horizontal = 2 * math.atan(cam_data.sensor_width / (2 * cam_data.lens))
                width = 2 * self.distance * math.tan(fov_horizontal / 2)
                height = width / render_aspect
            else:  # AUTO
                # Determine fit based on aspect ratio
                sensor_aspect = cam_data.sensor_width / cam_data.sensor_height
                if render_aspect >= sensor_aspect:
                    # Horizontal fit
                    fov_horizontal = 2 * math.atan(cam_data.sensor_width / (2 * cam_data.lens))
                    width = 2 * self.distance * math.tan(fov_horizontal / 2)
                    height = width / render_aspect
                else:
                    # Vertical fit
                    fov_vertical = 2 * math.atan(cam_data.sensor_height / (2 * cam_data.lens))
                    height = 2 * self.distance * math.tan(fov_vertical / 2)
                    width = height * render_aspect
        else:
            # Orthographic camera
            if cam_data.sensor_fit == 'VERTICAL' or (cam_data.sensor_fit == 'AUTO' and render_aspect < 1):
                height = cam_data.ortho_scale
                width = height * render_aspect
            else:
                width = cam_data.ortho_scale
                height = width / render_aspect
        
        # Multiply dimensions by 2 to make plane twice as large
        width *= 2
        height *= 2
        
        # Create plane mesh
        bpy.ops.mesh.primitive_plane_add(size=1)
        plane = context.active_object
        plane.name = f"{camera.name}_backplane"
        
        # Scale plane to exact dimensions (default plane is 2x2)
        plane.scale = (width / 2, height / 2, 1)
        
        # Get camera's world matrix
        cam_matrix = camera.matrix_world
        
        # Calculate position along camera's view direction (negative Z axis)
        view_direction = cam_matrix.to_quaternion() @ Vector((0, 0, -1))
        plane.location = camera.location + (view_direction * self.distance)
        
        # Match camera rotation
        plane.rotation_euler = camera.rotation_euler.copy()
        
        # Parent to camera with proper inverse matrix
        plane.parent = camera
        plane.matrix_parent_inverse = camera.matrix_world.inverted()
        
        # Apply UV projection from camera view
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.uv.project_from_view(camera_bounds=True, correct_aspect=True, scale_to_bounds=False)
        bpy.ops.object.mode_set(mode='OBJECT')
        
        self.report({'INFO'}, f"Created backplane ({width:.2f}x{height:.2f}m, 2x size) at {self.distance}m from camera")
        return {'FINISHED'}

class CAMERA_PT_backplane_panel(bpy.types.Panel):
    """Creates a Panel in the 3D Viewport sidebar"""
    bl_label = "Camera Backplane"
    bl_idname = "CAMERA_PT_backplane"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Backplane"
    
    def draw(self, context):
        layout = self.layout
        
        layout.label(text="Select a camera and click:")
        
        op = layout.operator("camera.create_backplane")

def register():
    bpy.utils.register_class(CAMERA_OT_create_backplane)
    bpy.utils.register_class(CAMERA_PT_backplane_panel)

def unregister():
    bpy.utils.unregister_class(CAMERA_OT_create_backplane)
    bpy.utils.unregister_class(CAMERA_PT_backplane_panel)

if __name__ == "__main__":
    register()
