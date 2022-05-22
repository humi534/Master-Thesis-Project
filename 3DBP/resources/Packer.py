# -*- coding: utf-8 -*-
"""
Created on Wed Aug 25 12:43:44 2021

@author: hugop
"""

from .Box import Box
from .Pallet import Pallet
from .constants import SortedBy, Axis, Rotation_type
from .Pivots_Manager import Pivots_Manager
from .Point import Point
import json
import ManipConfigFile

"""
à faire update:
Lorsque l'on vérifie les collisions entre boite dans le box fit, il faut inclure les placedBoxes, mais celle ci ne peuvent pas bouger

Comment se fait il que l'algo ne plante pas quand aucune pallette n'est initialisée? en fait pas sur à vérifier

Le pivot Manager doit simplement importer une fois les pivots, puis travaille en 'local' avec ses pivots le temps de l'algorthme
Une fois que l'algo est fini, il serait plus intéressant de tout fournir en une fois les nouvelles boites, nouveaux pivots, ...
au config plutot que de faire comme maintenant avec à chaque fois qu'une boite est placée virtuellement on la bouge dans le config

"""


"""
A faire:
    stabilité: à améliorer avec la diagonale
    ordre des boites dès le début: différents paramètres à tester
    réfléchir à faire une projection cette fois ci horizontale afin de corriger le petit probleme d'espace perdu, ou alors de mettre les prior2 en prior1 une fois les 1 finis
    Ajouter un niveau, techiquement un packer ne peut gérer que une seule palette, la répartition doit se faire plus haut
    la fonction set_box_direction doit etre améliorée afin de correspondre au sens de la palette
    Vérifier quand on renvoie None pour certaines fonctions que ca peut bien etre pris en compte dans les appels
    Attention le principe de priorité ne fonctionne pas quand une grosse boite
    empecher les mini boites au sol
     
    Check pivot validity n'est peut etre pas correct avec le get point below. à vérifier si prends le point juste en dessous ou si le meme est encore bon
    pour la stabilité une bonne idée serait d'effectuer un carré au centre et que les quatres coins sont bien positionné à la meme hauteur que le pivot
    
"""

