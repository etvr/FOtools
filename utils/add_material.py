'''
Created by Alexander de Bruijn 2022

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

FOtools: a set of blender tools to assist in 3D-Forensic analysis
'''
import bpy

def newMaterial(name: str) -> bpy.types.Material:
    """
    Creates a new Blender material or retrieves an existing one by name.
    If a material with the given name already exists, its node tree will be
    cleared to provide a clean slate for new shader setups.
    """
    mat = bpy.data.materials.get(name)

    if mat is None:
        mat = bpy.data.materials.new(name=name)

    mat.use_nodes = True

    # Clear existing nodes and links to ensure a clean slate for the new shader
    if mat.node_tree:
        mat.node_tree.links.clear()
        mat.node_tree.nodes.clear()

    return mat

def newShader(name: str, shader_type: str, r: float, g: float, b: float,
              emission_strength: float = 1.0, glossy_roughness: float = 0.0) -> bpy.types.Material:

    mat = newMaterial(name)
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    output = nodes.new(type="ShaderNodeOutputMaterial")
    shader = None # Initialize shader to None

    color = (r, g, b, 1) # Blender colors are typically RGBA

    if shader_type == "diffuse":
        shader = nodes.new(type="ShaderNodeBsdfDiffuse")
        shader.inputs[0].default_value = color

    elif shader_type == "emission":
        shader = nodes.new(type="ShaderNodeEmission")
        shader.inputs[0].default_value = color
        shader.inputs[1].default_value = emission_strength

    elif shader_type == "glossy":
        shader = nodes.new(type="ShaderNodeBsdfGlossy")
        shader.inputs[0].default_value = color
        shader.inputs[1].default_value = glossy_roughness
    else:
        raise ValueError(f"Unsupported shader type: {shader_type}. Supported types are 'diffuse', 'emission', 'glossy'.")

    # Link the shader to the material output
    if shader: # Ensure shader was created before linking
        links.new(shader.outputs[0], output.inputs[0])
        return mat
