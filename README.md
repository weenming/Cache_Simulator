# Cache Simulator

## Usage

Run `src/replacement_policy.py` with `python ./src/replacement_policy.py`. This program will execute simulation under different matrix sizes and replacement policies. 


## Requirements

Python modules `numpy` and `matplotlib` are required.


## File Structure

`cache.py` and `mat_mul.py` serves as modules to be imported.

In `cache.py` the cache class is implemented which includes replacement policies like LFU, LRU, etc, and the tag bits which is used to determine whether there is a cache hit or miss.

In `mat_mul.py` a matrix multiplication algorithm is implemented. There are 3 different orders of the nested loops, in function `mat_mul1`, `mat_mul2` and `mat_mul3`.

The report of this course project can be found in `report.pdf`. `supplementary_materials.pdf` is currently in Chinese.
