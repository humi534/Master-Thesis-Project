
from distutils.command.config import config
import json 
from resources.Box import Box
from resources.Pallet import Pallet
from resources.Point import Point


def getConfigData():
    with open('config.json') as f:
        return json.load(f)

def getPlacedBoxes() -> list:
    configData = getConfigData()
    return configData["placedBoxes"]

def addUndeterminedBox(box:Box):
    configData = getConfigData()
    boxDict = box.__dict__
    configData["undeterminedBoxes"].append(boxDict)
    updateAllConfigFile(configData)
    
def updateAllConfigFile(newConfig: dict) -> None:
    with open('config.json', 'w') as outfile:
        json.dump(newConfig, outfile)

def getListOfPlacedBoxes():
    configData = getConfigData()
    listOfPlacedBoxes = []
    for boxDict in configData["placedBoxes"]:
        box = Box(boxDict=boxDict)
        listOfPlacedBoxes.append(box)
    return listOfPlacedBoxes

def getListOfUndeterminedBoxes():
    configData = getConfigData()
    listOfUndeterminedBoxes = []
    for boxDict in configData["undeterminedBoxes"]:
        box = Box(boxDict=boxDict)
        listOfUndeterminedBoxes.append(box)
    return listOfUndeterminedBoxes

def getListOfUnplacedBoxes() -> list:
    configData = getConfigData()
    listOfUnplacedBoxes = []
    for boxDict in configData["unplacedBoxes"]:
        box = Box(boxDict=boxDict)
        listOfUnplacedBoxes.append(box)
    return listOfUnplacedBoxes

def getListOfNoFitBoxes():
    configData = getConfigData()
    listOfNoFitBoxes = []
    for boxDict in configData["noFitBoxes"]:
        box = Box(boxDict=boxDict)
        listOfNoFitBoxes.append(box)
    return listOfNoFitBoxes

def getLowestUnplacedBox() -> Box:
    configData = getConfigData()
    listOfUnplacedBoxes = getListOfUnplacedBoxes()
    if len(listOfUnplacedBoxes) == 0:
        raise Exception("Pas de boites a placer")

    lowest_box = listOfUnplacedBoxes[0]
    for box in listOfUnplacedBoxes:
        if box.end_y < lowest_box.end_y:
            lowest_box = box
    return lowest_box

def getIndexDictInList(element:dict, dicts:list) -> int:
    return next((i for i, item in enumerate(dicts) if item == element), None)

def moveBoxFromUnplacedToPlaced(box:Box):
    
    #Move the box from unplacedBoxes to placedBoxes
    configData = getConfigData()
    boxToMoveIndex = getIndexDictInList(box.__dict__, configData["unplacedBoxes"])
    del(configData["unplacedBoxes"][boxToMoveIndex])
    configData["placedBoxes"].append(box.__dict__)
    updateAllConfigFile(configData)

def copySeveralBoxesFromUndeterminedToUnplaced(listOfBoxesToMove):
    configData = getConfigData()
    try: 
        #---------Ajouter les boites transférées à placedBoxes
        for boxToMove in listOfBoxesToMove:
            configData["unplacedBoxes"].append(boxToMove.__dict__)
        updateAllConfigFile(configData)

    except:
        raise Exception ("une erreur s'est produite")

def copySeveralBoxesFromUndeterminedToNoFit(listOfBoxesToMove):
    configData = getConfigData()
    try: 
        #---------Ajouter les boites transférées à placedBoxes
        for boxToMove in listOfBoxesToMove:
            configData["noFitBoxes"].append(boxToMove.__dict__)
        updateAllConfigFile(configData)

    except:
        raise Exception ("une erreur s'est produite")

def clearUndeterminedBoxes():
    configData = getConfigData()
    configData["undeterminedBoxes"].clear()
    updateAllConfigFile(configData)

def moveAllUndeterminedBoxesToNoFitBoxes():
    configData = getConfigData()
    listOfUnplacedBoxes = getListOfUndeterminedBoxes()
    listOfNoFitBoxes = getListOfNoFitBoxes()

    for box in listOfUnplacedBoxes:
        listOfNoFitBoxes.append(box)

    configData["undeterminedBoxes"].clear()
    for i in listOfNoFitBoxes:
        configData["noFitBoxes"].append(i.__dict__)
    updateAllConfigFile(configData)
    
