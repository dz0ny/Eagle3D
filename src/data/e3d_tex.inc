/*
 * Copyright 2005-2010 Matthias Weisser <matthias@matwei.de>
 *
 * This file is part of Eagle3D
 *
 * Eagle3D is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; version 2 of the License.
 *
 * Eagle3D is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

/*
 * This is the global texture definition file. All texture definitions
 * for parts have to be taken from here or have to be defined here.
 */

#ifndef(__e3d_tex_inc)
#declare __e3d_tex_inc = true;

//******************************************************************************************************
//Color settings for a couple of parts

#declare col_gold = 
    texture{
        T_Gold_5E 
        finish{
            F_MetalA 
            ambient(0.35 * global_ambient_mul)
        }
    };
    
#declare col_silver = 
    texture{
        T_Silver_5A
        finish{
            F_MetalA 
            ambient (0.35 * global_ambient_mul)
        }
    };

//----------------------------------------------------------------------
//Shrouded Header
// glatter schwarzer Kunststoff
#declare col_Wannen = texture{
                            pigment{Gray70}
                            finish{ambient (0.1 * global_ambient_mul)}
                        };  // hellgrauer Kunststoff

//----------------------------------------------------------------------
//Molex Stiftleisten
// hellbeiger Kunststoff Molex-Stiftleisten
#declare col_Molex =    texture {
                            pigment{Wheat}
                            finish{ambient (0.1 * global_ambient_mul)}
                        };
//----------------------------------------------------------------------
//Keramik-Scheibenkondensatoren
// braune Keramik-Scheibenkondensatoren
#declare col_Kerko =    texture{
                            pigment{MediumWood}
                            finish{ambient (0.1 * global_ambient_mul)}
                        }
//******************************************************************************************************

#end //__e3d_tex_inc


