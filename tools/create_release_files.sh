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

##########################################
# Check for version string given
#########################################
if [ -z "$1" ]; then
    echo Please specify a version 
    exit
fi

##########################################
# Set the current version in all files
##########################################
echo "/// Set the current version in all files ///"
for i in $(find $RELEASEDIR -name "*.ulp"); do 
	sed s/###VERSIONDUMMY###/"$1"/ $i > $i.sed
	mv $i.sed $i	
done

for i in $(find $RELEASEDIR -name "*.dat"); do 
	sed s/###VERSIONDUMMY###/"$1"/ $i > $i.sed
	mv $i.sed $i	
done

for i in $(find $RELEASEDIR -name "*.inc"); do 
	sed s/###VERSIONDUMMY###/"$1"/ $i > $i.sed
	mv $i.sed $i	
done

for i in $(find $RELEASEDIR -name "*.txt"); do 
	sed s/###VERSIONDUMMY###/"$1"/ $i > $i.sed
	mv $i.sed $i	
done

##########################################
# Making filename from version argument
##########################################
FILENAME=`echo $1 | sed s/" "/_/g`
FILENAME=`echo $FILENAME | sed s/"\."/_/g`
FILENAME=$FILENAME$(date +_%d%m%G)

if [ -z "$2" ]; then
    ##########################################
    # Compressing Unix tar.bz2
    ##########################################
    echo "/// Compressing Unix archives ///"
    cd $BUILDDIR
    tar -caf $OUTPUTDIR/eagle3d_$FILENAME.tar.bz2 eagle3d/
    tar -caf $OUTPUTDIR/eagle3d_$FILENAME.tar.gz eagle3d/
    cd $WORKDIR

    if [ "$HASTODOS" = "1" ] || [ "$HASUNIX2DOS" = "1" ]; then    

        ##############################################
        #Make windows line endings for all text files
        ##############################################
        echo "/// Convert files ot have Windows line endings ///"
        if [ "$HASTODOS" = "1" ]; then
            todos $(find $RELEASEDIR | grep -E '(\.sh$)|(\.pl$)|(\.inc\.src$)|(\.dat$)|(\.pos$)|(\.pre$)|(\.inc$)|(\.ulp$)|(\.pov$)|(\.ini$)|(\.txt$)')
        elif [ "$HASUNIX2DOS" = "1" ]; then
            unix2dos $(find $RELEASEDIR | grep -E '(\.sh$)|(\.pl$)|(\.inc\.src$)|(\.dat$)|(\.pos$)|(\.pre$)|(\.inc$)|(\.ulp$)|(\.pov$)|(\.ini$)|(\.txt$)')
        fi
        
        if [ "$HASZIP" = "1" ]; then    
            ##########################################
            # Compressing Windows zip
            ##########################################
            echo "/// Compressing Windows zip ///"
            cd $BUILDDIR
            zip -9 -q -r $OUTPUTDIR/eagle3d_$FILENAME.zip eagle3d
            cd $WORKDIR
        fi
        
        if [ "$HASMAKENSIS" = "1" ]; then
            ##########################################
            # Creating windows installer
            ##########################################
            echo "/// Creating windows installer ///"
            cd $TOOLDIR/installer
            makensis -V2 "-DVERSION=$FILENAME" installer.nsi
            cd $WORKDIR
            chmod a+x *.exe
        fi
    fi
fi
    
echo "/// Done ///"












