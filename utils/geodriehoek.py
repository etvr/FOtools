"""
FOTools Custom Geodreieck (Set Square with Protractor) Gizmo
A complete single-file implementation for creating custom geodreieck empty objects in Blender.
"""

import bpy
import gpu
from gpu_extras.batch import batch_for_shader
from mathutils import Matrix
import math

bl_info = {
    "name": "Custom Geodreieck Empty Gizmo",
    "author": "FOTools",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Add > Empty",
    "description": "Create custom geodreieck empty gizmos",
    "category": "Object",
}

# ============================================================================
# Draw Handler
# ============================================================================

class GeodreieckEmptyDrawHandler:
    """Handler for drawing a geodreieck empty gizmo"""
    
    def __init__(self, obj):
        self.obj = obj
        self.shader = gpu.shader.from_builtin('UNIFORM_COLOR')
        
        # Define geodreieck vertices (isosceles right triangle with baseline)
        size = 1.0
        
        # Main triangle outline
        self.triangle_vertices = [
            (-size, 0, 0),      # Left base corner
            (size, 0, 0),       # Right base corner
            (0, size, 0)        # Top apex
        ]
        
        # Baseline parallel marks
        baseline_offset = -0.1
        self.baseline_vertices = [
            (-size, baseline_offset, 0),
            (size, baseline_offset, 0)
        ]
        
        # Center line (from base center to apex)
        self.centerline_vertices = [
            (0, 0, 0),
            (0, size, 0)
        ]
        
        # Protractor arc markings (semicircle along base)
        arc_segments = 18  # Every 10 degrees
        arc_radius = size * 0.9
        self.arc_vertices = []
        for i in range(arc_segments + 1):
            angle = math.pi * i / arc_segments
            x = arc_radius * math.cos(angle) - size * 0.5
            y = arc_radius * math.sin(angle) * 0.3
            self.arc_vertices.append((x, y, 0))
        
        # Angle markers (small radial lines every 10 degrees)
        self.angle_markers = []
        for i in range(0, 19, 1):  # Every 10 degrees
            angle = math.pi * i / 18
            inner_radius = size * 0.85
            outer_radius = size * 0.95
            x1 = inner_radius * math.cos(angle) - size * 0.5
            y1 = inner_radius * math.sin(angle) * 0.3
            x2 = outer_radius * math.cos(angle) - size * 0.5
            y2 = outer_radius * math.sin(angle) * 0.3
            self.angle_markers.extend([(x1, y1, 0), (x2, y2, 0)])
        
        # Combine all vertices for triangle outline
        all_vertices = (
            self.triangle_vertices + 
            self.baseline_vertices + 
            self.centerline_vertices +
            self.arc_vertices +
            self.angle_markers
        )
        
        # Define line indices
        triangle_indices = [(0, 1), (1, 2), (2, 0)]
        baseline_indices = [(3, 4)]
        centerline_indices = [(5, 6)]
        
        # Arc indices
        arc_start = 7
        arc_indices = [(arc_start + i, arc_start + i + 1) for i in range(len(self.arc_vertices) - 1)]
        
        # Angle marker indices
        marker_start = arc_start + len(self.arc_vertices)
        marker_indices = [(marker_start + i, marker_start + i + 1) for i in range(0, len(self.angle_markers), 2)]
        
        all_indices = triangle_indices + baseline_indices + centerline_indices + arc_indices + marker_indices
        
        # Create batch for efficient drawing
        self.batch = batch_for_shader(
            self.shader, 'LINES',
            {"pos": all_vertices},
            indices=all_indices
        )
    
    def draw(self):
        """Draw the geodreieck gizmo"""
        if not self.obj:
            return
        
        # Get object's world matrix
        matrix = self.obj.matrix_world
        
        # Get custom properties or use defaults
        color = self.obj.get("gizmo_color", (0.2, 0.6, 1.0, 1.0))
        line_width = self.obj.get("gizmo_line_width", 2.0)
        
        # Set up GPU state
        gpu.state.line_width_set(line_width)
        gpu.state.blend_set('ALPHA')
        
        # Apply transformation
        self.shader.bind()
        self.shader.uniform_float("color", color)
        
        # Apply object transformation matrix
        gpu.matrix.push()
        gpu.matrix.multiply_matrix(matrix)
        
        # Draw the batch
        self.batch.draw(self.shader)
        
        # Restore matrix
        gpu.matrix.pop()
        
        # Reset GPU state
        gpu.state.blend_set('NONE')

# Global storage for draw handlers
draw_handlers = {}
_draw_handler = None

def draw_callback():
    """Callback function that draws all geodreieck empties"""
    for obj in bpy.data.objects:
        if obj.type == 'EMPTY' and obj.get("geodreieck_gizmo", False):
            if obj.name not in draw_handlers:
                draw_handlers[obj.name] = GeodreieckEmptyDrawHandler(obj)
            draw_handlers[obj.name].draw()

def register_geodreieck_empty_draw():
    """Register the draw handler for all geodreieck empties"""
    return bpy.types.SpaceView3D.draw_handler_add(
        draw_callback, (), 'WINDOW', 'POST_VIEW'
    )

