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

def convert_index(index_i, index_j, N, K) -> tuple: 
    # convert row-major index to block-major index
    # block major index is the index of the element in the block-major array
    elem = index_i * N + index_j
    block = elem // (K * K)
    block_i = block // (N // K)
    block_j = block % (N // K)
    within_block = elem % (K * K)
    within_block_i = within_block // K
    within_block_j = within_block % K
    normal_i = within_block_i + block_i * K
    normal_j = within_block_j + block_j * K
    return (normal_i, normal_j)


def rec(low_i, high_i, low_j, high_j, A, B, C):
    if low_i == high_i and low_j == high_j:
        C[low_i][low_j] = A[low_i][low_j] * B[low_i][low_j]
    elif low_i == high_i:
        mid_j = (low_j + high_j) // 2
        rec(low_i, high_i, low_j, mid_j, A, B, C)
        rec(low_i, high_i, mid_j+1, high_j, A, B, C)
        C[low_i][low_j] = C[low_i][low_j] + C[low_i][mid_j+1]
    elif low_j == high_j:
        mid_i = (low_i + high_i) // 2
        rec(low_i, mid_i, low_j, high_j, A, B, C)
        rec(mid_i+1, high_i, low_j, high_j, A, B, C)
        C[low_i][low_j] = C[low_i][low_j] + C[mid_i+1][low_j]
    else:
        mid_i = (low_i + high_i) // 2
        mid_j = (low_j + high_j) // 2
        rec(low_i, mid_i, low_j, mid_j, A, B, C)
        rec(low_i, mid_i, mid_j+1, high_j, A, B, C)
        rec(mid_i+1, high_i, low_j, mid_j, A, B, C)
        rec(mid_i+1, high_i, mid_j+1, high_j, A, B, C)
        C[low_i][low_j] = C[low_i][low_j] + C[mid_i+1][mid_j+1]
    return C


def rec32(low_i, high_i, low_j, high_j, A, B, C, offset_A, offset_B, offset_C, cs1):
    mid_i = (low_i + high_i) // 2
    mid_j = (low_j + high_j) // 2
    if high_i - low_i == 1:
        cs1.load(offset_A + low_i * N + low_j)
        cs1.load(offset_A + low_i * N + high_j)
        cs1.load(offset_A + high_i * N + low_j)
        cs1.load(offset_A + high_i * N + high_j)
        cs1.load(offset_B + low_i * N + low_j)
        cs1.load(offset_B + low_i * N + high_j)
        cs1.load(offset_B + high_i * N + low_j)
        cs1.load(offset_B + high_i * N + high_j)
        cs1.store(offset_C + low_i * N + low_j)
        cs1.store(offset_C + low_i * N + high_j)
        cs1.store(offset_C + high_i * N + low_j)
        cs1.store(offset_C + high_i * N + high_j)
        A_00 = A[low_i][low_j]
        A_01 = A[low_i][high_j]
        A_10 = A[high_i][low_j]
        A_11 = A[high_i][high_j]
        B_00 = B[low_i][low_j]
        B_01 = B[low_i][high_j]
        B_10 = B[high_i][low_j]
        B_11 = B[high_i][high_j]
        C_00 = A_00 * B_00 + A_01 * B_10
        C_01 = A_00 * B_01 + A_01 * B_11
        C_10 = A_10 * B_00 + A_11 * B_10
        C_11 = A_10 * B_01 + A_11 * B_11
        return [[C_00, C_01], [C_10, C_11]]

    C_00 = rec31(low_i, mid_i, low_j, mid_j, A, B, C)
    C_01 = rec31(low_i, mid_i, mid_j + 1, high_j, A, B, C)
    C_10 = rec31(mid_i + 1, high_i, low_j, mid_j, A, B, C)
    C_11 = rec31(mid_i + 1, high_i, mid_j + 1, high_j, A, B, C)

    return merge(C_00, C_01, C_10, C_11)
    


# merge 4 sub matrices into one matrix, each is of size N/2 * N/2
def merge(C_00, C_01, C_10, C_11):
    C = [[0 for _ in range(N)] for _ in range(N)]
    mid_i = N // 2
    mid_j = N // 2
    for i in range(mid_i):
        for j in range(mid_j):
            C[i][j] = C_00[i][j]
            C[i][j + mid_j] = C_01[i][j]
            C[i + mid_i][j] = C_10[i][j]
            C[i + mid_i][j + mid_j] = C_11[i][j]
    return C



def rec31(low_i, high_i, low_j, high_j, A, B, C):
    mid_i = (low_i + high_i) // 2
    mid_j = (low_j + high_j) // 2
    if high_i - low_i == 1:
        A_00 = A[low_i][low_j]
        A_01 = A[low_i][high_j]
        A_10 = A[high_i][low_j]
        A_11 = A[high_i][high_j]
        B_00 = B[low_i][low_j]
        B_01 = B[low_i][high_j]
        B_10 = B[high_i][low_j]
        B_11 = B[high_i][high_j]
        C_00 = A_00 * B_00 + A_01 * B_10
        C_01 = A_00 * B_01 + A_01 * B_11
        C_10 = A_10 * B_00 + A_11 * B_10
        C_11 = A_10 * B_01 + A_11 * B_11
        return [[C_00, C_01], [C_10, C_11]]

    C_00 = rec31(low_i, mid_i, low_j, mid_j, A, B, C)
    C_01 = rec31(low_i, mid_i, mid_j + 1, high_j, A, B, C)
    C_10 = rec31(mid_i + 1, high_i, low_j, mid_j, A, B, C)
    C_11 = rec31(mid_i + 1, high_i, mid_j + 1, high_j, A, B, C)
    return merge(C_00, C_01, C_10, C_11)


            
def rec69(low_i, high_i, low_j, high_j, A, B, C):
    if low_i == high_i and low_j == high_j:
        C[low_i][low_j] = A[low_i][low_j] * B[low_i][low_j]
    else:
        mid_i = (low_i + high_i) // 2
        mid_j = (low_j + high_j) // 2
        rec69(low_i, mid_i, low_j, mid_j, A, B, C)
        rec69(low_i, mid_i, mid_j+1, high_j, A, B, C)
        rec69(mid_i+1, high_i, low_j, mid_j, A, B, C)
        rec69(mid_i+1, high_i, mid_j+1, high_j, A, B, C)


offset_A = 0
offset_B = N * N
offset_C = 2 * N * N

A1 = np.zeros([N, N])
B1 = np.zeros([N, N])
# store A1 and B1 in a row major way
for i in range(N):
    for j in range(N):
        cs1.store(offset_A + i * N + j)
        cs1.store(offset_B + i * N + j)
        A1[i][j] = rnd_vals1[i][j]
        B1[i][j] = rnd_vals2[i][j]

A2 = np.zeros([N, N])
B2 = np.zeros([N, N])
for i in range(N):
    for j in range(N):
        (normal_i, normal_j) = convert_index(i, j, N, K)
        cs2.store(offset_A + normal_i * N + normal_j)
        cs2.store(offset_B + normal_i * N + normal_j)
        A2[normal_i][normal_j] = rnd_vals1[i][j]
        B2[normal_i][normal_j] = rnd_vals2[i][j]

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
                C1[i][j] = C1[i][j] + A1[i][k] * B1[k][j]
    print("row major arrays:")
    print(A1)
    print(B1)
    print(C1, end="\n\n")
    
    C2 = np.zeros([N, N])
    # block array
    for i in range(N):
        for j in range(N):
            for k in range(N):
                (normal_i, normal_j) = convert_index(i, j, N, K)
                (normal_i2, normal_j2) = convert_index(i, k, N, K)
                (normal_i3, normal_j3) = convert_index(k, j, N, K)
                cs2.load(offset_C + normal_i * N + normal_j)
                cs2.load(offset_A + normal_i2 * N + normal_j2)
                cs2.load(offset_B + normal_i3 * N + normal_j3)
                cs2.store(offset_C + normal_i * N + normal_j)
                C2[normal_i][normal_j] = C2[normal_i][normal_j] + A2[normal_i2][normal_j2] * B2[normal_i3][normal_j3]
    print("block arrays:")
    print(A2)
    print(B2)
    print(C2, end="\n\n")

elif algorithm == 'recursive':
    # C1 = np.zeros([N, N])
    # # row-major array
    # for i in range(N):
    #     for j in range(N):
    #         for k in range(N):
    #             # access with offset
    #             cs1.load(offset_C + i * N + j)      # load C[i][j]
    #             cs1.load(offset_A + i * N + k)      # load A[i][k]
    #             cs1.load(offset_B + k * N + j)      # load B[k][j]
    #             cs1.store(offset_C + i * N + j)     # store C[i][j]
    #             # write solution into C1 matrix
    #             C1[i][j] = C1[i][j] + A1[i][k] * B1[k][j]
    # print("row major arrays:")
    # print(C1, end="\n\n")

    C1 = np.zeros([N, N])
    C1 = rec31(0, N - 1, 0, N - 1, A1, B1, C1)
    print("row major arrays:")
    print(A1)
    print(B1)
    print(C1, end="\n\n")

    C2 = np.zeros([N, N])
    # rec32(0, N - 1, 0, N - 1, A2, B2, C2)
    print("block arrays:")
    print(A2)
    print(B2)
    print(C2, end="\n\n")


# WRITE YOUR CODE ABOVE #

print('Row major array')
cs1.print_stats()


print('Block array')
cs2.print_stats()