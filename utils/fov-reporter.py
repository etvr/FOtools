bl_info = {
    "name": "Selected Camera FOV Reporter",
    "author": "LX-ETVR",
    "version": (1, 1, 0),
    "blender": (2, 93, 0),
    "location": "View3D > Sidebar > Camera",
    "description": "Shows horizontal/vertical FOV plus key camera parameters for the selected camera",
    "category": "3D View",
}

import bpy
import math
from mathutils import Euler


def _active_selected_camera(context):
    obj = context.object
    if obj and obj.type == 'CAMERA' and obj.data:
        return obj
    return None


def _effective_render_aspect(scene):
    r = scene.render
    x = r.resolution_x * r.pixel_aspect_x
    y = r.resolution_y * r.pixel_aspect_y
    if x <= 0 or y <= 0:
        return 1.0, 1.0
    return x, y


def _fov_perspective_degrees(cam_data, scene):
    aspect_x, aspect_y = _effective_render_aspect(scene)
    aspect = aspect_x / aspect_y

    lens = cam_data.lens  # mm
    sensor_w = cam_data.sensor_width   # mm
    sensor_h = cam_data.sensor_height  # mm

    fit = cam_data.sensor_fit
    if fit == 'AUTO':
        fit = 'HORIZONTAL' if aspect >= 1.0 else 'VERTICAL'

    if fit == 'HORIZONTAL':
        h_fov = 2.0 * math.atan((sensor_w * 0.5) / lens)
        v_fov = 2.0 * math.atan(((sensor_w / aspect) * 0.5) / lens)
    else:  # 'VERTICAL'
        v_fov = 2.0 * math.atan((sensor_h * 0.5) / lens)
        h_fov = 2.0 * math.atan(((sensor_h * aspect) * 0.5) / lens)

    return math.degrees(h_fov), math.degrees(v_fov)


def _fov_ortho_equivalent_degrees(cam_data, scene):
    aspect_x, aspect_y = _effective_render_aspect(scene)
    aspect = aspect_x / aspect_y

    d = max(cam_data.clip_start, 1e-6)
    view_w = cam_data.ortho_scale
    view_h = cam_data.ortho_scale / aspect

    h = 2.0 * math.atan((view_w * 0.5) / d)
    v = 2.0 * math.atan((view_h * 0.5) / d)
    return math.degrees(h), math.degrees(v)


def camera_fov_degrees(context, cam_obj):
    cam_data = cam_obj.data
    scene = context.scene

    if cam_data.type == 'PERSP':
        return _fov_perspective_degrees(cam_data, scene), "Perspective"
    elif cam_data.type == 'ORTHO':
        return _fov_ortho_equivalent_degrees(cam_data, scene), "Orthographic (equiv @ clip_start)"
    else:
        return (None, None), f"Unsupported camera type: {cam_data.type}"


def _world_euler_degrees(obj, order='XYZ'):
    # matrix_world -> rotation (world space)
    rot_euler = obj.matrix_world.to_euler(order)
    return tuple(math.degrees(a) for a in rot_euler)


class VIEW3D_PT_selected_camera_fov(bpy.types.Panel):
    bl_label = "Selected Camera FOV"
    bl_idname = "VIEW3D_PT_selected_camera_fov"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Camera'

    def draw(self, context):
        layout = self.layout
        cam_obj = _active_selected_camera(context)

        if not cam_obj:
            layout.label(text="Select a camera to see info.")
            return

        cam = cam_obj.data
        (hfov, vfov), mode_label = camera_fov_degrees(context, cam_obj)

        # Header
        layout.label(text=f"Camera: {cam_obj.name}")
        layout.label(text=f"Mode: {mode_label}")

        layout.separator()

        # Lens + sensor
        box = layout.box()
        box.label(text="Optics")
        col = box.column(align=True)

        if cam.type == 'PERSP':
            col.label(text=f"Lens: {cam.lens:.3f} mm")
            col.label(text=f"Sensor: {cam.sensor_width:.3f} × {cam.sensor_height:.3f} mm")
            # col.label(text=f"Sensor Fit: {cam.sensor_fit}")
        elif cam.type == 'ORTHO':
            col.label(text="Lens: (orthographic)")
            col.label(text=f"Ortho Scale: {cam.ortho_scale:.6g}")
            col.label(text=f"Sensor: {cam.sensor_width:.3f} × {cam.sensor_height:.3f} mm")
        else:
            col.label(text="Optics info limited for this type.")

        # FOV
        box = layout.box()
        box.label(text="Field of View")
        col = box.column(align=True)
        if hfov is None or vfov is None:
            col.label(text="FOV unavailable for this camera type.")
        else:
            col.label(text=f"Horizontal FOV: {hfov:.2f}°")
            col.label(text=f"Vertical FOV:   {vfov:.2f}°")
            if cam.type == 'ORTHO':
                col.label(text=f"(Equivalent @ clip_start={cam.clip_start:.6g})")

        # World transform
        box = layout.box()
        box.label(text="World Transform")
        col = box.column(align=True)

        loc = cam_obj.matrix_world.to_translation()
        rx, ry, rz = _world_euler_degrees(cam_obj, order='XYZ')

        col.label(text=f"Location: X {loc.x:.4f}, Y {loc.y:.4f}, Z {loc.z:.4f}")
        col.label(text=f"Rotation (XYZ): X {rx:.2f}°, Y {ry:.2f}°, Z {rz:.2f}°")


classes = (
    VIEW3D_PT_selected_camera_fov,
)


def register():
    for c in classes:
        bpy.utils.register_class(c)


def unregister():
    for c in reversed(classes):
        bpy.utils.unregister_class(c)


if __name__ == "__main__":
    register()