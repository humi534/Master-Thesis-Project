
from pymongo import MongoClient
import pprint

client = MongoClient("mongodb://localhost:27017/")
db = client["MasterThesisDatabase"]
collection = db["MasterThesisCollection"]

def saveToMongo(collectionName, data):
    client = MongoClient('localhost', 27017)
    db = client['MasterThesisDatabase']
    collection = db[collectionName]
    collection.insert_one(data)


def resetCollection(collectionName):
    startingDict = {"parameters": {"sortingAlgorithm": "volume"}, "currentBox":{}, "undeterminedBoxes":[], "placedBoxes": [], "unplacedBoxes": [], "noFitBoxes":[], "pallet": {}, "pivotPoints": []}

    print("Datapoint to insert : ")
    pprint.pprint(startingDict)
    saveToMongo(collectionName, startingDict)

resetCollection("MasterThesisCollection")

"""
#Get one datapoint back
print("Datapoint in collection : ")
pprint.pprint(collection.find_one())

#See all collections
print("collections : ",db.list_collection_names())
"""
