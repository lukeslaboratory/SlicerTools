#!/usr/bin/python
"""
	Slic3r post-processing script for RepRap firmware printers which prefer G10, particularily useful on toolchangers/IDEX
{1}
Usage:
	Two inputs -
	1)delta_temp - The amount of temperature you want to be subtracted from your active temp. 
		1a) FUTURE WORK - Make this dependent on filament type - more to come
	2)end_phrase - this is what you want to use to end your start gcode so the script can "close up" and deselect the tools.

Slic3r automagically puts M104 before any of your starting gcode, so as long as you have your extruders set up, all of this will be performed before any homing or other motion. 	
Args:
	Path: The path parameter will be provided by Slic3r.
Requirements:
{1}
	The latest version of Python.
	Note that I use this on windows and haven't tried it on any other platform.
	as long as all of your tool temperatures are posted in a row, you will be fine. 
{1}
Credit:
{1}
	Based on code originally posted by CCS86 on https://forum.duet3d.com/topic/15302/cura-script-to-automatically-probe-only-printed-area?_=1587348242875. - this is mostly just to import the file automagically, Wasn't sure how to auto-import the file. 
"""
 
import sys
import re
import math
import os
 
delta_temp = 20   # amount to subtract from the active temp
end_phrase ="Prantin" # String to search for to end your start gcode and insert the T-1 gcode
 
def main(fname, delta_temp, end_phrase):	
	print("BeepBopBoop Scanning...")
	
	try:
		_Slic3rFile = open(fname, encoding='utf-8')
	except TypeError:
		try:
			_Slic3rFile = open(fname)
		except:
			print("Open file exception. Exiting.")
			error()
	except FileNotFoundError:
		print('File not found. Exiting.')
		error()
		
	lines = _Slic3rFile.readlines()
	_Slic3rFile.close()
 
	linesNew = g10_swap(lines,delta_temp, end_phrase)
 
	_Slic3rFile = open(fname, "r+")
	_Slic3rFile.seek(0)                       
	_Slic3rFile.truncate()
	for element in linesNew:
		_Slic3rFile.write(element)
	_Slic3rFile.close()
	#print("press any key to close")
	#input()
	return
 
def error():
	# remove the next 2 lines to close console automatically
	print("Press Enter to close") 
	input()
	sys.exit()

def isint(value):
  try:
    int(value)
    return True
  except ValueError:
    return False

def g10_swap(lines,delta_temp, end_phrase):

	# Replace M104 with G10 Gcode
    linesNew = []
    tools_used = []
    start_gcode_ended = False
    count=0
    default_tool = False

    for line in lines:
        if line.startswith('M104'):
            if str.find(line,"T") == -1: # Catch no-tool statements
                tool = "0"
                print("no tool found, using tool 0")
                default_tool = True
            else: 
                tool=line[(str.find(line,"T")+1)]
            #tools_used.append(tool) #stores tools
            activetemp=line[(str.find(line,"S")+1):(str.find(line,"S")+4)]
            print(type(activetemp))
            #standbytemp=int(activetemp)-delta_temp
            if isint(activetemp):
                standbytemp=int(activetemp)-delta_temp
                linesNew.append(f"G10 P{tool} S{activetemp} R{standbytemp}" + "\n") #actual conversion
                print(f"M104 converted over to G10 P{tool} S{activetemp} R{standbytemp}")
            if start_gcode_ended==False: #activates tool to get it warmed up - for initial warmups
                linesNew.append(f"T{tool} P0" + "\n")
                count=count+1 #counts quantity of tools, used in removing m109's

            
        elif line.startswith("M109") and count>0 and start_gcode_ended==True:
                count = count-1
                continue
        else:
            if end_phrase in line: # Check for end of start gcode
                linesNew.append("T-1 P0" + "\n") #deactivates all tools w/out macros
                if default_tool:
                  linesNew.append("T0"+ "\n")
                start_gcode_ended = True

            linesNew.append(line)
    return linesNew

#main("foo.gcode", delta_temp, end_phrase) #testtesttest

if __name__ == '__main__':
    if sys.argv[1]:
        fname = sys.argv[1]
        main(fname, delta_temp, end_phrase)
    else:
        
        print('Error: Proper Slic3r post processing command is python3')
        error() 



