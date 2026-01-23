# Copilot / AI Agent Instructions for FOTools

Purpose: help AI coding agents become productive quickly when working on this Blender add-on.

Overview
- This repo is a Blender add-on providing forensic 3D utilities (see [README.md](README.md)).
- Core structure:
  - `operators/` — action code (operators invoked from UI or shortcuts), e.g. [operators/deflectioncone_operator.py](operators/deflectioncone_operator.py)
  - `panels/` — UI panels that expose operators to the Blender N-panel, e.g. [panels/sightline_pannel.py](panels/sightline_pannel.py)
  - `utils/` — reusable helper functions, e.g. [utils/add_material.py](utils/add_material.py)
  - `wheel/` — pre-built wheels included; Blender ships its own Python, so dependency installation must target Blender's Python environment.
  - `__init__.py` — addon registration point; classes are imported and registered here. See [__init__.py](__init__.py).

Big-picture notes
- Registration flows through `__init__.py`: new operator/panel classes must be imported and added to the `classes` list, then registered in `register()`.
- Operators mutate Blender scene state and often create/delete objects; many functions are written to mutate Blender data directly (not pure functions).
- Several utilities change Blender render/settings (see README warnings). Be conservative when running code on work-in-progress scenes.

Conventions & patterns (discoverable)
- File naming: operator files end with `_operator.py` (in `operators/`); panel files end with `_panel.py` (in `panels/`).
- Class naming: operator classes commonly use `FOtools_OT_*` or `FOTOOLS_OT_*`; panel classes use `FOTOOLS_PT_*` or `VIEW3D_PT_*`.
- UI registration: many panels append buttons to Blender menus (e.g., `bpy.types.VIEW3D_MT_mesh_add.append(add_visual_protractor_button)` in `__init__.py`).
- Props: Scene-level PointerProperties are declared in `__init__.py` (example: `bpy.types.Scene.ray_cast_props = bpy.props.PointerProperty(type=RayCastProperties)`).

Developer workflows
- Install / run inside Blender: zip the repo and install via Blender Edit → Preferences → Add-ons → Install (see [README.md](README.md)).
- Iterative dev: modify Python files, then in Blender use `Unregister` / `Register` (via addon UI) or restart Blender to reload changes. Calling `register()` from script console is possible but ensure classes are cleaned up via `unregister()`.
- Debug: use Blender's System Console or run Blender with a terminal attached. `print()` calls in `register()` show initialization messages (see [__init__.py](__init__.py)).
- External deps: wheels are included under `wheel/` but must be installed into Blender's Python environment if used. Prefer pure-Python fallbacks where possible.

How to add a new operator (concrete steps)
1. Create `operators/my_new_operator.py` following existing patterns (`bl_idname`, `bl_label`, `execute()` returning `{'FINISHED'}`).
2. Add corresponding UI in `panels/` or append a menu button like other tools.
3. Import the class in `__init__.py` and add it to the `classes` list.
4. Restart or re-register the addon in Blender to test.

What to watch for
- Many operators assume selected objects/active object semantics (see `operators/angle_measurement_operator.py`). Keep selection-handling defensive.
- Some utilities modify render settings or global scene settings — read README warnings before automated runs.

References (examples)
- Add-on entry: [__init__.py](__init__.py)
- Example operator: [operators/deflectioncone_operator.py](operators/deflectioncone_operator.py)
- Example panel: [panels/sightline_pannel.py](panels/sightline_pannel.py)
- Utility helpers: [utils/add_material.py](utils/add_material.py)
- Dependency wheels: [wheel/](wheel/)

If anything here is unclear, tell me which area you want expanded (architecture, adding features, or debug/run commands) and I'll iterate.
