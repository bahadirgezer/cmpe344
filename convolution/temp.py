import cache_module
import numpy
import time

# Prepare an RGB image containing 3 colour channels.
ROW = 1024
COL = 2048
Channel = 3
image = numpy.random.randint(0, 256, size=(ROW, COL, Channel), dtype=numpy.int64)

# Prepare a mask for the convolution operation.
mask_size = 3
up = 10
down = -10
mask = numpy.random.randint(down, up + 1, size=(mask_size, mask_size), dtype=numpy.int64)

# Prepare an empty result image. You will fill this empty array with your code.
result = numpy.zeros([ROW, COL, Channel], dtype=numpy.int64)

# Configuration for the cache simulator module.
l3 = ["L3", 16384, 16, 64, "LRU"]
l2 = ["L2", 4096, 8, 64, "LRU"]
l1 = ["L1", 1024, 4, 64, "LRU"]
m = 256 * 1024 * 1024
# m = 256 * 1024 * 1024
cm = cache_module.cache_module(l1, l2, l3, m)

###### WRITE YOUR CODE BELOW. ######

def convert_int64_to_uint8(data: numpy.int64) -> numpy.ndarray:
    # convert the data into a numpy.uint8 datatype using bitwise operations
    return numpy.frombuffer(data.tobytes(), dtype=numpy.uint8)

# data is an numpy.ndarray of numpy.uint8
def convert_uint8_to_int64(data: numpy.ndarray) -> numpy.int64:
    # convert the data into a numpy.int64 datatype using bitwise operations
    # the data is a numpy.ndarray of numpy.uint8 and the reshape should output a numpy.int64 datatype
    return numpy.frombuffer(data.tobytes(), dtype=numpy.int64).reshape(1)[0]

def read_from_memory(index: int) -> numpy.int64:
    # read the data from the memory and convert the numpy.uint8 datatype into numpy.int64 datatype using bitwise operations
    data = numpy.zeros(8, dtype=numpy.uint8)
    for i in range(8):
        data[i] = cm.read(index + i)
    return numpy.frombuffer(data.tobytes(), dtype=numpy.int64).reshape(1)[0]

def write_to_memory(index: int, data: numpy.int64):
    # write the data into the memory and convert the numpy.int64 datatype into numpy.uint8 datatype
    data_8bit = numpy.frombuffer(data.tobytes(), dtype=numpy.uint8)
    for i in range(8):
        cm.write(index + i, data_8bit[i])

a = numpy.int64(0x1234567890ABCDEF)
a_8bit_list = convert_int64_to_uint8(a)
a_reconstructed = convert_uint8_to_int64(a_8bit_list)
# print the uint8 array in binary form 
# format the output in a readable way
# replace quotes with spaces

print(format(a, "064b"))

print(format(a_reconstructed, "064b"))


write_to_memory(0, a)

print(format(read_from_memory(0), "064b"))




###### WRITE YOUR CODE ABOVE. ######

cm.finish()