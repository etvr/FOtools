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
'''

import bpy

class Protractor_Panel(bpy.types.Panel):
    bl_label = "Draw Given Triangle tool"
    bl_idname = "ETVR_PT_FO_protractor_tools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    #bl_context = "objectmode"
    bl_category = "FOtools"

    bpy.types.Scene.vertical_protractor_angle = bpy.props.FloatProperty( name="Vertical Angle", description=" Angle for the vertical angle polygon", min=0.0, max=360.0, default=44.0,)
    bpy.types.Scene.horizontal_protractor_angle = bpy.props.FloatProperty( name="Horizontal Angle", description=" Angle for the horizontal angle polygon", min=0.0, max=360.0, default=44.0,)
    bpy.types.Scene.protractor_radius = bpy.props.FloatProperty( name="Radius", description=" Radius of the drawn polygon", min=0.0, max=100.0, default=1.0,)

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True

        self.layout.prop(context.scene, "vertical_protractor_angle")
        self.layout.prop(context.scene, "horizontal_protractor_angle")
        self.layout.prop(context.scene, "protractor_radius")
        self.layout.separator_spacer()
        self.layout.operator("mesh.protractor_angle", text="Create Angle", icon="DRIVER_ROTATIONAL_DIFFERENCE")
        self.layout.operator("mesh.draw_frustum", text="Create Frustum", icon="VIEW_CAMERA_UNSELECTED")