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
import re
import math
import os
 
probeSpacing = 20   		# set your required probe point spacing for M557
 
def main(fname):	
	print("Starting Mesh Calculations")
 
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
 
	linesNew = calcBed(lines)
 
	_Slic3rFile = open(fname, "r+")
	_Slic3rFile.seek(0)                       
	_Slic3rFile.truncate()
	for element in linesNew:
		_Slic3rFile.write(element)
	_Slic3rFile.close()
	
	return
 
def error():
	# remove the next 2 lines to close console automatically
	print("Press Enter to close") 
	input()
	sys.exit()
 
def calcBed(lines):
	bounds = findBounds(lines)
	bed = findBed(lines)
 
	for axis in bounds:
		if bounds[axis]['max'] - bounds[axis]['min'] < bed[axis]:
			print(f'Success: {axis} mesh is smaller than bed')
			
		else:
			print('Error: Mesh is larger than bed. Exiting.')
			error()
 
		for limit in bounds[axis]:
			if limit == 'min':
				if (bed[axis]) - bounds[axis][limit] > 0: 
					print(f'Success: {axis} {limit} coordinate is on the bed.')
				else:
					print(f'Error: {axis} {limit} coordinate is off the bed. Exiting.')
					error()
 
			if limit == 'max':
				if (bed[axis]) - bounds[axis][limit] > 0: 
					print(f'Success: {axis} {limit} coordinate is on the bed.')
				else:
					print(f'Error: {axis} {limit} coordinate is off the bed. Exiting.')
					error()
	return fillGrid(bounds, lines)
	
def findBed(lines):
    bed = {
        'X': 0,
        'Y': 0,
        }
 
    for line in lines:
        if line.startswith(';   strokeXoverride,'):
            bed['X'] = int(re.search(r'\d.+\S', line).group())
        elif line.startswith(';   strokeYoverride,'):
            bed['Y'] = int(re.search(r'\d.+', line).group())
            break
            
    return bed
 
def findBounds(lines):
	bounds = {
		'X': {'min': 9999, 'max': 0},
		'Y': {'min': 9999, 'max': 0},
		}
	
	parsing = True
	for line in lines:
		if "move to next layer (0)" in line:
			parsing = True
			continue
		elif "move to next layer (1)" in line:
			break
 
		if parsing:
			# Get coordinates on this line
			for match in re.findall(r'([YX])([\d.]+)\s', line):
				# Get axis letter
				axis = match[0]
 
				# Skip axes we don't care about
				if axis not in bounds:
					continue
 
				# Parse parameter value
				value = float(match[1])
 
				# Update bounds
				bounds[axis]['min'] = math.floor(min(bounds[axis]['min'], value))
				bounds[axis]['max'] = math.ceil(max(bounds[axis]['max'], value))
				
	# make sure the bounds are at least 2 x Probe Point Spacing, for small prints.
    # also, make sure that the maximum amount of points isn't exceeded.
	if parsing:
		global probeSpacing
		
		for axis in bounds:
			spacing = (bounds[axis]['max'] - bounds[axis]['min'])/2
			if spacing < probeSpacing:
				probeSpacing = spacing
 
	print("Bounds are: " + str(bounds))			
	return bounds
 
 
def fillGrid(bounds, lines):
    #Check the quantity of points - cannot exceed 21points per axis, otherwise will throw error and ruin print by not running a mesh
    X_points=(bounds['X']['max']-bounds['X']['min'])/probeSpacing
    Y_points=(bounds['Y']['max']-bounds['Y']['min'])/probeSpacing
    if X_points>21 or Y_points>21:
     Points=True
	 #basically, if its over 21, just use 21, if not, round up, keeping roughly the same spacing for the non-affected axis
     if X_points>21: X_points = 21 
     else: X_points = math.ceil(X_points)
     if Y_points>21: Y_points=21
     else:Y_points = math.ceil(Y_points)
     print('With your required print footprint, you\'ll exceed 21 points on either axis, changing to point based. Your new point grid is {}:{} points'.format(X_points,Y_points))

    else: 
     Points=False
        
    if Points == True:
        # Fill in the level command template
        gridNew = 'M557 X{}:{} Y{}:{} P{}:{}'.format(bounds['X']['min'], bounds['X']['max'],bounds['Y']['min'], bounds['Y']['max'], X_points, Y_points)
    else:
	    # Fill in the level command template 
	    gridNew = 'M557 X{}:{} Y{}:{} S{}'.format(bounds['X']['min'], bounds['X']['max'],bounds['Y']['min'], bounds['Y']['max'], probeSpacing)

	# Replace M557 command in GCODE
    linesNew = []
    for line in lines:
        if line.startswith('M557'):
            linesNew.append(re.sub(r'^M557 X\d+:\d+ Y\d+:\d+ S\d+', gridNew, line, flags=re.MULTILINE))
            print('New M557: ' + linesNew[-1])
        else:
            linesNew.append(line)
    return linesNew
 
 
if __name__ == '__main__':

    if sys.argv[1]:
        main(fname = sys.argv[1])
    else:
        print('Error: Proper s3d post processing command is python3 <script_location>/meshgrid.py "[output_filepath]". Exiting meshgrid.py.')
        sys.exit()