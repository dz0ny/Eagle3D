#!/usr/bin/perl -w

use strict;
use warnings;
use File::Path;
use Getopt::Long;

###############################################################################
#Get the script options

my $src_dir     = '../';
my $build_dir   = '../';
my $verbose     = 0;

GetOptions("src=s"    => \$src_dir,
           "build=s"  => \$build_dir,
           "verbose+" => \$verbose);

###############################################################################
#Some static configuration
my $script_name = 'INC SRC Compiler v2.02';

#output directory names
my $dir_3dpack_name      = "3dpack";
my $dir_inc_name         = "inc";
my $dir_pov_name         = "pov";
my $dir_img_name         = "img";

#global filenames and directories
my $inc_src_dir          = "$src_dir/inc";
my $input_dir_data       = "$src_dir/data";

my $output_dir_3dpack    = "$build_dir/$dir_3dpack_name";
my $output_dir_inc       = "$build_dir/$dir_inc_name";
my $output_dir_pov       = "$build_dir/$dir_pov_name";
my $output_dir_img       = "$build_dir/$dir_img_name";

my $input_file_global_inc_pre = "$input_dir_data/pre.pre";
my $input_file_global_inc_pos = "$input_dir_data/pos.pos";
my $input_file_3dpack_add_dat = "$input_dir_data/3dpack_add.dat";
my $input_file_global_pov_pre = "$input_dir_data/prepov.pre";
my $input_file_global_pov_pos = "$input_dir_data/pospov.pos";

my $output_file_3dpack     = "$output_dir_3dpack/3dpack.dat";
my $output_file_povpre_pov = "$output_dir_pov/povpre.pov";
my $output_file_povpos_pov = "$output_dir_pov/povpos.pov";

###############################################################################
#A couple of utility functions

#prints current date and time
sub get_date_and_time 
{   
    my ($sec,$min,$hour,$mday,$mon,$year) = localtime(time);
    return sprintf("%02d.%02d.%04d %02d:%02d:%02d", $mday, $mon+1, $year+1900, $hour, $min, $sec);
}

#writes an array of lines to a file
sub print_string_array
{
    my ($file_handle, @array_to_print) = @_;
  
    foreach my $line (@array_to_print)
    {
        print {$file_handle} $line;
    }
}

#writes content of argument 1 to file handle in argument 0
sub print_file_content
{
    my $FILE;
    open $FILE,      '<', $_[1] or die "could not open $_[1]: $^E";
    my @content = <$FILE>;
    close $FILE;
    
    print_string_array($_[0], @content);
}

