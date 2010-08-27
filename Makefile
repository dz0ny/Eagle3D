all:
	tools/create_eagle_3d.sh
clean:
	tools/clean_eagle_3d.sh
lib:
	tools/create_lib_files.pl --src=./src --build=./build
render: all
	tools/render.sh
release: all
	tools/create_release_files.sh TEST
