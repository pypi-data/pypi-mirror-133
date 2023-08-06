import cython
import numpy as np
import sys

cimport cython
cimport numpy as np
from libc.math cimport ceil, sqrt
from libc.stdlib cimport free
from libc.stdlib cimport malloc

include "../../_parameters.pxi"

@cython.wraparound(False)
@cython.boundscheck(False)
cpdef np.ndarray[BTYPE_t, ndim=1] knn_condensed(
  np.ndarray[FTYPE_t, ndim=1] condensed_distances, int k
):
    """
    Computes the mask for a knn-graph from a condensed distance matrix.
  
    Maintains memory efficiency of condensed matrix at the cost of
    additional run time.
  
    Parameters
    ----------
    condensed_distances : 1D numpy array
      The pair-wise distances
    k : int
      The number of neighbours to add to the graph.
  
    Returns
    -------
    A boolean 1D numpy array indicating the edges of the knn-graph
    """
    print('testing')
    cdef int N = len(condensed_distances)
    cdef int n = <int>ceil(sqrt(<double>N * 2))
    cdef np.ndarray[BTYPE_t, ndim=1] res = np.zeros(N, dtype='bool')
    if k <= 1:
        return res
    k-=1

    cdef int row, i, j, jj
    cdef double distance, threshold
    cdef double *min_k = <double *> malloc(sizeof(double) * k)
    if min_k is NULL:
        raise Exception()
    cdef int *indices = <int *> malloc(sizeof(int) * n)
    if indices is NULL:
        raise Exception()

    cdef double MAX_FLOAT = sys.float_info.max

    # Loop over all nodes
    for row in range(n):
        # reset min_k values
        for j in range(k):
            min_k[j] = MAX_FLOAT

        # loop over all nodes again
        for i in range(n):
            # skip the initial node
            if i == row:
                continue
            # find the distance of node row to node i
            indices[i] = _sub2ind(row, i, n)
            distance = condensed_distances[indices[i]]
            # place the distance in the min_k array
            for j in range(k):
                if distance < min_k[j]:
                    for jj in range(k-2, j-1, -1):
                        min_k[jj+1] = min_k[jj]
                    min_k[j] = distance
                    break
        # determine the threshold distance
        threshold = min_k[k-1]
        print(threshold)
        # mark all edges shorter than the threshold
        for i in range(n):
          if i == row:
            continue
          j = indices[i]
          if condensed_distances[j] <= threshold:
            res[j] = True

    free(<void *>min_k)
    free(<void *>indices)
    return res


@cython.nonecheck(False)
@cython.wraparound(False)
@cython.boundscheck(False)
cdef inline unsigned int _sub2ind(unsigned int i,  unsigned int j,
                                  unsigned int n) nogil:
    # assert i != j, "no diagonal elements in condensed matrix"
    if i < j:
        i, j = j, i
    return n*j - j*(j+1)//2 + i - 1 - j