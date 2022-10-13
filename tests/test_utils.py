import pytest

import sys
cupy_module_name = 'cupy'
if cupy_module_name in sys.modules:
    import cupy as np
else:
    import numpy as np
sys.path.append('/home/nogabi/Workspace/capstone/bvhViewer')

import utils

def test_get_unit():
    a = np.array([10., 0., 0.], dtype=np.float64)
    np.testing.assert_allclose(utils.getUnit(a), np.array([1.,0.,0.], dtype=np.float64))