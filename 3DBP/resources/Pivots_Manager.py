# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 11:04:11 2021

@author: hugop
"""
from .Point import Point
import ManipConfigFile

class Pivots_Manager:
    def __init__(self):
        self.all_pivots = []
        existingPoints = ManipConfigFile.getAllPivotPoints()
        for point in existingPoints:
            self.add_pivot(point.x, point.y, point.z)
    
    def get_first_pivot(self) -> Point:
        if not self.all_pivots:
            return None
        return self.all_pivots[0]


    def add_pivot(self, x:int, y:int, z:int) -> None:
        
        index=0

        if len(self.all_pivots) == 0:
            self.all_pivots.insert(index, Point(x,y,z))

        while (y > self.all_pivots[index].y):
            index += 1
            if index >= len(self.all_pivots):
                self.all_pivots.insert(index, Point(x,y,z))
                return
            
        while(x < self.all_pivots[index].x and y == self.all_pivots[index].y):
            index += 1
            if index >= len(self.all_pivots):
                break
            
        self.all_pivots.insert(index, Point(x,y,z))

            
    def delete_pivot(self, pivot:Point) -> None:
        
        if pivot in self.all_pivots:
            self.all_pivots.remove(pivot)
            del pivot
            
        else:
            raise Exception("This pivot point does not exist")
            
    def is_empty(self) -> bool:
        """Return True if no pivot point exists, False otherwise"""
        return (not self.all_pivots)
            
    def print_state(self) -> None:
        print("All Pivots: " + str(self.all_pivots))
            
    def setNewPivotPointsInConfig(self):
        ManipConfigFile.setPivotPoints(self.all_pivots)
            
    
            
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        