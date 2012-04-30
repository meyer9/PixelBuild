
from info import __doc__
from numpy.version import version as __version__

import multiarray
import umath
import _internal # for freeze programs
import numerictypes as nt
multiarray.set_typeDict(nt.sctypeDict)
from numeric import *
from fromnumeric import *
import defchararray as char
import records as rec
from records import *
from memmap import *
from defchararray import chararray
import scalarmath
from function_base import *
from machar import *
from getlimits import *
from shape_base import *
del nt

from fromnumeric import amax as max, amin as min, \
     round_ as round
from numeric import absolute as abs

__all__ = ['char','rec','memmap']
__all__ += numeric.__all__
__all__ += fromnumeric.__all__
__all__ += rec.__all__
__all__ += ['chararray']
__all__ += function_base.__all__
__all__ += machar.__all__
__all__ += getlimits.__all__
__all__ += shape_base.__all__


from numpy.testing import Tester
test = Tester().test
bench = Tester().bench

# Make it possible so that ufuncs can be pickled
#  Here are the loading and unloading functions
# The name numpy.core._ufunc_reconstruct must be
#   available for unpickling to work.
def _ufunc_reconstruct(module, name):
    mod = __import__(module)
    return getattr(mod, name)

def _ufunc_reduce(func):
    from pickle import whichmodule
    name = func.__name__
    return _ufunc_reconstruct, (whichmodule(func,name), name)


import sys
if sys.version_info[0] < 3:
    import copy_reg as copyreg
else:
    import copyreg

copyreg.pickle(ufunc, _ufunc_reduce, _ufunc_reconstruct)
# Unclutter namespace (must keep _ufunc_reconstruct for unpickling)
del copyreg
del sys
del _ufunc_reduce
