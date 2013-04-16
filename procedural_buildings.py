'''
    Procedural building generator for blender 2.66
	Created on 19 Mar 2013
	@author: Dave Turvey
'''
import bpy
from bpy import context
from mathutils import Vector
from mathutils import Matrix 
from math import radians 
import random

class builder:
    ''' 
	
        Creates a single building each time it is invoked. One instance 
	    can create multiple buildings with multiple invocations of the
	    build method
	
	'''
    def __init__(self, max_l, max_w, max_h):
        self.width = max_w;
        self.length = max_l
        self.height = max_h;
        self.scalex = random.randint(1,self.width)
        self.scaley = random.randint(1,self.length)
        self.scalez = random.randint(1,self.height)
        return

    def addWindowModifier(self, target, new_window, axis):
	    # Add modifier based on axis 
        if axis == 'X':
            mod = new_window.modifiers.new(new_window.name, 'ARRAY')
            mod.fit_type = 'FIXED_COUNT'
            mod.count = (target.scale.x*target.dimensions.x) / (new_window.scale.x*new_window.dimensions.x)
        if axis == 'Y':
            mod = new_window.modifiers.new(new_window.name, 'ARRAY')
            mod.fit_type = 'FIXED_COUNT'
            mod.count = (target.scale.y*target.dimensions.y) / (new_window.scale.x*new_window.dimensions.x)
        # Apply the modifier - may want to do this at some point in the future
        #bpy.ops.object.visual_transform_apply()
        #bpy.ops.object.modifier_apply(apply_as='DATA', modifier='Chain')
        return
	

    def addWindows(self,target,window):
        '''
            Add windows using the window object in the scene - this will need the importer eventually 
            as there should be probabilities of different types of windows possibly based on the height of
            the building.
            
		'''
        reverse_rot = Matrix.Rotation(radians(180.0), 4, 'Z')
        ninety_rot = Matrix.Rotation(radians(90.0), 4, 'Z')	
        xlen = 	target.scale.x * target.dimensions.x
        ylen = target.scale.y * target.dimensions.y
        zlen = target.scale.z * target.dimensions.z
        # Each floor has a set of windows of the same type. Each floor is 1BU high
        for floor in range(int(zlen)):
            # First set is flush with the x-axis face
            fw = window.copy()
            context.scene.objects.link(fw)
			# slide the window to the edge of the building in the x-axis
            fw.location.x = (target.location.x - (xlen / 2)) + ((fw.scale.x * fw.dimensions.x) / 2)
			# we need to push the window slightly outside the cube to see it
            fw.location.y = target.location.y - (ylen/2) - 0.01 
            self.addWindowModifier(target, fw, 'X')
            fw.location.z = (target.location.z - zlen/2)+(fw.scale.z * fw.dimensions.z)/2+floor
                    
            # Second set is flush with the reverse x-axis face
            rw = window.copy()
            context.scene.objects.link(rw)
			# rotate the window around 180 on the z-axis so it faces out of the building
            rw.matrix_world = rw.matrix_world * reverse_rot
            # slide the window to the edge of the building in the x-axis
            rw.location.x = (target.location.x + (xlen / 2)) - ((rw.scale.x * rw.dimensions.x) / 2)
			# shift it on the y-axis to the opposite face of the building			
            rw.location.y = target.location.y + (ylen/2) + 0.01 
            self.addWindowModifier(target, rw, 'X')
            rw.location.z = (target.location.z - zlen/2)+(rw.scale.z * rw.dimensions.z)/2+floor

            # Third set is f90 degrees from x-axis face     
            sw = window.copy()
            context.scene.objects.link(sw)
	        # rotate the window around 90 on the z-axis so it faces out of the building
            sw.matrix_world = sw.matrix_world * ninety_rot
			# shift it on the y-axis to the positiveface of the building
            sw.location.y = (target.location.y - (ylen/2)) + ((rw.scale.x * rw.dimensions.x) / 2)
			# slide the window to the edge of the building in the x-axis
            sw.location.x = (target.location.x + xlen/2)+0.01
            self.addWindowModifier(target, sw, 'Y')
            sw.location.z = (target.location.z - zlen/2)+(fw.scale.z * fw.dimensions.z)/2+floor

            # Fourth set is reverse from third set
            rsw = window.copy()
            context.scene.objects.link(rsw)
            # rotate the window around another 180 on the z-axis so it faces out of the building
            rsw.matrix_world = rsw.matrix_world * reverse_rot * ninety_rot
	        # shift it on the y-axis to the opposite face of the building
            rsw.location.y = (target.location.y+(ylen/2))-((rw.scale.x * rw.dimensions.x) / 2)
	        # slide the window to the edge of the building in the x-axis
            rsw.location.x = (target.location.x - target.scale.x)-0.01
            self.addWindowModifier(target, rsw, 'Y')
            rsw.location.z = (target.location.z - zlen/2)+(fw.scale.z * fw.dimensions.z)/2+floor
        return
    
    def addBuildingTop(self,target):
        top = bpy.data.objects["building_top"]
        btop = top.copy()
        context.scene.objects.link(btop)
        btop.location.z = target.location.z + (target.scale.z*target.dimensions.z)/2
        btop.location.x = target.location.x
        btop.location.y = target.location.y
        btop.scale.x = target.scale.x
        btop.scale.y = target.scale.y
        return
    
    def decorate(self,target):
	    # 30% chance of it having a inset footprint
        if random.randint(0,100) < 30:
            obj_new=self.duplicateObject(context.scene,"insetfootprint",target)
            obj_new.scale.x = target.scale.x-0.15
            obj_new.scale.y = target.scale.y-0.15
            obj_new.scale.z = 1.0
            obj_new.location.z=1.0
			# Translate the original object up one floor and scale it down one floor
            target.location.z += 1.0
            target.scale.z -= 1.0
        # chances of different types of windows
        if random.randint(0,100) < 30:
            self.addWindows(target,bpy.data.objects["standard_windows"])
        else:
            if random.randint(0,100) < 50:
                self.addWindows(target,bpy.data.objects["inset_windows"])
            else:
                self.addWindows(target,bpy.data.objects["narrow_windows"]) 
        # 50% chance of having a ledge top
        if random.randint(0,100) < 50:
            self.addBuildingTop(target)
        return
    
    # The following function is adapted from  
    # Nick Keeline "Cloud Generator" addNewObject  
    # from object_cloud_gen.py (an addon that comes with the Blender 2.6 package) 
    def duplicateObject(self,scene, name, copyobj):
        # Create new mesh
        mesh = bpy.data.meshes.new(name)
        # Create new object associated with the mesh
        ob_new = bpy.data.objects.new(name, mesh)
        # Copy data block from the old object into the new object
        ob_new.data = copyobj.data.copy()
        ob_new.scale = copyobj.scale
        ob_new.location = copyobj.location
        # Link new object to the given scene and select it
        scene.objects.link(ob_new)
        ob_new.select = True
        return ob_new

    def build(self,target,name,alignment):
        # Get the current scene - the declaration allows the code completion to work in eclipse
        # scene = bpy.context.scene
        scene = context.scene        
        obj_new=self.duplicateObject(scene,name,target)        
        bpy.context.scene.objects.active=obj_new
        
        #Scale the object up
        obj_new.scale.x=self.scalex
        obj_new.scale.y=self.scaley
        obj_new.scale.z=self.scalez
       
        # move the new object in the x-axis, y-axis so it aligns as a street 
		# and the z axis so the base of the object it at 0.0
        tx = target.location.x+(target.dimensions.x*target.scale.x)/2+(obj_new.scale.x*obj_new.dimensions.x/2)+random.randrange(0,3)
        ty = target.location.y+((target.scale.y-obj_new.scale.y)*alignment)
        
        # Get some random stepping in the front faces of the buildings
        if random.randrange(0,100) < 50:
            ty += 0.1
        else:
            ty -=0.1
        tz = obj_new.scale.z
        obj_new.location = (tx,ty,tz)
		
		# produce a building like structure from the original object
        self.decorate(obj_new)
		
        #now generate a random scale and offset for the next bounding building
        
        self.scalex = random.randrange(2,self.width)
        self.scaley = random.randrange(2,self.length)
        self.scalez = random.randrange(3,self.height)
        return obj_new
 
# Get the base cube as a seed
random.seed()
 
# Transform the cube so the base is on the z axis
# types object API defines the methods on the OBJECT 
building = bpy.data.objects["Cube"]
building.location = (0,0,building.dimensions.z/2)
     
# Create a building factory
b = builder(10,12,15)
 
    # Build 20 random buildings
for n in range(1,25):
    building_name=""
    building_name="Building"+str(n)
    print("\n\n\nCreated "+building_name)
    building = b.build(building,building_name,1.0)

	# Build 20 random buildings

building = bpy.data.objects["Cube"]
building.location = (0,15.0,building.dimensions.z/2)
for n in range(1,25):
    building_name=""
    building_name="Building"+str(n)
    print("\n\n\nCreated "+building_name)
    building = b.build(building,building_name,-1.0)