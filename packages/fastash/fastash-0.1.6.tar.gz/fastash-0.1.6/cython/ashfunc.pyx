# distutils: language = c++

cdef extern from "stdlib.h":
    ctypedef void const_void "const void"
    void qsort(void *base, int nmemb, int size,
            int(*compar)(const void *, const void *)) nogil

from libcpp.vector cimport vector
from libc.stdlib cimport malloc, free
from libcpp cimport bool

from hyperclip import hyperfunc

import cython


import numpy as np
cimport numpy as np

np.import_array()

from cpython cimport array
import array

@cython.boundscheck(False)  # Deactivate bounds checking.
@cython.wraparound(False)   # Deactivate negative indexing.
@cython.cdivision(True) # Deactivate zero division checking.
def compute_bins_P_shift(np.ndarray[double, ndim=2] X, 
                         np.ndarray[double, ndim=1] x_min,
                         np.ndarray[double, ndim=1] norm_inf_w,
                         np.ndarray[double, ndim=1] norm_2_w,
                         double h, 
                         double shift, 
                         np.ndarray[double, ndim=2] A,
                         np.ndarray[double, ndim=1] R):
    cdef Py_ssize_t i, j, j_unique, i_hyp
    
    cdef int n = X.shape[0]
    cdef int d = X.shape[1]
    
    cdef int n_hyp = A.shape[1]
        
    X_digit_uniques = np.zeros((n, d), dtype=np.intc)
    cdef np.ndarray[int, ndim=2] X_digit_uniques_view = X_digit_uniques
    
    cdef double [:, :] A_x
    cdef double [:] R_x
        
    P = np.zeros(n, dtype=np.double)
    cdef np.ndarray[double, ndim=1] P_view = P
    
    cdef int **X_digit
            
    cdef bool trigger_unique, trigger_correction
    
    cdef int * last_x
    last_x = <int *> malloc(d * sizeof(int))
    
    cdef int i_last = 0
    cdef int i_unique = 0
    
    center = np.zeros(d, dtype=np.double)
    cdef np.ndarray[double, ndim=1] center_view = center
    
    cdef double hyp_correction
                
    cdef double * dist
        
    cdef int *close_i_hyp, *close_i_hyp_full
    cdef int card_close_i_hyp
    
    close_i_hyp_full = <int *> malloc(n_hyp * sizeof(int *))
    
    cdef int cnt_trigger_hyp
    
    # discretize
    X_digit = discretize(X=X, 
                         x_min = x_min,
                         n = n,
                         d = d,
                         h = h,
                         shift = shift)
    
    # sort
    sort_according_d(X_digit, n, d)
    
    # count
    for j in range(d):
        last_x[j] = X_digit[0][j]
    i_unique = -1
    i_last = 0
    
    for i in range(1,n):
        trigger_unique = False
        for j in range(d):
            if X_digit[i][j] != last_x[j] or (i == n-1 and j == 0):
                # if it's the first column to change
                if trigger_unique == False:
                    # their is a new unique !
                    # increment
                    i_unique = i_unique + 1
                                            
                    # # for each column
                    for j_unique in range(d):
                        # save center for boundary correction below
                        center_view[j_unique] = x_min[j_unique] - 1.5 * h + shift + h * last_x[j_unique]
                        # save the unique x
                        X_digit_uniques_view[i_unique, j_unique] = last_x[j_unique]
                    
                    
                    hyp_correction = 1.0
                    
                    # <!-- Boundary correction
                    dist = inf_distances_to_hyperplanes(center=center_view,
                                                        d=d,
                                                        A = A,
                                                        R = R,
                                                        n_hyp=n_hyp,
                                                        norm_inf_w=norm_inf_w,
                                                        norm_2_w = norm_2_w)
                    
                    card_close_i_hyp = 0
                    for i_hyp in range(n_hyp):
                        if dist[i_hyp] < h/2:
                            close_i_hyp_full[card_close_i_hyp] = i_hyp
                            card_close_i_hyp = card_close_i_hyp + 1
                            
                    close_i_hyp = <int *> malloc(card_close_i_hyp * sizeof(int *))
                    for i_hyp in range(card_close_i_hyp):
                        close_i_hyp[i_hyp] = close_i_hyp_full[i_hyp]
                                        
                    if card_close_i_hyp > 0:
                                                
                        A_x = np.zeros((d, card_close_i_hyp), dtype=np.double)
                        for j_unique in range(d):
                            for i_hyp in range(card_close_i_hyp):
                                A_x[j_unique, i_hyp] = A[j_unique][close_i_hyp[i_hyp]]
                            
                        R_x = np.zeros(card_close_i_hyp, dtype=np.double)
                        for i_hyp in range(card_close_i_hyp):
                            R_x[i_hyp] = R[close_i_hyp[i_hyp]]
                            
                            # translation and scale
                            for j_unique in range(d):
                                R_x[i_hyp] = R_x[i_hyp] + A_x[j_unique, i_hyp] * (center_view[j_unique] - h / 2)
                                A_x[j_unique, i_hyp] = A_x[j_unique, i_hyp] * h

                        hyp_correction = hyperfunc.volume(A = A_x,
                                                          R = R_x,
                                                          check_A = False)
                    
                    # end of boundary correction -->
                    
                    # save the proba
                    P_view[i_unique] = (i - i_last) / (n * hyp_correction)
                    i_last = i
                
                # finally save this new last unique
                last_x[j] = X_digit[i][j]
                # and set trigger True
                # to say that a unique is found
                trigger_unique = True
    
    i_to_keep = P>0
    X_digit_uniques = X_digit_uniques[i_to_keep,:]
    P = P[i_to_keep]
    
    for i in range(n):
        free(X_digit[i])
    free(X_digit)
    free(dist)
    free(close_i_hyp)
    free(close_i_hyp_full)
    free(last_x)
    
    return(X_digit_uniques, P, shift)