# ============================================================================
# Property Group
# ============================================================================

class GeodreieckEmptyProperties(bpy.types.PropertyGroup):
    """Property group for geodreieck empty settings"""
    size: bpy.props.FloatProperty(
        name="Size",
        default=1.0,
        min=0.01,
        max=100.0
    )
    color: bpy.props.FloatVectorProperty(
        name="Color",
        subtype='COLOR',
        default=(0.2, 0.6, 1.0, 1.0),
        size=4,
        min=0.0,
        max=1.0
    )
    line_width: bpy.props.FloatProperty(
        name="Line Width",
        default=2.0,
        min=1.0,
        max=10.0
    )

# ============================================================================
# Operators
# ============================================================================

class FOT_OT_AddGeodreieckEmpty(bpy.types.Operator):
    """Add a custom geodreieck empty gizmo"""
    bl_idname = "object.fot_add_geodreieck_empty"
    bl_label = "Add Geodreieck Empty"
    bl_description = "Create a custom empty object with a geodreieck gizmo"
    bl_options = {'REGISTER', 'UNDO'}
    
    size: bpy.props.FloatProperty(
        name="Size",
        description="Size of the geodreieck gizmo",
        default=1.0,
        min=0.01,
        max=100.0
    )
    
    color: bpy.props.FloatVectorProperty(
        name="Color",
        subtype='COLOR',
        default=(0.2, 0.6, 1.0, 1.0),
        size=4,
        min=0.0,
        max=1.0
    )
    
    line_width: bpy.props.FloatProperty(
        name="Line Width",
        default=2.0,
        min=1.0,
        max=10.0
    )
    
    def execute(self, context):
        # Create empty object
        empty = bpy.data.objects.new("Geodreieck_Empty", None)
        empty.empty_display_type = 'PLAIN_AXES'
        empty.empty_display_size = self.size
        
        # Store custom properties
        empty["geodreieck_gizmo"] = True
        empty["gizmo_color"] = self.color[:]
        empty["gizmo_line_width"] = self.line_width
        
        # Link to collection
        context.collection.objects.link(empty)
        
        # Set location at 3D cursor
        empty.location = context.scene.cursor.location
        
        # Select the new empty
        bpy.ops.object.select_all(action='DESELECT')
        empty.select_set(True)
        context.view_layer.objects.active = empty
        
        # Force viewport update
        for area in context.screen.areas:
            if area.type == 'VIEW_3D':
                area.tag_redraw()
        
        self.report({'INFO'}, f"Created Geodreieck Empty: {empty.name}")
        return {'FINISHED'}

# ============================================================================
# UI Panel
# ============================================================================

class FOT_PT_GeodreieckEmptyPanel(bpy.types.Panel):
    """Panel for geodreieck empty gizmo controls"""
    bl_label = "Geodreieck Empty Gizmo"
    bl_idname = "FOT_PT_geodreieck_empty"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'FOTools'
    
    def draw(self, context):
        layout = self.layout
        
        # Add button
        layout.operator("object.fot_add_geodreieck_empty", icon='EMPTY_DATA')
        
        # Properties for selected geodreieck empty
        obj = context.active_object
        if obj and obj.type == 'EMPTY' and obj.get("geodreieck_gizmo", False):
            layout.separator()
            layout.label(text="Selected Geodreieck Empty:")
            
            box = layout.box()
            box.prop(obj, '["gizmo_color"]', text="Color")
            box.prop(obj, '["gizmo_line_width"]', text="Line Width")
            box.prop(obj, "empty_display_size", text="Size")

# ============================================================================
# Add Menu Integration
# ============================================================================

def menu_func(self, context):
    """Add to the Add > Empty menu"""
    self.layout.operator(
        FOT_OT_AddGeodreieckEmpty.bl_idname,
        text="Geodreieck Empty",
        icon='EMPTY_DATA'
    )

# ============================================================================
# Registration
# ============================================================================

classes = (
    GeodreieckEmptyProperties,
    FOT_OT_AddGeodreieckEmpty,
    FOT_PT_GeodreieckEmptyPanel,
)

def register():
    """Register addon classes and handlers"""
    global _draw_handler
    
    # Register classes
    for cls in classes:
        bpy.utils.register_class(cls)
    
    # Register draw handler
    _draw_handler = register_geodreieck_empty_draw()
    
    # Add to menu
    bpy.types.VIEW3D_MT_add.append(menu_func)
    
    print("Custom Geodreieck Empty Gizmo registered")

def unregister():
    """Unregister addon classes and handlers"""
    global _draw_handler
    
    # Remove from menu
    bpy.types.VIEW3D_MT_add.remove(menu_func)
    
    # Unregister draw handler
    if _draw_handler:
        bpy.types.SpaceView3D.draw_handler_remove(_draw_handler, 'WINDOW')
    
    # Unregister classes
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    
    # Clear draw handlers
    draw_handlers.clear()
    
    print("Custom Geodreieck Empty Gizmo unregistered")

# ============================================================================
# Script Entry Point
# ============================================================================

if __name__ == "__main__":
    register()
