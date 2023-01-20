from cache import cache
import numpy as np
import matplotlib.pyplot as plt
import time
from matrix import mat_mul1
from matrix import mat_mul2
from matrix import mat_mul3

mat_mul = mat_mul1


def cache_sim_LFU(sizes, T):
    # size of cache: 8 * 16 * 2 = 256
    # mat multiplication is N^3

    hit_rates = []
    for size in sizes:
        A = B = [[0] * size] * size
        # prepare the cache
        c = cache()
        c.setLFU(T)
        # simulate and count
        hit, miss = mat_mul(A, B, c)

        hit_rates.append(hit / (miss + hit))
    return hit_rates


def cache_sim_NFU(sizes, max_frequency):
    # size of cache: 8 * 16 * 2 = 256
    # mat multiplication is N^3

    hit_rates = []
    for size in sizes:
        A = B = [[0] * size] * size
        # prepare the cache
        c = cache()
        c.setNFU(max_frequency)
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


def hit_rate():
    fig, ax = plt.subplots(1, 1)

    # NFU
    start = time.time()
    sizes = list(range(1, 19)) + list(range(20, 100, 15))
    hit_rates_NFU = cache_sim_NFU(sizes, 8)
    mat_sizes = [np.log10(2 * size ** 2)
                 for size in sizes]  # 2 matrices, n^2 each
    ax.plot(mat_sizes, hit_rates_NFU, marker='.', label='NFU', c='C0')
    end = time.time()
    print('NFU:', end - start)

    # LFU, about ?s
    start = time.time()
    sizes = list(range(1, 10)) + [10, 15, 20, 50, 70, 100]
    mat_sizes = [np.log10(2 * size ** 2)
                 for size in sizes]  # 2 matrices, n^2 each
    hit_rates_LFU = cache_sim_LFU(sizes, 8)
    ax.plot(mat_sizes, hit_rates_LFU, marker='.', label='LFU', c='C1')
    end = time.time()
    print('LFU:', end - start)

    # random
    sizes = list(range(1, 10, 1)) + list(range(10, 50, 20))
    mat_sizes = [np.log10(2 * size ** 2)
                 for size in sizes]  # 2 matrices, n^2 each
    hit_rates_rand = cache_sim_rand(sizes)
    ax.plot(mat_sizes, hit_rates_rand, marker='.',
            label='random', c='C2')

    # cache size / matrix size
    mat_sizes_dense = np.linspace(ax.get_xlim()[0], ax.get_xlim()[1], 1000)
    c = cache()
    cache_size = c.S * c.E * c.B
    ax.plot((mat_sizes_dense), [
            cache_size / 10**mat_size for mat_size in mat_sizes_dense], label='cache size / matrix size', c='grey', alpha=0.5)
    ax.legend()
    ax.set_xlabel('log 10 matrix size')
    ax.set_ylabel('hit rate')
    ax.set_ylim(-0.05, 1.05)
    ax.set_xlim(0, max(mat_sizes))
    plt.show()


def best_length():
    fig, ax = plt.subplots(1, 1)
    hit_rate_img = []
    ls = [1 << x for x in range(0, 500, 30)]
    for l in ls:
        # NFU
        start = time.time()
        sizes = list(range(1, 20, 2)) + list(range(20, 100, 25))
        hit_rates_NFU = cache_sim_NFU(sizes, l)
        mat_sizes = [np.log2(2 * size ** 2)
                     for size in sizes]  # 2 matrices, n^2 each
        hit_rate_img.append(hit_rates_NFU)
        end = time.time()
        print('NFU:', end - start)
    s = ax.imshow(np.array(hit_rate_img), cmap='cividis')
    ax.set_xticks(list(range(len(mat_sizes))), [f'{x:.0f}' for x in mat_sizes])
    # wtf why does not np.log support int
    ax.set_yticks(list(range(len(ls))), [
                  f'{np.log2(float(l)):.0f}' for l in ls])
    ax.set_xlabel('log 2 matrix size')
    ax.set_ylabel('steps with impact')
    plt.colorbar(s, label='hit rate')

    plt.show()
    fig.savefig('NFU_length_size.png', dpi=400)


if __name__ == '__main__':
    best_length()
