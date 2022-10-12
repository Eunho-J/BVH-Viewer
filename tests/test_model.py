from bvhModel import *
from bvhRenderer import render_animation
import sys

from window.windowManager import *


def test_parse_hierarchy():
        
    skel = BvhSkeleton("test")

    skel.parse_hierarchy(
    '''
    ROOT Hips
    {
        OFFSET	0.00	0.00	0.00
        CHANNELS 6 Xposition Yposition Zposition Zrotation Xrotation Yrotation
        JOINT Chest
        {
            OFFSET	 0.00	 5.21	 0.00
            CHANNELS 3 Zrotation Xrotation Yrotation
            JOINT Neck
            {
                OFFSET	 0.00	 18.65	 0.00
                CHANNELS 3 Zrotation Xrotation Yrotation
                JOINT Head
                {
                    OFFSET	 0.00	 5.45	 0.00
                    CHANNELS 3 Zrotation Xrotation Yrotation
                    End Site 
                    {
                        OFFSET	 0.00	 3.87	 0.00
                    }
                }
            }
            JOINT LeftCollar
            {
                OFFSET	 1.12	 16.23	 1.87
                CHANNELS 3 Zrotation Xrotation Yrotation
                JOINT LeftUpArm
                {
                    OFFSET	 5.54	 0.00	 0.00
                    CHANNELS 3 Zrotation Xrotation Yrotation
                    JOINT LeftLowArm
                    {
                        OFFSET	 0.00	-11.96	 0.00
                        CHANNELS 3 Zrotation Xrotation Yrotation
                        JOINT LeftHand
                        {
                            OFFSET	 0.00	-9.93	 0.00
                            CHANNELS 3 Zrotation Xrotation Yrotation
                            End Site 
                            {
                                OFFSET	 0.00	-7.00	 0.00
                            }
                        }
                    }
                }
            }
            JOINT RightCollar
            {
                OFFSET	-1.12	 16.23	 1.87
                CHANNELS 3 Zrotation Xrotation Yrotation
                JOINT RightUpArm
                {
                    OFFSET	-6.07	 0.00	 0.00
                    CHANNELS 3 Zrotation Xrotation Yrotation
                    JOINT RightLowArm
                    {
                        OFFSET	 0.00	-11.82	 0.00
                        CHANNELS 3 Zrotation Xrotation Yrotation
                        JOINT RightHand
                        {
                            OFFSET	 0.00	-10.65	 0.00
                            CHANNELS 3 Zrotation Xrotation Yrotation
                            End Site 
                            {
                                OFFSET	 0.00	-7.00	 0.00
                            }
                        }
                    }
                }
            }
        }
        JOINT LeftUpLeg
        {
            OFFSET	 3.91	 0.00	 0.00
            CHANNELS 3 Zrotation Xrotation Yrotation
            JOINT LeftLowLeg
            {
                OFFSET	 0.00	-18.34	 0.00
                CHANNELS 3 Zrotation Xrotation Yrotation
                JOINT LeftFoot
                {
                    OFFSET	 0.00	-17.37	 0.00
                    CHANNELS 3 Zrotation Xrotation Yrotation
                    End Site 
                    {
                        OFFSET	 0.00	-3.46	 0.00
                    }
                }
            }
        }
        JOINT RightUpLeg
        {
            OFFSET	-3.91	 0.00	 0.00
            CHANNELS 3 Zrotation Xrotation Yrotation
            JOINT RightLowLeg
            {
                OFFSET	 0.00	-17.63	 0.00
                CHANNELS 3 Zrotation Xrotation Yrotation
                JOINT RightFoot
                {
                    OFFSET	 0.00	-17.14	 0.00
                    CHANNELS 3 Zrotation Xrotation Yrotation
                    End Site 
                    {
                        OFFSET	 0.00	-3.75	 0.00
                    }
                }
            }
        }
    }          
    ''')

    for idx, joint in enumerate(skel.joints):
        print(idx, "=", joint.index, ": ", joint.name, "\n    P: ", joint.parent_index)
        
def test_name_split():
    file = "/home/nogabi/Workspace/capstone/bvhViewer/tests/test_bvh.bvh"
    anim = BvhAnimation(file)
    print(anim.name, " ", anim.skeleton.name)
    for joints in anim.skeleton.joints:
        print(joints.channels)
        for idx, move_info in enumerate(joints.movement_infos):
            print("{:d} ".format(idx), move_info.movement_per_channel)
    
def test_name_split():
    file = "/home/nogabi/Workspace/capstone/bvhViewer/tests/test_bvh.bvh"
    anim = BvhAnimation(file)


def main():
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    
    file = "/home/nogabi/Workspace/capstone/bvhViewer/tests/bvh_files/sample-spin.bvh"
    anim = BvhAnimation(file)
    
    win.glWidget.set_bvh_animation(anim)
    
    win.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()