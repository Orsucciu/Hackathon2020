#!/bin/sh

for filename in *
do
	if [[ $filename =~ \.gltf ]]; then
		echo "$filename"
		"CHEMIN VERS BLENDER " --background --python impExp.py -- filename
	fi
done
