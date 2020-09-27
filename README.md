# SlicerTools
Helpful tools for slicers

Currently I use SuperSlicer and S3d - I'll try to merge all of my scripts per feature so that it supports either w/out having seperate scripts.

Currently, Mesh+G10 are standalone.
Upload.py requires DuetWebAPI which is in my different repo.

What they are:
Meshtool
  Updates the mesh coordinates to just cover the printed area. Useful for very large beds to get the most out of mesh resolution. Should work for S3D and PS/SS/Slic3r

G10
  Updates M104+M109 over to G10 and activates tools. moves M190 (wait for bed temp) to after tools are preheated. 
  
Upload
  Automagically uploads the file to your duet 3 machine. Will include a prompt in future for starting the print after upload completes. [My fork of DuetWebAPI]( https://github.com/lukeslaboratory/DuetWebAPI) needs to be symlinked into the folder (or just copy-pasted) for this to work correctly.
 
