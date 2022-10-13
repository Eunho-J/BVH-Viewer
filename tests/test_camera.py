import pytest
import sys
cupy_module_name = 'cupy'
if cupy_module_name in sys.modules:
    import cupy as np
else:
    import numpy as np
sys.path.append('/home/nogabi/Workspace/capstone/bvhViewer')
from camManager import Camera

@pytest.fixture
def camera():
    camera = Camera()
    return camera
    
def test_orbit_change(camera):
    camera.orbit(15, 11, 0.1)
    np.testing.assert_allclose(camera.xang, -np.radians(30) + 11 * 0.1)
    np.testing.assert_allclose(camera.yang, np.radians(45) + 15 * 0.1)
    
def test_panning_change(camera):
    camera.panning(15, 11, 0.1)
    
    np.testing.assert_array_almost_equal(camera.target, 
                                         camera.current_cam[0,:3] * -15 * 0.1 * camera.zoom 
                                         + camera.current_cam[1,:3] * 11 * 0.1 * camera.zoom)
    
def test_zoomming_change(camera):
    camera.zoomming(13)
    np.testing.assert_allclose(camera.zoom, 3.0 - 13)
    
def test_target_change(camera):
    camera.set_target(np.array([3., 5., 7.], dtype=np.float64))
    np.testing.assert_array_almost_equal(camera.target, np.array([3., 5., 7.], dtype=np.float64))
    
    