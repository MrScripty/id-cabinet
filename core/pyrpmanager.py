import operator as oper
import itertools as itr


class RPArray():
    '''
    Relative Position Array. Creates a grid of coordinates in 3D space whos
    positions are defined by arbitrary size values.
    '''
    def __init__(self, name, location=[0,0,0]):
        self.rp_origin = location
        self.rp_name = name

        #[axis][level][length(0) or accumulative(1)]
        self.rp_array = (
            [[[1,0]],
            [[1,0]],
            [[1,0]]])
            

    def ResizeArray(self, axis, index, size):
        '''
        Adds or removes a row from rp_array. Will not remove a row if 
        last one. Will remove a row of size is 0. Axis is type Int from 0-2
        representing XYZ. Index is position row is to be added/removed. Size
        is length.    
        '''
        if size == 0:
            #Remove Row
            if len(self.rp_array[axis]) > 1:
                del(self.rp_array[axis][index])
        else:
            #Add row
            self.rp_array[axis].insert(index, [size, 0])        
    
    def ResizeRow(self, axis, index, size):
        '''
        Assignes a new size/length to the given row. Axis is Int from 0-2 
        representing XYZ. Index is the row to be altered. Size is length.
        If row is given size 0 ResizeArray() will automaticaly be called to
        delete it from rp_array.
        '''
        if size == 0:
            self.ResizeArray(axis, index, 0)
        else:
            #Resize the row
            self.rp_array[axis][index][0] = size

    def AccumulateArray(self):
        '''
        Loops through rp_array adding together lengths to update XYZ positions
        in array.
        '''
        for axis in range(3):
            last = self.rp_array[axis][0][0]
            for index, i in enumerate(self.rp_array[axis]):
                if index == 0:
                    self.rp_array[axis][index][1] = self.rp_array[axis][index][0]
                    continue
                self.rp_array[axis][index][1] = last + self.rp_array[axis][index][0]
                last = self.rp_array[axis][index][0]

    def ReturnIndex(self, index):
        '''
        Returns XnYnZn location and XpYpZp size of specified index.
        Index is Vec3 with each value representing position along axis.
        '''
        position = [[],[],[]]
        position[0] = self.rp_array[0][index[0]]
        position[1] = self.rp_array[1][index[1]]
        position[2] = self.rp_array[2][index[2]]
        return(position)

    def UpdateCall():
        '''
        Calls objects outside instance when indexes are altered.
        '''
        pass


#Create array
rpa = RPArray('SpamArray')
print(rpa.rp_array)
#Add row to array (can also remove)
rpa.ResizeArray(0, 1, 5)
rpa.ResizeArray(0, 1, 3
)
print(rpa.rp_array)
#Resize a row
rpa.ResizeRow(1, 0, 6)
print(rpa.rp_array)
#Updates rp_array with current locations
rpa.AccumulateArray()
print(rpa.rp_array)
#Get position and size of index
position = rpa.ReturnIndex([1,0,0])
print(position)