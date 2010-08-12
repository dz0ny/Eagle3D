all:
	tools/create_eagle_3d.sh TEST
clean:
	tools/clean_eagle_3d.sh
lib:
	tools/create_lib_files.pl --src=./src --build=./build
render: all
	tools/render.sh