@cython.boundscheck(False)  # Deactivate bounds checking.
@cython.wraparound(False)   # Deactivate negative indexing.
@cython.cdivision(True)
def merge_predict_shift(np.ndarray[int, ndim=2] X_digit_uniques,
                        np.ndarray[double, ndim=1] P,
                        np.ndarray[double, ndim=2] Y,
                        np.ndarray[double, ndim=1] x_min,
                        double h,
                        double shift):
        
    cdef Py_ssize_t j
    
    cdef int n_X = X_digit_uniques.shape[0]
    cdef int d = X_digit_uniques.shape[1]
    
    cdef int n_Y = Y.shape[0]
    
    cdef int i_X
    
    cdef bool trigger_set_P, keep_search
    
    # Y_digit is [[y0, y1, 0], [y0, y1, 1], ... [y0, y1, n_y]]
    # by this way, the index is kept after the sort process
    cdef int **Y_digit
    
    
    f = np.zeros(n_Y, dtype=np.double)
    cdef np.ndarray[double, ndim=1] f_view = f
    
    cdef int last_j_success_level, j_success_level
    
    # discretize
    Y_digit = discretize(X = Y,
                     x_min = x_min,
                     n = n_Y,
                     d = d,
                     h = h,
                     shift = shift,
                     index_column = True)
    
    # sort
    sort_according_d(Y_digit, n_Y, d)
    
    i_X = -1
    
    for i_Y in range(n_Y):
        trigger_set_P = False
        
        keep_search = True
        
        while i_X < n_X and keep_search:
            i_X = i_X + 1
            
            for j in range(d):
                if Y_digit[i_Y][j] > X_digit_uniques[i_X, j]:
                    break
                elif Y_digit[i_Y][j] < X_digit_uniques[i_X, j]:
                    keep_search = False
                    break
                else:
                    if keep_search and j + 1 == d:
                        f_view[Y_digit[i_Y][d]] = f_view[Y_digit[i_Y][d]] + P[i_X]
                        keep_search = False
        
        i_X = i_X -1
    
    for i in range(n_Y):
        free(Y_digit[i])
    free(Y_digit)
    
    return(f)

@cython.boundscheck(False)  # Deactivate bounds checking.
@cython.wraparound(False)   # Deactivate negative indexing.
cdef bool lower(int *a,
                int *b,
                int d):
    for j in range(d):
        if a[j] < b[j]:
            return(True)
    return(False)

