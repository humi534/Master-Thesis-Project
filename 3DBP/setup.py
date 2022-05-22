# -*- coding: utf-8 -*-
"""
Created on Wed Aug 25 12:37:34 2021

@author: hugop
"""

from resources import Box, Pallet, Packer
import json

packer = Packer("volume")
packer.add_pallet(Pallet(width=300,height=400, depth=300))
packer.add_box(Box(width=190,height=190,depth=190))
packer.add_box(Box(width=110,height=70,depth=80))
packer.add_box(Box(width=90,height=90,depth=90))
packer.add_box(Box(width=90,height=90,depth=90))
packer.add_box(Box(width=90,height=90,depth=90))
packer.add_box(Box(width=85,height=45,depth=45))
packer.add_box(Box(width=20,height=65,depth=70))
packer.add_box(Box(width=65,height=65,depth=70))
packer.add_box(Box(width=80,height=90,depth=40))
packer.add_box(Box(width=40,height=50,depth=40))
packer.add_box(Box(width=50,height=60,depth=70))
packer.add_box(Box(width=85,height=75,depth=40))
packer.add_box(Box(width=95,height=100,depth=80))
packer.add_box(Box(width=70,height=50,depth=80))
packer.add_box(Box(width=70,height=50,depth=80))
packer.add_box(Box(width=70,height=50,depth=80))
packer.add_box(Box(width=70,height=80,depth=70))
packer.add_box(Box(width=85,height=45,depth=45))
packer.add_box(Box(width=55,height=55,depth=55))
packer.add_box(Box(width=75,height=30,depth=40))
packer.add_box(Box(width=20,height=30,depth=40))
packer.add_box(Box(width=25,height=35,depth=35))
packer.add_box(Box(width=20,height=20,depth=20))
packer.add_box(Box(width=10,height=20,depth=20))
packer.add_box(Box(width=110,height=70,depth=80))
packer.add_box(Box(width=90,height=90,depth=90))
packer.add_box(Box(width=90,height=90,depth=90))
packer.add_box(Box(width=90,height=90,depth=90))
packer.add_box(Box(width=85,height=45,depth=45))
packer.add_box(Box(width=20,height=65,depth=70))
packer.add_box(Box(width=65,height=65,depth=70))
packer.add_box(Box(width=80,height=90,depth=40))
packer.add_box(Box(width=40,height=50,depth=40))
packer.add_box(Box(width=50,height=60,depth=70))
packer.add_box(Box(width=85,height=75,depth=40))
packer.add_box(Box(width=95,height=100,depth=80))
packer.add_box(Box(width=70,height=50,depth=80))
packer.add_box(Box(width=70,height=50,depth=80))
packer.add_box(Box(width=70,height=50,depth=80))
packer.add_box(Box(width=70,height=80,depth=70))
packer.add_box(Box(width=55,height=80,depth=60))
packer.add_box(Box(width=70,height=80,depth=70))
packer.add_box(Box(width=80,height=80,depth=80))
packer.add_box(Box(width=80,height=80,depth=80))
packer.add_box(Box(width=80,height=80,depth=80))


packer.pack_boxes()
packer.print_state()
data = packer.to_json()

with open("../../../memoire/3DBP/Assets/boxes.json", "w") as jsonFile:
    json.dump(data, jsonFile)
    jsonFile.truncate() #si la nouvelle version est plus courte

