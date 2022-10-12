from PyQt5 import QtCore # core Qt functionality, QtWidgets
from PyQt5 import QtGui # extends QtCore with GUI functionality, QtWidgets
from PyQt5 import QtWidgets

class ControlWidget(QtWidgets.QWidget):
    def __init__(self, parent, linked_glWidget):
        QtWidgets.QWidget.__init__(self, parent)
        self.setGeometry(0,0,30,30)
        self.linked_glWidget = linked_glWidget
        self.initGui()
        
    def initGui(self):
        self.grid_layout = QtWidgets.QGridLayout()
        self.setLayout(self.grid_layout)
        
        self.frame_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.play_btn = QtWidgets.QPushButton(self)
        self.stop_btn = QtWidgets.QPushButton(self)
        self.frame_edit = QtWidgets.QLineEdit(self)
        self.frame_max_label = QtWidgets.QLabel(self)
        
        self.play_btn.setIcon(QtGui.QIcon("icons/play.png"))
        self.stop_btn.setIcon(QtGui.QIcon("icons/stop.png"))
        
        self.grid_layout.addWidget(self.play_btn, 0, 0)
        self.grid_layout.addWidget(self.stop_btn, 0, 1)
        self.grid_layout.addWidget(self.frame_slider, 0, 2)
        self.grid_layout.addWidget(self.frame_edit, 0, 3)
        self.grid_layout.addWidget(self.frame_max_label, 0,4)
        
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.frame_slider.setSizePolicy(sizePolicy)
        
        size = QtCore.QSize(32, 32)
        self.play_btn.setFixedSize(size)
        self.stop_btn.setFixedSize(size)
        self.frame_edit.setFixedSize(size)
        
        size = QtCore.QSize(64, 32)
        self.frame_max_label.setFixedSize(size)
        
        self.frame_edit.setAlignment(QtCore.Qt.AlignRight)
        # self.frame_max_label.setAlignment(QtCore.Qt.AlignLeft)
        
        self.set_frame_max(0)
        self.frame_edit.setText(str(0))
        
        self.play_btn.clicked.connect(lambda val: self._play_btn_click())
        self.stop_btn.clicked.connect(lambda val: self._stop_btn_click())
        self.frame_edit.textEdited.connect(lambda val: self._set_frame_index(int(val)) if val.isdigit() else self._set_frame_index(0))
        self.frame_slider.valueChanged.connect(lambda val: self._set_frame_index(val))
            
    def _play_btn_click(self):
        self.linked_glWidget.play_or_pause_animation()
        if self.linked_glWidget.is_animation_play:
            self.play_btn.setIcon(QtGui.QIcon("icons/pause.png"))
        else:
            self.play_btn.setIcon(QtGui.QIcon("icons/play.png"))
    
    def _stop_btn_click(self):
        self.linked_glWidget.stop_animation()
        self.play_btn.setIcon(QtGui.QIcon("icons/play.png"))
    
    def _set_frame_index(self, index):
        result = self.linked_glWidget.set_frame(index)
        if result == 0:
            self.frame_edit.setText(str(index))
            self.frame_slider.setSliderPosition(index)
        elif result == 1:
            self.linked_glWidget.set_frame(0)
            self.frame_edit.setText(str(0))
            self.frame_slider.setSliderPosition(0)
            QtWidgets.QMessageBox.warning(None, "Wrong Frame Number!", "Entered number is out of range")
        elif result == 2:
            self.frame_edit.setText(str(0))
            self.frame_slider.setSliderPosition(0)
        
    def set_frame_max(self, max_val:int):
        self.frame_slider.setMaximum(max_val)
        self.frame_max_label.setText("/ {:d}".format(max_val))
    
    def attach_current_frame_to_ui(self, index):
        self.frame_edit.setText(str(index))
        self.frame_slider.setSliderPosition(index)
        
    def attach_play_btn_current_state(self, is_playing:bool):
        if is_playing:
            self.play_btn.setIcon(QtGui.QIcon("./window/icons/pause.png"))
        else:
            self.play_btn.setIcon(QtGui.QIcon("./window/icons/play.png"))