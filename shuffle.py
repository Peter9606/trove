import numpy as np

class Array(object):
    def __init__(self, *shape):
        self.d = np.ndarray(shape=shape, dtype=np.int32)
    def __str__(self):
        m, n = self.d.shape
        result = ""
        for row in range(m):
            for col in range(n):
                el = self.d[row, col]
                if el < 10:
                    result += ' '
                if el < 100:
                    result += ' '
                result += str(el) + ' '
            result += '\n'
        return result
    def __getitem__(self, key):
        return self.d[key]
    def __setitem__(self, key, val):
        self.d[key] = val
    def shape(self):
        return self.d.shape

def offset_constant(m, n):
    for i in range(m):
        val = n * i
        if val % m == 1:
            return val / m
        
def rotate_constant(m, n):
    for i in range(m):
        val = n * i
        if val % m == 1:
            return val / n

def offset_p2_constant(m, n):
    for i in range(n):
        val = m * i
        dest_col = val % n
        if dest_col == 2:
            return i
        
def offset_p2_constant_2(m, n):
    for i in range(n/2):
        val = 2 + (m * i)
        if (val % n) == 0:
            return i

def permute_p2_constant(m, n):
    return n % m
        
def make_row_array(m, n):
    result = Array(m, n)
    for row in range(m):
        for col in range(n):
            result[row, col] = col + row * n
    return result

def make_col_array(m, n):
    result = Array(m, n)
    for row in range(m):
        for col in range(n):
            result[row, col] = row + col * m
    return result

def col_permute(a, p):
    m, n = a.shape()
    result = Array(m, n)
    for col in range(n):
        for row in range(m):
            result[row, col] = a[p[row], col]
    return result

def col_rotate(a, r):
    m, n = a.shape()
    result = Array(m, n)
    for col, rotation in zip(range(n), r):
        for row in range(m):
            result[row, col] = a[(row + rotation) % m, col]
    return result

def col_subrotate(a, r):
    m, n = a.shape()
    result = Array(m, n)
    for col, rotation in zip(range(n), r):
        for row in range(0, m/2):
            result[row, col] = a[row, col]
            result[row + m/2, col] = a[(row + rotation) % (m/2) + m/2, col]
    return result

def row_shuffle(a, s):
    m, n = a.shape()
    result = Array(m, n)
    for row in range(m):
        for col in range(n):
            result[row, col] = a[row, s[row, col]]
    return result

def col_pair_swap(a, s):
    m, n = a.shape()
    result = Array(m, n)
    for col, swap in zip(range(n), s):
        for row in range(0, m, 2):
            if swap:
                result[row, col] = a[row+1, col]
                result[row+1, col] = a[row, col]
            else:
                result[row, col] = a[row, col]
                result[row+1, col] = a[row+1, col]
    return result

def factor_two_swaps(a):
    m, n = a.shape()
    return map(lambda xi: xi >= n/2, range(n))

def golden_shuffles(a):
    m, n = a.shape()
    result = Array(m, n)
    for row in range(m):
        for col in range(n):
            dest_col = a[row, col] % n
            result[row, dest_col] = col
    return result

def factor_two_shuffles(a):
    m, n = a.shape()
    result = Array(m, n)
    for col in range(n):
        odd = col % 2
        state = ((col / 2) * (offset_p2_constant(m, n))) % (n / 2) 
        row_offset = offset_p2_constant_2(m, n)
        for row in range(0, m, 2):
            if not odd:
                result[row, col] = state
                result[row + 1, col] = state + n / 2
            else:
                result[row + 1, col] = state
                result[row, col] = state + n / 2
            state = (state + (row_offset)) % (n / 2)
    return result

def factor_two_rotates(a):
    m, n = a.shape()
    return map(lambda xi: xi % m, range(n))

def factor_two_permutes(a):
    m, n = a.shape()
    #return range(0, m, 2) + range(1, m, 2) 
    return map(lambda xi: (xi * 4) % m, range(m/2)) + map(lambda xi: ((xi * 4) % m) + 1, range(m/2)) 
    
def factor_two_subrotates(a):
    m, n = a.shape()
    return map(lambda xi: (m/2-1) * (xi % 2), range(n))

def transpose(a):
    swapped = col_pair_swap(a, factor_two_swaps(a))
    shuffled = row_shuffle(swapped, factor_two_shuffles(a))
    rotated = col_rotate(shuffled, factor_two_rotates(a))
    permuted = col_permute(rotated, factor_two_permutes(a))
    subrotated = col_subrotate(permuted, factor_two_subrotates(a))
    return permuted


def r2c_conflict_free(a):
    m, n = a.shape()
    for row in range(m):
        dest_cols = set()
        for col in range(n):
            dest_col = a[row, col] / m
            if dest_col in dest_cols:
                return False
            dest_cols.add(dest_col)
    return True
            
def r2c_odd_rotates(a):
    m, n = a.shape()
    constant = m - rotate_constant(m, n)
    return map(lambda xi: (constant * xi) % m, range(n))
    # for rotation in range(m):
    #     candidate_rotation = map(lambda xi: (rotation* xi) % m, range(n))
    #     if r2c_conflict_free(col_rotate(a, candidate_rotation)):
    #         print("Rotation constant: %s" % rotation)
    #         return candidate_rotation
    #assert(False)

def r2c_golden_shuffles(a):
    m, n = a.shape()
    result = Array(m, n)
    for row in range(m):
        for col in range(n):
            dest_col = a[row, col] / m
            result[row, dest_col] = col
    return result

def r2c_odd_shuffles(a):
    m, n = a.shape()
    result = Array(m, n)
    for col in range(n):
        for row in range(m):
            result[row, col] = (m * col + (n % m * row) % m) % n 
    return result

def r2c_odd_permute(a):
    m, n = a.shape()
    constant = rotate_constant(m, n)
    result = map(lambda xi: (xi * constant) % m, range(m))
    return result

def r2c_transpose(a):
    rotated = col_rotate(a, r2c_odd_rotates(a))
    shuffled = row_shuffle(rotated, r2c_odd_shuffles(a))
    permuted = col_permute(shuffled, r2c_odd_permute(a))
    return permuted
   
a = make_col_array(14, 32)
print(a)
b = transpose(a)
print(b)

    


# a = make_row_array(5, 32)
# print(a)
# print(r2c_odd_shuffles(a))
# b = r2c_transpose(a)
# print(b)

# def check_shuffles(a):
#     shuffles = factor_two_shuffles(a)
#     goldens = golden_shuffles(col_pair_swap(a, factor_two_swaps(a)))
#     print shuffles
#     print goldens

# check_shuffles(a)