@cython.boundscheck(False)  # Deactivate bounds checking.
@cython.wraparound(False)   # Deactivate negative indexing.
@cython.cdivision(True)
cdef int ** discretize(np.ndarray[double, ndim=2] X,
                       np.ndarray[double, ndim=1] x_min,
                       int n,
                       int d,
                       double h,
                       double shift,
                       bool index_column = False):
    cdef Py_ssize_t i, j
    
    cdef int **X_digit
    X_digit = <int **> malloc(n * sizeof(int*))
    
    cdef double *slide = <double *> malloc(d * sizeof(double))
    for j in range(d):
        slide[j] = x_min[j] - 2 * h + shift
    
    if index_column:
        for i in range(n):
            X_digit[i] = <int *> malloc((d + 1) * sizeof(int))
            for j in range(d):
                X_digit[i][j] = <int>((X[i,j] - slide[j]) / h)
            
            X_digit[i][d] = i
        
    else:
        for i in range(n):
            X_digit[i] = <int *> malloc(d * sizeof(int))
            for j in range(d):
                X_digit[i][j] = <int>((X[i,j] - slide[j]) / h)
    
    free(slide)
    return(X_digit)

@cython.boundscheck(False)  # Deactivate bounds checking.
@cython.wraparound(False)   # Deactivate negative indexing.
@cython.cdivision(True)
cpdef int [:,:] discretize_numpy(double[:, :] X,
                                 double[:] x_min,
                                 int n,
                                 int d,
                                 double h,
                                 double shift,
                                 bool index_column = False):
    cdef Py_ssize_t i, j
    
    cdef int [:, :] X_digit = np.zeros((n, d), dtype=np.double)
    
    cdef double *slide = <double *> malloc(d * sizeof(double))
    for j in range(d):
        slide[j] = x_min[j] - 2 * h + shift
    
    if index_column:
        for i in range(n):
            for j in range(d):
                X_digit[i, j] = <int>((X[i,j] - slide[j]) / h)
            
            X_digit[i,d] = i
        
    else:
        for i in range(n):
            for j in range(d):
                X_digit[i,j] = <int>((X[i,j] - slide[j]) / h)
    
    free(slide)
    return(X_digit)

@cython.boundscheck(False)  # Deactivate bounds checking.
@cython.wraparound(False)   # Deactivate negative indexing.
@cython.cdivision(True)
cdef double * inf_distances_to_hyperplanes(np.ndarray[double, ndim=1] center,
                                           int d,
                                           np.ndarray[double, ndim=2] A, 
                                           np.ndarray[double, ndim=1] R,
                                           int n_hyp,
                                           np.ndarray[double, ndim=1] norm_inf_w,
                                           np.ndarray[double, ndim=1] norm_2_w):
    
    cdef double * dist
    dist = <double *> malloc(n_hyp * sizeof(double))
    cdef Py_ssize_t i_hyp, j
    
    # initialize dist_min greater than the limit condition
    for i_hyp in range(n_hyp):
        # distance to hyperplan
        dist[i_hyp] = 0.0
        for j in range(d):
            dist[i_hyp] = dist[i_hyp] + center[j] * A[j, i_hyp]
        dist[i_hyp] = dist[i_hyp] + R[i_hyp]
        # dist[i_hyp] = abs(dist[i_hyp]) / norm_2_w[i_hyp]
        dist[i_hyp] = abs(dist[i_hyp]) / norm_2_w[i_hyp]**2 * norm_inf_w[i_hyp]
        
    return(dist)

@cython.boundscheck(False)  # Deactivate bounds checking.
@cython.wraparound(False)   # Deactivate negative indexing.
@cython.cdivision(True)
cdef double hyperplanes_clip_volume_monte_carlo(np.ndarray[double, ndim=1] center,
                                    int d, 
                                    np.ndarray[double, ndim=2] X_mc,
                                    int n_mc, 
                                    np.ndarray[double, ndim=2] A,
                                    np.ndarray[double, ndim=1] r,
                                    int n_hyp, 
                                    bool * trigger_hyp):
    cdef double dot
    cdef double hyp_correction = 0.0
    cdef bool trigger_mc_inside
    
    cdef Py_ssize_t i_hyp, i_mc, j
    for i_mc in range(n_mc):
        trigger_mc_inside = True
        for i_hyp in range(n_hyp):
            if trigger_hyp[i_hyp]:
                dot = 0.0
                for j in range(d):
                    dot = dot + (center[j]+X_mc[i_mc, j]) * A[j, i_hyp]
                dot = dot + r[i_hyp]
                                                    
                if dot < 0.0:
                    trigger_mc_inside = False
        
        if trigger_mc_inside:
            hyp_correction = hyp_correction + 1
        
    hyp_correction = hyp_correction / n_mc
    
    return(hyp_correction)

