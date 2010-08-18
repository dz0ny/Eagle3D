#!/bin/sh

# Copyright 2010 Matthias Weisser <matthias@matwei.de>
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

if [ ! -f $1 ] || [ ! -n $2 ] || [ ! -f $BUILDDIR/3dpack/3dpack.dat ]; then
    echo "Not all input/output conditions are met"
    exit 1;
fi

LST1=$(cat $1 | sort -u)
LST2=$(cat $BUILDDIR/3dpack/3dpack.dat | awk 'BEGIN { FS = ":" }; { print $1 }' | sort -u | sed 's/;/\\n/g')

echo "$LST1 $LST2" | sort | uniq -u > $2