def toString():
    return getConfigData()

def resetConfigFile():
    # placedBoxes = les boites qui ont été placées virtuellement et manuellement
    # unplacedBoxes = les boites qui ont été placées virtuellement
    # noFitBoxes = les boites pour lesquelles l'algorithme n'a pas trouvé de place virtuellement
    # underterminedBoxes = Les boites qui n'ont pas encore été placées virtuellement ni manuellement
    jsonString = '{"parameters": {"sortingAlgorithm": "volume"}, "currentBox":{}, "undeterminedBoxes":[], "placedBoxes": [], "unplacedBoxes": [], "noFitBoxes":[], "pallet": {}, "pivotPoints": []}'
    with open('config.json', 'w') as outfile:
        outfile.write(jsonString)

def addAllUndeterminedBoxes():
    
    addUndeterminedBox(Box(name="Tic Tac Boom", width=26,height=8,depth=26,start_x=-55, start_y=-65, start_z=130))
    addUndeterminedBox(Box(name="Talisman", width=30,height=7,depth=30,start_x=-84, start_y=-66, start_z=134))
    addUndeterminedBox(Box(name="Unlock", width=21,height=7,depth=27,start_x=-25, start_y=-68, start_z=160))
    addUndeterminedBox(Box(name="Peaky Blinder", width=14,height=4,depth=19,start_x=-27, start_y=-60, start_z=196))
    addUndeterminedBox(Box(name="Brainstorm", width=20,height=9,depth=27,start_x=-77, start_y=-66, start_z=193))
    addUndeterminedBox(Box(name="Les aventuriers du rail", width=30,height=7,depth=30,start_x=-82, start_y=-66, start_z=168))
    addUndeterminedBox(Box(name="Team UP!", width=13,height=24,depth=12,start_x=-10, start_y=-64, start_z=183))
    addUndeterminedBox(Box(name="Buzz it!", width=15,height=14,depth=8,start_x=-54, start_y=-68, start_z=164))
    addUndeterminedBox(Box(name="Taboo", width=20,height=7,depth=27,start_x=-49, start_y=-66, start_z=186))
    addUndeterminedBox(Box(name="Le routard", width=16,height=9,depth=15,start_x=-27, start_y=-66, start_z=181))
    addUndeterminedBox(Box(name="Timeline", width=30,height=7,depth=30,start_x=-26, start_y=-67, start_z=130))

    
    
    """
    addUndeterminedBox(Box(width=190,height=190,depth=190))
    addUndeterminedBox(Box(width=110,height=70,depth=80))
    addUndeterminedBox(Box(width=90,height=90,depth=90))
    addUndeterminedBox(Box(width=90,height=90,depth=90))
    addUndeterminedBox(Box(width=90,height=90,depth=90))
    addUndeterminedBox(Box(width=85,height=45,depth=45))
    addUndeterminedBox(Box(width=20,height=65,depth=70))
    addUndeterminedBox(Box(width=65,height=65,depth=70))
    addUndeterminedBox(Box(width=80,height=90,depth=40))
    addUndeterminedBox(Box(width=40,height=50,depth=40))
    addUndeterminedBox(Box(width=50,height=60,depth=70))
    addUndeterminedBox(Box(width=85,height=75,depth=40))
    addUndeterminedBox(Box(width=95,height=100,depth=80))
    addUndeterminedBox(Box(width=70,height=50,depth=80))
    addUndeterminedBox(Box(width=70,height=50,depth=80))
    addUndeterminedBox(Box(width=70,height=50,depth=80))
    addUndeterminedBox(Box(width=70,height=80,depth=70))
    addUndeterminedBox(Box(width=85,height=45,depth=45))
    addUndeterminedBox(Box(width=55,height=55,depth=55))
    addUndeterminedBox(Box(width=75,height=30,depth=40))
    addUndeterminedBox(Box(width=20,height=30,depth=40))
    addUndeterminedBox(Box(width=25,height=35,depth=35))
    addUndeterminedBox(Box(width=20,height=20,depth=20))
    addUndeterminedBox(Box(width=10,height=20,depth=20))
    addUndeterminedBox(Box(width=110,height=70,depth=80))
    addUndeterminedBox(Box(width=90,height=90,depth=90))
    addUndeterminedBox(Box(width=90,height=90,depth=90))
    addUndeterminedBox(Box(width=90,height=90,depth=90))
    addUndeterminedBox(Box(width=85,height=45,depth=45))
    addUndeterminedBox(Box(width=20,height=65,depth=70))
    addUndeterminedBox(Box(width=65,height=65,depth=70))
    addUndeterminedBox(Box(width=80,height=90,depth=40))
    addUndeterminedBox(Box(width=40,height=50,depth=40))
    addUndeterminedBox(Box(width=50,height=60,depth=70))
    addUndeterminedBox(Box(width=85,height=75,depth=40))
    addUndeterminedBox(Box(width=95,height=100,depth=80))
    addUndeterminedBox(Box(width=70,height=50,depth=80))
    addUndeterminedBox(Box(width=70,height=50,depth=80))
    addUndeterminedBox(Box(width=70,height=50,depth=80))
    addUndeterminedBox(Box(width=70,height=80,depth=70))
    addUndeterminedBox(Box(width=55,height=80,depth=60))
    addUndeterminedBox(Box(width=70,height=80,depth=70))
    addUndeterminedBox(Box(width=80,height=80,depth=80))
    addUndeterminedBox(Box(width=80,height=80,depth=80))
    addUndeterminedBox(Box(width=80,height=80,depth=80))
    """

