'''
FO-Tools: Mesh Statistics Logic

Contains functions for calculating mesh properties.
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
'''
import bpy
import bmesh

def get_mesh_stats(obj: bpy.types.Object, context: bpy.types.Context) -> dict:
    """
    Calculates the surface area and volume of a mesh object.

    Args:
        obj (bpy.types.Object): The mesh object to analyze.
        context (bpy.types.Context): The current Blender context.

    Returns:
        dict: A dictionary with 'area' and 'volume' keys.
    """
    if not obj or obj.type != 'MESH':
        return {'area': 0.0, 'volume': 0.0,'delta_X':0.0, 'delta_Y':0.0, 'delta_Z':0.0, 'distance_v1_v2':0.0}

    depsgraph = context.evaluated_depsgraph_get()
    evaluated_obj = obj.evaluated_get(depsgraph)
    mesh = evaluated_obj.data

    bm = bmesh.new()
    bm.from_mesh(mesh)
    bm.transform(obj.matrix_world)

    area = sum(f.calc_area() for f in bm.faces)
    volume = bm.calc_volume()

    if not (obj and obj.type == 'MESH' and obj.mode == 'EDIT'):  
        deltax = 0.0000
        deltay = 0.0000
        deltaz = 0.0000
        distancev1v2 = 0.0000
    else:
        bm = bmesh.from_edit_mesh(obj.data)
        selected_verts_count = len([v for v in bm.verts if v.select])
        if  (selected_verts_count == 2):
            v1, v2 = [v for v in bm.verts if v.select]
            deltax = v2.co.x - v1.co.x
            deltay = v2.co.y - v1.co.y
            deltaz = v2.co.z - v1.co.z
            distancev1v2 = (deltax**2 + deltay**2 + deltaz**2)**0.5
        else:
            deltax = 0.0000
            deltay = 0.0000
            deltaz = 0.0000
            distancev1v2 = 0.0000

    bm.free()

    return {'area':area, 'volume':abs(volume), 'delta_X':deltax, 'delta_Y':deltay, 'delta_Z':deltax, 'distance_v1_v2':abs(distancev1v2)}