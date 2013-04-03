import bpy
#
# Utility class to export a mesh to a file. 
# D Turvey
# 27-3-13
#

m = bpy.data.meshes["Cube"]
f = open("C:/Users/Dave/Documents/Blender scripts/export_data.dat", 'w')

#
# Print vertices
#

# step through each vertex in turn to count how many we have and write it to the file
vcount=0 
for v in m.vertices:
    vcount+=1
f.write(str(vcount))
f.write("\n")

# write ech vertex in turn as comma delimited x,y,z
for v in m.vertices:
    str_val = str(v.co.x) + ","
    str_val += str(v.co.y) + ","
    str_val += str(v.co.z) + "\n"
    f.write(str_val)

#
# Print faces 
#

# step through each face to count how many we have and write it to the file
m.update (calc_tessface=True) # make sure the faces have been generated first 
fcount=0
for face in m.tessfaces:
    fcount+=1
f.write(str(fcount))
f.write("\n")
	# write each face as a set if four comma delimited values
for face in m.tessfaces:
    str_val = str(face.vertices[0])+","
    str_val += str(face.vertices[1])+","
    str_val += str(face.vertices[2])+","
    str_val += str(face.vertices[3])+"\n"
    f.write(str_val)
f.close()