def addPallet(pallet:Pallet):
    configData = getConfigData()
    palletDict = pallet.__dict__
    configData["pallet"] = (palletDict)
    updateAllConfigFile(configData)

def get_parameters():
    configData = getConfigData()
    return configData["parameters"]

def getPallet() -> Pallet:
    configData = getConfigData()
    return Pallet(palletDict=configData["pallet"])

def setFirstPivotPointBasedOnPalletPosition():
    configData = getConfigData()
    pallet = getPallet()
    configData["pivotPoints"].append({"x":pallet.x, "y":pallet.y, "z":pallet.z})
    updateAllConfigFile(configData)

def getAllPivotPoints() -> list:
    configData = getConfigData()
    listOfPoints = []
    for point in configData["pivotPoints"]:
        listOfPoints.append(Point(point["x"],point["y"], point["z"]))
    return listOfPoints

def setPivotPoints(listOfPoints):
    """Met a jour la liste des points pivots en ecrasant la precedente"""
    configData = getConfigData()
    configData["pivotPoints"].clear()

    for point in listOfPoints:
        configData["pivotPoints"].append(point.__dict__)

    updateAllConfigFile(configData)

def setCurrentBox(box: Box):
    configData = getConfigData()
    configData["currentBox"] = box.__dict__
    updateAllConfigFile(configData)

def getCurrentBox() -> Box:
    configData = getConfigData()
    return Box(boxDict = configData["currentBox"])

def clearCurrentBox():
    configData = getConfigData()
    configData["currentBox"] = {}
    updateAllConfigFile(configData)

def getPlacedBoxesFillingRate() -> float:
    """Renvoie le ratio de boites placées comparées aux boites pas encore placées"""
    configData = getConfigData()
    placedBoxesLength = len(configData["placedBoxes"])
    unplacedBoxesLength = len(configData["unplacedBoxes"])
    print("length placed boxes : ", placedBoxesLength)
    return round((placedBoxesLength/(placedBoxesLength+unplacedBoxesLength)),2)

def getCompletePalletFillingRate():
    """Renvoie le ratio d'espace rempli une fois toutes les boites posées sur la palette"""
    configData = getConfigData()
    totalSpaceBoxes = 0
    for unplacedBox in getListOfUnplacedBoxes():
        totalSpaceBoxes += unplacedBox.get_volume()

    for placedBox in getListOfPlacedBoxes():
        totalSpaceBoxes += placedBox.get_volume()

    totalSpacePallet = getPallet().get_volume()
    return round(totalSpaceBoxes/totalSpacePallet,3)

    