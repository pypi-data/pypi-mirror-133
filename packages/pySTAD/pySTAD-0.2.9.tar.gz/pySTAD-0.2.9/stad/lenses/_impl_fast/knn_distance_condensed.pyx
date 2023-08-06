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
cpdef np.ndarray[FTYPE_t, ndim=1] knn_distance_condensed(
  np.ndarray[FTYPE_t, ndim=1] condensed_distances, int k
):
    """
    Computes the distance of each node's k-closest neighbour.

    Performs all operations on the condensed distance matrix. Uses less
    memory, but more compute time than the dense version.

    Parameters
    ----------
    condensed_distances : a condensed distance matrix (upper triangle)
    k : the closest neighbour to find

    Returns
    -------
    A 1D numpy vector with the distance to each node's k-closest neighbour. 
    """
    cdef int n = <int>ceil(sqrt(<double>len(condensed_distances) * 2))
    cdef np.ndarray[FTYPE_t, ndim=1] res = np.zeros(n)
    if k <= 1:
        return res
    k -= 1

    cdef int row, i, j, jj
    cdef double distance
    cdef double *min_k = <double *> malloc(sizeof(double) * k)
    if min_k is NULL:
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
            distance = condensed_distances[_sub2ind(row, i, n)]
            # place the distance in the min_k array
            for j in range(k):
                if distance < min_k[j]:
                    for jj in range(k-2, j-1, -1):
                        min_k[jj+1] = min_k[jj]
                    min_k[j] = distance
                    break
        # return the k-th smallest value
        res[row] = min_k[k-1]

    free(<void *>min_k)
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