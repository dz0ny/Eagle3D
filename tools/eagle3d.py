#! /usr/bin/env python
# -*- coding: utf-8 -*-

from optparse import OptionParser
import datetime
import glob
import logging
import os
import re
import shutil
import subprocess
import sys

import fileinput

#SCRIPT_VERSION = "3.00"
SCRIPT_VERSION = "2.02"
#SCRIPT_NAME = "Eagle3D INC SRC Compiler v%s"%SCRIPT_VERSION
SCRIPT_NAME = "INC SRC Compiler v%s"%SCRIPT_VERSION

INCLUDE_FILE_SUFFIX = '.inc.src'

INCLUDE_PREFIX_MAP = {
	'cap': 'CAP_',
	'capwima': 'CAP_',
	'connector': 'CON_',
	'diode': 'DIODE_',
	'ic': 'IC_',
	'qfp': 'QFP_',
	'resistor': 'RES_',
	'socket': 'SOCKET_',
	'special': 'SPC_',
	'switch': 'SWITCH_',
	'trafo': 'TRAFO_',
	'transistor': 'TR_'
}

MACRO_PARAM_PATTERNS = [
	['', ''],
	['value,col,tra,height',           '"POV",Red,0.7,0'],
	['col,tra,height',                 'Red,0.7,0'],
	['col,tra',                        'Red,0.7'],
	['color_sub',                      'DarkWood'],
	['value,logo',                     '"POV",""'],
	['value,height',                   '"POV",3'],
	['value',                          '"POV"'],
	['name,logo',                      '"POV",""'],
	['name',                           '"POV"'],
	['height',                         '3'],
	['c1,c2,c3,c4',                    'texture{pigment{Yellow}finish{phong 0.2}},texture{pigment{Violet*1.2}finish{phong 0.2}},texture{pigment{Red*0.7}finish{phong 0.2}},texture {T_Gold_5C finish{reflection 0.1}}'],
	['j',                              '1'],
]


###############################################################################
#
def upDir(path, levels=1):
	if levels == 1:
		return os.path.dirname(path)
	elif levels > 1:
		return upDir(os.path.dirname(path), levels-1)
	else:
		return None


###############################################################################
#
def which(program):
	import os
	def is_exe(fpath):
		#print fpath+': '+str(os.path.isfile(fpath))+', '+str(os.access(fpath, os.X_OK))
		return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

	fpath, fname = os.path.split(program)
	if fpath:
		if is_exe(program):
			return program
	else:
		for path in os.environ["PATH"].split(os.pathsep):
			exe_file = os.path.join(path, program)
			if is_exe(exe_file):
				return exe_file

	return False


def touch(filepath):
	if not os.path.exists(filepath):
		open(filepath, 'w').close()


def subprocess_call(command, cwd=None):
	NULL = open('/dev/null', 'w')
	return subprocess.call(command, cwd=cwd, stdout=NULL, stderr=NULL)


###############################################################################
#
class Callable:
	def __init__(self, _callable):
		self.__call__ = _callable


