from cache import cache
import numpy as np
import matplotlib.pyplot as plt
from matrix import mat_mul1
from matrix import mat_mul2
from matrix import mat_mul3


def cache_sim_FIFO(sizes):
    # size of cache: 8 * 16 * 2 = 256
    # mat multiplication is N^3

    hit_rates = []
    for size in sizes:
        A = B = [[0] * size] * size
        # prepare the cache
        c = cache()
        c.setFIFO()
        # simulate and count
        hit, miss = mat_mul(A, B, c)

        hit_rates.append(hit / (miss + hit))
    return hit_rates


def cache_sim_LRU(sizes):
    # size of cache: 8 * 16 * 2 = 256
    # mat multiplication is N^3

    hit_rates = []
    for size in sizes:
        A = B = [[0] * size] * size
        # prepare the cache
        c = cache()
        c.setLRU()
        # simulate and count
        hit, miss = mat_mul(A, B, c)

        hit_rates.append(hit / (miss + hit))
    return hit_rates


def cache_sim_rand(sizes):
    # size of cache: 8 * 16 * 2 = 256
    # mat multiplication is N^3

    hit_rates = []
    for size in sizes:
        A = B = [[0] * size] * size
        # prepare the cache
        c = cache()
        c.setRandom()
        # simulate and count
        hit, miss = mat_mul(A, B, c)

        hit_rates.append(hit / (miss + hit))
    return hit_rates


if __name__ == '__main__':

    fig, ax = plt.subplots(1, 1)

    # LRU, about ?s
    mat_mul = mat_mul1
    sizes = list(range(1, 10, 1)) + list(range(10, 20, 1)) + list(range(20, 40, 1)) + \
        list(range(40, 100, 10))
    mat_sizes = [np.log2(2 * size ** 2)
                 for size in sizes]  # 2 matrices, n^2 each
    hit_rates_LRU = cache_sim_LRU(sizes)
    ax.plot(mat_sizes, hit_rates_LRU, marker='.',
            label='LRU loop order ijk', c='C0', ls=':')

    # LRU, about ?s
    mat_mul = mat_mul2
    sizes = list(range(1, 10, 1)) + list(range(10, 20, 1)) + list(range(20, 40, 1)) + \
        list(range(40, 100, 10))
    mat_sizes = [np.log2(2 * size ** 2)
                 for size in sizes]  # 2 matrices, n^2 each
    hit_rates_LRU = cache_sim_LRU(sizes)
    ax.plot(mat_sizes, hit_rates_LRU, marker='.',
            label='LRU loop order ikj', c='C1', ls=':')

    # LRU, about ?s
    mat_mul = mat_mul3
    sizes = list(range(1, 10, 1)) + list(range(10, 20, 1)) + list(range(20, 40, 1)) + \
        list(range(40, 100, 10))
    mat_sizes = [np.log2(2 * size ** 2)
                 for size in sizes]  # 2 matrices, n^2 each
    hit_rates_LRU = cache_sim_LRU(sizes)
    ax.plot(mat_sizes, hit_rates_LRU, marker='.',
            label='LRU loop order jik', c='C2', ls=':')

    # cache size / matrix size
    mat_sizes_dense = np.linspace(ax.get_xlim()[0], ax.get_xlim()[1], 1000)
    c = cache()
    cache_size = c.S * c.E * c.B
    ax.plot((mat_sizes_dense), [
            cache_size / 2**mat_size for mat_size in mat_sizes_dense], label='cache size / matrix size', c='grey', alpha=0.5)

    ax.legend()
    ax.set_xlabel('log 2 matrix size')
    ax.set_ylabel('hit rate')
    ax.set_ylim(-0.05, 1.05)
    ax.set_xlim(0, max(mat_sizes))
    plt.show()
    fig.savefig('FIFO_LRU.png', dpi=400)
