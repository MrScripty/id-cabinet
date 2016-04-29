'''
Script demonstraits creating a mesh object as a class, then creating a cabinet 
with the meshes which dimentions can easly be modified. 

April 28 2016

This script will form one of the core functionalitys of Habitus.

This script does not provide a GUI, please use variables in script.
'''

import bpy
import scaleConverter


class CubeMesh():
    '''
    Creates rectangular meshes of defined size and provides functions for 
    resizing, rotating, placment, naming.
    
    Measurments must be provided in metric units.
    '''
    def __init__(self, name='Rename', location=[0,0,0], rotation=[0,0,0], size=[0.3048,0.3048,0.3048]):
        '''
        Creates a new mesh object and variables needed for other functions to 
        operate.
        '''        
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
        verts = [(0,0,0), 
                (0, size[1], 0),
                (size[0], 0, 0),
                (size[0], size[1], 0),
                (0, 0, size[2]),
                (0, size[1], size[2]),
                (size[0], 0, size[2]),
                (size[0], size[1], size[2])
                ]
                
        #Vertex forming faces in order of Xn, Xp, Yn, Yp, Zn, Zp 
        faces = [(0,1,5,4), 
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
        
        #Test our functions
        self.ResizeMesh()
        
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
        
        
CubeMesh()