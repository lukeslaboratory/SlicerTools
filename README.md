# SlicerTools
Helpful tools for slicers

Currently I use SuperSlicer and S3d - I'll try to merge all of my scripts per feature so that it supports either w/out having seperate scripts.

Currently, Mesh+G10 are standalone.
Upload.py requires DuetWebAPI which is in my different repo.

What they are:
Mesh
  Updates the mesh coordinates to just cover the printed area. Should make things a bit simpler.

G10
  Updates M104+M109 over to G10 and activates tools. Still in work, but should do most of the job.
  
Upload
  Automagically uploads the file to your duet 3 machine. Will include a prompt in future for starting the print after upload completes. DuetWebAPI needs to be symlinked into the folder (or just copy-pasted) for this to work correctly.
 