cdef void sort_according_d(void *base, 
                           int n,
                           int d):
    
    if d == 1:
        qsort(base, n, sizeof(int*), compare_1d)
    elif d == 2:
        qsort(base, n, sizeof(int*), compare_2d)
    elif d == 3:
        qsort(base, n, sizeof(int*), compare_3d)
    elif d == 4:
        qsort(base, n, sizeof(int*), compare_4d)
    elif d == 5:
        qsort(base, n, sizeof(int*), compare_5d)
    elif d == 6:
        qsort(base, n, sizeof(int*), compare_6d)
    elif d == 7:
        qsort(base, n, sizeof(int*), compare_7d)
    elif d == 8:
        qsort(base, n, sizeof(int*), compare_8d)
    elif d == 9:
        qsort(base, n, sizeof(int*), compare_9d)
    elif d == 10:
        qsort(base, n, sizeof(int*), compare_10d)
    elif d == 11:
        qsort(base, n, sizeof(int*), compare_11d)
    elif d == 12:
        qsort(base, n, sizeof(int*), compare_12d)
    elif d == 13:
        qsort(base, n, sizeof(int*), compare_13d)
    elif d == 14:
        qsort(base, n, sizeof(int*), compare_14d)
    elif d == 15:
        qsort(base, n, sizeof(int*), compare_15d)
    elif d == 16:
        qsort(base, n, sizeof(int*), compare_16d)
    elif d == 17:
        qsort(base, n, sizeof(int*), compare_17d)
    elif d == 18:
        qsort(base, n, sizeof(int*), compare_18d)
    elif d == 19:
        qsort(base, n, sizeof(int*), compare_19d)
    elif d == 20:
        qsort(base, n, sizeof(int*), compare_20d)

# =============================================================================
# Compare functions
# =============================================================================

@cython.boundscheck(False)  # Deactivate bounds checking.
@cython.wraparound(False)   # Deactivate negative indexing.
@cython.cdivision(True) # Deactivate zero division checking.
cdef int compare_1d(const void *a, const void *b):
    cdef Py_ssize_t j
    
    cdef int *ai = (<int**>a)[0]
    cdef int *bi = (<int**>b)[0]
    
    for j in range(1):
        if ai[j] < bi[j]:
            return -1
        if ai[j] > bi[j]:
            return +1
    
    return 0

@cython.boundscheck(False)  # Deactivate bounds checking.
@cython.wraparound(False)   # Deactivate negative indexing.
@cython.cdivision(True) # Deactivate zero division checking.
cdef int compare_2d(const void *a, const void *b):
    cdef Py_ssize_t j
    
    cdef int *ai = (<int**>a)[0]
    cdef int *bi = (<int**>b)[0]
    
    for j in range(2):
        if ai[j] < bi[j]:
            return -1
        if ai[j] > bi[j]:
            return +1
    
    return 0

@cython.boundscheck(False)  # Deactivate bounds checking.
@cython.wraparound(False)   # Deactivate negative indexing.
@cython.cdivision(True) # Deactivate zero division checking.
cdef int compare_3d(const void *a, const void *b):
    cdef Py_ssize_t j
    
    cdef int *ai = (<int**>a)[0]
    cdef int *bi = (<int**>b)[0]
    
    for j in range(3):
        if ai[j] < bi[j]:
            return -1
        if ai[j] > bi[j]:
            return +1
    
    return 0

@cython.boundscheck(False)  # Deactivate bounds checking.
@cython.wraparound(False)   # Deactivate negative indexing.
@cython.cdivision(True) # Deactivate zero division checking.
cdef int compare_4d(const void *a, const void *b):
    cdef Py_ssize_t j
    
    cdef int *ai = (<int**>a)[0]
    cdef int *bi = (<int**>b)[0]
    
    for j in range(4):
        if ai[j] < bi[j]:
            return -1
        if ai[j] > bi[j]:
            return +1
    
    return 0

