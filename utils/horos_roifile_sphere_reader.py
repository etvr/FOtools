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

    FOtools: a set of blender tools to assist in 3D-Forensic analysis Alexander de Bruijn 2022

    the script takes a HOROS Region Of Interest (ROI) file and places blender spheres on the extracted coordinate points.
    HOROS is a software designed for medical image visualization and analysis, particularly in the field of radiology.
    https://horosproject.org
'''

import bpy

# setup
#TODO: native fileselection dialog

roi_file_path = "C:\\Users\\alexander\\OneDrive\\Desktop\\Test ETVR\\rois.txt"
split_string_line = "3D Pos:"
split_string_coordinates = "mm"
sphereradius =5
coordinatelist = []

# store 3d cursor original location
original_3dcursor_position = bpy.context.scene.cursor.location

# read data
roi_file = open(roi_file_path, "rb")
txt = str(roi_file.readline())

# split the data
buffer = txt.split(split_string_line)
buffer.pop(0)

#clean up the coordinates
for item in buffer:
    coordinate_buffer = item.split(split_string_coordinates)
    coordinatelist.append((coordinate_buffer[0][3:-1], coordinate_buffer[1][3:-1], coordinate_buffer[1][3:-1]))
    
# create the roi spheres
for item in coordinatelist:
    print(item)
    roi_location = float(item[0]), float(item[1]), float(item[2])
    bpy.context.scene.cursor.location = roi_location
    bpy.ops.mesh.primitive_uv_sphere_add(radius=sphereradius, segments=32, ring_count=64)
    bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', radius=sphereradius*2)


# set 3d cursor back to original position
bpy.context.scene.cursor.location = original_3dcursor_position