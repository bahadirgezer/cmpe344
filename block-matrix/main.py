'''
Description
In this assignment, you will implement matrix multiplication algorithms with two different caching data structures: the row-major array and the block array. These data structures map multidimensional arrays onto the one-dimensional internal linear address space in a particular way.

The row-major array, which is the standard way to store arrays in most programming languages, arranges elements sequentially row by row and then moves on to the next row. On the other hand, the block array partitions the array into several smaller (K, K) row-major subarrays and then combine them in a block of arrays. Such data structures are illustrated in the below figure for an 8x8 array with K=4 for the block array.



With these structures, you will implement two matrix multiplication algorithms: a simple one multiplying the matrices elementwise with three loops and a recursive one which divides the matrices into blocks and performs multiplication according to the rules shown below. Given two NxN matrices A and B, where N is 2^m, their multiplication can be computed with blocks of (N/2)x(N/2) using the following formula recursively:



We provide you with a program which takes the name of the matrix multiplication algorithm (simple, recursive), the size of arrays N and subarray size K for the block array as input. The program prepares two separate caches for each caching data structure and generates two random arrays. You are expected to complete the program so that it runs the given algorithm with each caching structure and prints the corresponding statistics.

Notes:

Assume that N and K are powers of 2.
You are allowed to create files for implementing structures and algorithms as needed.

'''
import numpy as np

from cachesim import CacheSimulator, Cache, MainMemory
from argparse import ArgumentParser


def make_cache() -> CacheSimulator:
    mem = MainMemory()
    l3 = Cache("L3", 20480, 16, 64, "LRU")                           
    mem.load_to(l3)
    mem.store_from(l3)
    l2 = Cache("L2", 512, 8, 64, "LRU", store_to=l3, load_from=l3)  
    l1 = Cache("L1", 64, 8, 64, "LRU", store_to=l2, load_from=l2) 
    cs = CacheSimulator(l1, mem)
    return cs


parser = ArgumentParser()
parser.add_argument('-a', '--algorithm', type=str, choices=['simple', 'recursive'])
parser.add_argument('-N', '--N', type=int)
parser.add_argument('-K', '--K', type=int)
args = parser.parse_args()

algorithm, N, K = args.algorithm, args.N, args.K

cs1 = make_cache()
cs2 = make_cache()

rnd_vals1 = np.random.rand(N, N)
rnd_vals2 = np.random.rand(N, N)

# WRITE YOUR CODE BELOW #

offset_A = 0
offset_B = N * N
offset_C = 2 * N * N

A1 = np.zeros([N, N])
B1 = np.zeros([N, N])
# store A and B in a row major way
for i in range(N):
    for j in range(N):
        cs1.store(offset_A + i * N + j)
        cs1.store(offset_B + i * N + j)
        A1[i][j] = rnd_vals1[i][j]
        B1[i][j] = rnd_vals2[i][j]

A2 = np.zeros([N, N])
B2 = np.zeros([N, N])
# load values in rnd_vals1 and rnd_vals2 into A2 and B2, A2 and B2 are the block version of A1 and B1. The order of the values in A2 and B2 is different from A1 and B1, which is row major.
# load rnd_val1 and rnd_val2 into A2 and B2. Each of them are N*N matrices.
# A2 and B2 are block matrices, each block is K*K
# A2 and B2 are stored in a block major way
# store the values from rnd_val1 and rnd_val2 into A2 and B2, each of them are N*N matrices.

elem = 0
for block_i in range(N // K):
    for block_j in range(N // K):
        for within_block_i in range(K):
            for within_block_j in range(K):
                index_i = within_block_i + block_i * K
                index_j = within_block_j + block_j * K
                normal_i = elem // N
                normal_j = elem % N
                cs2.store(offset_A + index_i * N + index_j)
                cs2.store(offset_B + index_i * N + index_j)
                A2[normal_i][normal_j] = rnd_vals1[index_i][index_j]
                B2[normal_i][normal_j] = rnd_vals2[index_i][index_j]
                elem += 1


if algorithm == 'simple':
    C1 = np.zeros([N, N])
    # row-major array
    for i in range(N):
        for j in range(N):
            for k in range(N):
                # access with offset
                cs1.load(offset_C + i * N + j)      # load C[i][j]
                cs1.load(offset_A + i * N + k)      # load A[i][k]
                cs1.load(offset_B + k * N + j)      # load B[k][j]
                cs1.store(offset_C + i * N + j)     # store C[i][j]
                # write solution into C1 matrix
                C1[i][j] = C1[i][j] + rnd_vals1[i][k] * rnd_vals2[k][j]
    print("row major arrays:")
    print(A1)
    print(B1)
    print(C1, end="\n\n")

    
    C2 = np.zeros([N, N])
    # block array
    for i in range(N):
        for j in range(N):
            for k in range(N):
                # access with offset
                cs2.load(offset_C + i * N + j)      # load C[i][j]
                cs2.load(offset_A + i * N + k)      # load A[i][k]
                cs2.load(offset_B + k * N + j)      # load B[k][j]
                cs2.store(offset_C + i * N + j)     # store C[i][j]
                # write solution into C2 matrix
                C2[i][j] = C2[i][j] + rnd_vals1[i][k] * rnd_vals2[k][j]
    print("block arrays:")
    print(A2)
    print(B2)
    print(C2, end="\n\n")

elif algorithm == 'recursive':
    # recursive block matrix multiplication with matrix size N and block size K
    def recursive_block_matrix_multiplication(A, B, C, N, K):
        if N == K:
            for i in range(N):
                for j in range(N):
                    for k in range(N):
                        cs2.load(i * N + j)
                        cs2.load(i * N + k)
                        cs2.load(k * N + j)
                        cs2.store(i * N + j)
        else:
            recursive_block_matrix_multiplication(A, B, C, N // 2, K)
            recursive_block_matrix_multiplication(A, B, C, N // 2, K)
            recursive_block_matrix_multiplication(A, B, C, N // 2, K)
            recursive_block_matrix_multiplication(A, B, C, N // 2, K)
    recursive_block_matrix_multiplication(rnd_vals1, rnd_vals2, np.zeros([N, N]), N, K)


# WRITE YOUR CODE ABOVE #

print('Row major array')
cs1.print_stats()


print('Block array')
cs2.print_stats()