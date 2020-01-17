#!/usr/bin/python
import bpy
import sys
import os

argv = sys.argv

argv = argv[argv.index("--") + 1:]  # get all args after "--"

print(argv)  # --> ['example', 'args', '123']

if len(argv[0]) > 0:
    inputfile = argv[0]
else:
    print("Error. No inputed file.")

if len(argv) >= 2:
    outputfile = argv[1]
else:
    outputfile = argv[0] + ".stl"

bpy.ops.wm.read_factory_settings(use_empty=True)

bpy.ops.import_scene.gltf(filepath=inputfile)
bpy.ops.export_mesh.stl(filepath=outputfile)
