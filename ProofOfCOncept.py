import bpy
import scaleConverter


class ObjectBoard():
    def __init__ (self,loc=[0,0,0], size=[6,6,6], name="Unassigned"):
        self.object = self.MakeMesh(size, loc, name)
        
        #object.select = True
        bpy.context.scene.objects.active = self.object
        #bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.context.object.data.show_extra_edge_length = True
        bpy.context.object.show_wire = True
        
        
    def MakeMesh(self, size, loc, name):
        #Convert Inches to Meter
        size[0], size[1], size[2] = scaleConverter.ImperialToMetric([size[0], size[1], size[2]])
        loc[0], loc[1], loc[2] = scaleConverter.ImperialToMetric([loc[0], loc[1], loc[2]])

        #verts = LowerBackLeft, LowerBackRight, LowerFrontLeft, LowerFrontRight
        verts = [(0,0,0),(size[0],0,0),(0,size[1],0),(size[0],size[1],0),(0,0,size[2]),(size[0],0,size[2]),(0,size[1],size[2]),(size[0],size[1],size[2])]
        #Faces = BotomVerts, TopVerts, FrontVerts, BackVerts, LeftVerts, RightVerts
        faces = [(0,1,3,2),(4,5,7,6),(2,3,7,6),(0,1,5,4),(0,2,6,4),(1,3,7,5)]
        
        #Define mesh and object
        mesh = bpy.data.meshes.new(name)
        object = bpy.data.objects.new(name, mesh)
        object.location = (loc)
        bpy.context.scene.objects.link(object)
        
        #Create mesh
        mesh.from_pydata(verts,[],faces)
        mesh.update(calc_edges=True)

        return(object)


    def Size(self, size=None):
        if size is None:
            #Get XYZ of every vert
            vertXYZ = []
            for vertex in self.object.data.vertices:
                vertXYZ.append(vertex.co)
            #Calc size of object in meters
            minVertXYZ = min(vertXYZ)
            maxVertXYZ = max(vertXYZ)
            
            return(maxVertXYZ[0]-minVertXYZ[0], maxVertXYZ[1]-minVertXYZ[1], maxVertXYZ[2]-minVertXYZ[2])
        
        else:
            #Change size of mesh
            size = scaleConverter.ImperialToMetric(size)
            for vertex in self.object.data.vertices:
                if vertex.co.x != size[0] and vertex.co.x > 0:
                    vertex.co.x = size[0]
            for vertex in self.object.data.vertices:
                if vertex.co.y != size[1] and vertex.co.y > 0:
                    vertex.co.y = size[1]
            for vertex in self.object.data.vertices:
                if vertex.co.z != size[2] and vertex.co.z > 0:
                    vertex.co.z = size[2]
              
                
    def Name(self, name=None):
        if name is None:
            return self.object.name
        else:
            self.object.name = name
        
    def Location(self, loc=None):
        if loc is None:
            return(self.object.location)
        else:
            self.object.location = loc



def Allign(objectList, allignAxis=1):
    count = 0
    for objects in objectList:
        if count == 0:
            #Object to align all other objects too
            originalLoc = objectList[count].Location()
            size = objectList[count].Size()
            allignLoc = [(originalLoc[0]+size[0]), (originalLoc[1]+size[1]), (originalLoc[2]+size[2])]
            count += 1
        else:
            #Move to align location
            #0=x, 1=y, 2=z
            if allignAxis == 0:
                objectList[count].Location((allignLoc[0],originalLoc[1],originalLoc[2]))
            elif allignAxis == 1:
                objectList[count].Location((originalLoc[0],allignLoc[1],originalLoc[2]))
            elif allignAxis == 2:
                objectList[count].Location((originalLoc[0],originalLoc[1],allignLoc[2]))
            
            #Calc next allign location
            size = objectList[count].Size()
            allignLoc = [(allignLoc[0]+size[0]), (allignLoc[1]+size[1]), (allignLoc[2]+size[2])]
            count += 1
        

def MakeStuff(amount=12):
    stuff = []
    count = 0
    while count < amount:
        stuff.append(ObjectBoard(name="Board"+str(count), size=[6,6,6], loc=[0,0,12]))
        print("Name", stuff[count].Name())
        print("Loc", stuff[count].Location())
        print("Size", stuff[count].Size())
        count += 1
    
    Allign(stuff, allignAxis=1)

    #for objects in stuff:
    #    print(objects.Location)
        
MakeStuff()