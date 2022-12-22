N = 8
elem = 0
for i in range(N):
    for j in range(N):
        # print index with elem
        print(f"[{elem} : ({i},{j})]", end="\t")
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

    
    
        
    
        