@cython.boundscheck(False)  # Deactivate bounds checking.
@cython.wraparound(False)   # Deactivate negative indexing.
@cython.cdivision(True) # Deactivate zero division checking.
cdef int compare_5d(const void *a, const void *b):
    cdef Py_ssize_t j
    
    cdef int *ai = (<int**>a)[0]
    cdef int *bi = (<int**>b)[0]
    
    for j in range(5):
        if ai[j] < bi[j]:
            return -1
        if ai[j] > bi[j]:
            return +1
    
    return 0

@cython.boundscheck(False)  # Deactivate bounds checking.
@cython.wraparound(False)   # Deactivate negative indexing.
@cython.cdivision(True) # Deactivate zero division checking.
cdef int compare_6d(const void *a, const void *b):
    cdef Py_ssize_t j
    
    cdef int *ai = (<int**>a)[0]
    cdef int *bi = (<int**>b)[0]
    
    for j in range(6):
        if ai[j] < bi[j]:
            return -1
        if ai[j] > bi[j]:
            return +1
    
    return 0

@cython.boundscheck(False)  # Deactivate bounds checking.
@cython.wraparound(False)   # Deactivate negative indexing.
@cython.cdivision(True) # Deactivate zero division checking.
cdef int compare_7d(const void *a, const void *b):
    cdef Py_ssize_t j
    
    cdef int *ai = (<int**>a)[0]
    cdef int *bi = (<int**>b)[0]
    
    for j in range(7):
        if ai[j] < bi[j]:
            return -1
        if ai[j] > bi[j]:
            return +1
    
    return 0

@cython.boundscheck(False)  # Deactivate bounds checking.
@cython.wraparound(False)   # Deactivate negative indexing.
@cython.cdivision(True) # Deactivate zero division checking.
cdef int compare_8d(const void *a, const void *b):
    cdef Py_ssize_t j
    
    cdef int *ai = (<int**>a)[0]
    cdef int *bi = (<int**>b)[0]
    
    for j in range(8):
        if ai[j] < bi[j]:
            return -1
        if ai[j] > bi[j]:
            return +1
    
    return 0

@cython.boundscheck(False)  # Deactivate bounds checking.
@cython.wraparound(False)   # Deactivate negative indexing.
@cython.cdivision(True) # Deactivate zero division checking.
cdef int compare_9d(const void *a, const void *b):
    cdef Py_ssize_t j
    
    cdef int *ai = (<int**>a)[0]
    cdef int *bi = (<int**>b)[0]
    
    for j in range(9):
        if ai[j] < bi[j]:
            return -1
        if ai[j] > bi[j]:
            return +1
    
    return 0

@cython.boundscheck(False)  # Deactivate bounds checking.
@cython.wraparound(False)   # Deactivate negative indexing.
@cython.cdivision(True) # Deactivate zero division checking.
cdef int compare_10d(const void *a, const void *b):
    cdef Py_ssize_t j
    
    cdef int *ai = (<int**>a)[0]
    cdef int *bi = (<int**>b)[0]
    
    for j in range(10):
        if ai[j] < bi[j]:
            return -1
        if ai[j] > bi[j]:
            return +1
    
    return 0

@cython.boundscheck(False)  # Deactivate bounds checking.
@cython.wraparound(False)   # Deactivate negative indexing.
@cython.cdivision(True) # Deactivate zero division checking.
cdef int compare_11d(const void *a, const void *b):
    cdef Py_ssize_t j
    
    cdef int *ai = (<int**>a)[0]
    cdef int *bi = (<int**>b)[0]
    
    for j in range(11):
        if ai[j] < bi[j]:
            return -1
        if ai[j] > bi[j]:
            return +1
    
    return 0

@cython.boundscheck(False)  # Deactivate bounds checking.
@cython.wraparound(False)   # Deactivate negative indexing.
@cython.cdivision(True) # Deactivate zero division checking.
cdef int compare_12d(const void *a, const void *b):
    cdef Py_ssize_t j
    
    cdef int *ai = (<int**>a)[0]
    cdef int *bi = (<int**>b)[0]
    
    for j in range(12):
        if ai[j] < bi[j]:
            return -1
        if ai[j] > bi[j]:
            return +1
    
    return 0

