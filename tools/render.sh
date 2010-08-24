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

POV_FILES=$BUILDDIR/pov
INC_FILES=$RELEASEDIR/povray
WIDTH=640
HEIGHT=480
AAVALUE=0.3
OUTPUT_DIR=$BUILDDIR/img
PROCESSES=16
NAMEMASK='*.pov'

if [ $# -gt 0 ] 
then
    NAMEMASK=$1
fi

for i in $(find $POV_FILES -type f -name $NAMEMASK | sort)
do 
    FILENAME=$(basename $i)
    
    if [ "$FILENAME" = "povpre.pov" ] || [ "$FILENAME" = "povpos.pov" ]
    then       
        continue
    fi
        
    echo "Rendering $FILENAME"
    nice -n 19 povray +L$INC_FILES \
                      +L$POV_FILES \
                      +W$WIDTH +H$HEIGHT +A$AAVALUE \
                      -GW$OUTPUT_DIR/warning/$FILENAME.warnings.txt \
                      -GF$OUTPUT_DIR/fatal/$FILENAME.fatal.txt \
                      +O$OUTPUT_DIR/$FILENAME.png \
                      -GS -GR -GD -V -D +I$i > /dev/null 2>&1 &

    while [  $(ps | grep -i "povray" | wc -l) -ge $PROCESSES ]; do
        sleep .05
    done
        
done

while [  $(ps | grep -i "povray" | wc -l) -ge 1 ]; do
    echo "Waiting for last render job done"
    sleep .5
done

#Removing empty fatal files
FATALCOUNT=0
for i in $(find $OUTPUT_DIR/fatal -type f -name *.txt)
do 

    if [ ! -s $i ]
    then
        rm $i
    else
        FATALCOUNT=$(($FATALCOUNT+1))
    fi

done

if [ $FATALCOUNT -gt 0 ] 
then
    echo "We have $FATALCOUNT files which do not render!"
    echo "Check build/img/fatal!"
fi

#Removing empty warning files
for i in $(find $OUTPUT_DIR/warning -type f -name *.txt)
do 

    if [ ! -s $i ]
    then
        rm $i
    fi

done

#Create the final output file
echo "Creating gallery file"
nice -n 19 montage -geometry 64x48 -tile 10x $(find $OUTPUT_DIR -type f | grep png$ | sort) $OUTPUT_DIR/../gallery.png

