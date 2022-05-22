# -*- coding: utf-8 -*-
"""
Created on Sat Jul  3 18:09:02 2021

@author: Hugo Poncelet
"""

from .constants import Axis, Rotation_type

class Box:
    
    counter = 0 #class variable
    
    def __init__(self, name=None, width=0, depth=0, height=0, start_x=0, start_y=0, start_z=0, weight=1, boxDict=None): 

        if boxDict == None:
            self.name = name
            self.width = width
            self.depth = depth
            self.height = height
            self.start_x = start_x
            self.start_y = start_y
            self.start_z = start_z
            self.end_x = None
            self.end_y = None
            self.end_z = None
            self.id = self.counter
            self.rotation_type = 0
            self.weight = weight
            Box.counter += 1

        else:
            for key, value in boxDict.items():
                setattr(self, key, value)
        
    def __repr__(self) -> repr:
        return repr((self.id, self.width, self.height, self.depth, self.start_x, self.start_y, self.start_z, self.end_x,
                    self.end_y, self.end_y, self.weight))
    
    def set_end_position(self, x:int ,y:int ,z:int ) -> None:
        self.end_x = x
        self.end_y = y
        self.end_z = z
    
    def toString(self) -> str:
        return  "{ id: " + str(self.id) + ", " + "width: " + str(self.width) + ", " + "depth: " + str(self.depth) + ", " + "height: " + str(self.height) + ", " + "x: " + str(self.end_x) + ", " + "y: " + str(self.end_y)  + ", " + "z: " + str(self.end_z)  + " }"
    
    def get_volume(self) -> int:
        return int(self.width * self.height * self.depth)
    
    def get_biggest_surface(self) -> int:
        sizes = [self.width, self.depth, self.height]
        sizes.sort(reverse=True)
        return sizes[0]*sizes[1]
    
    def set_direction(self, dir1:int, dir2:int, dir3:int) -> None:
        """Oriente la boite dans l'ordre des axes donnés"""
        sizes = [self.width, self.depth, self.height]
        sizes.sort(reverse=True)
        
        #_______dir1_________
        
        if dir1 == Axis.width:
            self.width = sizes[0]
            
        elif dir1 == Axis.height:
            self.height = sizes[0]
            
        elif dir1 == Axis.depth:
            self.depth = sizes[0]
            
        #_______dir2_________
            
        if dir2 == Axis.width:
            self.width = sizes[1]
            
        elif dir2 == Axis.height:
            self.height = sizes[1]
            
        elif dir2 == Axis.depth:
            self.depth = sizes[1]
            
        #_______dir3_________
    
        if dir3 == Axis.width:
            self.width = sizes[2]
            
        elif dir3 == Axis.height:
            self.height = sizes[2]
            
        elif dir3 == Axis.depth:
            self.depth = sizes[2]
    
    def reset_rotation_type(self) -> None:
        if self.rotation_type == Rotation_type.X:
            tmp = self.depth
            self.depth = self.height
            self.height = tmp
        
        elif self.rotation_type == Rotation_type.Y:
            tmp = self.width
            self.width = self.depth
            self.depth = tmp
        
        elif self.rotation_type == Rotation_type.Z:
            tmp = self.width
            self.width = self.height
            self.height = tmp
            
        elif self.rotation_type == Rotation_type.XY:
            tmp = self.width
            self.width = self.depth
            self.depth = self.height
            self.height = tmp
            
        elif self.rotation_type == Rotation_type.XZ:
            tmp = self.width
            self.width = self.height
            self.height = self.depth
            self.depth = tmp
        
        self.rotation_type = Rotation_type.Default
    
    def set_rotation_type(self, rotation_type:int) -> None:
        """
            Effectue une rotation de la boite afin de la positionner à la bonne 
            rotation par rapport à sa rotation d'origine
        """
        self.reset_rotation_type()
        
        if rotation_type == Rotation_type.X:
            self.rotation_type = Rotation_type.X
            tmp = self.depth
            self.depth = self.height
            self.height = tmp
            
        elif rotation_type == Rotation_type.Y:
            self.rotation_type = Rotation_type.Y
            tmp = self.width
            self.width = self.depth
            self.depth = tmp
        
        elif rotation_type == Rotation_type.Z:
            self.rotation_type = Rotation_type.Z
            tmp = self.width
            self.width = self.height
            self.height = tmp
            
        elif rotation_type == Rotation_type.XY:
            self.rotation_type = Rotation_type.XY
            tmp = self.width
            self.width = self.height
            self.height = self.depth
            self.depth = tmp
            
        elif rotation_type == Rotation_type.XZ:
            self.rotation_type = Rotation_type.XZ
            tmp = self.width
            self.width = self.depth
            self.depth = self.height
            self.height = tmp
    
    def get_dimensions(self) -> list:
        return [self.width, self.height, self.depth]