#returns the comment part of a .inc.src file
sub get_comment_from_inc_src
{
    my $result = "";
    my $i = 0;
    
    foreach my $line (@_)
    {
        if(0 == $i++) { next; }
        if($line =~ /^#{20,}/) { last; }
        $result .= $line;
    }
    return $result;
}

#returns the macro name of a .inc.src file
sub get_macro_name_from_inc_src
{
    my $result = "";
    my $i = 0;
    
    foreach my $line (@_)
    {
        if($line =~ /^#{20,}/) { $i++; next; }
        if($i == 2)
        {
            $result = $line;
            chomp($result);
            last;
        }
    }
    return $result;
}

#returns the macro name of a .inc.src file
sub get_macro_parms_from_inc_src
{
    my $result = "";
    my $i = 0;
    my $j = 0;
    
    foreach my $line (@_)
    {
        if($line =~ /^#{20,}/) { $i++; $j = 0; next; }
        if($i == 2)
        {
            $j++;
            if($j == 2)
            {
                $result = $line;
                chomp($result);
                last;
            }
        }
    }
    return $result;
}

#returns the macro head of a .inc.src file
sub get_macro_head_from_inc_src
{
    my $result = get_macro_name_from_inc_src(@_);
    $result .= get_macro_parms_from_inc_src(@_);
    
    return $result;
}

#returns the macro body of a .inc.src file
sub get_macro_body_from_inc_src
{
    my $result = "";
    my $i = 0;
    
    foreach my $line (@_)
    {
        if($line =~ /^#{20,}/) { $i++; next; }
        if($i == 5)
        {
            $result .= $line;
        }
    }
    return $result;
}

#returns the calls to the macro as defined in a .inc.src file
sub get_macro_calls_from_inc_src
{
    my $result = "";
    my $i = 0;
    
    my $macro_name = get_macro_name_from_inc_src(@_);
    
    foreach my $line (@_)
    {
        if($line =~ /^#{20,}/) { $i++; next; }
        if($i == 3)
        {
            if($line =~ /^#{20,}/) { last; }
            
            if($line =~ /^\/\//) { $result .= $line; next; }
            if($line =~ /^[A-Za-z]/) { $result .= "#macro " . $line; next; }
            if($line =~ /^\(/) 
            {                
                $result .= $macro_name . $line . "#end\n";
                next;
            }
        }
    }
    
    return $result;
}

#returns the 3dpack.dat lines of a .inc.src file
sub get_macro_pack_info_from_inc_src
{
    my $result = "";
    my $i = 0;
    
    foreach my $line (@_)
    {
        if($line =~ /^#{20,}/) { $i++; next; }
        if($i == 1)
        {
            if($line =~ /^#{20,}/) { last; }
            
            $result .= $line;
        }
    }
    return $result;
}

#returns all macro names (called base macros) of a .inc.src file
sub get_macro_names_from_inc_src
{
    my $result = "";
    my $i = 0;
        
    foreach my $line (@_)
    {
        if($line =~ /^#{20,}/) { $i++; next; }
        if($i == 3)
        {
            if($line =~ /^#{20,}/) { last; }
            
            if($line =~ /^\/\//) { next; }
            if($line =~ /^[A-Za-z]/) { $result .= $line; next; }
            if($line =~ /^\(/) { next; }
        }
    }    
    return $result;
}

###############################################################################
#Main 

print "##########################\n";
print "# $script_name #\n";
print "##########################\n";

#Create output directories
mkpath( "$output_dir_3dpack");
mkpath( "$output_dir_inc");
mkpath( "$output_dir_pov");
mkpath( "$output_dir_img");
mkpath( "$output_dir_img" . '/warning');
mkpath( "$output_dir_img" . '/fatal');

#Open global output files
open my $PACK_FILE,      '>', "$output_file_3dpack"    or die "could not open $output_file_3dpack: $^E";

opendir my $MAIN_DIR, "$inc_src_dir/" or die "could not open directory $inc_src_dir/ : $!";
my @main_dirs = readdir $MAIN_DIR;
closedir $MAIN_DIR;

my $all_macro_names = "";
my $all_3dpack_dat_lines = "";
my $macro_count = 0;

#iterate over all the dirs matching the string_dir condition
foreach my $cur_dir (@main_dirs)
{
    if($cur_dir =~ /^[^.][a-zA-Z0-9]+$/)
    {
        opendir my $INC_DIR, "$inc_src_dir/$cur_dir" or 
            die "could not open directory $inc_src_dir/$cur_dir : $!";
        my @inc_dir_contents = readdir $INC_DIR;
        closedir $INC_DIR;
        
        if($verbose > 0) { print "\nDirectory: $cur_dir\n"; }
        
        #Get the output file name for this directory
        my $output_inc_file_name = $cur_dir . ".inc";
        open my $INC_FILE, '>', "$output_dir_inc/e3d_$output_inc_file_name" or 
            die "could not open $output_dir_inc/$output_inc_file_name: $^E";
        
        #Write file header
        print $INC_FILE "//Eagle3D ###VERSIONDUMMY### INC-File $output_inc_file_name\n";
	    print $INC_FILE "//created by: $script_name\n";
		print $INC_FILE "//created on: " . get_date_and_time() . "\n";
        print $INC_FILE "//(c) 2002-2010 by M. Weisser\n";
	    print $INC_FILE "//or the author of the macro\n\n";
        
        #Write the global and then the local .pre file
		print_file_content($INC_FILE, $input_file_global_inc_pre);
		print_file_content($INC_FILE, "$inc_src_dir/$cur_dir/pre.pre");
        
        #Process only .inc.src files
        my @inc_dir_inc_src_files;        
        foreach my $inc_dir_element (@inc_dir_contents)
        {
            if($inc_dir_element =~ /\.inc\.src$/)
            {
                push @inc_dir_inc_src_files, $inc_dir_element;
            }
        }
        @inc_dir_inc_src_files = sort(@inc_dir_inc_src_files);
        
        #now iterate over all .inc.src files
        foreach my $inc_dir_src_file (@inc_dir_inc_src_files)
        {
            if($verbose > 1) { print "    File: $inc_dir_src_file\n"; }
            
            #Read the .inc.src file
            open my $INC_SRC_FILE, '<', "$inc_src_dir/$cur_dir/$inc_dir_src_file" or 
                die "could not open $inc_src_dir/$cur_dir/$inc_dir_src_file : $^E";
            my @inc_src_content = <$INC_SRC_FILE>;
            close $INC_SRC_FILE;
            
            #Write the macro definition and the calls to the current include file
            print $INC_FILE "/********************************************************************************************************************************************\n";
			print $INC_FILE get_comment_from_inc_src(@inc_src_content);
			print $INC_FILE "********************************************************************************************************************************************/\n";
			print $INC_FILE "#macro " . get_macro_head_from_inc_src(@inc_src_content) . "\n";
			print $INC_FILE get_macro_body_from_inc_src(@inc_src_content) . "\n";
			print $INC_FILE get_macro_calls_from_inc_src(@inc_src_content) . "\n";
			print $INC_FILE "\n";
			
			#write the 3dpack info from .inc.src file to 3dpack.dat
			print $PACK_FILE get_macro_pack_info_from_inc_src(@inc_src_content);
			
			#Save the macro names and 3dpack lines for later statistic usage
			$all_macro_names .= get_macro_names_from_inc_src(@inc_src_content);
			$all_3dpack_dat_lines .= get_macro_pack_info_from_inc_src(@inc_src_content);
			
			#Write the POV file for all of the macros
			my @local_macros = split("\n", get_macro_names_from_inc_src(@inc_src_content));
			
			foreach my $local_macro (@local_macros)
            {
                chomp($local_macro);
                #Split the macro in its name and argument list
                my $local_macro_name   = $local_macro;
                my $local_macro_params = $local_macro;
                $local_macro_name   =~ s/\(.+//;
                $local_macro_params =~ s/[^\(]+//;
                
                if($verbose > 2) { print "        Macro: $local_macro_name\n"; }
                
                #replace parameter list with working values
                my $param_list_matched = 0;
                if($local_macro_params =~ s/\(value, col, tra, height\)/("POV",Red,0\.7,0)/) { $param_list_matched++; }
                if($local_macro_params =~ s/\(col,tra,height\)/(Red,0\.7,0)/)                { $param_list_matched++; }
                if($local_macro_params =~ s/\(col,tra\)/(Red,0\.7)/)                         { $param_list_matched++; }
                if($local_macro_params =~ s/\(color_sub\)/(DarkWood)/)                       { $param_list_matched++; }
                if($local_macro_params =~ s/\(value,logo\)/("POV","")/)                      { $param_list_matched++; }
                if($local_macro_params =~ s/\(value,height\)/("POV",3)/)                     { $param_list_matched++; }
                if($local_macro_params =~ s/\(value\)/("POV")/)                              { $param_list_matched++; }
                if($local_macro_params =~ s/\(name,logo\)/("POV","")/)                       { $param_list_matched++; }
                if($local_macro_params =~ s/\(name\),/("POV")/)                              { $param_list_matched++; }
                if($local_macro_params =~ s/\(height\)/(3)/)                                 { $param_list_matched++; }
                if($local_macro_params =~ s/\(c1,c2,c3,c4\)/(texture{pigment{Yellow}finish{phong 0.2}},texture{pigment{Violet*1.2}finish{phong 0.2}},texture{pigment{Red*0.7}finish{phong 0.2}},texture {T_Gold_5C finish{reflection 0.1}})/) { $param_list_matched++; }
                if($local_macro_params =~ s/\(j\)/(1)/)                                      { $param_list_matched++; }
                if($local_macro_params =~ s/\(\)/()/)                                        { $param_list_matched++; }
                
                if($param_list_matched == 0) { print "        $inc_dir_src_file: !!! Paramter list of $local_macro_name didn't match any replacement!!!\n"; }
                if($param_list_matched  > 1) { print "        $inc_dir_src_file: !!! Paramter list matched more then once!!!\n"; }
                
                #Open the matching POV file
                open my $POV_FILE, '>', "$output_dir_pov/$local_macro_name.pov" or 
                    die "could not open $output_dir_pov/$local_macro_name.pov : $^E";
                print $POV_FILE "//POVRay test file for macro $local_macro_name\n";
                print $POV_FILE "//created by: $script_name\n";
		        print $POV_FILE "//created on: " . get_date_and_time() . "\n";
                print $POV_FILE "//(c) 2002-2010 by M. Weisser\n\n";
                print $POV_FILE "#include \"povpre.pov\"\n";                
                print $POV_FILE "#local macroname = \"$local_macro_name\"\n\n";
		
                print $POV_FILE "#local obj = object{$local_macro_name$local_macro_params}\n";
					
                print $POV_FILE "#local x_size = (max_extent(obj) - min_extent(obj)).x;\n";
                print $POV_FILE "#local y_size = (max_extent(obj) - min_extent(obj)).y;\n";
                print $POV_FILE "#local z_size = (max_extent(obj) - min_extent(obj)).z;\n";
					
                print $POV_FILE "#local scale_f = 2/max(x_size,y_size,z_size);\n";
                
                print $POV_FILE "camera{location <cam_x,cam_y,cam_z>\n" .
                                "look_at <0,0,0>angle 18}\n" .
                                "object{obj scale scale_f\n" .
                                "translate<0,-min_extent(obj).y*scale_f,0>\n" .
                                "translate<0,-y_size/2*scale_f,0>}\n" .
                                "#include \"povpos.pov\"\n";

                close $POV_FILE;
				
				$macro_count++;
            }
        }
        
        #Write the local and then the global .pos file
        print_file_content($INC_FILE, $input_file_global_inc_pos);
        print_file_content($INC_FILE, "$inc_src_dir/$cur_dir/pos.pos");
        
        close $INC_FILE;
    }   
}


#write the additional lines from 3dpack_add.dat to 3dpack.dat
print_file_content($PACK_FILE, $input_file_3dpack_add_dat);

#the prefix POVRay file    
open my $POVPRE_FILE, '>', $output_file_povpre_pov or die "could not open $output_file_povpre_pov : $^E";
print_file_content($POVPRE_FILE, $input_file_global_pov_pre);
close $POVPRE_FILE;

#the postfix POVRay file
open my $POVPOS_FILE, '>', $output_file_povpos_pov or die "could not open $output_file_povpos_pov : $^E";
print_file_content($POVPOS_FILE, $input_file_global_pov_pos);
close $POVPOS_FILE;

#close global output files
close $PACK_FILE;

#Create a vector with all macro names in 3dpack.dat
my @pack_dat_lines = split("\n", $all_3dpack_dat_lines);
my @pack_dat_macro_names;
foreach my $pack_dat_line (@pack_dat_lines)
{
    #print $pack_dat_line . "\n";
    my @pack_dat_fields = split(":", $pack_dat_line);
    $pack_dat_fields[31] =~ s/\(//;
    push (@pack_dat_macro_names, $pack_dat_fields[31]);
}

#Create a vector with all macro names in the .inc.src files
my @inc_src_macro_names = split("\n", $all_macro_names);

#Now compare all macors in 3dpack.dat against all macros 
my $num_pack_dat_macros = @pack_dat_macro_names;
my @parts_not_in_3dpack_dat;
foreach my $inc_src_macro_name (@inc_src_macro_names)
{
    $inc_src_macro_name   =~ s/\(.+//;
    my $i = 0;
            
    foreach my $pack_dat_macro_name (@pack_dat_macro_names)
    {
        if($pack_dat_macro_name eq $inc_src_macro_name) { last; }
        $i++;        
    }   
    
    if($i == $num_pack_dat_macros)
    {
        push(@parts_not_in_3dpack_dat, $inc_src_macro_name);
    }
}

if(@parts_not_in_3dpack_dat > 0)
{
    my $tmp = @parts_not_in_3dpack_dat;
    print "\n$tmp parts not in 3dpack.dat found. These are:\n";
    foreach my $dummy (@parts_not_in_3dpack_dat)
    {
        print "    $dummy\n";   
    }
}

print "\nTotal of $macro_count macros\n";

print "##########################\n";
print "# $script_name #\n";
print "# finished               #\n";
print "##########################\n";
