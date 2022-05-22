
import json 
from resources import Box, Pallet, Packer, Point
import json
import ManipConfigFile

"""
# Directly from dictionary
with open('json_data.json', 'w') as outfile:
    json.dump(json_string, outfile)
  
# Using a JSON string
with open('json_data.json', 'w') as outfile:
    outfile.write(json_string)



myBox1 = Box(20,10,20,50,10,30,10)
myBox1.set_end_position(50,80,70)
myBox2 = Box(20,10,20,50,10,30,10)
myBox2.set_end_position(50,100,70)
ManipConfigFile.addUnplacedBox(myBox1)
ManipConfigFile.addUnplacedBox(myBox2)
"""


ManipConfigFile.resetConfigFile()
#ManipConfigFile.addAllUndeterminedBoxes()
print(ManipConfigFile.toString())
myBox1 = Box(20,10,20,50,10,30,10)
myBox1.set_end_position(50,80,70)
myBox2 = Box(20,10,20,50,10,30,10)
myBox2.set_end_position(50,100,70)
ManipConfigFile.addUndeterminedBox(myBox1)
ManipConfigFile.addUndeterminedBox(myBox2)
listOfBoxes = []
listOfBoxes.append(myBox1)
listOfBoxes.append(myBox2)
ManipConfigFile.copySeveralBoxesFromUndeterminedToUnplaced(listOfBoxes)
ManipConfigFile.clearUndeterminedBoxes()
print("Après l'algo: ", ManipConfigFile.getConfigData())
print("-------------")
lowestBox = ManipConfigFile.getLowestUnplacedBox()
print("lowest Box: ", lowestBox.__dict__)
ManipConfigFile.setCurrentBox(lowestBox)
print("currentBox: ", ManipConfigFile.getCurrentBox().__dict__)
print("")
ManipConfigFile.moveBoxFromUnplacedToPlaced(lowestBox)
print(ManipConfigFile.getConfigData())

"""
ManipConfigFile.resetConfigFile()
ManipConfigFile.addPallet(Pallet(width=300,height=400, depth=300))
ManipConfigFile.setFirstPivotPointBasedOnPalletPosition()


print("Initialisation: ", ManipConfigFile.toString())

print('__________________________________________________________________')


ManipConfigFile.addAllUndeterminedBoxes()
packer = Packer()
packer.pack_boxes()
packer.update_config_file()
#ManipConfigFile.moveAllUnplacedBoxesToNoFitBoxes()  Normallement ne sert plus à rien

print('__________________________________________________________________')
print("final:", ManipConfigFile.toString())
"""

"""
class Student:
    def __init__(self, name, age) -> None:
        self.name = name
        self.age = age
    
    def __repr__(self) -> str:
        return self.name

s1 = Student("Hugo", 25)
s2 = Student("Guillaume",24)
s3 = Student("Hugo",25)

students = []
students.append(s1)
students.append(s2)
students.append(s3)
print(students)
newStudents = list(filter(lambda x: x.__dict__ != s1.__dict__, students))
print(newStudents)
"""

"""
print("_____________________")

print(ManipConfigFile.toString())

print("_________________________________________________")
lowestBox = ManipConfigFile.getLowestUnplacedBox()
lowestBoxDict = lowestBox.__dict__
print(lowestBoxDict)
"""
"""
ManipConfigFile.addAllUnplacedBoxes()
packer = Packer()
packer.pack_boxes()
print("ajout des deux boites dans unplaced ----------------------")
print(ManipConfigFile.toString())
print("--------------------------------")
lowestBox = ManipConfigFile.getLowestUnplacedBox()
lowestBoxDict = lowestBox.__dict__
print(lowestBoxDict)

ManipConfigFile.MoveBoxFromUnplacedToPlaced(lowestBox)
print(ManipConfigFile.toString())
"""

