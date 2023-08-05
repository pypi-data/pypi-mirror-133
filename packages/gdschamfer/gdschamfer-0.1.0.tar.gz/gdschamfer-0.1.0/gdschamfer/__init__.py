######################################################################
#                                                                    #
#              Copyright Arun Goud Akkala 2021.                      #
#  Distributed under the Boost Software License, Version 1.0.        #
#          (See accompanying LICENSE file or copy at                 #
#            https://www.boost.org/LICENSE_1_0.txt)                  #
#                                                                    #
######################################################################

from ._version import __version__
from .gdschamfer import *

__all__ = ["__version__", "chamfer_polygons", "chamfer_cell", "chamfer_gds"]
