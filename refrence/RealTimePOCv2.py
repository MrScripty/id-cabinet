import bpy
import time
import threading
import scaleConverter

object_list = bpy.context.selected_objects
print(object_list)

class ScriptThread (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.FPS = 1
        self.is_running = True
    
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
        

    def Allign(self, object_list, allign_axis=[1,1,1], allign_shift=[1,0,0]):
        '''
        Takes a list of objects and alligns them beside eachother.
        '''
        origin_loc = [0,0,0]
        origin_size = [0,0,0]
        first = True
        for objects in object_list:
            if first is True:
                origin_loc = objects.location
                origin_size = self.Size(objects)
                allign_loc = [(origin_loc[0]+self.Size(objects)[0]), (origin_loc[1]+self.Size(objects)[1]), (origin_loc[2]+self.Size(objects)[2])]
                first = False
            else:
                loc = objects.location
                size = self.Size(objects)
                if allign_axis[0] == 1:
                    objects.location.x = allign_loc[0]+origin_size[0]
            

    def Size(self, object):
        #Get XYZ of every vert
        vertXYZ = []
        for vertex in object.data.vertices:
            vertXYZ.append(vertex.co)
        #Calc size of object in meters
        minVertXYZ = min(vertXYZ)
        maxVertXYZ = max(vertXYZ)

        return(maxVertXYZ[0]-minVertXYZ[0], maxVertXYZ[1]-minVertXYZ[1], maxVertXYZ[2]-minVertXYZ[2])
    
    def run(self):
        object_list = []
        object_list.append(self.MakeMesh(size=[6,6,6], loc=[0,0,0], name="Test1"))
        object_list.append(self.MakeMesh(size=[6,6,6], loc=[12,0,0], name="Test2"))
        tick = time.time()
        loop = 0
        while self.is_running is True:
            if time.time() >= tick+(1/self.FPS):
                tick = time.time()
                print(loop)
                time.sleep(1/self.FPS)
                loop += 1
                self.Allign(object_list)
                if loop >= 100:
                    self.is_running = False
            else:
                continue
            


#Make thread
thread = ScriptThread(1, "thread")
thread.start()
