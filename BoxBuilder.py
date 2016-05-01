'''
Script demonstraits creating a mesh object as a class, then creating a cabinet 
with the meshes which dimentions can easly be modified. 

April 28 2016

This script will form one of the core functionalitys of Habitus.

This script does not provide a GUI, please use variables in script.
'''

import bpy
import scaleConverter


class CabinetBox():
    #Variables expressing axis as XYZ represent arbitrary values.
    #Arbitary values are always interpreted as X=Depth, Y=Width, Z=Height
    #regrardless of orientation or global position. 
    #Variables expressing axis as XpYpZp represent a position or direction 
    #as either +(p) or -(n) axis directions. Yn is left, Yp is right...
    def __init__(
        self,
        name = 'Rename',
        overhang = (0,0),
        kick_height = 0.1016,
        strecher_depth = 0.1016,
        planton_location = (0,0),
        overhang_amount = 0.0254,
        counter_thickness = 0.03175,
        size = (0.5588,0.9144,0.9144),
        door_thickness = 0.019049999999999997,
        material_thickness = 0.019049999999999997
        ):
        '''
        Creates a cabinet of specified size and location
        '''
         
        #Variables needed for calculating size and location of all cabinet components 
        self.name = name
        self.size = size
        self.overhang = overhang
        self.kick_height = kick_height
        self.strecher_depth = strecher_depth
        self.door_thickness = door_thickness
        self.overhang_amount = overhang_amount
        self.planton_location = planton_location
        self.counter_thickness = counter_thickness
        self.material_thickness = material_thickness

        #Calculate component vectors
        box_z = self.size[2] - self.kick_height - self.counter_thickness
        box_x = self.size[0] - self.overhang_amount - self.door_thickness
        inside_y = self.size[1] - self.material_thickness*2
        inside_x = box_x - self.material_thickness*2
        
        
        #Create box components
        self.gabble_yn = CubeMesh(
            size=(box_x, self.material_thickness, box_z),
            name = "%s_gabble_yn" %(self.name),
            location=[0,0,self.kick_height],
            rotation=[0,0,0]
            )
        
        self.gabble_yp = CubeMesh(
            rotation = [0,0,0],
            name = "%s_gabble_yp" %(self.name),
            size = (
                box_x,
                self.material_thickness,
                box_z),
            location = (
                0,
                self.size[1]-self.material_thickness,
                self.kick_height)
            )
            
        self.bottom_zn = CubeMesh(
            rotation = [0,0,0],
            name = "%s_bottom_zn" %(self.name),
            size = (
                box_x,
                inside_y,
                self.material_thickness),
            location = (
                0,
                self.material_thickness,
                self.kick_height))
                
        self.back_xn = CubeMesh(
            rotation = [0,0,0],
            name = "%s_back_xn" %(self.name),
            size = (
                self.material_thickness,
                self.size[1] - (self.material_thickness*2),
                box_z - self.material_thickness),
            location = (
                0,
                self.material_thickness,
                self.kick_height + self.material_thickness))
        
        self.strecher_xn = CubeMesh(
            rotation = [0,0,0],
            name = "%s_strecher_xn" %(self.name),
            size = (
                self.strecher_depth,
                inside_y,
                self.material_thickness),
            location = (
                self.material_thickness,
                self.material_thickness,
                self.kick_height + box_z-self.material_thickness)
            )
            
        self.strecher_xp = CubeMesh(
            rotation = [0,0,0],
            name = "%s_strecher_xp" %(self.name),
            size = (
                self.strecher_depth,
                inside_y,
                self.material_thickness),
            location = (
                box_x - self.strecher_depth,
                self.material_thickness,
                self.kick_height + box_z-self.material_thickness)
            )
        
        #Add components to group
        self.cabinet_group = bpy.data.groups.new(self.name)
        
        self.cabinet_group.objects.link(self.gabble_yn.Object)
        self.cabinet_group.objects.link(self.gabble_yp.Object)
        self.cabinet_group.objects.link(self.bottom_zn.Object)
        self.cabinet_group.objects.link(self.back_xn.Object)
        self.cabinet_group.objects.link(self.strecher_xn.Object)
        self.cabinet_group.objects.link(self.strecher_xp.Object)
        
        
        #Parent components to a bone at XnYnZn
        '''
        self.pivot_bone = bpy.ops.object.empty_add(location=(0,0,0))
        
        self.pivot_bone = bpy.data.armatures.new('spam')
        object = bpy.data.objects.new(name, self.pivot_bone)
        bpy.context.scene.objects.link(object)
        print(dir(self.pivot_bone))
        
        print(dir(bpy.context.scene))
        bpy.context.scene.armatures.link(self.pivot_bone)
        
        objects = bpy.data.objects
        a = objects['Cube']
        b = self.gabble_yn.Object
        print(b)
        print(self.pivot_bone.location)
        b.parent = a
        '''
        
        #Move components to repective layer
        self.gabble_yn.Object.layers[1] = True
        self.gabble_yp.Object.layers[1] = True
        self.bottom_zn.Object.layers[1] = True
        self.back_xn.Object.layers[1] = True
        self.strecher_xn.Object.layers[1] = True
        self.strecher_xp.Object.layers[1] = True
        
        self.gabble_yn.Object.layers[0] = False
        self.gabble_yp.Object.layers[0] = False
        self.bottom_zn.Object.layers[0] = False
        self.back_xn.Object.layers[0] = False
        self.strecher_xn.Object.layers[0] = False
        self.strecher_xp.Object.layers[0] = False