@cython.boundscheck(False)  # Deactivate bounds checking.
@cython.wraparound(False)   # Deactivate negative indexing.
@cython.cdivision(True) # Deactivate zero division checking.
cdef int compare_13d(const void *a, const void *b):
    cdef Py_ssize_t j
    
    cdef int *ai = (<int**>a)[0]
    cdef int *bi = (<int**>b)[0]
    
    for j in range(13):
        if ai[j] < bi[j]:
            return -1
        if ai[j] > bi[j]:
            return +1
    
    return 0

@cython.boundscheck(False)  # Deactivate bounds checking.
@cython.wraparound(False)   # Deactivate negative indexing.
@cython.cdivision(True) # Deactivate zero division checking.
cdef int compare_14d(const void *a, const void *b):
    cdef Py_ssize_t j
    
    cdef int *ai = (<int**>a)[0]
    cdef int *bi = (<int**>b)[0]
    
    for j in range(14):
        if ai[j] < bi[j]:
            return -1
        if ai[j] > bi[j]:
            return +1
    
    return 0

@cython.boundscheck(False)  # Deactivate bounds checking.
@cython.wraparound(False)   # Deactivate negative indexing.
@cython.cdivision(True) # Deactivate zero division checking.
cdef int compare_15d(const void *a, const void *b):
    cdef Py_ssize_t j
    
    cdef int *ai = (<int**>a)[0]
    cdef int *bi = (<int**>b)[0]
    
    for j in range(15):
        if ai[j] < bi[j]:
            return -1
        if ai[j] > bi[j]:
            return +1
    
    return 0

@cython.boundscheck(False)  # Deactivate bounds checking.
@cython.wraparound(False)   # Deactivate negative indexing.
@cython.cdivision(True) # Deactivate zero division checking.
cdef int compare_16d(const void *a, const void *b):
    cdef Py_ssize_t j
    
    cdef int *ai = (<int**>a)[0]
    cdef int *bi = (<int**>b)[0]
    
    for j in range(16):
        if ai[j] < bi[j]:
            return -1
        if ai[j] > bi[j]:
            return +1
    
    return 0

@cython.boundscheck(False)  # Deactivate bounds checking.
@cython.wraparound(False)   # Deactivate negative indexing.
@cython.cdivision(True) # Deactivate zero division checking.
cdef int compare_17d(const void *a, const void *b):
    cdef Py_ssize_t j
    
    cdef int *ai = (<int**>a)[0]
    cdef int *bi = (<int**>b)[0]
    
    for j in range(17):
        if ai[j] < bi[j]:
            return -1
        if ai[j] > bi[j]:
            return +1
    
    return 0

@cython.boundscheck(False)  # Deactivate bounds checking.
@cython.wraparound(False)   # Deactivate negative indexing.
@cython.cdivision(True) # Deactivate zero division checking.
cdef int compare_18d(const void *a, const void *b):
    cdef Py_ssize_t j
    
    cdef int *ai = (<int**>a)[0]
    cdef int *bi = (<int**>b)[0]
    
    for j in range(18):
        if ai[j] < bi[j]:
            return -1
        if ai[j] > bi[j]:
            return +1
    
    return 0

@cython.boundscheck(False)  # Deactivate bounds checking.
@cython.wraparound(False)   # Deactivate negative indexing.
@cython.cdivision(True) # Deactivate zero division checking.
cdef int compare_19d(const void *a, const void *b):
    cdef Py_ssize_t j
    
    cdef int *ai = (<int**>a)[0]
    cdef int *bi = (<int**>b)[0]
    
    for j in range(19):
        if ai[j] < bi[j]:
            return -1
        if ai[j] > bi[j]:
            return +1
    
    return 0

@cython.boundscheck(False)  # Deactivate bounds checking.
@cython.wraparound(False)   # Deactivate negative indexing.
@cython.cdivision(True) # Deactivate zero division checking.
cdef int compare_20d(const void *a, const void *b):
    cdef Py_ssize_t j
    
    cdef int *ai = (<int**>a)[0]
    cdef int *bi = (<int**>b)[0]
    
    for j in range(20):
        if ai[j] < bi[j]:
            return -1
        if ai[j] > bi[j]:
            return +1
    
    return 0
