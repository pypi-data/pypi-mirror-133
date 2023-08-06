"""Classes and functions that generate data with the potential of artistic use.

The module is organised in different submodules where each submodule is named after the first known
person who introduced the respective algorithms. Unlike the :mod:`mutwo.converters` module the entered
data and the resulting data can be very different in type and form.

The term 'generators' simply labels the functionality of the module and shouldn't be confused with the Python
term for specific functions with the 'yield' keyword.
"""

from . import edwards_constants
from . import sabat_constants

from . import brown
from . import brun
from . import edwards
from . import generic
from . import gray
from . import koenig
from . import toussaint
from . import wilson
