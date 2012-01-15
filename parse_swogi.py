# script to make the swogi spreadsheets into the json file we want.
import json
from collections import Counter

# Takes a dict (or Counter) and an int, returns a new dict with all
# the values multiplied by the int
def cmul(di, n):
    ret = type(di)(di)
    for k in ret.keys():
        ret[k] *= n
    return ret
Counter.__mul__ = cmul

id_to_card = {}
name_to_ids = {}
hikki_schema = ["id","name","kr_name","faction","episode","type","rarity",
        "life","size","limit","attack","defense","stamina","level","points",
        "ability"]

# hikki.txt is all of the columns from hikki's list of all cards.
for line in open("hikki.txt"):
    entries = zip(hikki_schema, [s.strip() for s in line.split('\t')])
    if len(entries) != len(hikki_schema):
        print "Failed to parse hikki line:\n%r"%line
        continue
    card = {"recipe": None, "location": None, "base_recipe": None}
    for k,v in entries:
        card[k]=v
    if len(card["episode"]) > 0 and card["episode"][0] != "E":
        card["episode"] = "EP"+card["episode"]
    id_to_card[card["id"]] = card
    if card["name"] not in name_to_ids:
        name_to_ids[card["name"]] = set()
    name_to_ids[card["name"]].add(card["id"])

# hikki_materials.txt is the materials section of hikki's spreadsheet.
for line in open("hikki_materials.txt"):
    entries = [s.strip() for s in line.split('\t')]
    idd = entries[0]
    loc = entries[-1]
    id_to_card[idd]["location"] = loc

idd = None
recipe = {}
n=0
# recipes.txt is nvm's list of recipes.
for line in open("recipes.txt"):
    entries = [s.strip() for s in line.split(' ')]
    if len(entries) == 1:
        if idd is not None:
            id_to_card[idd]["recipe"] = recipe
            id_to_card[idd]["base_recipe"] = Counter(recipe)
        idd = entries[0][1:]
        recipe = {}
    else:
        recipe[entries[0]] = int(entries[1][1:])
id_to_card[idd]["recipe"] = recipe

while True:
    changed = False
    for to_build in id_to_card.values():
        recipe = to_build["base_recipe"]
        if recipe is not None:
            for mat,count in recipe.items():
                sub_recipe = id_to_card[mat]["base_recipe"]
                if sub_recipe is not None:
                    changed = True
                    recipe += sub_recipe * count
                    print mat,count,sub_recipe
                    del recipe[mat]
        to_build["base_recipe"] = recipe
    if not changed:
        break

# cbt.txt is the first 4 columns of the CBT card list.
for line in open("cbt.txt"):
    line = [s.strip() for s in line.split('\t')]
    if len(line) != 4:
        print "Failed to parse cbt line:\n%r"%line
        continue
    name = line[0]
    id = line[-1]
    if name not in name_to_ids:
        name_to_ids[name] = set()
    name_to_ids[name].add(id)

for k,v in name_to_ids.iteritems():
    name_to_ids[k] = list(v)

out = open("swogi.json", "w")
out.write(json.dumps({"id_to_card":id_to_card, "name_to_ids":name_to_ids}))
out.close()
