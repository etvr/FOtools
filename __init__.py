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

# from .panels.best_fit_line_panel import BestFitLinePanel
# from .operators.best_fit_line_operator import Best_Fit_Line_Operator
from .panels.sightline_pannel import Sightline_analysis_pannel
from .panels.geonode_pointcloud_pannel import Geonode_pointcloud_Panel
from .panels.impact_backprojection_panel import Backprojection_Panel
from .panels.boolean_cutter_panel import Boolcut_Panel
from .panels.protractor_panel import Protractor_Panel
from .operators.deflectioncone_operator import FOtools_OT_DeflectionCone
from .operators.bool_cut_operator import FOtools_OT_Bool_cut
from .operators.protractor_operator import FOtools_OT_Protractor
from .operators.frustum_operator import FOtools_OT_Frustum
from .operators.geonode_operator import FOtools_OT_GeonodePointcloud
from .operators.sightline_operator import FOtools_OT_Sightlines
from .operators.clean_voxel_mesh_operator import MESH_OT_remove_close_faces
from .operators.create_voxelmesh_from_p_cloud_operator import FOtools_OT_CreateVoxelMeshFromCloud
from .operators.import_ply_file_operator import FOtools_OT_ImportPLY
from .panels.best_fit_primitive_panel import FOTOOLS_PT_fit_panel
from .operators.fit_primitive import FOTOOLS_OT_fit_plane, FOTOOLS_OT_fit_line
from .operators.fit_primitive import FOTOOLS_OT_fit_sphere
from .operators.fit_primitive import FOTOOLS_OT_fit_cylinder
from .operators.fit_primitive import FOTOOLS_OT_fit_circle
from .operators.visual_angle_protractor_operator import OBJECT_OT_add_angle_protractor
from .operators.visual_angle_protractor_operator import add_visual_protractor_button
from .operators.concentric_circles_operator import FOTOOLS_OT_concentric_circles
from .panels.concentric_circles_panel import FOTOOLS_PT_concentric_circles
from .operators.angle_measurement_operator import FOTOOLS_OT_MeasureAngle
from .panels.angle_measurement_panel import FOTOOLS_PT_AngleMeasurementPanel
from .panels.advanced_ruler_panel import FOTOOLS_PT_AdvancedRulerPanel
from .operators.advanced_ruler_operator import FOTOOLS_OT_AdvancedDrawRuler    
from .utils import add_material
from .panels.stats_panel import FOTOOLS_PT_mesh_info
from .operators.stats_operator import get_mesh_stats


# bl_info = {
#     "name": "FOtools",
#     "description": "3D-forensic Utillities for Blender by ETVR, https://www.politie.nl/informatie/expertteam-visualisatie-en-reconstructie.html",
#     "author": "Alexander de Bruijn",
#     "version": (0, 2, 1),
#     "blender": (4, 4, 0),
#     "wiki_url": "https://github.com/etvr/fotools",
#     "tracker_url": "https://github.com/etvr/fotools",
#     "category": "Generic"
# }


classes = [
    Backprojection_Panel,
    FOtools_OT_DeflectionCone,
    Boolcut_Panel,
    Protractor_Panel,
    Sightline_analysis_pannel,
    Geonode_pointcloud_Panel,
    FOtools_OT_Frustum,
    FOtools_OT_Sightlines,
    FOtools_OT_GeonodePointcloud,
    FOtools_OT_Protractor,
    FOtools_OT_CreateVoxelMeshFromCloud,
    FOtools_OT_Bool_cut,
    FOtools_OT_ImportPLY,
    FOTOOLS_OT_fit_line,
    MESH_OT_remove_close_faces,
    FOTOOLS_OT_fit_plane,
    FOTOOLS_OT_fit_sphere,
    FOTOOLS_OT_fit_cylinder,
    FOTOOLS_OT_fit_circle,
    FOTOOLS_PT_fit_panel,
    FOTOOLS_OT_concentric_circles,
    FOTOOLS_PT_concentric_circles,
    FOTOOLS_OT_MeasureAngle,
    FOTOOLS_PT_AngleMeasurementPanel,
    FOTOOLS_PT_AdvancedRulerPanel,
    FOTOOLS_OT_AdvancedDrawRuler,
    FOTOOLS_PT_mesh_info,
    get_mesh_stats
    ]


def register():
    add_material.register()
    print("Registering Protractor Operator")
    bpy.utils.register_class(OBJECT_OT_add_angle_protractor)
    bpy.types.VIEW3D_MT_mesh_add.append(add_visual_protractor_button)
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    add_material.unregister()
    bpy.utils.unregister_class(OBJECT_OT_add_angle_protractor)
    bpy.types.VIEW3D_MT_mesh_add.remove(add_visual_protractor_button)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()

    ''''
    #from the blender documentation:
    # https://docs.blender.org/manual/en/latest/advanced/scripting/python_api/interactive

    
    # In the middle of a script you may want to inspect variables, run functions and inspect the flow.

    import code
    code.interact(local=locals())
    
    # If you want to access both global and local variables run this:

    import code
    namespace = globals().copy()
    namespace.update(locals())
    code.interact(local=namespace)
    
    # The next example is an equivalent single line version of the script above which is easier to paste into your code:

    __import__('code').interact(local=dict(globals(), **locals()))
    
    # code.interact can be added at any line in the script and will pause the script to launch an interactive interpreter in the terminal, when you’re done you can quit the interpreter and the script will continue execution.

    # If you have IPython installed you can use its embed() function which uses the current namespace. The IPython prompt has auto-complete and some useful features that the standard Python eval-loop doesn’t have.

    import IPython
    IPython.embed()
    
    # Admittedly this highlights the lack of any Python debugging support built into Blender, but its still a handy thing to know.
'''