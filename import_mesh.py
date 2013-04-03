'''
	Created on 26 Mar 2013
	@author: Dave Turvey
'''
import bpy

class meshImporter:
    def __init__(self):
        return
	
    def buildBaseMesh(self):
        # Read the vertices from the file
        f = open("C:/Users/Dave/Documents/Blender scripts/export_data.dat", 'r')

        # read the first value as the number of vertices in the object
        n_vertex = int(f.readline())
        coords = []
        for vertex in range(n_vertex):
            # Read the line and split it into the three strings
            line = f.readline()
            vals = line.split(',',3)
            # Convert each into tuple of floats
            t = float(vals[0]) , float(vals[1]) , float(vals[2]) 
            # Add the data to the coordinate list
            coords.append(t)        
        print(coords)

        # read the first value as the number of faces in the object
        n_face = int(f.readline())
        faces = []
        for vertex in range(n_face):
            # Read the line and split it into the four strings
            line = f.readline()
            vals = line.split(',',4)
            # Convert each into tuple of ints
            t = int(vals[0]) , int(vals[1]) , int(vals[2]), int(vals[3]) 
            # Add the data to the coordinate list
            faces.append(t)        
        print(faces)

        f.close()
		
        me = bpy.data.meshes.new("Base")   # create a new mesh
        ob = bpy.data.objects.new("Base", me)          # create an object with that mesh
        ob.location = bpy.context.scene.cursor_location   # position object at 3d-cursor
        bpy.context.scene.objects.link(ob)                # Link object to scene
		
		# Fill the mesh with verts, edges, faces
        me.from_pydata(coords,[],faces)   # edges or faces should be [], or you ask for problems
        me.update(calc_edges=True)    # Update mesh with new data
        return
  

b = meshImporter()
b.buildBaseMesh() 