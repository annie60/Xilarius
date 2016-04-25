from Class import Xilarius

#Helper to generate new list of cells
def list_xil(WW, WH):
    list_x = []
    
    X = WW
    Y = WH
    
    Xi = 0
    Yi = 0
    
    while Yi < int(WH/26):
        while Xi < int(WW/26):
            list_x.append(Xilarius((Xi * 26, Yi * 26)))
            Xi += 1
            
        Xi = 0
        Yi += 1    
        
    return list_x
#Helper to fill temporary list of cells
def fill_list_x2(list_x1):
    list_x2 = []
    for i in list_x1:
        list_x2.append(i)    
        
    return list_x2