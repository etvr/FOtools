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
        return {'area': 0.0, 'volume': 0.0}

    depsgraph = context.evaluated_depsgraph_get()
    evaluated_obj = obj.evaluated_get(depsgraph)
    mesh = evaluated_obj.data

    bm = bmesh.new()
    bm.from_mesh(mesh)
    bm.transform(obj.matrix_world)

    area = sum(f.calc_area() for f in bm.faces)
    volume = bm.calc_volume()

    bm.free()

    return {'area': area, 'volume': abs(volume)}