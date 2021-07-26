# A python script that verifies all the sprite urls are still up
# for each sprite index mentioned in the sprite-indices.json file
# NOTE: Sprite indices not encoded in UTF-8 may not be read correctly. Comments are fine

import os
import requests
import sys
import urllib.request
import commentjson as json

## online mode?
onlineMode = input("Enter 'y' for online only mode...")
if onlineMode.lower() == "y":
    onlineMode = True
else:
    onlineMode = False

# URLs & Paths
baseURL = "https://raw.githubusercontent.com/project-pku/pkuSprite/main/"
repo_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

# Constants for discerning the structure of the sprite indices
spriteBlocks = ["Default", "Egg", "Shadow"]
shinyBlocks = ["Regular", "Shiny"]
spriteTypes = ["Box", "Front", "Back"]

# Checks if a given image url exists
def exists(path):
    if(not onlineMode and path[0:len(baseURL)] == baseURL): #if this is a local image and in local mode
        return os.path.isfile(os.path.join(repo_root, path[len(baseURL):]))
    try:
        r = requests.head(path, timeout=5)
        return r.status_code == requests.codes.ok
    except requests.exceptions.ConnectionError:
        return False

# Print errors regarding the given sprite (i.e. missing URL, invalid URL, missing Author)
def check_sprite(index, species, form, appearance, spriteBlock, shinyBlock, isFemale, spriteType):
    block = index[species]["Forms"][form] #find form
    if appearance is not None: #find appearance if it exists
        block = block["Appearance"][appearance]
    block = block["Sprites"][spriteBlock][shinyBlock]
    if isFemale: #get female sprite
        block = block["Female"]
    block = block[spriteType]

    femString = "Female/" if isFemale else ""
    appString = f"{appearance}/" if appearance is not None else ""

    if "URL" not in block:
        print(f"Missing URL at: {species}/{form}/{appString}{spriteBlock}/{shinyBlock}/{femString}{spriteType}")
    elif(not exists(block["URL"])):
            print(f"Broken URL at: {species}/{form}/{appString}{spriteBlock}/{shinyBlock}/{femString}{spriteType}")

    if "Author" not in block:
        print(f"Missing Author at: {species}/{form}/{appString}{spriteBlock}/{shinyBlock}/{femString}{spriteType}")

def checkSprites(index, species, form, appearance):
    block = index[species]["Forms"][form]
    if appearance is not None: #find appearance if it exists
        block = block["Appearance"][appearance]
    for spriteBlock in block["Sprites"]: # Run through each sprite block in this form (i.e. Regular, Egg, Shadow)
        if spriteBlock in spriteBlocks: # If this is a recognized sprite block, continue the check, else ignore
            for shinyBlock in block["Sprites"][spriteBlock]:
                if shinyBlock in shinyBlocks: # Run through each shiny block type (i.e. Regular, Shiny)
                    for spriteType in block["Sprites"][spriteBlock][shinyBlock]: # run through each spriteType in the shinyBlock (and Female block if it exists)
                        if spriteType in spriteTypes: # If this is a recognized spriteType, check if it's a valid url
                            check_sprite(index, species, form, appearance, spriteBlock, shinyBlock, False, spriteType)
                        elif spriteType == "Female":
                            for spriteType in block["Sprites"][spriteBlock][shinyBlock]["Female"]: # run through each spriteType in the female block
                                if spriteType in spriteTypes: # If this is a recognized spriteType, check if it's a valid url
                                    check_sprite(index, species, form, appearance, spriteBlock, shinyBlock, True, spriteType)

# ----------------
## Begin Script
# ----------------

# Open sprite-indices.json
if onlineMode:
    try:
        with urllib.request.urlopen(baseURL + 'sprite-indices.json') as url:
            indices = json.loads(url.read().decode())
    except:
        print(f"The sprite-indices.json URL is invalid...")
        input("Press enter to finish...")
        sys.exit()
else:
    path_to_json = os.path.join(repo_root, 'sprite-indices.json')
    try:
        indices_file = open(path_to_json)
        indices = json.load(indices_file)
    except:
        print("Malformed sprite-indices.json file.")
        input("Press enter to finish...")
        sys.exit()


# Run through each sprite index
for indexName in indices:
    # Open index.json
    if (not onlineMode) and indices[indexName][0:len(baseURL)] == baseURL: #if this is a local index and in local mode
        path_to_json = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, indices[indexName][len(baseURL):])
        index_file = open(path_to_json)
    else:
        try:
            with urllib.request.urlopen(indices[indexName]) as url:
                index_file = url.read().decode()
        except:
            print(f"The {indexName} sprite index's URL is invalid...")
            continue
    
    # Read through index json
    try:
        index = json.loads(index_file) if isinstance(index_file, str) else json.load(index_file)

        print(f"Checking: {indexName}...")
        for species in index: # Run through each species in index
            for form in index[species]["Forms"]: # Run through each form of the species
                checkSprites(index, species, form, None) # sprites for no appearance
                if "Appearance" in index[species]["Forms"][form]:
                    for appearance in index[species]["Forms"][form]["Appearance"]:
                        checkSprites(index, species, form, appearance) # sprites for each appearance

        # close index file if possible
        try:
            index_file.close()
        except:
            pass
        print(f"Finished checking: {indexName}")
    except:
        print(f"Malformed {indexName} sprite index.")

# close indices file if possible
try:
    indices_file.close()
except:
        pass

print(f"Finished checking all indices!")
input("Press enter to finish...")