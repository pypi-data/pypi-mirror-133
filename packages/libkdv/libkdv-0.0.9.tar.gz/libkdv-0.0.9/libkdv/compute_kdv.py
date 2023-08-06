import ctypes
import os
import platform


def load_library(libname, loader_path):
    """
    It is possible to load a library using
    >>> lib = ctypes.cdll[<full_path_name>] # doctest: +SKIP

    But there are cross-platform considerations, such as library file extensions,
    plus the fact Windows will just load the first library it finds with that name.
    NumPy supplies the load_library function as a convenience.

    Parameters
    ----------
    libname : str
        Name of the library, which can have 'lib' as a prefix,
        but without an extension.
    loader_path : str
        Where the library can be found.

    Returns
    -------
    ctypes.cdll[libpath] : library object
        A ctypes library object

    Raises
    ------
    OSError
        If there is no library with the expected extension, or the
        library is defective and cannot be loaded.
    """
    if ctypes.__version__ < '1.0.1':
        import warnings
        warnings.warn("All features of ctypes interface may not work "
                        "with ctypes < 1.0.1", stacklevel=2)

    ext = os.path.splitext(libname)[1]
    if not ext:
        # Try to load library with platform-specific name, otherwise
        # default to libname.[so|pyd].  Sometimes, these files are built
        # erroneously on non-linux platforms.
        from numpy.distutils.misc_util import get_shared_lib_extension
        so_ext = get_shared_lib_extension()
        libname_ext = [libname + so_ext]
        # mac, windows and linux >= py3.2 shared library and loadable
        # module have different extensions so try both
        so_ext2 = get_shared_lib_extension(is_python_ext=True)
        if not so_ext2 == so_ext:
            libname_ext.insert(0, libname + so_ext2)
    else:
        libname_ext = [libname]

    loader_path = os.path.abspath(loader_path)
    if not os.path.isdir(loader_path):
        libdir = os.path.dirname(loader_path)
    else:
        libdir = loader_path

    for ln in libname_ext:
        libpath = os.path.join(libdir, ln)
        if os.path.exists(libpath):
            try:
                return ctypes.cdll[libpath]
            except OSError:
                ## defective lib file
                raise
    ## if no successful return in the libname_ext loop:
    raise OSError("no file with expected extension")
    


dll_name = 'rapid_kdv.so'

library_path = os.path.abspath(os.path.join(os.path.dirname(__file__), dll_name))

rapid_kdv_C_library = load_library('rapid_kdv.so',library_path)
rapid_kdv = rapid_kdv_C_library.kdv
rapid_kdv.argtypes = (ctypes.c_int,ctypes.POINTER(ctypes.c_char_p))
rapid_kdv.restype = ctypes.c_char_p

def compute_kdv(args):
    args = (ctypes.c_char_p * len(args))(*args)    
    kdv = rapid_kdv(len(args),args).decode('utf-8')
    return kdv




  

  

    


