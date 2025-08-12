'''
Created by Alexander de Bruijn 2025,


    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

FOtools: a set of blender tools to assist in 3D-Forensic analysis
This file contains the operator to create concentric circles.
'''

import bpy
from math import radians
from mathutils import Euler, Vector

class FOTOOLS_OT_concentric_circles(bpy.types.Operator):
    """Create concentric circles around the active object based on panel settings"""
    bl_idname = "fotools.create_concentric_circles"
    bl_label = "Create Concentric Circles"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        # This operator should only be active in Object Mode with an active object
        return context.active_object is not None and context.mode == 'OBJECT'

    def _create_circle_and_label(self, context, radius, center, parent, target_obj, align, label_size, label_orientation):
        """
        Helper function to create a single circle and its corresponding label,
        and parent them to a given object.
        """
        bpy.ops.mesh.primitive_circle_add(
            vertices=64,
            radius=radius,
            fill_type='NOTHING',
            align='WORLD',
            location=center
        )
        circle_obj = context.active_object
        circle_obj.name = f"Circle_Radius_{radius:.2f}".replace('.', '_')
        circle_obj.parent = parent

        # Define the label's position relative to the circle's center
        label_offset_local = Vector((radius, 0, 0))

        if align:
            # Align to target object's rotation
            target_rotation_matrix = target_obj.rotation_euler.to_matrix()

            # Apply target's rotation to the circle
            circle_obj.rotation_euler = target_obj.rotation_euler

            # Calculate world position for the label by rotating the local offset
            label_location_world = center + (target_rotation_matrix @ label_offset_local)

            rot_x_90 = Euler((radians(label_orientation), 0, 0), 'XYZ')

            final_rotation_matrix = target_rotation_matrix @ rot_x_90.to_matrix()
            label_rotation_euler = final_rotation_matrix.to_euler('XYZ')
        else:
            # Default world alignment (no rotation for circle)
            label_location_world = center + label_offset_local

            label_rotation_euler = Euler((radians(label_orientation), 0, 0), 'XYZ')

        # Create the text object with the calculated position and rotation
        bpy.ops.object.text_add(location=label_location_world, rotation=label_rotation_euler)
        label_obj = context.active_object
        label_obj.name = f"Label_Radius_{radius:.2f}".replace('.', '_')
        label_obj.data.body = f"{radius:.2f}"
        label_obj.data.align_x = 'CENTER'
        label_obj.data.align_y = 'CENTER'
        label_obj.data.size = label_size
        label_obj.parent = parent

    def execute(self, context):
        target_obj = context.active_object

        center_location = target_obj.location

        # Create a parent empty to group the circles and labels

        bpy.ops.object.empty_add(type='PLAIN_AXES', location=center_location)
        parent_empty = context.active_object
        parent_empty.name = "Concentric_Circles_Group"

        # Get properties from the scene, set by the panel
        scene = context.scene
        num_circles = scene.concentric_num_circles
        start_radius = scene.concentric_start_radius
        radius_step = scene.concentric_radius_step
        align_to_object = scene.concentric_align_to_object
        label_size = scene.concentric_label_size
        label_orientation = scene.label_orientation

        for i in range(num_circles):
            radius = start_radius + (i * radius_step)
            self._create_circle_and_label(
                context,
                radius,
                center_location,
                parent_empty,
                target_obj,
                align_to_object,
                label_size,
                label_orientation
            )

        # Restore original selection
        context.view_layer.objects.active = target_obj
        target_obj.select_set(True)
        parent_empty.select_set(False)

        self.report({'INFO'}, f"Created {num_circles} concentric circles around '{target_obj.name}'")
        return {'FINISHED'}