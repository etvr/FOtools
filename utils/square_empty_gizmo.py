"""
FOTools Custom Square Empty Gizmo
A complete single-file implementation for creating custom square empty objects in Blender.
"""

import bpy
import gpu
from gpu_extras.batch import batch_for_shader
from mathutils import Matrix

bl_info = {
    "name": "Custom Square Empty Gizmo",
    "author": "FOTools",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Add > Empty",
    "description": "Create custom square empty gizmos",
    "category": "Object",
}

# ============================================================================
# Draw Handler
# ============================================================================

class SquareEmptyDrawHandler:
    """Handler for drawing a square empty gizmo"""
    
    def __init__(self, obj):
        self.obj = obj
        self.shader = gpu.shader.from_builtin('UNIFORM_COLOR')
        
        # Define square vertices (2D coordinates)
        size = 1.0
        self.vertices = [
            (-size, -size, 0),
            (size, -size, 0),
            (size, size, 0),
            (-size, size, 0)
        ]
        
        # Define line indices for the square outline
        self.indices = [(0, 1), (1, 2), (2, 3), (3, 0)]
        
        # Create batch for efficient drawing
        self.batch = batch_for_shader(
            self.shader, 'LINES',
            {"pos": self.vertices},
            indices=self.indices
        )
    
    def draw(self):
        """Draw the square gizmo"""
        if not self.obj:
            return
        
        # Get object's world matrix
        matrix = self.obj.matrix_world
        
        # Get custom properties or use defaults
        color = self.obj.get("gizmo_color", (1.0, 0.5, 0.0, 1.0))
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
    """Callback function that draws all square empties"""
    for obj in bpy.data.objects:
        if obj.type == 'EMPTY' and obj.get("square_gizmo", False):
            if obj.name not in draw_handlers:
                draw_handlers[obj.name] = SquareEmptyDrawHandler(obj)
            draw_handlers[obj.name].draw()

def register_square_empty_draw():
    """Register the draw handler for all square empties"""
    return bpy.types.SpaceView3D.draw_handler_add(
        draw_callback, (), 'WINDOW', 'POST_VIEW'
    )

# ============================================================================
# Property Group
# ============================================================================

class SquareEmptyProperties(bpy.types.PropertyGroup):
    """Property group for square empty settings"""
    size: bpy.props.FloatProperty(
        name="Size",
        default=1.0,
        min=0.01,
        max=100.0
    )
    color: bpy.props.FloatVectorProperty(
        name="Color",
        subtype='COLOR',
        default=(1.0, 0.5, 0.0, 1.0),
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

class FOT_OT_AddSquareEmpty(bpy.types.Operator):
    """Add a custom square empty gizmo"""
    bl_idname = "object.fot_add_square_empty"
    bl_label = "Add Square Empty"
    bl_description = "Create a custom empty object with a square gizmo"
    bl_options = {'REGISTER', 'UNDO'}
    
    size: bpy.props.FloatProperty(
        name="Size",
        description="Size of the square gizmo",
        default=1.0,
        min=0.01,
        max=100.0
    )
    
    color: bpy.props.FloatVectorProperty(
        name="Color",
        subtype='COLOR',
        default=(1.0, 0.5, 0.0, 1.0),
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
        empty = bpy.data.objects.new("Square_Empty", None)
        empty.empty_display_type = 'PLAIN_AXES'
        empty.empty_display_size = self.size
        
        # Store custom properties
        empty["square_gizmo"] = True
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
        
        self.report({'INFO'}, f"Created Square Empty: {empty.name}")
        return {'FINISHED'}

# ============================================================================
# UI Panel
# ============================================================================

class FOT_PT_SquareEmptyPanel(bpy.types.Panel):
    """Panel for square empty gizmo controls"""
    bl_label = "Square Empty Gizmo"
    bl_idname = "FOT_PT_square_empty"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'FOTools'
    
    def draw(self, context):
        layout = self.layout
        
        # Add button
        layout.operator("object.fot_add_square_empty", icon='EMPTY_DATA')
        
        # Properties for selected square empty
        obj = context.active_object
        if obj and obj.type == 'EMPTY' and obj.get("square_gizmo", False):
            layout.separator()
            layout.label(text="Selected Square Empty:")
            
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
        FOT_OT_AddSquareEmpty.bl_idname,
        text="Square Empty",
        icon='EMPTY_DATA'
    )

# ============================================================================
# Registration
# ============================================================================

classes = (
    SquareEmptyProperties,
    FOT_OT_AddSquareEmpty,
    FOT_PT_SquareEmptyPanel,
)

def register():
    """Register addon classes and handlers"""
    global _draw_handler
    
    # Register classes
    for cls in classes:
        bpy.utils.register_class(cls)
    
    # Register draw handler
    _draw_handler = register_square_empty_draw()
    
    # Add to menu
    bpy.types.VIEW3D_MT_add.append(menu_func)
    
    print("Custom Square Empty Gizmo registered")

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
    
    print("Custom Square Empty Gizmo unregistered")

# ============================================================================
# Script Entry Point
# ============================================================================

if __name__ == "__main__":
    register()
