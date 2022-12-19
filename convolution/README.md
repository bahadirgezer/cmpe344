# Convolution Implementation
In this project, we used the cache module of Python [pycachesim](https://pypi.org/project/pycachesim). It helps simulate a cache hierarchy. You can construct a set of caches connected to the main memory by defining their shape and replacement policies. Whenever you need to do some load or store operation you need to give memory indices and data to the module. The module processes those memory accesses and calculates the data movement between the caches and main memory. 

However, this module misses an important feautre, it does not contain a mechanism to actually save the data, it only takes the accessed indices into account not the values. For this reason we have a simple class called cache_module. 

The [cache_module](./cache_module.py) class has three levels of caches and a main memory, these are all constructed and connected. To imitate the main memory we use a a large array. 

This project uses the cache module to implement a simple convolution operation. The program is given with the following variables:

* **image:** 3D array which imitates an RGB image.
* **mask:** 3x3 array to be used as a mask for the convolution.
* **result:** result array to store the convolution result



## Run 

Use the terminal line to run the program. 


```
python task.py
```

## Implementation Details

The program runs in three main steps. 

### Step 1:

The image array is loaded into the memory array using the cache module write function. The image is placed starting from the first index of the memory. This is done for program simplicity. The image is loaded in way such that we have image.row rows and (image.col * 3) columns and each column is padded with zero values. 

### Step 2:

The image is fetched from the memory using the cache module read function. Then the mask is applied for each cell of the image. In this step, the result array is not used. Resulting convoluted cell value is stored directly back to the memory. The memory space for the result is determined by an offset which is the size of the image array plus another column. 

### Step 3:

The result array is fetched from the memory using the cache module read function. The offset is used to determine the starting index of the result array. 

### Data Conversion

The input image uses the numpy.int64 datatype and the simulated memory uses numpy.uint8 datatype. So we need to convert the data types. The conversion is done by hand using the numpy.frombuffer and numpy.tobytes functions. One int64 value corresponds to an array of 8 uint8 values. 