#!/bin/sh

. $(dirname $0)/setup_env.sh

##############################################
#Copying ulp files to release directory
##############################################
echo "/// Copying ulp files to release directory ///"

#Creating different versions

#Eagle3D for Eagle 5.0
grep -v -E "(^#40)|(^#O)" $SRCDIR/ulp/3d.ulp     | sed "s/\(^#41\)\|\(^#50\)/   /" > $RELEASEDIR/ulp/3d50.ulp
grep -v -E "(^#40)|(^#O)" $SRCDIR/ulp/3dfunc.ulp | sed "s/\(^#41\)\|\(^#50\)/   /" > $RELEASEDIR/ulp/3dfunc50.ulp

#Eagle3D for Eagle 4.1
grep -v -E "(^#40)|(^#O)|(^#50)" $SRCDIR/ulp/3d.ulp     | sed "s/^#41/   /" > $RELEASEDIR/ulp/3d41.ulp
grep -v -E "(^#40)|(^#O)|(^#50)" $SRCDIR/ulp/3dfunc.ulp | sed "s/^#41/   /" > $RELEASEDIR/ulp/3dfunc41.ulp

#Eagle3D for Eagle 4.0
grep -v -E "(^#41)|(^#O)|(^#50)" $SRCDIR/ulp/3d.ulp     | sed "s/^#40/   /" > $RELEASEDIR/ulp/3d40.ulp
grep -v -E "(^#41)|(^#O)|(^#50)" $SRCDIR/ulp/3dfunc.ulp | sed "s/^#40/   /" > $RELEASEDIR/ulp/3dfunc40.ulp

cp    $SRCDIR/ulp/eagle2svg.ulp     $RELEASEDIR/ulp
cp    $SRCDIR/ulp/3dlang*.dat       $RELEASEDIR/ulp
cp    $SRCDIR/ulp/3dcol*.dat       $RELEASEDIR/ulp
cp    $SRCDIR/ulp/3d*.png           $RELEASEDIR/ulp
touch $RELEASEDIR/ulp/3dconf.dat

