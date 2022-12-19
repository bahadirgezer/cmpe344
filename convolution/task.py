import cache_module
import numpy
import time

# Prepare an RGB image containing 3 colour channels.
ROW = 32
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

def read_from_memory(index: int) -> numpy.int64:
    data = numpy.zeros(8, dtype=numpy.uint8)
    if index < 0:
        return numpy.int64(0)
    for i in range(8):
        data[i] = cm.read(index + i)
    return numpy.frombuffer(data.tobytes(), dtype=numpy.int64).reshape(1)[0]

def write_to_memory(index: int, data: numpy.int64):
    data_8bit = numpy.frombuffer(data.tobytes(), dtype=numpy.uint8)
    for i in range(8):
        cm.write(index + i, data_8bit[i])
 

# 1. Load the image into the memory

for i in range(ROW):
    for j in range(COL + 2):
        if (j == 0 or j == COL + 1):
            continue
        for k in range(Channel):
            index = (i * (COL + 2) * Channel + j * Channel + k) * 8
            write_to_memory(index, image[i][j - 1][k])


# 2. Traverse the image array and apply the mask. Write the results into the memory

offset = 8 * ROW * (COL + 2) * Channel + (COL + 2) * Channel * 8 + 1
for i in range(ROW):
    for j in range(COL + 2):
        for k in range(Channel):
            index = offset + (i * (COL + 2) * Channel + j * Channel + k) * 8 
            if (j == 0 or j == COL + 1):
                write_to_memory(index, numpy.int64(0))
                continue
            cell_result: numpy.int64 = numpy.int64(mask[0][0] * read_from_memory(((i - 1) * (COL + 2) * Channel + (j - 1) * Channel + k) * 8) + 
            mask[0][1] * read_from_memory(((i - 1) * (COL + 2) * Channel + (j) * Channel + k) * 8) +
            mask[0][2] * read_from_memory(((i - 1) * (COL + 2) * Channel + (j + 1) * Channel + k) * 8) +
            mask[1][0] * read_from_memory(((i) * (COL + 2) * Channel + (j - 1) * Channel + k) * 8) +
            mask[1][1] * read_from_memory(((i) * (COL + 2) * Channel + (j) * Channel + k) * 8) +
            mask[1][2] * read_from_memory(((i) * (COL + 2) * Channel + (j + 1) * Channel + k) * 8) +
            mask[2][0] * read_from_memory(((i + 1) * (COL + 2) * Channel + (j - 1) * Channel + k) * 8) +
            mask[2][1] * read_from_memory(((i + 1) * (COL + 2) * Channel + (j) * Channel + k) * 8) +
            mask[2][2] * read_from_memory(((i + 1) * (COL + 2) * Channel + (j + 1) * Channel + k) * 8))

            write_to_memory(index, cell_result)

# 3. Load the result image from memory through the read function.

for i in range(ROW):
    for j in range(COL + 2):
        if (j == 0 or j == COL + 1):
            continue
        for k in range(Channel):
            # read the matrix from the memory
            # write the matrix into the result array
            index = offset + (i * (COL + 2) * Channel + j * Channel + k) * 8
            result[i][j-1][k] = read_from_memory(index)


###### WRITE YOUR CODE ABOVE. ######

cm.finish()