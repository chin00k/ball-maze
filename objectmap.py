import numpy as np #for the map array
import random 
import hashlib #to generate an array


def hashseed(string):
    #to convert any string
    #to a 256 bit int number using SHA-256
    
    #the sha256. It ouputs a hex string
    result = hashlib.sha256(string.encode()).hexdigest()
    
    #conversion to binary
    result = int(result, base=16)
    
    #then to a string
    result = str(bin(result))
    
    #then add leading zeros to get to 256 numbers
    result = str(result[2:].zfill(256))
        
    return result

def setup(string, manualset, px, py):
    
    def cr(lb, ub):
        return random.randint(lb, ub)
    
    
    hashtable = hashseed(string) #get the 256 bit processed seed
    
    #make a 16 by 16 empty numpy array
    objectsarray = np.zeros((16,16)) 
    
    #for every entry in the empty array
    for i in range(16):
        for j in range(16):
            '''
            add either 1 or 0 (based on the hashed seed)
            to the linear position of that 1 or 0
            
            This creates an int seed that is given to a random
            number generator, which picks between 1 and 3,
            and if it gets 1, add a 1 (a block) to the map array
            
            Do this for every position in the map array
            
            These steps ensure that for a given seed, the map is always
            the same.
            '''
            seed = hashtable[16 * i + j] + str((16 * i + j))
            random.seed(int(seed))
            choice = cr(1, 3)
            if choice == 1:
                objectsarray[i][j] = 1
    
    

    random.seed() #reset the RNG seed to the system time (the default)
    
    #If we are manually adding the portal, add it here
    #it will overwrite anything
    if manualset == True:
        objectsarray[px][py] = 9
    
    #If we are not manually adding the portal
    #add it randomly here
    if manualset == False:
        while 1:
            #The loop loops until it finds an open spot
            #and then adds the portal
            
            #actually random RNG, not like the blocks
            x = cr(0,15)
            y = cr(0,15)       
            if objectsarray[x, y] == 0:
                objectsarray[x, y] = 9
                break
        
    
        
    #adds a number of spikes    
    for i in range(12):
        random.seed(int(seed))        
        while 1:
            #same as above, it will only add a spike to an
            #empty block, and it will keep trying until
            #it gets an empty block
            x = cr(0,15)
            y = cr(0,15)       
            if objectsarray[x, y] == 0:
                objectsarray[x, y] = 5
                break
    
    
    return objectsarray #return the completed map of the game level