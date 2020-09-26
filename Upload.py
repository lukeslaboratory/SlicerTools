#!/usr/bin/env python3
"""Simplify3D post-processing script for RepRap firmware printers which dynamically defines the mesh grid dimensions (M557) based on the print dimensions. 
{1}
Usage:
{1}
    Within Simplify3D > Process Settings > Scripts > Post Processing > add the following command:
        python3 <script_location>/meshgrid.py "[output_filepath]"
    
    Starting script must contain M557 Command (ie M557 X30:300 Y30:300 P20).
{1}
Args:
{1}
    Path: Complete path to the gcode file created by Simplify 3d.
{1}
Requirements:
{1}
    Tested using Python 3.8.1.
{1}
Credit:
{1}
    Adapted from code originally posted by CCS86 on https://forum.duet3d.com/topic/15302/cura-script-to-automatically-probe-only-printed-area?_=1587348242875.
{1}
"""
import sys
import DuetWebAPI as DWA
import os

 
probeSpacing = 20   		# set your required probe point spacing for M557
 
def main(fname, IP):	
    print("uploading...")
    
    Machine = DWA.DuetWebAPI(f'http://'+IP)
    if fname.rfind('/') != -1: #checks for full-path (used by slicers)
            name=fname[fname.rfind('/')+1:]
    else:
            name=fname

    try:
        _Slic3rFile = open(fname, encoding='utf-8')
        
        Machine.yeetJob(name, _Slic3rFile)
    except TypeError:
        try:
            _Slic3rFile = open(fname)
        except:
            print("Open file exception. Exiting.")
            error()
    except FileNotFoundError:
        print('File not found. Exiting.')
        error()

    #data = _Slic3rFile.readlines()
    #_Slic3rFile.close()
    
    #cut off the extra junk for the filename
    
    
    
    #Machine.yeetJob(fname[len_name:], data)

    return
 
def error():
	# remove the next 2 lines to close console automatically
	print("Press Enter to close") 
	input()
	sys.exit()
 

 
 
if __name__ == '__main__':

    if sys.argv[2]:
        main(fname = sys.argv[1], IP=sys.argv[2])
    else:
        print('Error: Proper s3d post processing command is python3 <script_location>/meshgrid.py "[output_filepath]" [http]. Exiting meshgrid.py.')
        sys.exit()