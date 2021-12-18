# A script that compiles the entries of sprite-indices.json into a masterSpriteDex.json
import commentjson
import os

# custom to_json method
def to_json(o, level=0):
  INDENT = 2
  SPACE = " "
  NEWLINE = "\n"
  ret = ""
  if isinstance(o, dict):
    ret += "{" + NEWLINE
    comma = ""
    for k, v in o.items():
      ret += comma
      comma = ",\n"
      ret += SPACE * INDENT * (level + 1)
      ret += '"' + str(k) + '":' + SPACE
      ret += to_json(v, level + 1)
    ret += NEWLINE + SPACE * INDENT * level + "}"
  elif isinstance(o, str):
    if(o == "\u0000"): # properly escape null terminator
      ret += '"\\u0000"'
    else:
      ret += '"' + o + '"'
  elif isinstance(o, list):
    ret += "[" + ", ".join([to_json(e, level + 1) for e in o]) + "]"
  # Tuples are interpreted as lists
  elif isinstance(o, tuple):
    ret += "[" + ", ".join(to_json(e, level + 1) for e in o) + "]"
  elif isinstance(o, bool):
    ret += "true" if o else "false"
  elif isinstance(o, int):
    ret += str(o)
  elif isinstance(o, float):
    ret += '%.7g' % o
  elif o is None:
    ret += 'null'
  else:
    raise TypeError("Unknown type '%s' for json serialization" % str(type(o)))
  return ret

# Merges two dictionaries in-place. Treats lists as sets and unions them.
def merge_dicts(base, new):
  for k, v in new.items():
    if k in base and type(base[k]) is not type(v):
      raise Exception("Datadex type mismatch")
    if type(v) is list and k in base:
      base[k].extend(x for x in v if x not in base[k])
    elif type(v) is dict and k in base:
      merge_dicts(base[k], v)
    else:
      base[k] = v

# ----------------
## Begin Script
# ----------------

# initialize
root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
spriteindices = commentjson.load(open(os.path.join(root, "sprite-indices.json"), encoding="utf8"))

# merge sprite-indices
first = True
base = None
for index in spriteindices:
  sdex = commentjson.load(open(os.path.join(root, spriteindices[index]), encoding="utf8"))
  if first:
    base = sdex
    first = False
  else:
    merge_dicts(base, sdex)

# merging complete, write file
with open(os.path.join(root, 'masterSpriteDex.json'), 'w', encoding='utf-8') as f:
  f.write(to_json(base))

print("\nFinished compiling the masterSpriteDex!")
input("Press enter to finish...")