class CubeMesh():
    '''
    Creates rectangular meshes of defined size and provides functions for 
    resizing, rotating, placment, naming, etc...
    
    Measurments must be provided in metric units.
    '''
    def __init__(
        self,
        name,
        location,
        rotation,
        size
        ):
              
        #Important for positioning mesh around origin. Not currently implemented.
        self.originPosition = (-0, -1, -2)
        
        #Vertex groups forming faces pointing in following directions... p=+
        #Vertex order of mesh must be maintained or this will not work.
        #We never alter faces pointing in a negitive direction to prevent
        #meshes that read negative edge lengths.
        self.FaceXp = [2,3,6,7]
        self.FaceYp = [1,3,5,7]
        self.FaceZp = [4,5,6,7]
        
        #Create empty mesh and make object
        self.Mesh = bpy.data.meshes.new(name)
        self.Object = bpy.data.objects.new(name, self.Mesh)
        
        #Vert position XYZ in order of XnYnZn, XnYpZn, XpYnZn, XpYpZn...
        verts = [
            (0,0,0), 
            (0, size[1], 0),
            (size[0], 0, 0),
            (size[0], size[1], 0),
            (0, 0, size[2]),
            (0, size[1], size[2]),
            (size[0], 0, size[2]),
            (size[0], size[1], size[2])
            ]
                
        #Vertex forming faces in order of Xn, Xp, Yn, Yp, Zn, Zp 
        faces = [
            (0,1,5,4), 
            (2,3,7,6),
            (0,2,6,4),
            (1,3,7,5),
            (0,1,3,2),
            (4,5,7,6)
            ]
        
        #Link object to scene
        bpy.context.scene.objects.link(self.Object)
        #move object location
        self.Object.location = location
        #Create vertices and faces for mesh
        self.Mesh.from_pydata(verts, [], faces)
        self.Mesh.update(calc_edges=True)
        
        self.Object.select = False
        
    def ResizeMesh(self, size=(1,1,1)):
        '''
        Pushes vertices of Xp Yp Zp faces to resize the mesh. Do not pass
        negitive values, move/rotate instead.
        '''
        for vertID in self.FaceXp:
            self.Object.data.vertices[vertID].co.x = size[0]
        for vertID in self.FaceYp:
            self.Object.data.vertices[vertID].co.y = size[1]
        for vertID in self.FaceZp:
            self.Object.data.vertices[vertID].co.z = size[2]
            
    def MoveObject(location, rotation):
        pass
    
    def Object():
        return(self.Object)
    
    def Name():
        return(self.name)
    
class CabinetRow():
    '''
    Creates a row of cabinets that conform to the specified dimentions.
    '''
    def __init__(self):
        CabinetBox()
        CabinetBox()
        
CabinetRow()
#CabinetBox() 
#CubeMesh()