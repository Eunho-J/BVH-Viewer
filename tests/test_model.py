import pytest
import sys
sys.path.append('/home/nogabi/Workspace/capstone/bvhViewer')

from bvhModel import *
from bvhRenderer import render_animation


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

    result = ""
    for idx, joint in enumerate(skel.joints):
        # print(idx, "=", joint.index, ": ", joint.name, "\n    P: ", joint.parent_index)
        result += "\n{:d} = {:d} :  {:s} \n    P:  {:d}".format(idx, joint.index, joint.name, joint.parent_index)
    
    compare = '''
0 = 0 :  Hips 
    P:  0
1 = 1 :  Chest 
    P:  0
2 = 2 :  Neck 
    P:  1
3 = 3 :  Head 
    P:  2
4 = 4 :  Head_Site 
    P:  3
5 = 5 :  LeftCollar 
    P:  1
6 = 6 :  LeftUpArm 
    P:  5
7 = 7 :  LeftLowArm 
    P:  6
8 = 8 :  LeftHand 
    P:  7
9 = 9 :  LeftHand_Site 
    P:  8
10 = 10 :  RightCollar 
    P:  1
11 = 11 :  RightUpArm 
    P:  10
12 = 12 :  RightLowArm 
    P:  11
13 = 13 :  RightHand 
    P:  12
14 = 14 :  RightHand_Site 
    P:  13
15 = 15 :  LeftUpLeg 
    P:  0
16 = 16 :  LeftLowLeg 
    P:  15
17 = 17 :  LeftFoot 
    P:  16
18 = 18 :  LeftFoot_Site 
    P:  17
19 = 19 :  RightUpLeg 
    P:  0
20 = 20 :  RightLowLeg 
    P:  19
21 = 21 :  RightFoot 
    P:  20
22 = 22 :  RightFoot_Site 
    P:  21'''        
    assert compare == result


def test_file_load():
    animation = BvhAnimation("/home/nogabi/Workspace/capstone/bvhViewer/tests/test_bvh.bvh")
    
    assert animation.name == "test_bvh"
    assert animation.skeleton.name == "test_bvh"
    compare_joints = ["Hips", "Chest", "Neck", "Head", "Head_Site", 
                      "LeftCollar", "LeftUpArm", "LeftLowArm", "LeftHand", "LeftHand_Site",
                      "RightCollar", "RightUpArm", "RightLowArm", "RightHand", "RightHand_Site",
                      "LeftUpLeg", "LeftLowLeg", "LeftFoot", "LeftFoot_Site",
                      "RightUpLeg", "RightLowLeg", "RightFoot", "RightFoot_Site" ]
    for idx, joint in enumerate(animation.skeleton.joints):
        assert joint.name == compare_joints[idx]
        
    