###############################################################################
#
class env:
	WORKDIR = None
	SCRIPTDIR = None
	ARCHIVE_OUTPUT_DIR = None
	SRCDIR = None
	TOOLDIR = None

	DATADIR = None
	INCDIR = None
	ULPDIR = None

	OUTDIR_ROOT = None
	OUTDIR_3DPACK = None
	OUTDIR_INC = None
	OUTDIR_POV = None
	OUTDIR_IMG = None

	RELEASEDIR = None
	RELEASEDIR_ULP = None
	RELEASEDIR_POVRAY = None
	RELEASEDIR_ULP = None
	RELEASEDIR_EXAMPLES = None

	HASZIP = False
	HASTAR = False
	HASGZIP = False
	HASBZIP2 = False

	HASTODOS = False
	HASUNIX2DOS = False
	HASDOS2UNIX = False

	def init():
		#get the directory we are in currently
		env.WORKDIR = os.getcwd()
		#get the directory this script is in
		env.SCRIPTDIR = os.path.dirname(os.path.abspath(__file__))

		if env.WORKDIR == env.SCRIPTDIR:
			env.ARCHIVE_OUTPUT_DIR = upDir(env.WORKDIR)
			env.SRCDIR = os.path.join(upDir(env.WORKDIR),'src')
			env.TOOLDIR = os.path.join(upDir(env.WORKDIR),'tools')
			env.DATADIR = os.path.join(env.SRCDIR,'data')
			env.INCDIR = os.path.join(env.SRCDIR,'inc')
			env.ULPDIR = os.path.join(env.SRCDIR,'ulp')

			env.OUTDIR_ROOT = os.path.join(upDir(env.WORKDIR),'build')
			env.OUTDIR_3DPACK = os.path.join(env.OUTDIR_ROOT, "3dpack")
			env.OUTDIR_INC = os.path.join(env.OUTDIR_ROOT, "inc")
			env.OUTDIR_POV = os.path.join(env.OUTDIR_ROOT, "pov")
			env.OUTDIR_IMG = os.path.join(env.OUTDIR_ROOT, "img")

			env.RELEASEDIR = os.path.join(env.OUTDIR_ROOT,'eagle3d')
			env.RELEASEDIR_ULP = os.path.join(env.RELEASEDIR,'ulp')
			env.RELEASEDIR_POVRAY = os.path.join(env.RELEASEDIR,'povray')
			env.RELEASEDIR_ULP = os.path.join(env.RELEASEDIR,'doc')
			env.RELEASEDIR_EXAMPLES = os.path.join(env.RELEASEDIR,'examples')

		elif os.path.isdir(os.path.join(env.WORKDIR,'src')) and os.path.isdir(os.path.join(env.WORKDIR,'tools')):
			env.ARCHIVE_OUTPUT_DIR = env.WORKDIR
			env.SRCDIR = os.path.join(env.WORKDIR,'src')
			env.TOOLDIR = os.path.join(env.WORKDIR,'tools')
			env.DATADIR = os.path.join(env.SRCDIR,'data')
			env.INCDIR = os.path.join(env.SRCDIR,'inc')
			env.ULPDIR = os.path.join(env.SRCDIR,'ulp')

			env.OUTDIR_ROOT = os.path.join(env.WORKDIR,'build')
			env.OUTDIR_3DPACK = os.path.join(env.OUTDIR_ROOT, "3dpack")
			env.OUTDIR_INC = os.path.join(env.OUTDIR_ROOT, "inc")
			env.OUTDIR_POV = os.path.join(env.OUTDIR_ROOT, "pov")
			env.OUTDIR_IMG = os.path.join(env.OUTDIR_ROOT, "img")

			env.RELEASEDIR = os.path.join(env.OUTDIR_ROOT,'eagle3d')
			env.RELEASEDIR_ULP = os.path.join(env.RELEASEDIR,'ulp')
			env.RELEASEDIR_POVRAY = os.path.join(env.RELEASEDIR,'povray')
			env.RELEASEDIR_DOC = os.path.join(env.RELEASEDIR,'doc')
			env.RELEASEDIR_EXAMPLES = os.path.join(env.RELEASEDIR,'examples')

		else:
			WORKDIR = None
			SCRIPTDIR = None
			#echo "Sript run from invalid position."
			#echo "Start it from the root of the Eagle3D source or from the tools/ dir."
			#exit
		#fi

		env.HASZIP = which('zip')
		env.HASTAR = which('tar')
		env.HASGZIP = which('gzip')
		env.HASBZIP2 = which('bzip2')

		env.HASTODOS = which('todos')
		env.HASUNIX2DOS = which('unix2dos')
		env.HASDOS2UNIX = which('dos2unix')

	init = Callable(init)

	def dump():
		print "PATHS:"
		print "  WORKDIR: %s"%env.WORKDIR
		print "  SCRIPTDIR: %s"%env.SCRIPTDIR
		print "  ARCHIVE_OUTPUT_DIR: %s"%env.ARCHIVE_OUTPUT_DIR
		print "  SRCDIR: %s"%env.SRCDIR
		print "  OUTDIR_ROOT: %s"%env.OUTDIR_ROOT
		print "  TOOLDIR: %s"%env.TOOLDIR
		print "  RELEASEDIR: %s"%env.RELEASEDIR
		print "  OUTDIR_INC: %s"%env.OUTDIR_INC
		print "  OUTDIR_POV: %s"%env.OUTDIR_POV
		print "  OUTDIR_IMG: %s"%env.OUTDIR_IMG
		print "UTILITIES:"
		print "  HASZIP: "+str(env.HASZIP)
		print "  HASTODOS: "+str(env.HASTODOS)
		print "  HASUNIX2DOS: "+str(env.HASUNIX2DOS)
	dump = Callable(dump)


