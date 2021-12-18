# A script that verifies that all the sprite urls in the masterSpriteDex.json are still up.
import os
import requests
import sys
import commentjson as json

# URLs & Paths
root = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

# Constants for discerning the structure of the sprite indices
spriteBlocks = ["Default", "Egg", "Shadow"]
shinyBlocks = ["Regular", "Shiny"]
spriteTypes = ["Box", "Front", "Back"]

# Checks if a given image url exists
def exists(path):
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

# Open master-SpriteDex.json
try:
  spriteDex = json.load(open(os.path.join(root, "masterSpriteDex.json"), encoding="utf8"))
except:
  print("Malformed masterSpriteDex.json file.")
  input("Press enter to finish...")
  sys.exit()

# Check each species
count = 0
for species in spriteDex: # Run through each species in index
  if count % 50 == 0:
    print("Checking species {0}...".format(count))
  for form in spriteDex[species]["Forms"]: # Run through each form of the species
    checkSprites(spriteDex, species, form, None) # sprites for no appearance
    if "Appearance" in spriteDex[species]["Forms"][form]:
      for appearance in spriteDex[species]["Forms"][form]["Appearance"]:
        checkSprites(spriteDex, species, form, appearance) # sprites for each appearance
  count += 1

print(f"Finished checking all {0} species in the masterSpriteDex!".format(len(spriteDex)))
input("Press enter to finish...")