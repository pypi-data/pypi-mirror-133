#cython: infer_types=True
#cython: embedsignature=True
#cython: binding=False
#cython: language_level=2
#distutils: language=c++

"""
Python wrapper for CityHash-CRC
"""

__author__      = "Eugene Scherba"
__email__       = "escherba+cityhash@gmail.com"
__version__     = '0.3.2'
__all__         = [
    "CityHashCrc128",
    "CityHashCrc128WithSeed",
    "CityHashCrc256",
]


cdef extern from * nogil:
    ctypedef unsigned long int uint32_t
    ctypedef unsigned long long int uint64_t


cdef extern from "<utility>" namespace "std" nogil:
    cdef cppclass pair[T, U]:
        T first
        U second
        pair()
        pair(pair&)
        pair(T&, U&)
        bint operator == (pair&, pair&)
        bint operator != (pair&, pair&)
        bint operator <  (pair&, pair&)
        bint operator >  (pair&, pair&)
        bint operator <= (pair&, pair&)
        bint operator >= (pair&, pair&)


cdef extern from "city.h" nogil:
    ctypedef uint32_t uint32
    ctypedef uint64_t uint64
    ctypedef pair[uint64, uint64] uint128


cdef extern from "citycrc.h" nogil:
    cdef uint128 c_CityHashCrc128 "CityHashCrc128" (const char *s, size_t length)
    cdef uint128 c_CityHashCrc128WithSeed "CityHashCrc128WithSeed" (const char *s, size_t length, uint128 seed)
    cdef void c_CityHashCrc256 "CityHashCrc256" (const char *s, size_t length, uint64 *result)


from cpython cimport long

from cpython.buffer cimport PyObject_CheckBuffer
from cpython.buffer cimport PyObject_GetBuffer
from cpython.buffer cimport PyBuffer_Release
from cpython.buffer cimport PyBUF_SIMPLE

from cpython.unicode cimport PyUnicode_Check
from cpython.unicode cimport PyUnicode_AsUTF8String

from cpython.bytes cimport PyBytes_Check
from cpython.bytes cimport PyBytes_GET_SIZE
from cpython.bytes cimport PyBytes_AS_STRING
from cpython.bytes cimport PyBytes_FromStringAndSize


cdef object _type_error(argname: str, expected: object, value: object):
    return TypeError(
        "Argument '%s' has incorrect type: expected %s, got '%s' instead" %
        (argname, expected, type(value).__name__)
    )


def CityHashCrc128(data) -> int:
    """Obtain a 128-bit hash from input data using CityHashCRC
    Args:
        data (str, buffer): input data (either string or buffer type)
    Returns:
        int: a 128-bit hash of the input data
    Raises:
        ValueError, TypeError
    Raises:
        ValueError: if input buffer is not C-contiguous
        TypeError: if input data is not a string or a buffer
    """
    cdef Py_buffer buf
    cdef bytes obj
    cdef pair[uint64, uint64] result
    if PyUnicode_Check(data):
        obj = PyUnicode_AsUTF8String(data)
        PyObject_GetBuffer(obj, &buf, PyBUF_SIMPLE)
        result = c_CityHashCrc128(<const char*>buf.buf, buf.len)
        PyBuffer_Release(&buf)
    elif PyBytes_Check(data):
        result = c_CityHashCrc128(<const char*>PyBytes_AS_STRING(data),
                               PyBytes_GET_SIZE(data))
    elif PyObject_CheckBuffer(data):
        PyObject_GetBuffer(data, &buf, PyBUF_SIMPLE)
        result = c_CityHashCrc128(<const char*>buf.buf, buf.len)
        PyBuffer_Release(&buf)
    else:
        raise _type_error("data", ["basestring", "buffer"], data)
    return 0x10000000000000000L * long(result.first) + long(result.second)


def CityHashCrc256(data) -> bytes:
    """Obtain a 256-bit hash from input data using CityHashCRC
    Args:
        data (str, buffer): input data (either string or buffer type)
    Returns:
        bytes: hashed value
    Raises:
        ValueError, TypeError
    Raises:
        ValueError: if input buffer is not C-contiguous
        TypeError: if input data is not a string or a buffer
    """
    cdef Py_buffer buf
    cdef bytes obj
    cdef uint64 out[4]
    if PyUnicode_Check(data):
        obj = PyUnicode_AsUTF8String(data)
        PyObject_GetBuffer(obj, &buf, PyBUF_SIMPLE)
        c_CityHashCrc256(<const char *>buf.buf, buf.len, out)
        PyBuffer_Release(&buf)
    elif PyBytes_Check(data):
        c_CityHashCrc256(
            <const char *>PyBytes_AS_STRING(data),
            PyBytes_GET_SIZE(data), out)
    elif PyObject_CheckBuffer(data):
        PyObject_GetBuffer(data, &buf, PyBUF_SIMPLE)
        c_CityHashCrc256(<const char *>buf.buf, buf.len, out)
        PyBuffer_Release(&buf)
    else:
        raise _type_error("data", ["basestring", "buffer"], data)
    return PyBytes_FromStringAndSize(<char *>out, 32)


def CityHashCrc128WithSeed(data, seed=0L) -> int:
    """Obtain a 128-bit hash from input data given a seed.
    Args:
        data (str, buffer): input data (either string or buffer type)
        seed (int, default=0): seed for random number generator
    Returns:
        int: a 128-bit hash of the input data
    Raises:
        ValueError, TypeError, OverflowError
    Raises:
        TypeError: if input data is not a string or a buffer
        ValueError: if input buffer is not C-contiguous
        OverflowError: if seed cannot be converted to unsigned int64
    """
    cdef Py_buffer buf
    cdef bytes obj
    cdef pair[uint64, uint64] result
    cdef pair[uint64, uint64] tseed

    tseed.first = seed >> 64ULL
    tseed.second = seed & ((1ULL << 64ULL) - 1ULL)

    if PyUnicode_Check(data):
        obj = PyUnicode_AsUTF8String(data)
        PyObject_GetBuffer(obj, &buf, PyBUF_SIMPLE)
        result = c_CityHashCrc128WithSeed(<const char*>buf.buf, buf.len, tseed)
        PyBuffer_Release(&buf)
    elif PyBytes_Check(data):
        result = c_CityHashCrc128WithSeed(<const char*>PyBytes_AS_STRING(data),
                                       PyBytes_GET_SIZE(data), tseed)
    elif PyObject_CheckBuffer(data):
        PyObject_GetBuffer(data, &buf, PyBUF_SIMPLE)
        result = c_CityHashCrc128WithSeed(<const char*>buf.buf, buf.len, tseed)
        PyBuffer_Release(&buf)
    else:
        raise _type_error("data", ["basestring", "buffer"], data)
    return 0x10000000000000000L * long(result.first) + long(result.second)
