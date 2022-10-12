from typing import List
from typing_extensions import Self
import re
import os


import sys
cupy_module_name = 'cupy'
if cupy_module_name in sys.modules:
    import cupy as np
else:
    import numpy as np
    
class BvhMovementInfo:
    def __init__(self) -> None:
        self.movement_per_channel = []

class BvhJoint:
    def __init__(self, name, type, index):
        self.name = name
        self.offsets = []
        self.channels = []
        self.movement_infos: List[BvhMovementInfo] = []
        self.type = type
        
        self.num_child = 0
        self.children_index = []
        self.parent_index = 0
        self.index = index
        self.num_channel = 0
        
    def __repr__(self) -> str:
        return self.name
    
    def add_child(self, idx: int):
        self.children_index.append(idx)
        self.num_child += 1
    
    def set_parent(self, idx: int):
        self.parent_index = idx
    

class BvhSkeleton:
    def __init__(self, name:str) -> None:
        self.name = name
        self.joints: List[BvhJoint] = []

    def parse_hierarchy(self, hierarchy: str):
        lines = re.split('\\s*\\n+\\s*', hierarchy) #space(0+) + 개행(1+) + space(0+) 로 split -> 각 줄 trim

        parent_index_stack = []
        parent_index = 0
        current_index = 0
        
        for line in lines:
            words = re.split('\\s+', line) #space 로 분리
            symbol = words[0]
            
            if symbol == "ROOT":
                root = BvhJoint(words[1], symbol, current_index)
                self.joints.append(root)
                
                parent_index_stack.append(parent_index)
                parent_index = current_index
                current_index += 1
                
            elif symbol == "JOINT" or symbol == "End":
                name = words[1]
                if name == "Site":
                    name = self.joints[parent_index].name + "_" + name
                joint = BvhJoint(name, symbol, current_index)
                
                self.joints.append(joint)
                joint.set_parent(parent_index)
                self.joints[parent_index].add_child(current_index)
                
                parent_index_stack.append(parent_index)
                
                parent_index = current_index
                current_index += 1
            
            elif symbol == "OFFSET": #float로 변환해서 offset에 extend
                self.joints[current_index - 1].offsets.extend(map(float, words[1:]))
            
            elif symbol == "CHANNELS": #channel 설정
                num_channel = int(words[1])
                self.joints[current_index - 1].num_channel = num_channel
                self.joints[current_index - 1].channels.extend(words[2:2+num_channel])
            
            elif symbol == "}":
                parent_index = parent_index_stack.pop()
            
            
    def parse_and_add_movement(self, words: List[str]):
        words.reverse() #queue로 쓰기 위해
        for joint in self.joints:
            joint_move_info = BvhMovementInfo()
            
            for i in range(joint.num_channel):
                joint_move_info.movement_per_channel.append(float(words.pop()))
            
            joint.movement_infos.append(joint_move_info)
            
    def get_location_of_root(self, index_of_motion:int):
        joint = self.joints[0]
        location = np.array([joint.offsets[0], joint.offsets[1], joint.offsets[2], 1], dtype=np.float64)
        
        for i in range(joint.num_channel):
            if joint.channels[i].upper() == "Xposition".upper():
                translation = joint.movement_infos[index_of_motion].movement_per_channel[i]
                location[0] += translation
            elif joint.channels[i].upper() == "Yposition".upper():
                translation = joint.movement_infos[index_of_motion].movement_per_channel[i]
                location[1] += translation
            elif joint.channels[i].upper() == "Zposition".upper():
                translation = joint.movement_infos[index_of_motion].movement_per_channel[i]
                location[2] += translation
        return location[:3]


class BvhAnimation:
    def __init__(self, file):
        f = open(file, 'r')
        self.content = f.read()
        f.close()
        
        self.name, _ = os.path.splitext(re.split('\\/+', file)[-1])
        self.skeleton = BvhSkeleton(self.name)
        
        self.num_of_frame = 0
        self.frame_interval = 0
        
        hierarchy, animation = self.content.split("MOTION")
        self.skeleton.parse_hierarchy(hierarchy)
        self._parse_motion(animation)
    
    def _parse_motion(self, animation):
        lines = re.split('\\s*\\n+\\s*', animation)
        for line in lines:
            if line == '':
                continue
            
            words = re.split('\\s+', line)
            if line.startswith("Frame Time:"):
                self.frame_interval = float(words[2])
                continue
            elif line.startswith("Frames:"):
                self.num_of_frame = int(words[1])
                continue
            
            self.skeleton.parse_and_add_movement(words)