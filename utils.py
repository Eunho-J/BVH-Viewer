
import sys
cupy_module_name = 'cupy'
if cupy_module_name in sys.modules:
    import cupy as np
else:
    import numpy as np


def getUnit(arr):
    return arr / np.linalg.norm(arr)