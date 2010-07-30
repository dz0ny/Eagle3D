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

WORKDIR=$(pwd)
SCRIPTDIR=$(basename $0)

#Check if we are running from the correct position and setup directories
if [ "$WORKDIR" = "$SCRIPTDIR" ]; then
    OUTPUTDIR=$WORKDIR/..
    SRCDIR=$WORKDIR/../src    
    BUILDDIR=$WORKDIR/../build
    TOOLDIR=$WORKDIR/../tools
elif [ -d "$WORKDIR/src" ] && [ -d "$WORKDIR/tools" ]; then
    OUTPUTDIR=$WORKDIR
    SRCDIR=$WORKDIR/src    
    BUILDDIR=$WORKDIR/build
    TOOLDIR=$WORKDIR/tools
else
    echo "Sript run from invalid position."
    echo "Start it from the root of the Eagle3D source or from the tools/ dir."
    exit
fi
RELEASEDIR=$BUILDDIR/eagle3d

#Check for some tools
type zip      > /dev/null 2>&1 && HASZIP="1"      || HASZIP="0"
type todos    > /dev/null 2>&1 && HASTODOS="1"    || HASTODOS="0"
type unix2dos > /dev/null 2>&1 && HASUNIX2DOS="1" || HASUNIX2DOS="0"



