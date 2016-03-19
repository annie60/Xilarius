from Class import Xilarius


def list_xil(WW, WH):
    list_x = []
    
    X = WW
    Y = WH
    
    Xi = 0
    Yi = 0
    
    while Yi < int(WH/16):
        while Xi < int(WW/16):
            list_x.append(Xilarius((Xi * 16, Yi * 16)))
            Xi += 1
            
        Xi = 0
        Yi += 1    
        
    return list_x

def fill_list_x2(list_x1):
    list_x2 = []
    for i in list_x1:
        list_x2.append(i)    
        
    return list_x2