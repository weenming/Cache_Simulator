from cache import cache


def mat_mul1(A: list[list], B: list[list], c: cache):
    '''
    count the hit number and miss number in a matrix multiplication
    '''
    rowA = len(A)
    colA = len(A[0])
    rowB = len(B)
    colB = len(B[0])
    assert rowB == colA, 'ill defined matrix multiplication'
    # adopt the first method: sum by row and col
    adrA_max = cache.matToIdx(rowA, colA, colA)
    # swapping i and j does not matter
    for i in range(rowA):
        for j in range(colB):
            for k in range(colA):
                # tmp_ij = A[i][k] * B[k][j]
                adrA = cache.matToIdx(i, k, colA)
                # assuming A and B are continuous in adr
                adrB = cache.matToIdx(k, j, colB) + adrA_max
                c.read(adrA)
                c.read(adrB)
                adrC = cache.matToIdx(i, j, colB)
                c.read(adrC)
    hit = c.hit
    miss = c.miss
    return hit, miss

# This is more efficient


def mat_mul2(A: list[list], B: list[list], c: cache):
    '''
    count the hit number and miss number in a matrix multiplication
    '''
    rowA = len(A)
    colA = len(A[0])
    rowB = len(B)
    colB = len(B[0])
    assert rowB == colA, 'ill defined matrix multiplication'
    # adopt the first method: sum by row and col
    adrA_max = cache.matToIdx(rowA, colA, colA)
    for i in range(rowA):
        for k in range(colA):
            for j in range(colB):
                # tmp_ij += A[i][k] * B[k][j]
                # assuming A and B are continuous in adr
                adrB = cache.matToIdx(k, j, colB) + adrA_max
                c.read(adrB)
                adrA = cache.matToIdx(i, k, colA)
                c.read(adrA)
                adrC = cache.matToIdx(i, j, colB)
                c.read(adrC)

    hit = c.hit
    miss = c.miss
    return hit, miss


def mat_mul3(A: list[list], B: list[list], c: cache):
    '''
    count the hit number and miss number in a matrix multiplication
    '''
    rowA = len(A)
    colA = len(A[0])
    rowB = len(B)
    colB = len(B[0])
    assert rowB == colA, 'ill defined matrix multiplication'
    # adopt the first method: sum by row and col
    adrA_max = cache.matToIdx(rowA, colA, colA)
    # swapping i and j does not matter
    for j in range(colB):
        for k in range(colA):
            adrB = cache.matToIdx(k, j, colB) + adrA_max
            c.read(adrB)
            for i in range(rowA):
                # tmp_ij = A[i][k] * B[k][j]
                # assuming A and B are continuous in adr
                adrA = cache.matToIdx(i, k, colA)
                c.read(adrA)
                adrC = cache.matToIdx(i, j, colB)
                c.read(adrC)
    hit = c.hit
    miss = c.miss
    return hit, miss
