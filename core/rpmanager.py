'''
RPManager
'''

rp_grids = {}


class RPGrid():
    '''
    Calculates grids
    '''
    def __init__(self, name='rename', location=[0,0,0]):
        self.rp_data = [[],[],[[],[],[]]]
        self.rp_data[0]= name
        self.rp_data[1] = location

    def MakeRows(self, rows=[0,0,0]):
        '''
        Adds or removes X# XYZ rows to the RPGrid.
        '''
        for axis in range(3):
            axis -= 1
            if rows[axis] < 0:
                #Remove Rows
                while rows[axis] < 0:
                    rows[axis] += 1
                    del self.rp_data[2][axis][-1]
            elif rows[axis] > 0:
                #Add rows
                while rows[axis] > 0:
                    rows[axis] -= 1
                    self.rp_data[2][axis].append(0)

    def Name(self, name=None):
        '''
        Returns RPGrid name if no name provided, renames if provided.
        '''
        if name is None:
            #Return name of RPGrid
            return(self.rp_data[0])
        else:
            #Rename RPGrid
            self.rp_data[0] = name

    def DumpData(self):
        return(self.rp_data)

def RPGDic(name, instance=False, isnew=False):
    '''
    Maintains a dictionarly of every RPGrid instance.
    '''
    if isnew == True and instance != False:
        #Add a new RPGrid
        rp_grids[name] = instance
    else:
        #Return an existing RPGrid
        if len(rp_grids) >= 1:
            if name == False:
                #No name was specified so return full dictionary
                return(rp_grids)
            else:
                #We have a name, find and return its value
                for keys, values in rp_grids.items():
                    if values.Name() is name:
                        return(values)
                        break


def Make(type, name, location=[0,0,0], rows=[0,0,0]):
    '''
    Abstracts internal workings of RPManager to provide a simple API
    '''
    if type == 'RPGRID':
        #Create a new RPGrid
        instance = RPGrid(name)
        #New RPGrids must be added to the RPGDic or we cant acess them!
        RPGDic(name, instance, True)
    elif type == 'ROW':
        #Add rows to a RPGrid
        #First get our RPGrid instance
        instance = RPGDic(name)
        #Add some rows
        instance.MakeRows(rows)
        #Print
        print(instance.DumpData())
