import numpy as np
import tensorflow as tf

#A function to print three dimensional cube tensors in MATLAB or Fortran style, to clearly see each layer in depth
#(The NumPy or Python representation follows the C style which is not very intuitive)

def print3d(input3d): 
    if len(input3d.shape) == 3: #Check that there are three dimensions (only print matrices with three dimensions)
        depth = input3d.shape[2] #Determine the number of layers, how deep the cube is
        for i in range(depth): #For each layer
            print(input3d[:,:,i], '\n') #Print a cross-section matrix or slice of the cube
    else: #Otherwise throw an error
        print('Error: This is not a 3D matrix.')

#A function to check whether a tensor is a TensorFlow object or a NumPy array
#TensorFlow objects are then converted to NumPy arrays while NumPy arrays are left unchanged

def convert(input_tensor):
    if isinstance(input_tensor, np.ndarray):
        return input_tensor
    else:
        numpy_tensor = input_tensor.numpy()
        return numpy_tensor

#A function which takes in a sparse tensor in COO format, prompts the user for slicing indices, and returns a sliced tensor, also in COO format
#Note that this function works for tensors with 1, 2, or 3 dimensions

def slice(input_tensor_raw): #Note that input_tensor_raw should be in COO format (can be NumPy or TensorFlow object)
    
    input_tensor = convert(input_tensor_raw) #First check if tensor is a NumPy format; if not, then convert to NumPy array
    
    dimensionality = input_tensor.shape[1] - 1 #Determine the dimensionality of the tensor, i.e. is it 1d, 2d, 3d, etc.
    
    if dimensionality == 1: #This is a vector
        
        print("This is a " + str(dimensionality) + " dimensional tensor" + '\n')
        
        print('Original Tensor in Sparse COO Format')
        print(input_tensor, '\n')
        
        #Determine the size or length of the vector
        length = np.max(input_tensor[:,0]) + 1 
        
        #Convert from sparse COO format to dense format
        denseform = np.zeros(length) 
        denseform[input_tensor[:,0]] = input_tensor[:,1]
        print('Original Tensor in Dense Format')
        print(denseform, '\n')
        
        #Prompt user for slicing indices
        #Declare default values in case left empty
        start = 0
        stop = length
        step = 1
        stringdefault = str(start)+":"+str(stop)+":"+str(step)
        userinput = input("Enter slicing indices in the format start:stop:step, type here -> ") or stringdefault
        response = userinput.split(':')
        responselist = list(map(int, response))
        start = responselist[0]
        stop = responselist[1]
        step = responselist[2]
        
        #Slice the tensor using indices provided by user
        denseformsliced = denseform[start:stop:step] 
        print('')
        print('Sliced Tensor in Dense Format')
        print(denseformsliced, '\n')

        #Convert from dense format back into sparse COO format
        indicescoo = np.where(denseformsliced != 0)[0]
        valuescoo = denseformsliced[indicescoo]
        outputcoo = np.transpose(np.vstack((indicescoo, valuescoo)))
        print('Sliced Tensor in Sparse COO Format')
        print(outputcoo, '\n')
        
        return outputcoo
    
    if dimensionality == 2: #This is a matrix
        
        print("This is a " + str(dimensionality) + " dimensional tensor" + '\n')
        
        print('Original Tensor in Sparse COO Format')
        print(input_tensor, '\n')
        
        #Determine the size or shape of the matrix
        rows = np.max(input_tensor[:,0]) + 1
        cols = np.max(input_tensor[:,1]) + 1
        
        #Convert from sparse COO format to dense format
        denseform = np.zeros((rows, cols)) 
        denseform[input_tensor[:,0], input_tensor[:,1]] = input_tensor[:,2]
        print('Original Tensor in Dense Format')
        print(denseform, '\n')
        
        #Prompt user for slicing indices (for each dimension)
        #Declare default values in case left empty
        start = 0
        stop1 = rows
        stop2 = cols
        step = 1
        stringdefault1 = str(start)+":"+str(stop1)+":"+str(step)
        stringdefault2 = str(start)+":"+str(stop2)+":"+str(step)
        userinput1 = input("Enter slicing indices for the first dimension in the format start:stop:step, type here -> ") or stringdefault1
        response1 = userinput1.split(':')
        responselist1 = list(map(int, response1))
        start1 = responselist1[0]
        stop1 = responselist1[1]
        step1 = responselist1[2]
        userinput2 = input("Enter slicing indices for the second dimension in the format start:stop:step, type here -> ") or stringdefault2
        response2 = userinput2.split(':')
        responselist2 = list(map(int, response2))
        start2 = responselist2[0]
        stop2 = responselist2[1]
        step2 = responselist2[2]
        
        #Slice the tensor using indices provided by user
        denseformsliced = denseform[start1:stop1:step1, start2:stop2:step2]
        print('')
        print('Sliced Tensor in Dense Format')
        print(denseformsliced, '\n')

        #Convert from dense format back into sparse COO format
        rowscoo = np.where(denseformsliced != 0)[0]
        colscoo = np.where(denseformsliced != 0)[1]
        valuescoo = denseformsliced[rowscoo, colscoo]
        outputcoo = np.transpose(np.vstack((rowscoo, colscoo, valuescoo)))
        print('Sliced Tensor in Sparse COO Format')
        print(outputcoo, '\n')
        
        return outputcoo

    if dimensionality == 3: #This is a cube
   
        print("This is a " + str(dimensionality) + " dimensional tensor" + '\n')
    
        print('Original Tensor in Sparse COO Format')
        print(input_tensor, '\n')
    
        #Determine the size or shape of the cube
        rows = np.max(input_tensor[:,0]) + 1
        cols = np.max(input_tensor[:,1]) + 1
        layers = np.max(input_tensor[:,2]) + 1
        
        #Convert from sparse COO format to dense format
        denseform = np.zeros((rows, cols, layers))
        denseform[input_tensor[:,0], input_tensor[:,1], input_tensor[:, 2]] = input_tensor[:,3]
        print('Original Tensor in Dense Format')
        print3d(denseform)
        
        #Prompt user for slicing indices (for each dimension)
        #Declare default values in case left empty
        start = 0
        stop1 = rows
        stop2 = cols
        stop3 = layers
        step = 1
        stringdefault1 = str(start)+":"+str(stop1)+":"+str(step)
        stringdefault2 = str(start)+":"+str(stop2)+":"+str(step)
        stringdefault3 = str(start)+":"+str(stop3)+":"+str(step)
        userinput1 = input("Enter slicing indices for the first dimension in the format start:stop:step, type here -> ") or stringdefault1
        response1 = userinput1.split(':')
        responselist1 = list(map(int, response1))
        start1 = responselist1[0]
        stop1 = responselist1[1]
        step1 = responselist1[2]
        userinput2 = input("Enter slicing indices for the second dimension in the format start:stop:step, type here -> ") or stringdefault2
        response2 = userinput2.split(':')
        responselist2 = list(map(int, response2))
        start2 = responselist2[0]
        stop2 = responselist2[1]
        step2 = responselist2[2]
        userinput3 = input("Enter slicing indices for the third dimension in the format start:stop:step, type here -> ") or stringdefault3
        response3 = userinput3.split(':')
        responselist3 = list(map(int, response3))
        start3 = responselist3[0]
        stop3 = responselist3[1]
        step3 = responselist3[2]
        
        #Slice the tensor using indices provided by user
        denseformsliced = denseform[start1:stop1:step1, start2:stop2:step2, start3:stop3:step3]
        print('')
        print('Sliced Tensor in Dense Format')
        print3d(denseformsliced)
                                                          
        #Convert from dense format back into sparse COO format
        rowscoo = np.where(denseformsliced != 0)[0]
        colscoo = np.where(denseformsliced != 0)[1]
        layerscoo = np.where(denseformsliced != 0)[2]
        valuescoo = denseformsliced[rowscoo, colscoo, layerscoo]
        outputcoo = np.transpose(np.vstack((rowscoo, colscoo, layerscoo, valuescoo)))
        print('Sliced Tensor in Sparse COO Format')
        print(outputcoo, '\n')
        
        return outputcoo
                                    