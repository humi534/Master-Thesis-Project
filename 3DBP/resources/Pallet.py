# -*- coding: utf-8 -*-
"""
Created on Sat Jul  3 18:22:11 2021

@author: hugop
"""

class Pallet:
    
    counter = 0 #class variable
    
    def __init__(self, width=0, depth=0, height=0, x=0, y=0, z=0, max_weight=200, palletDict=None): 
        if palletDict == None:
            self.width = width
            self.depth = depth
            self.height = height # correspond à la hauteur max que peuvent prendre les boites
            self.x = x
            self.y = y
            self.z = z
            self.id = self.counter
            self.max_weight = max_weight
            Pallet.counter += 1
        else:
            for key, value in palletDict.items():
                setattr(self, key, value)
         
    def __repr__(self) -> repr:
        return repr((self.width, self.height, self.depth, self.x, self.y, self.z))

    def get_volume(self):
        return int(self.width * self.height * self.depth)
    
    
    