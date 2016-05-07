'''
NumPy Relative Position Manager (nrpmanager)
RPManager moduel utilising NumPy arrays.

Creates and maintains an axis alligned 3D array.
Returns vector coordinates and dimentions of array indexes
Makes update calls when an index is altered.
'''

import numpy as np


class RPArray():
    '''
    Calculates XYZ arrays
    '''
    def __init__(self, name, location=[0,0,0]):
        self.rp_origin = location
        self.rp_name = name

        #Contains distances, not Coordinates
        self.rp_xyzarray = np.array(
            [[[0]],
            [[0]],
            [[0]]])

    def ReshapeArray(self, index, axis, add=True):
        '''
        Reshapes xyz array, effectivly adding and removing rows of RP's.
        '''
        newrow = (
            [[[1],[1]],
            [[1],[1]],
            [[1],[1]]])
        self.rp_xyzarray = np.hstack((self.rp_xyzarray, newrow))
        print(self.rp_xyzarray)
        pass

    def ArrayUpdate(self, index):
        '''
        Updates xyz array's to conform with specified index.
        '''
        pass

    def ReturnIndex(self, index):
        '''
        Returns XnYnZn location and XpYpZp size of specified index
        '''
        pass

    def UpdateCall():
        '''
        Calls objects outside instance when indexes are altered.
        '''
        pass


rpa = RPArray('SpamArray')
print(rpa.rp_name)
rpa.ReshapeArray(0,0)
#rpa.ReshapeArray()