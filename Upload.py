#!/usr/bin/env python3
"""post-processing script for RepRap firmware printers which uploads the created file to the jobs folder. 
{1}
Usage:
{1}
    Within Simplify3D > Process Settings > Scripts > Post Processing > add the following command:
    Within Slicer, should be part of the profile.
        python3 <script_location>/Upload.py "[output_filepath]" {http of your machine}
{1}
Args:
{1}
    Path: Complete path to the gcode file created by Slicer
    IP: Ip address of your printer you want uploaded to
{1}
Requirements:
{1}
    Tested using Python 3.8.1.
{1}
Credit:
{1}
    Adapted from code originally posted by CCS86 on https://forum.duet3d.com/topic/15302/cura-script-to-automatically-probe-only-printed-area?_=1587348242875.
    This basically taught me how to accept files from slicers. 
    Also, Huge credit to Danal (RIP) for his DuetWebAPI work which I expanded to add some put files. 
{1}
"""
import sys
import DuetWebAPI as DWA
import os

 
def main(fname, IP):	
    print("uploading...")
    
    Machine = DWA.DuetWebAPI(f'http://'+IP)
    if fname.rfind('/') != -1: #checks for full-path (used by slicers)
            name=fname[fname.rfind('/')+1:]
    else:
            name=fname

    try:
        Gcode = open(fname, encoding='utf-8')
        
        Machine.yeetJob(name, Gcode)
    except TypeError:
        try:
            Gcode = open(fname)
        except:
            print("Open file exception. Exiting.")
            error()
    except FileNotFoundError:
        print('File not found. Exiting.')
        error()


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
        print('Error: Proper post processing command is python3 <script_location>/Upload.py "[output_filepath]"(s3d) "Http". Exiting Upload.py.')
        sys.exit()