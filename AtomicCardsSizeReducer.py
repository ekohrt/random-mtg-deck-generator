# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 18:29:46 2021

@author: ekohrt

AtomicCards.json from the MTGJson project is too big to put on github.
It also has a lot of unnecessary data in it. 
This code creates a new smaller file with just the important information.

"""

import json

with open('AtomicCards.json', encoding='utf-8') as json_file:
    cards_dict = json.load(json_file)

# a lot of attributes are not necessary
attributesToSkip = {'edhrecRank', 'foreignData', 'hand', 'isReserved', 'leadershipSkills',
                    'life', 'purchaseUrls', 'rulings', }

newJsonObject = {'data': {}}
for card in cards_dict['data'].keys():
    cardEntry = cards_dict['data'][card]
    # cards can have multiple faces, with different attributes
    newFaces = []
    for idx, face in enumerate(cardEntry):
        faceData = {}
        
        # add all attributes to the new file, escept the ones we want to skip
        for attr in cards_dict['data'][card][idx].keys():
            if attr not in attributesToSkip:
                faceData[attr] = cards_dict['data'][card][idx][attr]
        newFaces.append(faceData)
        
    newJsonObject['data'][card] = newFaces

#Convert dict back to json format and write to the file
jsonString = json.dumps(newJsonObject, indent=4, sort_keys=True)
with open("AtomicCards_Small.json", 'w') as fp:
        json.dump(newJsonObject, fp)
        
print(jsonString[:10000])
print("File 'AtomicCards_Small.json' created.")