N = 8
elem = 0
K = 4

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

for i in range(N):
    for j in range(N):
        print(f"({convert_index(i, j, N, K)})", end="\t")
    print()


for i in range(N):
    for j in range(N):
        # print index with elem
        print(f"[{elem} : ({i},{j}), ({convert_index(i, j, N, K)})]", end="\t")
        # print(f"[{elem} : ({convert_index(i, j, N, K)})]", end="\t")
        elem += 1
    print()

print()
n = N
k = 4
elem = 0
for block_i in range(n // k):
    for block_j in range(n // k):
        print(f"block: ({block_i}, {block_j})", end="\n")
        for within_block_i in range(k):
            for within_block_j in range(k):
                # print the index of the element 
                # print elem also
                index_i = within_block_i + block_i * k
                index_j = within_block_j + block_j * k
                print(f"[{elem} : ({index_i}, {index_j})]", end="\t")
                # print(f"[{elem} : ({within_block_i}, {within_block_j})]", end="\t")
                elem += 1
            print()
        print()

    
