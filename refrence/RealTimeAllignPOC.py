import bpy
import time
import threading
import scaleConverter


class ObjectBoard(threading.Thread):
    def __init__ (self, threadID, name="Unassigned"):
        self.threadID = threadID
        threading.Thread.__init__(self)
        self.name = name
        self.FPS = 4
        self.is_running = True


    def run(self):
        #Create objects
        self.object_list = []
        count = 10
        while count > 0:
            self.object_list.append(self.MakeMesh(size=[6,6,6], loc=[0,0,0], name="Test%s"%(count)))
            count -= 1
        
        #Main program loop
        objectList_size = []
        objectList_loc = []
        tick = time.time()
        loop = 0
        while self.is_running is True:
            if time.time() >= tick+(1/self.FPS):
                tick = time.time()
                time.sleep(1/self.FPS)
                loop += 1
                #Note that objectList_size & ..._loc are actually objectList._last... in Allign()
                objectList_size, objectList_loc = self.Allign(objectList_lastSize=objectList_size, objectList_lastLoc=objectList_loc)
                #print(objectList_loc[0])
                if loop >= 100:
                    self.is_running = False
            else:
                continue
        
        
    def MakeMesh(self, size, loc, name):
        '''
        Creates cubes with specified dimentions and location in inches.
        '''
        #Convert Inches to Meter
        size = scaleConverter.ImperialToMetric(size)
        loc = scaleConverter.ImperialToMetric(loc)

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
    
    
    def Allign(self, objectList_lastSize, objectList_lastLoc, allign_axis=[0,1,0], allign_shift=[1,0,0]):
        '''
        Takes a list of objects and alligns them beside eachother.
        Returns two lists with size and loc of objects.
        '''
        #We will need this variable frequently for loops and to ensure we dont get 'Out of range errors' when doing index math.
        objectList_len = len(self.object_list)
        
        #If first run
        if len(objectList_lastSize) == 0:
            #Get current object size and loc
            objectList_size = []
            objectList_loc = []
            for object_number in range(objectList_len):
                objectList_size.append(self.Size(object_number))
                objectList_loc.append(self.object_list[object_number])
            
            #Set current as last since we need this to do calculations what changed from last lookup.
            objectList_lastSize = objectList_size
            objectList_lastLoc = objectList_loc
            
            #We need this for the allignment code so it knows to allign to index 0 before alligning according to user changes
            first_run = True
        
        #if not first run...
        else:
            #Get current object size and loc
            objectList_size = []
            objectList_loc = []
            for object_number in range(objectList_len):
                objectList_size.append(self.Size(object_number))
                objectList_loc.append(self.object_list[object_number].location)
            
            first_run = False
            
            #print(objectList_loc[0])
            
        #Find which object(s) have changed by comparing current and last size, loc.
        object_changed = []
        
        #last and current always same?
        for object_number in range(objectList_len):
            if objectList_lastLoc[object_number] != self.object_list[object_number].location:
                object_changed.append(object_number)
                print("New Change!")
                
        print(objectList_lastLoc[0])
        print(self.object_list[0].location)
        
        '''
        for object_number in range(objectList_len):
            if objectList_size[object_number] != objectList_lastSize[object_number]:
                object_changed.append(object_number)
            elif objectList_loc[object_number] != objectList_lastLoc[object_number]:
                object_changed.append(object_number)
        '''
                
        #Reallign objects with user edits
        #Currently this only works with one change
        if first_run is True:
            for object_number in range(objectList_len):
                #Dont allign the first object
                if object_number == 0:
                    pass
                else:
                    #Allign non first objects to XYZ according to allign_axis
                    if allign_axis[0] == 1:
                        self.object_list[(object_number)].location.x = (self.object_list[object_number-1].location.x+(objectList_size[object_number-1][0]))
                    if allign_axis[1] == 1:
                        self.object_list[(object_number)].location.y = (self.object_list[object_number-1].location.y+(objectList_size[object_number-1][1]))
                    if allign_axis[2] == 1:
                        self.object_list[(object_number)].location.z = (self.object_list[object_number-1].location.z+(objectList_size[object_number-1][2]))
        
        #If not first run
        else:
            objectChanged_len = len(object_changed)
            #If we have user modified objects...
            if objectChanged_len > 0:
                #Make sure we arnt using last index so that we have an object to allign reading up our object index
                if object_changed[0] < objectList_len:
                    for object_number in range(object_changed[0], objectList_len):
                        #print(object_number)
                        pass
                #If our changed object is not index 0 then we need to allign down the object index
                if object_changed[0] > 0:
                    pass
                
            #There were no user modified objects
            else:
                pass
            
        return(objectList_size, objectList_loc)
                      
        
        '''
        #Old allign code
        last_loc = []
        last_size = []
        allign_loc = []
        for object_number in range(len(self.object_list)):
            if object_number == 0:
                last_loc = self.object_list[object_number].location
                last_size = self.Size(object_number)
                allign_loc = [(last_loc[0]+self.Size(object_number)[0]), (last_loc[1]+self.Size(object_number)[1]), (last_loc[2]+self.Size(object_number)[2])]
            else:
                self.object_list[object_number].location.y = last_loc[1]+last_size[1]
                
                
                size = self.Size(object_number)
                if allign_axis[0] == 1:
                    self.object_list[object_number].location.x = allign_loc[0]+last_size[0]
                if allign_axis[1] == 1:
                    self.object_list[object_number].location.y = allign_loc[1]+last_size[1] 
                if allign_axis[2] == 1:
                    self.object_list[object_number].location.z = allign_loc[2]+last_size[2]
                
                
                last_loc = self.object_list[object_number].location
                last_size = self.Size(object_number)
                allign_loc = [(last_loc[0]+self.Size(object_number)[0]), (last_loc[1]+self.Size(object_number)[1]), (last_loc[2]+self.Size(object_number)[2])]
        '''
            
                
    def LastLocSize(self, object):
            last_loc = object.location
            last_size = self.Size(object)
            allign_loc = [(last_loc[0]+self.Size(object)[0]), (last_loc[1]+self.Size(object)[1]), (last_loc[2]+self.Size(object)[2])]
            return last_loc, last_size, allign_loc
        
                    
    def Size(self, object_number):
        #Get XYZ of every vert
        vertXYZ = []
        for vertex in self.object_list[object_number].data.vertices:
            vertXYZ.append(vertex.co)
        #Calc size of object in meters
        minVertXYZ = min(vertXYZ)
        maxVertXYZ = max(vertXYZ)

        return(maxVertXYZ[0]-minVertXYZ[0], maxVertXYZ[1]-minVertXYZ[1], maxVertXYZ[2]-minVertXYZ[2])
        
        
thread = ObjectBoard(1)
thread.start()