###############################################################################
#
class make:

	quiet = None
	version = None
	static_date = None

	###############################################################################
	# return the time and date in the format of: 22.08.2010 22:31:52
	def formatted_datetime():
		if make.static_date != None:
			return make.static_date.strftime('%d.%m.%Y %H:%M:%S')
		else:
			return datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')
	formatted_datetime = Callable(formatted_datetime)


	########################################
	#
	def version_to_filename():
		if make.version == None:
			return None
		filename = make.version.replace(' ', '_').replace('.', '_')
		if make.static_date != None:
			filename = filename + make.static_date.strftime('_%d%m%G')
		else:
			filename = filename + datetime.datetime.now().strftime('_%d%m%G')
		return filename
	version_to_filename = Callable(version_to_filename)


	########################################
	#
	def parse_inc_src(inc_src_content=[], inc_src_block=0):
		result = []
		inc_src_content_len = len(inc_src_content)
		inc_src_index = 1
		inc_src_block_index = 0
		while inc_src_index<inc_src_content_len and inc_src_block_index != inc_src_block:
			if inc_src_content[inc_src_index][:20] == "#"*20:
				inc_src_block_index = inc_src_block_index+1
			inc_src_index = inc_src_index+1
		while inc_src_index<inc_src_content_len and inc_src_content[inc_src_index][:20] != "#"*20:
			result.append(inc_src_content[inc_src_index])
			inc_src_index = inc_src_index+1
		return result
	parse_inc_src = Callable(parse_inc_src)


	########################################
	#
	def verify():
		all_errors_found = 0

		logger.info("VERIFYING BUILD")
		logger.info('')

		####################
		#
		all_inc_macros = []
		for rootdir, dirlist, filelist in os.walk(env.INCDIR):

			# skip the base directory
			if rootdir != env.INCDIR:

				rootdir_rel = rootdir[len(env.WORKDIR)+1:]
				#if not make.quiet: logger.info("  directory: "+rootdir_rel)

				rootdir_basename = os.path.basename(rootdir)

				for rootdir2, dirlist2, filelist2 in os.walk(rootdir):
					filelist2.sort()
					for file in filelist2:
						#ignore files
						if file in ["pre.pre", "pos.pos"]:
							continue

						f_inc_src_filepath = os.path.join(rootdir2, file)
						f_inc_src_filepath_rel = f_inc_src_filepath[len(env.INCDIR)+1:]

						#if not make.quiet: logger.info("    file: "+f_inc_src_filepath_rel)

						f_inc_src = open(f_inc_src_filepath, 'r')
						f_inc_src_content = f_inc_src.read()
						f_inc_src.close()
						f_inc_src_content = f_inc_src_content.split("\n")
						f_inc_src_index = 0

						for i in make.parse_inc_src(f_inc_src_content, 3):
							if i.strip() == '' or i[:2] == "//" or i[:1] == "(":
								pass
							else:
								i_split = i.split('(')
								if len(i_split) > 1:
									all_inc_macros.append(i_split[0])
								else:
									logger.info("    ERROR: "+f_inc_src_filepath_rel+'; line: '+i)

		logger.info("total of %s macros"%(str(len(all_inc_macros))))
		logger.info('')


		logger.info("checking defined macros against used macros...")

		f_3dpack = open(os.path.join(env.OUTDIR_3DPACK, "3dpack.dat"), 'r')
		f_3dpack_content = f_3dpack.readlines()
		f_3dpack.close()

		f_3dpack_macros = []
		for i in f_3dpack_content:
			i_split = i.split(':')
			if len(i_split) > 30:
				f_3dpack_macros.append(i_split[31][:-1])
			else:
				logger.info("    ERROR: 3dpack.dat; "+i)

		missing_inc_macros_count = 0
		missing_inc_macros = []
		for i in all_inc_macros:
			if i not in f_3dpack_macros:
				missing_inc_macros_count = missing_inc_macros_count+1
				missing_inc_macros.append(i)

		if missing_inc_macros_count>0:
			logger.info("found %s defined parts that are not in 3dpack.dat:"%(str(missing_inc_macros_count)))
			for i in missing_inc_macros:
				logger.info("  %s"%(i))
		else:
			logger.info('no unused parts found.')
		logger.info('')

		all_errors_found = all_errors_found+missing_inc_macros_count

		####################
		#
		logger.info("checking macro include file format...")
		for rootdir, dirlist, filelist in os.walk(env.INCDIR):
			filelist.sort()
			for inc in filelist:
				#ignore files
				if inc in ["pre.pre", "pos.pos"]:
					continue

				filepath = os.path.join(rootdir, inc)
				filepath_rel = filepath[len(env.INCDIR)+1:]

				macro = ''
				if inc.endswith(INCLUDE_FILE_SUFFIX):
					macro = inc[:-len(INCLUDE_FILE_SUFFIX)]

				errors_found = 0

				subdir = os.path.basename(os.path.dirname(filepath))
				if not inc.startswith(INCLUDE_PREFIX_MAP[subdir]):
					logger.info('  '+filepath_rel+': file name is inconsistant with naming rules')
					errors_found = errors_found+1

				filepathHandle = open(filepath, 'r')
				capture_next_line = False
				line_index = 0

				#*.src.inc format:
				# Part name (Currently ignored, only one line)
				# //Comments inserted before the macro (always prefixed by "//")
				# ################################################################
				# Lines for the 3dpack.dat
				# ################################################################
				# Main macro name (without parameter list, see naming conventions above)
				# Main macro parameter list
				# ################################################################
				# //Comment for the sub macro (optional)
				# Sub macro name(parameter list)
				# Parameter list for main macro
				# ################################################################
				# ################################################################
				# Actual macro

				# line index: description
				#          0: first line of data for 3dpack.dat
				#          1: main macro name
				#          2: first line of sub-macro list
				#          3: first line double hash
				#          4: first line of main macro body
				for line in filepathHandle:
					line = line.strip()
					if capture_next_line:
						if line_index == 1:
							if line != macro:
								logger.info('  '+filepath_rel+': file name is inconsistant with macro name: '+line+'; '+macro)
								errors_found = errors_found+1
						line_index = line_index + 1
						capture_next_line = False
					#if "#"*100 in line:
					if line[:20] == "#"*20:
						capture_next_line = True
				filepathHandle.close()

				if not make.quiet and errors_found<1:
					logger.info('  '+filepath_rel+': no errors found')

				if errors_found != None:
					all_errors_found = all_errors_found+errors_found

		return all_errors_found

	verify = Callable(verify)


	########################################
	#
	def clean():

		########################################
		# remove intermediate files
		if os.path.exists(env.OUTDIR_ROOT):
			if os.path.isdir(env.OUTDIR_ROOT):
				shutil.rmtree(env.OUTDIR_ROOT)
				#try:
					#shutil.rmtree(env.OUTDIR_ROOT)
				#except exception shutil.Error:
					#return False
			else:
				return 1
		if os.path.exists(env.ARCHIVE_OUTPUT_DIR):
			for filepath in glob.glob(os.path.join(env.ARCHIVE_OUTPUT_DIR, "eagle3d*.zip")):
				os.remove(filepath)
			for filepath in glob.glob(os.path.join(env.ARCHIVE_OUTPUT_DIR, "eagle3d*.tar.gz")):
				os.remove(filepath)
			for filepath in glob.glob(os.path.join(env.ARCHIVE_OUTPUT_DIR, "eagle3d*.tar.bz2")):
				os.remove(filepath)
			for filepath in glob.glob(os.path.join(env.ARCHIVE_OUTPUT_DIR, "partSize.dat")):
				os.remove(filepath)

	clean = Callable(clean)


	########################################
	#
	def create():
		make.clean()

		total_errors = 0

		logger.info('creating output directories...')
		os.makedirs(env.OUTDIR_ROOT)

		os.makedirs(env.OUTDIR_3DPACK)
		os.makedirs(env.OUTDIR_INC)
		os.makedirs(env.OUTDIR_POV)
		os.makedirs(env.OUTDIR_IMG)
		os.makedirs(os.path.join(env.OUTDIR_IMG, "warning"))
		os.makedirs(os.path.join(env.OUTDIR_IMG, "fatal"))

		logger.info('creating library files...')
		f_3dpack = open(os.path.join(env.OUTDIR_3DPACK, "3dpack.dat"), 'w')
		for rootdir, dirlist, filelist in os.walk(env.INCDIR):

			# skip the base directory
			if rootdir != env.INCDIR:

				rootdir_rel = rootdir[len(env.WORKDIR)+1:]
				if not make.quiet: logger.info("  directory: "+rootdir_rel)

				rootdir_basename = os.path.basename(rootdir)

				# get the output file name for this directory
				f_inc_filepath = os.path.join(env.OUTDIR_INC, "e3d_"+rootdir_basename)+".inc"
				f_inc = open(f_inc_filepath, 'w')

				# write file header
				f_inc.write("//Eagle3D ###VERSIONDUMMY### INC-File %s\n"%(os.path.basename(f_inc_filepath)))
				f_inc.write("//created by: %s\n"%(SCRIPT_NAME))
				f_inc.write("//created on: %s\n"%(make.formatted_datetime()))
				f_inc.write("//(c) 2002-2010 by M. Weisser\n")
				f_inc.write("//or the author of the macro\n")
				f_inc.write("\n")

				# include global .pre file
				f_global_inc_pre = open(os.path.join(env.DATADIR, "pre.pre"), 'r')
				f_inc.write(f_global_inc_pre.read())
				f_global_inc_pre.close()

				# include local .pre file
				f_local_inc_pre = open(os.path.join(env.INCDIR, rootdir_basename, "pre.pre"), 'r')
				f_inc.write(f_local_inc_pre.read())
				f_local_inc_pre.close()

				for rootdir2, dirlist2, filelist2 in os.walk(rootdir):
					filelist2.sort()
					for file in filelist2:
						#ignore files
						if file in ["pre.pre", "pos.pos"]:
							continue

						f_inc_src_filepath = os.path.join(rootdir2, file)
						f_inc_src_filepath_rel = f_inc_src_filepath[len(env.INCDIR)+1:]

						if not make.quiet: logger.info("    file: "+f_inc_src_filepath_rel)

						f_inc_src = open(f_inc_src_filepath, 'r')
						f_inc_src_content = f_inc_src.read()
						f_inc_src.close()
						f_inc_src_content = f_inc_src_content.split("\n")
						f_inc_src_index = 0

						#get the main macro name and argument list
						f_inc_src_mainmacro = make.parse_inc_src(f_inc_src_content, 2)

						f_inc.write("/********************************************************************************************************************************************\n")
						#print $INC_FILE get_comment_from_inc_src(@inc_src_content);
						for i in make.parse_inc_src(f_inc_src_content, 0):
							f_inc.write(i)
							f_inc.write("\n")
						f_inc.write("********************************************************************************************************************************************/\n")

						#print $INC_FILE "#macro " . get_macro_head_from_inc_src(@inc_src_content) . "\n";
						f_inc.write("#macro ")
						f_inc.write(f_inc_src_mainmacro[0])
						f_inc.write(f_inc_src_mainmacro[1])
						f_inc.write("\n")

						#print $INC_FILE get_macro_body_from_inc_src(@inc_src_content) . "\n";
						for i in make.parse_inc_src(f_inc_src_content, 5):
							f_inc.write(i)
							f_inc.write("\n")

						#print $INC_FILE get_macro_calls_from_inc_src(@inc_src_content) . "\n";
						for i in make.parse_inc_src(f_inc_src_content, 3):
							if i.strip() == '':
								pass
							elif i[:2] == "//":
								f_inc.write(i)
								f_inc.write("\n")
							elif i[:1] == "(":
								f_inc.write(f_inc_src_mainmacro[0])
								f_inc.write(i)
								f_inc.write("\n#end\n")
							else:
								f_inc.write("#macro ")
								f_inc.write(i)
								f_inc.write("\n")

						f_inc.write("\n\n")

						####################
						# append the 3dpack.dat file
						for i in make.parse_inc_src(f_inc_src_content, 1):
							f_3dpack.write(i)
							f_3dpack.write("\n")

						####################
						# build the povray files
						macros = []
						for i in make.parse_inc_src(f_inc_src_content, 3):
							if i.strip() == '' or i[:2] == "//" or i[:1] == "(":
								pass
							else:
								i_split = i.split('(')

								if len(i_split)>1:
									i_split[1] = i_split[1].strip()
									if i_split[1] == ')':
										i_split = i_split[:-1]
									else:
										i_split[1] = i_split[1][:-1].strip().replace(' ', '')

								macros.append(i_split)

						for i in macros:
							if i[0] == '':
								continue
							matched = 0
							if len(i)>1:
								for j in MACRO_PARAM_PATTERNS:
									if i[1] == j[0]:
										i[1] = j[1]
										matched = matched+1
								if matched <1:
									logger.info("ERROR, unmatched argument string: "+i[0]+'('+i[1]+')')
								elif matched >1:
									logger.info("ERROR, argument string matched more than once: "+i[0]+'('+i[1]+')')

							# open the matching POV file
							f_pov = open(os.path.join(env.OUTDIR_POV, i[0]+'.pov'), 'w')

							f_pov.write('//POVRay test file for macro %s\n'%(i[0]))
							f_pov.write("//created by: %s\n"%(SCRIPT_NAME))
							f_pov.write("//created on: %s\n"%(make.formatted_datetime()))
							f_pov.write('//(c) 2002-2010 by M. Weisser\n')
							f_pov.write('\n')
							f_pov.write('#include "povpre.pov"\n')
							f_pov.write('#local macroname = "%s"\n'%(i[0]))
							f_pov.write('\n')

							if len(i)>1:
								f_pov.write('#local obj = object{%s(%s)}\n'%(i[0], i[1]))
							else:
								f_pov.write('#local obj = object{%s()}\n'%(i[0]))

							f_pov.write('#local x_size = (max_extent(obj) - min_extent(obj)).x;\n')
							f_pov.write('#local y_size = (max_extent(obj) - min_extent(obj)).y;\n')
							f_pov.write('#local z_size = (max_extent(obj) - min_extent(obj)).z;\n')
							f_pov.write('#local scale_f = 2/max(x_size,y_size,z_size);\n')
							f_pov.write('\n')
							f_pov.write('camera{location <cam_x,cam_y,cam_z>\n')
							f_pov.write('look_at <0,0,0>angle 18}\n')
							f_pov.write('object{obj scale scale_f\n')
							f_pov.write('translate<0,-min_extent(obj).y*scale_f,0>\n')
							f_pov.write('translate<0,-y_size/2*scale_f,0>}\n')
							f_pov.write('\n')
							f_pov.write('#include "povpos.pov"\n')

							f_pov.close()

				# include global .pos file
				f_global_inc_pos = open(os.path.join(env.DATADIR, "pos.pos"), 'r')
				f_inc.write(f_global_inc_pos.read())
				f_global_inc_pos.close()

				# include local .pos file
				f_local_inc_pos = open(os.path.join(env.INCDIR, rootdir_basename, "pos.pos"), 'r')
				f_inc.write(f_local_inc_pos.read())
				f_local_inc_pos.close()

				f_inc.close()


		f_3dpack_add = open(os.path.join(env.DATADIR, "3dpack_add.dat"), 'r')
		f_3dpack.write(f_3dpack_add.read())
		f_3dpack_add.close()

		f_3dpack.close()

		shutil.copy2(os.path.join(env.DATADIR, 'prepov.pre'), os.path.join(env.OUTDIR_POV, 'povpre.pov'))
		shutil.copy2(os.path.join(env.DATADIR, 'pospov.pos'), os.path.join(env.OUTDIR_POV, 'povpos.pov'))

		logger.info('creating release directories...')
		os.makedirs(env.RELEASEDIR)
		os.makedirs(env.RELEASEDIR_DOC)
		os.makedirs(env.RELEASEDIR_EXAMPLES)
		os.makedirs(env.RELEASEDIR_POVRAY)
		os.makedirs(env.RELEASEDIR_ULP)

		shutil.copy2(os.path.join(upDir(env.SRCDIR), 'COPYING'), env.RELEASEDIR)

		logger.info('copying doc files to release directory...')
		for filepath in glob.glob(os.path.join(env.SRCDIR, 'doc', '*')):
			shutil.copy2(filepath, env.RELEASEDIR_DOC)

		logger.info('copying example files to release directory...')
		for filepath in glob.glob(os.path.join(env.SRCDIR, 'examples', '*')):
			shutil.copy2(filepath, env.RELEASEDIR_EXAMPLES)

		logger.info('copying povray files to release directory...')
		for filepath in glob.glob(os.path.join(env.OUTDIR_INC, '*.inc')):
			shutil.copy2(filepath, env.RELEASEDIR_POVRAY)
		touch(os.path.join(env.RELEASEDIR_POVRAY, "e3d_user.inc"))

		logger.info('copying data files to release directory...')
		for filepath in glob.glob(os.path.join(env.DATADIR, 'fonts', '*.ttf')):
			shutil.copy2(filepath, env.RELEASEDIR_POVRAY)
		for filepath in glob.glob(os.path.join(env.DATADIR, 'tex', '*.png')):
			shutil.copy2(filepath, env.RELEASEDIR_POVRAY)
		for filepath in glob.glob(os.path.join(env.DATADIR, '*.inc')):
			shutil.copy2(filepath, env.RELEASEDIR_POVRAY)


		logger.info('copying ulp files to release directory...')

		f_3d_ulp = open(os.path.join(env.ULPDIR, "3d.ulp"), 'r')
		f_3d_ulp_content = f_3d_ulp.read().split("\n")
		f_3d_ulp.close()

		f_3dfunc_ulp = open(os.path.join(env.ULPDIR, "3dfunc.ulp"), 'r')
		f_3dfunc_ulp_content = f_3dfunc_ulp.read().split("\n")
		f_3dfunc_ulp.close()

		logger.info('writing Eagle3D 5.0 ulp files...')
		exp1 = re.compile("^#40|^#O")
		exp2 = re.compile("^#41|^#50")

		f_3d50_ulp = open(os.path.join(env.RELEASEDIR_ULP, "3d50.ulp"), 'w')
		for line in f_3d_ulp_content:
			if exp1.match(line) == None:
				if exp2.match(line) == None:
					f_3d50_ulp.write(line+"\n")
				else:
					f_3d50_ulp.write("   "+line[3:]+"\n")
		f_3d50_ulp.close()

		f_3dfunc50_ulp = open(os.path.join(env.RELEASEDIR_ULP, "3dfunc50.ulp"), 'w')
		for line in f_3dfunc_ulp_content:
			if exp1.match(line) == None:
				if exp2.match(line) == None:
					f_3dfunc50_ulp.write(line+"\n")
				else:
					f_3dfunc50_ulp.write("   "+line[3:]+"\n")
		f_3dfunc50_ulp.close()


		logger.info('writing Eagle3D 4.1 ulp files...')
		exp1 = re.compile("^#40|^#O|^#50")
		exp2 = re.compile("^#41")

		f_3d41_ulp = open(os.path.join(env.RELEASEDIR_ULP, "3d41.ulp"), 'w')
		for line in f_3d_ulp_content:
			if exp1.match(line) == None:
				if exp2.match(line) == None:
					f_3d41_ulp.write(line+"\n")
				else:
					f_3d41_ulp.write("   "+line[3:]+"\n")
		f_3d41_ulp.close()

		f_3dfunc41_ulp = open(os.path.join(env.RELEASEDIR_ULP, "3dfunc41.ulp"), 'w')
		for line in f_3dfunc_ulp_content:
			if exp1.match(line) == None:
				if exp2.match(line) == None:
					f_3dfunc41_ulp.write(line+"\n")
				else:
					f_3dfunc41_ulp.write("   "+line[3:]+"\n")
		f_3dfunc41_ulp.close()


		logger.info('writing Eagle3D 4.0 ulp files...')
		exp1 = re.compile("^#41|^#O|^#50")
		exp2 = re.compile("^#40")

		f_3d40_ulp = open(os.path.join(env.RELEASEDIR_ULP, "3d40.ulp"), 'w')
		for line in f_3d_ulp_content:
			if exp1.match(line) == None:
				if exp2.match(line) == None:
					f_3d40_ulp.write(line+"\n")
				else:
					f_3d40_ulp.write("   "+line[3:]+"\n")
		f_3d40_ulp.close()

		f_3dfunc40_ulp = open(os.path.join(env.RELEASEDIR_ULP, "3dfunc40.ulp"), 'w')
		for line in f_3dfunc_ulp_content:
			if exp1.match(line) == None:
				if exp2.match(line) == None:
					f_3dfunc40_ulp.write(line+"\n")
				else:
					f_3dfunc40_ulp.write("   "+line[3:]+"\n")
		f_3dfunc40_ulp.close()



		shutil.copy2(os.path.join(env.ULPDIR, 'eagle2svg.ulp'), env.RELEASEDIR_ULP)
		for filepath in glob.glob(os.path.join(env.ULPDIR, '3dlang*.dat')):
			shutil.copy2(filepath, env.RELEASEDIR_ULP)
		for filepath in glob.glob(os.path.join(env.ULPDIR, '3dcol*.dat')):
			shutil.copy2(filepath, env.RELEASEDIR_ULP)
		for filepath in glob.glob(os.path.join(env.ULPDIR, '3d*.png')):
			shutil.copy2(filepath, env.RELEASEDIR_ULP)
		touch(os.path.join(env.RELEASEDIR_ULP, "3dconf.dat"))

		shutil.copy2(os.path.join(env.OUTDIR_3DPACK, '3dpack.dat'), env.RELEASEDIR_ULP)

		logger.info('done')
		logger.info('totalerrors: %s'%(str(total_errors)))
	create = Callable(create)


	########################################
	#
	def release():

		total_errors = 0

		logger.info('setting the current version in all files...')
		for filepattern in ['*.ulp', '*.dat', '*.inc', '*.txt']:
			for rootdir, dirlist, filelist in os.walk(env.RELEASEDIR):
				for filepath in glob.glob(os.path.join(rootdir, filepattern)):
					if not make.quiet: logger.info('  %s'%(filepath))
					#retcode = subprocess.call(["sed", "-i", "s,###VERSIONDUMMY###,%s,"%(make.version), filepath])
					retcode = subprocess_call(["sed", "-i", "s,###VERSIONDUMMY###,%s,"%(make.version), filepath])
					if retcode != 0:
						total_errors = total_errors+1

		logger.info('preparing release for *nix systems...')
		cmd = env.HASDOS2UNIX
		if cmd:
			logger.info('making UNIX line endings for all text files...')
			for filepattern in ['*.sh', '*.pl', '*.inc', '*.src', '*.dat', '*.pos', '*.pre', '*.inc', '*.ulp', '*.pov', '*.ini', '*.txt']:
				for rootdir, dirlist, filelist in os.walk(env.RELEASEDIR):
					for filepath in glob.glob(os.path.join(rootdir, filepattern)):
						if not make.quiet: logger.info('  %s'%(filepath))
						retcode = subprocess_call([cmd, filepath])
						if retcode != 0:
							total_errors = total_errors+1

		if env.HASTAR:
			filepath = os.path.join(env.ARCHIVE_OUTPUT_DIR, "eagle3d_"+make.version_to_filename()+".tar.bz2")
			command = ['tar', '-c', '-a', '-f', filepath, os.path.basename(env.RELEASEDIR) ]
			logger.info('calling: '+" ".join(command))
			retcode = subprocess_call(command, env.OUTDIR_ROOT)
			if retcode != 0:
				total_errors = total_errors+1

			filepath = os.path.join(env.ARCHIVE_OUTPUT_DIR, "eagle3d_"+make.version_to_filename()+".tar.gz")
			command = ['tar', '-c', '-a', '-f', filepath, os.path.basename(env.RELEASEDIR) ]
			logger.info('calling: '+" ".join(command))
			retcode = subprocess_call(command, env.OUTDIR_ROOT)
			if retcode != 0:
				total_errors = total_errors+1

		logger.info('preparing release for non *nix systems...')
		cmd = env.HASUNIX2DOS
		if not cmd:
			cmd = env.HASTODOS
		if cmd:
			logger.info('making DOS line endings for all text files...')
			for filepattern in ['*.sh', '*.pl', '*.inc', '*.src', '*.dat', '*.pos', '*.pre', '*.inc', '*.ulp', '*.pov', '*.ini', '*.txt']:
				for rootdir, dirlist, filelist in os.walk(env.RELEASEDIR):
					for filepath in glob.glob(os.path.join(rootdir, filepattern)):
						if not make.quiet: logger.info('  %s'%(filepath))
						subprocess_call([cmd, filepath])
						if retcode != 0:
							total_errors = total_errors+1

		if env.HASZIP:
			filepath = os.path.join(env.ARCHIVE_OUTPUT_DIR, "eagle3d_"+make.version_to_filename()+".zip")
			command = ['zip', '-9', '-q', '-r', filepath, os.path.basename(env.RELEASEDIR) ]
			logger.info('calling: '+" ".join(command))
			retcode = subprocess_call(command, env.OUTDIR_ROOT)
			if retcode != 0:
				total_errors = total_errors+1

		logger.info('done')
		logger.info('totalerrors: %s'%(str(total_errors)))
	release = Callable(release)


