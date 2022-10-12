from PyQt5 import QtCore # core Qt functionality, QtWidgets
from PyQt5 import QtGui # extends QtCore with GUI functionality, QtWidgets
from PyQt5 import QtOpenGL # provides QGLWidget, QtWidgets,a special OpenGL QWidget
from PyQt5 import QtWidgets
import OpenGL.GL as gl # python wrapping of OpenGL
import sys # we'll need this later to run our Qt application

cupy_module_name = "cupy"
if cupy_module_name in sys.modules:
    import cupy as np
else:
    import numpy as np

from camManager import *
from bvhRenderer import *

from window.windowUI import *

class GLWidget(QtOpenGL.QGLWidget):
    def __init__(self, parent):
        self.parent = parent
        QtOpenGL.QGLWidget.__init__(self, parent)
        
        self.follow_model = False
        
        self.cam = Camera()
        self.default_target = np.array([0,0,0], dtype=np.float64)
        self.cam.set_target(self.default_target)
        self.cursor_orbit_sensitivity = 0.003
        self.cursor_panning_sensitivity = 0.001
        self.wheel_sensitivity = 0.005
        self.mouse_pose_x_tmp = 0
        self.mouse_pose_y_tmp = 0
        self.is_mouse_left_btn_pressed = False
        self.is_mouse_right_btn_pressed = False
        
        self.index_of_frame = 0
        self.is_animation_play = False
        self.is_animation_on = False
        self.is_wiered = False
        self.bvh_animation:BvhAnimation = None
        
    def link_ui(self, linked_ui):
        self.linked_ui = linked_ui
        
    def change_wiered(self):
        self.is_wiered = not self.is_wiered
        
    def set_bvh_animation(self, bvh_animation:BvhAnimation):
        self.bvh_animation = bvh_animation
        
    def play_or_pause_animation(self):
        self.is_animation_on = True
        self.is_animation_play = not self.is_animation_play
        
    def set_frame(self, index: int):
        if self.bvh_animation == None:
            QtWidgets.QMessageBox.warning(None, "No BVH File!", "No bvh file attached!")
            return 2
        
        if index >= self.bvh_animation.num_of_frame or index < 0:
            return 1
        
        self.index_of_frame = index
        return 0
        
    def follow_or_unfollow_model(self):
        self.follow_model = not self.follow_model
    
    def stop_animation(self):
        self.is_animation_play = False
        self.is_animation_on = False
        self.index_of_frame = 0
        self.linked_ui.attach_current_frame_to_ui(0)

    def initializeGL(self):
        # self.qglClearColor(QtGui.QColor(50, 50, 50)) # initialize the screen to blue
        glClearColor(0.2, 0.2, 0.2, 1.0)
        gl.glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        gl.glEnable(GL_DEPTH_TEST)
        gl.glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    def resizeGL(self, width, height):
        self.cam.viewport_width = width
        self.cam.viewport_height = height

    def paintGL(self):
        if self.follow_model and self.bvh_animation != None:
            if self.is_animation_on:
                self.cam.set_target(self.bvh_animation.skeleton.get_location_of_root(self.index_of_frame))
            else:
                self.cam.set_target(np.array([0,0,0], dtype=np.float64))
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        
        self.cam.lookAt()
        # gluLookAt(5*np.sin(gCamAng), gCamHeight, 5*np.cos(gCamAng), 0,0,0, 0,1,0)
        
        draw_frame()
        draw_grid(50, 50)
        
        if self.is_animation_on and self.bvh_animation != None:
            self.linked_ui.attach_current_frame_to_ui(self.index_of_frame)
            if self.is_wiered:
                render_animation_wiered(self.bvh_animation, self.index_of_frame)
            else:
                render_animation(self.bvh_animation, self.index_of_frame)
        else :
            render_model(self.bvh_animation)
            
    def update_index_of_frame(self):
        if not self.is_animation_play:
            return
        self.index_of_frame += 1
        if self.index_of_frame == self.bvh_animation.num_of_frame:
            self.index_of_frame = 0

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        if a0.button() == QtCore.Qt.LeftButton:
            self.is_mouse_left_btn_pressed = True
        elif a0.button() == QtCore.Qt.RightButton:
            self.is_mouse_right_btn_pressed = True
        if a0.button() == QtCore.Qt.LeftButton or a0.button() == QtCore.Qt.RightButton:
            self.mouse_pose_x_tmp = a0.localPos().x()
            self.mouse_pose_y_tmp = a0.localPos().y()
            
    
    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
        if a0.button() == QtCore.Qt.LeftButton:
            self.is_mouse_left_btn_pressed = False
        elif a0.button() == QtCore.Qt.RightButton:
            self.is_mouse_right_btn_pressed = False
    
    def mouseMoveEvent(self, a0: QtGui.QMouseEvent) -> None:
        if self.is_mouse_left_btn_pressed:
            self.cam.orbit(self.mouse_pose_x_tmp - a0.localPos().x(), 
                           self.mouse_pose_y_tmp - a0.localPos().y(), 
                           self.cursor_orbit_sensitivity)
        if self.is_mouse_right_btn_pressed:
            self.cam.panning(a0.localPos().x() - self.mouse_pose_x_tmp, 
                             a0.localPos().y() - self.mouse_pose_y_tmp, 
                             self.cursor_panning_sensitivity)
        if self.is_mouse_left_btn_pressed or self.is_mouse_right_btn_pressed:
            self.mouse_pose_x_tmp = a0.localPos().x()
            self.mouse_pose_y_tmp = a0.localPos().y()
            
    def wheelEvent(self, a0: QtGui.QWheelEvent) -> None:
        self.cam.zoomming(a0.angleDelta().y() * self.wheel_sensitivity)
        
    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        if a0.key() == QtCore.Qt.Key_R:
            self.default_target = np.array([0., 0., 0.], dtype=np.float64)
            self.cam.set_target(self.default_target)
            self.cam.zoom = 3.0
        elif a0.key() == QtCore.Qt.Key_F:
            self.follow_or_unfollow_model()
        elif a0.key() == QtCore.Qt.Key_V:
            self.cam.change_orth()
        elif a0.key() == QtCore.Qt.Key_1:
            self.cam.view_target_at(0, 0, self.default_target)
        elif a0.key() == QtCore.Qt.Key_3:
            self.cam.view_target_at(0, np.radians(-90), self.default_target)
        elif a0.key() == QtCore.Qt.Key_5 and self.bvh_animation != None:
            self.cam.set_target(self.bvh_animation.skeleton.get_location_of_root(self.index_of_frame))
        elif a0.key() == QtCore.Qt.Key_7:
            self.cam.view_target_at(np.radians(90), 0, self.default_target)
        elif a0.key() == QtCore.Qt.Key_9:
            self.cam.view_target_at(np.radians(-90), 0, self.default_target)
        elif a0.key() == QtCore.Qt.Key_0:
            self.cam.view_target_at(np.radians(-30), np.radians(45), self.default_target)
        elif a0.key() == QtCore.Qt.Key_Space:
            self.play_or_pause_animation()
            self.linked_ui.attach_play_btn_current_state(self.is_animation_play)
        elif a0.key() == QtCore.Qt.Key_Escape:
            self.stop_animation()
        elif a0.key() == QtCore.Qt.Key_F4:
            self.change_wiered()

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self) # call the init for the parent class

        self.resize(1280, 720)
        self.setWindowTitle('BVH Viewer')
        self.setWindowIcon(QtGui.QIcon('icons/app.png'))

        self.glWidget = GLWidget(self)
        self.control_widget = ControlWidget(None, self.glWidget)
        self.glWidget.link_ui(self.control_widget)
        self.initGUI()
        self.setAcceptDrops(True)

        timer = QtCore.QTimer(self)
        timer.setInterval(20) # period, in milliseconds
        timer.timeout.connect(self.glWidget.updateGL)
        timer.start()

        self.timer_for_index_update = QtCore.QTimer(self.glWidget)
        self.timer_for_index_update.timeout.connect(self.glWidget.update_index_of_frame)

    def initGUI(self):
        central_widget = QtWidgets.QWidget()
        gui_layout = QtWidgets.QGridLayout()
        central_widget.setLayout(gui_layout)

        self.setCentralWidget(central_widget)

        gui_layout.addWidget(self.glWidget,0,0)
        gui_layout.addWidget(self.control_widget,1,0)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.control_widget.setSizePolicy(sizePolicy)
        
    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        return self.glWidget.keyPressEvent(a0)
    
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()
    
    def dropEvent(self, a0: QtGui.QDropEvent) -> None:
        files = [f.toLocalFile() for f in a0.mimeData().urls()]
        if len(files) > 1:
            print("many files! only first will loaded")
        print("file dropped!")
        file = files[0]
        self.glWidget.set_bvh_animation(BvhAnimation(file))
        self.control_widget.set_frame_max(self.glWidget.bvh_animation.num_of_frame - 1)
        
        interval = 1000 * self.glWidget.bvh_animation.frame_interval
        self.setWindowTitle('BVH Viewer [{:s}] fps:{:.1f}'.format(file, 1000 / interval) )
        self.glWidget.set_frame(0)
        print("interval set to ", interval)
        
        if self.timer_for_index_update.isActive():
            self.timer_for_index_update.stop()
        self.timer_for_index_update.setInterval(interval) # period, in milliseconds
        self.timer_for_index_update.start()