class Packer:
    
    def __init__(self):
        
        self.undeterminedBoxes = ManipConfigFile.getListOfUndeterminedBoxes()
        self.newlyUnplacedBoxes = []
        self.sorted_by = ManipConfigFile.get_parameters()["sortingAlgorithm"]

        try:
            self.pallet = ManipConfigFile.getPallet()
        except: 
            raise Exception("une palette doit etre initialisée pour que packer puisse fonctionner")

        self.pivots_manager = Pivots_Manager()
        self.current_height = 0
        self.print_details = False

    def __repr__(self) -> repr:
        return repr(self.undeterminedBoxes)

    def update_config_file(self):
        """update le fichier config concernant les pivots (en appelant simplement la fonction de pivot Manager), les unplaced
        boxes, les placed boxes, les no fit boxes"""
        #--------Les points pivots
        self.pivots_manager.setNewPivotPointsInConfig()

        ManipConfigFile.copySeveralBoxesFromUndeterminedToUnplaced(self.newlyUnplacedBoxes)
        ManipConfigFile.copySeveralBoxesFromUndeterminedToNoFit(self.undeterminedBoxes)
        ManipConfigFile.clearUndeterminedBoxes()
             
    def set_box_direction(self):
        """à modifier en fonction de la palette"""
        for b in self.undeterminedBoxes:
            b.set_direction(Axis.width, Axis.depth, Axis.height)
    
    def sort_boxes(self):
        if self.sorted_by == "volume":
            if self.print_details:
                print("sorted by volume")
            self.undeterminedBoxes.sort(key=lambda box: box.get_volume(),reverse=True)
            
        elif self.sorted_by == "biggest_surface":
            if self.print_details:
                print("sorted by biggest surface")
            self.undeterminedBoxes.sort(key=lambda box: box.get_biggest_surface(), reverse=True)
        
        elif self.sorted_by == "longest_edge":
            pass
        
        else: raise Exception("sorted_by variable not valid")
            
    def rectangle_overlap(self, box1:Box, box2:Box, axis1:int, axis2:int) -> bool:
        
        dim1 = box1.get_dimensions()
        dim2 = box2.get_dimensions()
        
        pos1 = [box1.end_x, box1.end_y, box1.end_z]
        pos2 = [box2.end_x, box2.end_y, box2.end_z]
        
        if(((pos1[axis1]+dim1[axis1])<=pos2[axis1]) or ((pos2[axis1]+dim2[axis1])<=pos1[axis1]) or ((pos1[axis2]+dim1[axis2])<=pos2[axis2]) or ((pos2[axis2]+dim2[axis2])<=pos1[axis2])):
            return False
        else:
            return True
        
    def overlap(self, box1:Box, box2:Box) -> bool:
        """Return True if box1 and box2 overlap (intersect) eachother, False otherwise"""
        return (self.rectangle_overlap(box1, box2, Axis.width, Axis.depth) 
                and self.rectangle_overlap(box1, box2, Axis.width, Axis.height) 
                and self.rectangle_overlap(box1, box2, Axis.height, Axis.depth))
    
    def get_highest_point_below(self, point:Point) -> Point:
        """Renvoie un Point correspondant au point le plus haut situé juste en dessous du point mis en paramètre
            Si pas de boite, renvoie un point à hauteur de la palette"""
        possible_boxes = []
        for unplaced_box in self.newlyUnplacedBoxes:
            if (unplaced_box.end_x <= point.x < unplaced_box.end_x + unplaced_box.width and unplaced_box.end_z <= point.z < unplaced_box.end_z + unplaced_box.depth and unplaced_box.end_y + unplaced_box.height <= point.y):
                possible_boxes.append(unplaced_box)
        
        if not possible_boxes:
            return Point(point.x, self.pallet.y, point.z)
        
        highest_box = possible_boxes[0]
        for box in possible_boxes:
            if box.end_y > highest_box.end_y and box.end_y <= point.y and box.end_y > highest_box.end_y:
                highest_box = box
            
        return Point(point.x,highest_box.end_y+highest_box.height, point.z)
    
    def box_fit(self, box:Box, pivot:Point) -> bool:
        
        box.set_end_position(pivot.x, pivot.y, pivot.z)
        #check intersection with already placed boxes
        for other_box in self.newlyUnplacedBoxes:
            if self.overlap(box, other_box):
                #print("box position: " + str(box.x) + " " + str(box.y) + " " + str(box.z) + " " + str(box.get_dimensions()) )
                #print("Box not fit because overlap with other box: " + str(other_box.x) + " " + str(other_box.y) + " " + str(other_box.z))
                return False
            
        #check limits of pallet
        if box.end_x + box.width > self.pallet.x + self.pallet.width or box.end_y + box.height > self.pallet.y + self.pallet.height or box.end_z + box.depth > self.pallet.z + self.pallet.depth:
            #print("Box not fit because border of pallet")
            return False
            
        
        #check stability
        stability = self.check_box_stability(box)
        if not stability:
            return False
        
        if self.print_details:
            print("Box " + str(box.id) + " fit at: " + str([box.end_x, box.end_y, box.end_z]) + "\n")
            
        return True
        
    def pack_boxes(self):
        self.sort_boxes()
        self.set_box_direction()
        
        while (not self.pivots_manager.is_empty() and self.undeterminedBoxes): #tant qu'il reste des pivots et des boites non placées
            pivot = self.pivots_manager.get_first_pivot()
            if self.print_details:
                print("lowest pivot: " + str(pivot.y))
                self.pivots_manager.print_state() 
            
            #--------pivot validity---------
            pivot_validity = self.check_pivot_validity(pivot)
            if not pivot_validity:
                if self.print_details:
                    print("invalid pivot, go lower")
                
                #attention imaginons qu'il n'y ai pas de boite en dessous, il faudrait peut etre mieux juste renvoyer le point le plus haut
                highest_point_below = self.get_highest_point_below(pivot) 
                pivot.modify(y = highest_point_below.y) #projection
            
            
            flag = False #permet de faire un double break
            for box in self.undeterminedBoxes:
                for rotation_number in Rotation_type.ALL:
                    box.set_rotation_type(rotation_number)
                    if self.box_fit(box, pivot):
                        #box.set_position(pivot.x, pivot.y, pivot.z) #est techniquement inutile vu qu'on déplace deja la boite dans le box fit
                        self.undeterminedBoxes.remove(box)
                        self.newlyUnplacedBoxes.append(box)
                        self.pivots_manager.add_pivot(x=pivot.x+box.width, y=pivot.y, z=pivot.z)
                        self.pivots_manager.add_pivot(x=pivot.x, y=pivot.y, z=pivot.z+box.depth)
                        self.pivots_manager.add_pivot(x=pivot.x, y=pivot.y+box.height, z=pivot.z)
                        
                        flag = True
                        break
                    
                if flag: #break the nested loop
                    break

            self.pivots_manager.delete_pivot(pivot)
    
    def print_state(self):
        print("\nUNPLACED BOXES:")
        for box in self.newlyUnplacedBoxes:
            print('{"id":%s, "width:"%s, "height:"%s, "depth:"%s, "x:"%s, "y:"%s, "z:"%s' % (box.id, 
                box.width, box.height, box.depth, box.x, box.y, box.z))
        
        print(len(self.underterminedBoxes))
        print("\nNO FIT BOXES:")
        for box in self.underterminedBoxes:
            print('{"id":%s, "width:"%s, "height:"%s, "depth:"%s' % (box.id, box.width, box.height, box.depth))
        
    def check_pivot_validity(self, pivot:Point) -> bool:
        """Check if the pivot point is not sitting on an empty space (standing in the air)"""
        highest_point_below = self.get_highest_point_below(pivot)
        
        if (highest_point_below.y != pivot.y):
            return False
        
        return True
        
    def check_box_stability(self, box:Box) -> bool:
        """Assuming the box sit on another box"""
        # à ameliorer avec la diagonale
        #pour le moment, on check juste si le centre de gravité est sur un emplacement à même hauteur
        center = Point(box.end_x+box.width/2, box.end_y, box.end_z+box.depth/2)
        corner1 = Point(center.x+box.width/4, box.end_y, center.z+box.depth/4)
        corner2 = Point(center.x-box.width/4, box.end_y, center.z+box.depth/4)
        corner3 = Point(center.x+box.width/4, box.end_y, center.z-box.depth/4)
        corner4 = Point(center.x-box.width/4, box.end_y, center.z-box.depth/4)
        
        highest_point_below_center = self.get_highest_point_below(center)
        highest_point_below_corner1 = self.get_highest_point_below(corner1)
        highest_point_below_corner2 = self.get_highest_point_below(corner2)
        highest_point_below_corner3 = self.get_highest_point_below(corner3)
        highest_point_below_corner4 = self.get_highest_point_below(corner4)
                
        #si la boite située en dessous du centre de gravité est plus basse, rejeter 
        if (highest_point_below_center.y < box.end_y or highest_point_below_corner1.y < box.end_y or highest_point_below_corner2.y < box.end_y or highest_point_below_corner3.y < box.end_y or highest_point_below_corner4.y < box.end_y):

            #print("Box not fit because no stability")
            return False
            
        return True
    
    def check_box_stability_v2(self, box:Box) -> bool:
        center = Point(box.end_x + box.width/2, box.end_y, box.end_z + box.depth/2)
        corner1 = Point(box.end_x, box.end_y, box.end_z)
        corner2 = Point(box.end_x + box.width, box.end_y, box.end_z)
        corner3 = Point(box.end_x, box.end_y, box.end_z+box.depth)
        corner4 = Point(box.end_x + box.width, box.end_y, box.end_z + box.depth)
        
        highest_point_below_center = self.get_highest_point_below(center)
        highest_point_below_corner1 = self.get_highest_point_below(corner1)
        highest_point_below_corner2 = self.get_highest_point_below(corner2)
        highest_point_below_corner3 = self.get_highest_point_below(corner3)
        highest_point_below_corner4 = self.get_highest_point_below(corner4)
        
        total_points_with_empty_space_below = 0
        if highest_point_below_center.y < box.end_y:
            total_points_with_empty_space_below += 1
        if highest_point_below_corner1.y < box.end_y:
            total_points_with_empty_space_below += 1
        if highest_point_below_corner2.y < box.end_y:
            total_points_with_empty_space_below += 1
        if highest_point_below_corner3.y < box.end_y:
            total_points_with_empty_space_below += 1
        if highest_point_below_corner4.y < box.end_y:
            total_points_with_empty_space_below += 1

        if total_points_with_empty_space_below > 1:

            """
            print("\nbox dimension: ", box.get_dimensions(), "\nRejected because total_points_with_empty_space_below = ", total_points_with_empty_space_below, "\n At position: ", box.end_x, " ", box.end_y, " ", box.end_z)
            print("center: ", center, " highest_point_below_center: ", highest_point_below_center, " boxendX: ", box.end_x, " width: ", box.width)
            print("corner1: ", corner1, " highest_point_below_corner1: ", highest_point_below_corner1)
            print("corner2: ", corner2, " highest_point_below_corner2: ", highest_point_below_corner2)
            print("corner3: ", corner3, " highest_point_below_corner3: ", highest_point_below_corner3)
            print("corner4: ", corner4, " highest_point_below_corner4: ", highest_point_below_corner4)
            """

            return False
        return True

    def to_json(self) -> dict:
        #fonction utile uniquement pour le fichier setup.py
        dic = {}
        dic["boxes"] = []
        for i, box in enumerate(self.pallet.boxes):
            dic["boxes"].append(dict())
            dic["boxes"][i]["id"] = box.id
            dic["boxes"][i]["width"] = box.width
            dic["boxes"][i]["height"] = box.height
            dic["boxes"][i]["depth"] = box.depth
            dic["boxes"][i]["x"] = box.x
            dic["boxes"][i]["y"] = box.y
            dic["boxes"][i]["z"] = box.z

        dic["pallet"] = dict()
        dic["pallet"]["id"] = self.pallet.id
        dic["pallet"]["width"] = self.pallet.width
        dic["pallet"]["depth"] = self.pallet.depth
        dic["pallet"]["height"] = self.pallet.height
        dic["pallet"]["x"] = self.pallet.x
        dic["pallet"]["y"] = self.pallet.y
        dic["pallet"]["z"] = self.pallet.z

        return dic

    def get_score(self):
        """Le score est une fonction avec les parametres possibles suivants:
            - nombre de boxes sur une pallet
            - hauteur max de la pallet
            - espace rempli (pourcentage par rapport au total d'espace)
        """
        return self.get_filling_rate()

    def get_filling_rate(self):
        """Return la valeur relative de l'espace rempli par les boites par rapport à l'epace total possible"""
        current_fill = 0
        for box in self.newlyUnplacedBoxes:
            current_fill += box.get_volume()
        total_fill = self.pallet.get_volume()
        return current_fill/total_fill