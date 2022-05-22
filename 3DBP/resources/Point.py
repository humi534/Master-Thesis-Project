# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 10:58:47 2021

@author: hugop
"""

class Point:
    def __init__(self, x:int, y:int, z:int):
        self.x = x
        self.y = y
        self.z = z
    
    def __repr__(self) -> repr:
        return repr((self.x, self.y, self.z))
        
    def modify(self, x=None, y=None, z=None):
        if x != None:
            self.x = x
        if y != None:
            self.y = y
        if z != None:
            self.z = z
            
    def get_coordinates(self):
        return [self.x, self.y, self.z]
        
            
    