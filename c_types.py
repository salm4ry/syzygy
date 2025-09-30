import ctypes

# map C type strings to ctypes fundamental types
# base: https://docs.python.org/3/library/ctypes.html#fundamental-data-types
TYPES = {
    # bytes
    "bool": ctypes.c_bool,
    "char": ctypes.c_char,
    "wchar_t": ctypes.c_wchar,
    "unsigned char": ctypes.c_ubyte,
    # integers
    "short": ctypes.c_short,
    "unsigned short": ctypes.c_ushort,
    "int": ctypes.c_int,
    "int8_t": ctypes.c_int8,
    "int16_t": ctypes.c_int16,
    "int32_t": ctypes.c_int32,
    "int64_t": ctypes.c_int64,
    "unsigned int": ctypes.c_uint,
    "uint8_t": ctypes.c_uint8,
    "uint16_t": ctypes.c_uint16,
    "uint32_t": ctypes.c_uint32,
    "uint64_t": ctypes.c_uint64,
    "long": ctypes.c_long,
    "unsigned long": ctypes.c_ulong,
    "long long": ctypes.c_longlong,
    # size
    "size_t": ctypes.c_size_t,
    "ssize_t": ctypes.c_ssize_t,
    # time
    "time_t": ctypes.c_time_t,
    # floating point
    "float": ctypes.c_float,
    "double": ctypes.c_double,
    "long double": ctypes.c_longdouble,
    # pointer (treat all types as void pointer)
    "*": ctypes.c_void_p,
}
