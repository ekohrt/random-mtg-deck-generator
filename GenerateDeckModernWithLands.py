# -*- coding: utf-8 -*-
"""
Generates a Modern-legal deck with: 
    - 1, 2, or 3 colors
    - appropriate distribution of basic lands (based on mana symbols)
    - cards are still chosen randomly (from Modern-legal sets)
    - default 24 basic lands
    
    Future considerations:
    - appropriate number of basic lands (based on avg cmc) (make a graph by plotting existing decks)
    - playsets instead of 1-of-each (default 4 or some way to tell?)
    - mana curve (math)
    - non-basic lands
    - synergy of some kind
Created on Fri Nov 27 17:05:19 2020
@author: ekohrt

"""
import random
import json
import sys

#Load json file of all cards into a dictionary
with open('AtomicCards_Small.json', encoding="utf8") as f:
    cards_dict = json.load(f)





"""
input a number of colors to put in deck
@param numColors is an int between 0 and 5, for how many colors the deck should be
"""
def generate_modern_deck(numColors):
    finalDeckList = []
    
    #get some colors
    allowed_colors = get_n_rand_colors(numColors)
    
    #get dict of card names
    card_names = cards_dict["data"]
    
    #loop over all cards and pick 36
    while len(finalDeckList) < 36:
        #choose any random card in all of mtg
        cardName = random.choice(list(card_names))
        #check that the card is modern and right color
        if (is_modern(cardName) and is_allowed_color(cardName, allowed_colors)):
            finalDeckList.append( cardName )
    
    #add 24 basic lands, in the right ratio of colors
    lands_to_add = add_basic_lands(finalDeckList, allowed_colors)
    
    #convert deck list to string
    deckListString = "\n".join("1 " + str(card) for card in finalDeckList) 
    for lands in lands_to_add:
        deckListString += "\n" + lands
    
    return deckListString


"""
Adds the right ratio of basic lands to a given deck
@param deckList is a list of card names that make up a deck
@param colorsList is a list of colors to use (ex. ["R", "G", "W"])
"""
def add_basic_lands(deckList, colorsList):
    lands_to_add = []
    
    #count up mana symbols
    sym_counts = count_mana_symbols(deckList)
    total = sum(sym_counts.values())
    
    #calculate ratios of each color in the deck
    color_ratios = {}
    for sym in sym_counts:
        color_ratios[sym] = sym_counts[sym]/total
    
    #determine how many of each basic lands (guarantee at least 1 of each)
    totalLands = 24
    lands = totalLands - len(colorsList)
    land_counts = {}
    for color in color_ratios:
        land_counts[color] = int(round(lands*color_ratios[color]))
        if (color_ratios[color] != 0): land_counts[color] += 1  #at least 1 of each
        
    #add lands to the decklist and return it
    landNames = {"R": "Mountain", "G": "Forest", "B": "Swamp", "U": "Island", "W": "Plains", "C": "Wastes"}
    for land in land_counts:
        if land_counts[land] > 0:
            lands_to_add.append(str(land_counts[land]) + " " + landNames[land])
            
    return lands_to_add


"""
counts the number of each mana symbol in a given decklist (of string cardNames)
"""
def count_mana_symbols(deckList):
    #count up each mana symbol in the deck and divide by total
    symbols = ['R', 'B', 'G', 'U', 'W', 'C']
    symbolCounts = {"R":0, "B":0, "G":0, "U":0, "W":0, "C":0}
    
    for cardName in deckList:
        if "manaCost" in cards_dict["data"][cardName][0]:
            cmc = cards_dict["data"][cardName][0]["manaCost"]
            for sym in symbols:
                symbolCounts[sym] += cmc.count(sym)
    return symbolCounts


"""
Returns true if the card is "Legal" in modern (not banned/restricted)
"""
def is_modern(cardName):
    #get dict of card's legalities
    #ex. "Sol Ring": {'commander': 'Legal', 'duel': 'Banned', 'legacy': 'Banned', 'vintage': 'Restricted'}
    #ex. "Ancient Den": {'commander': 'Legal', 'duel': 'Legal', 'legacy': 'Legal', 'modern': 'Banned', 'pauper': 'Legal', 'vintage': 'Legal'}
    legalities_dict = cards_dict["data"][cardName][0]["legalities"]
    
    #this dict must a) contain the key "modern", and also b) have "Legal" as value
    return "modern" in legalities_dict.keys() and legalities_dict["modern"] == "Legal"


"""
Returns true if the given card is one of the allowed colors
@param cardName is the String name of a card
@param allowedColorsList is a list of allowed colors (ex. ["R","B","G"])
"""
def is_allowed_color(cardName, allowedColorsList):
    #use the property "colorIdentity" (array of "B","G","U","W","R" or empty) (no "C" for eldrazi colorless)
    #maybe also use "manaCost" (ex. "{3}{W}{W}") (includes "C" for eldrazi colorless mana)
    colorId = cards_dict["data"][cardName][0]["colorIdentity"]
    
    #check that each color in card's color ID are allowed
    for color in colorId:
        if color not in allowedColorsList:
            return False
    return True


"""
returns a list of n random colors (max 5). Options: R,B,G,U,W.
"""
def get_n_rand_colors(n):
    if (n > 5): sys.exit("Error in get_n_rand_colors: n must be less than 5: n=" + n)
    return random.sample(["R", "B", "G", "U", "W"], n)


"""
returns a property of a given card 
(for all properties see: https://mtgjson.com/data-models/card-atomic/)
"""
def get_property(cardName, prop):
    if prop in cards_dict["data"][cardName][0]:
        return cards_dict["data"][cardName][0][prop]
    else: 
        return None


def main():
    print(generate_modern_deck(2))
    

if __name__ == "__main__":
    main()