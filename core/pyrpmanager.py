import operator as oper
import itertools as itr

#Stores relations between RPArrays in a tree like structure 
rpa_tree = []

#Depreciated
rpa_dictionary = {}


class RPArray():
    '''
    Relative Position Array. Creates a grid of coordinates in 3D space whos
    positions are defined by arbitrary size values.
    '''
    def __init__(self, name, location=[0,0,0]):
        self.rpa_origin = location
        self.rpa_name = name

        #[axis][level][length(0), accumulative(1), lock(2)]
        self.rpa_array = (
            [[[1,0,False]],
            [[1,0,False]],
            [[1,0,False]]])
            

    def ResizeArray(self, axis, index, size):
        '''
        Adds or removes a row from rp_array. Will not remove a row if 
        last one. Will remove a row of size is 0. Axis is type Int from 0-2
        representing XYZ. Index is position row is to be added/removed. Size
        is length.    
        '''
        if size == 0:
            #Remove Row
            if len(self.rpa_array[axis]) > 1:
                del(self.rpa_array[axis][index])
        else:
            #Add row
            self.rpa_array[axis].insert(index, [size, 0])        
    
    def ResizeRow(self, axis, index, size):
        '''
        Assignes a new size/length to the given row. Axis is Int from 0-2 
        representing XYZ. Index is the row to be altered. Size is length.
        '''
        #Resize the row
        self.rpa_array[axis][index][0] = size

    def AccumulateArray(self):
        '''
        Loops through rp_array adding together lengths to update XYZ positions
        in array.
        '''
        for axis in range(3):
            for index, i in enumerate(self.rpa_array[axis]):
                if index == 0:
                    self.rpa_array[axis][index][1] = 0
                else:
                    self.rpa_array[axis][index][1] = self.rpa_array[axis][index-1][0] + self.rpa_array[axis][index-1][1]

    def ReturnIndex(self, index):
        '''
        Returns [[Xn,Yn,Zn],[Xp,Yp,Zp]] location and size of specified index.
        Index is Vec3 with each value representing position along axis.
        Remember to use AccumulateArray() to update XpYpZp.
        '''
        position = [[0,0,0],[0,0,0]]
        for axis, value in enumerate(position[0]):
            position[0][axis] = self.rpa_array[axis][index[axis]][1]
        for axis, value in enumerate(position[1]):
            position[1][axis] = self.rpa_array[axis][index[axis]][0]
        
        return(position)
    
    def NameRPArray(self, name=None):
        '''
        Returns name of instance if name is None.
        Renames instance if name provided.
        RPATree must be updated after a name change.
        '''
        if name:
            self.rpa_name = name
        else:
            return(self.rpa_name)
        
    def ScaleRPArray(self):
        '''
        Resizes rpa_array to conform with
        '''
        pass


def RPADictionary(instance=None, name=None):
    '''
    Depreciated
    Adds new instances to rpa_dictionary and returns instance of given name.
    New instance is added when instance is passed.
    '''
    if instance:
        #Add to dic
        name = instance.NameRPArray()
        rpa_dictionary[name] = instance
    else:
        #return instance
        return(rpa_dictionary[name])

def RPADicRemove(name):
    '''
    Depreciated
    Removes an entry from rpa_dictionary.
    Name is name of entry to remove.
    '''
    if name:
        del(rpa_dictionary[name])

def RPADicUpdate(name):
    '''
    Depreciated
    Updates rp_dictionary names.
    Name is name of instance before renaming.
    If name is passed will update single entry only.
    If no name passed will recursivly update all entrys.
    '''
    if name:
        #Update single entry
        instance = rpa_dictionary[name]
        new_name = instance.NameRPArray()
        rpa_dictionary[new_name] = rpa_dictionary.pop(name)
    else:
        #Update all entrys
        for name, instance in rpa_dictionary.items():
            name = instance.NameRPArray()
            rpa_dictionary[name] = instance
    
    
def MakeRPArray(name, location=[0,0,0], rows=[0,0,0]):
    '''
    Create a new rparray.
    Abstracts internal workings of pyrpmanager to provide a simple API
    '''
    #Create a new RPArray
    instance = RPArray(name)
    #Add RPArray to RPADictionary so we have a record.
    RPADictionary(instance)
    return(instance)
    





if __name__ == '__main__':
    print('Testing pyrpmanager functions...')
    #New array
    instance = MakeRPArray('SpamArray')
    instance2 = MakeRPArray('SpamArray2')
    print(instance.rpa_array)
    #Check if instance added to RPADictionary
    print(rpa_dictionary)
    #New row
    instance.ResizeArray(0,0,2)
    print(instance.rpa_array)
    #remove row
    instance.ResizeArray(0,0,0)
    print(instance.rpa_array)
    #Resize row
    instance.ResizeRow(0,0,7)
    print(instance.rpa_array)
    #Get name
    print(instance.NameRPArray())
    #Change name
    instance.NameRPArray('NewSpam')
    print(instance.NameRPArray())
    #See if RPADictionary updated to new name
    print(RPADictionary(name='NewSpam'))
    #New row
    instance.ResizeArray(0,0,2)
    print(instance.rpa_array)
    #New row
    instance.ResizeArray(0,0,3)
    print(instance.rpa_array)
    #Calculate XYZ locations
    instance.AccumulateArray()
    print(instance.rpa_array)
    #Get XYZ XpYpZp of index
    print(instance.ReturnIndex([1,0,0]))