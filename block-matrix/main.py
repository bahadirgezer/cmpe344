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



# WRITE YOUR CODE ABOVE #

print('Row major array')
cs1.print_stats()


print('Block array')
cs2.print_stats()