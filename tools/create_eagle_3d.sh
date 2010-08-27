#!/bin/sh

# Copyright 2005-2010 Matthias Weisser <matthias@matwei.de>
#
# This file is part of Eagle3D
#
# Eagle3D is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
#
# Eagle3D is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

. $(dirname $0)/setup_env.sh

##############################################
#Removing intermediate files
##############################################
echo "/// Removing intermediate files ///"
$TOOLDIR/clean_eagle_3d.sh 
mkdir -p $BUILDDIR

##############################################
#Create library files
##############################################
echo "/// Create library files ///"
$TOOLDIR/create_lib_files.pl --src=$SRCDIR --build=$BUILDDIR

##############################################
#Copying povray files to release directory
##############################################
echo "/// Copying povray files to release directory ///"
mkdir -p $RELEASEDIR/ulp
mkdir -p $RELEASEDIR/povray
mkdir -p $RELEASEDIR/doc
mkdir -p $RELEASEDIR/examples

cp    $BUILDDIR/inc/*.inc   $RELEASEDIR/povray
touch $RELEASEDIR/povray/e3d_user.inc

cp    $SRCDIR/data/fonts/*.ttf  $RELEASEDIR/povray
cp    $SRCDIR/data/tex/*.png    $RELEASEDIR/povray
cp    $SRCDIR/data/*.inc        $RELEASEDIR/povray

##############################################
#Copying ulp files to release directory
##############################################
$TOOLDIR/create_ulp.sh 
cp    $BUILDDIR/3dpack/3dpack.dat     $RELEASEDIR/ulp

##############################################
#Copying example files to release directory
##############################################
echo "/// Copying example files to release directory ///"
cp    $SRCDIR/examples/*              $RELEASEDIR/examples

##############################################
#Copying doc files to release directory
##############################################
echo "/// Copying doc files to release directory ///"
cp    $SRCDIR/doc/*                   $RELEASEDIR/doc
cp    $BASEDIR/COPYING                $RELEASEDIR