###############################################################################
# entry
# this constuct allows the file to be imported as a module as well as executed.
if __name__ == "__main__":

	usage_string = """Usage: %s [ACTION] [options]
  ACTION       The administrative action to be performed.
  verify       verify that include files are the correct format.
  clean        remove previous attempts to create an eagle3d distribution.
  create       create an eagle3d distribution.
  release      set VERSION variable in files and create archives."""%(os.path.basename(sys.argv[0]))

	if len(sys.argv) < 2:
		print usage_string
		sys.exit(1)

	action = None
	if sys.argv[1] in ["verify", "clean", "create", "env"]:
		action = sys.argv[1]
		usage_string = """Usage: %prog [ACTION] [options]"""
	elif sys.argv[1] == "release":
		action = "release"
		usage_string = """Usage: %prog [VERSION] [options]
  VERSION       The version of EagleD you are creating."""
	else:
		print usage_string
		sys.exit(1)


	parser = OptionParser(usage=usage_string, version="%prog v"+SCRIPT_VERSION)
	parser.add_option(      "--noconsole",   action="store_true", dest="noconsole",   default=False, help="do not print to console, only to log file.")
	parser.add_option("-q", "--quiet",       action="store_true", dest="quiet",       default=False, help="do not print 'no errors' message.")
	parser.add_option("-s", "--silent",      action="store_true", dest="silent",      default=False, help="print and log nothing, return non-zero on any error.")
	parser.add_option(      "--static-date", action="store_true", dest="static_date", default=False, help="calculate date and time only once at start.")
	(options, args) = parser.parse_args()

	logger = logging.getLogger(action)

	#create takes an additional argument
	if action == "release":
		if len(args) < 2:
			parser.print_help()
			sys.exit(1)
		else:
			make.version = args[1]

	env.init()
	if env.WORKDIR == None:
		parser.print_help()
		sys.exit(1)

	if options.static_date:
		make.static_date = datetime.datetime.now()

	if not options.silent:
		loghandler = logging.FileHandler(os.path.join(os.path.dirname(os.path.abspath(__file__)), action+'.log'), 'w')
		loghandler.setFormatter(logging.Formatter('%(message)s'))
		logger.addHandler(loghandler)
		logger.setLevel(logging.INFO)

	if not options.silent and not options.noconsole:
		logger.addHandler(logging.StreamHandler())

	make.quiet = options.quiet

	if action == "verify":
		sys.exit(make.verify())
	elif action == "clean":
		sys.exit(make.clean())
	elif action == "create":
		sys.exit(make.create())
	elif action == "release":
		sys.exit(make.release())
	elif action == "env":
		sys.exit(env.dump())
