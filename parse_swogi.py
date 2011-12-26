# script to make the swogi spreadsheets into the json file we want.
import json

id_to_card = {}
name_to_ids = {}
hikki_schema = ["id","name","kr_name","faction","episode","type","rarity",
        "life","size","limit","attack","defense","stamina","level","points",
        "ability"]
# hikki.txt is all of the columns from all of hikki's card lists.
for line in open("hikki.txt"):
    entries = zip(hikki_schema, [s.strip() for s in line.split('\t')])
    if len(entries) != len(hikki_schema):
        print "Failed to parse hikki line:\n%r"%line
        continue
    card = {}
    for k,v in entries:
        card[k]=v
    if len(card["episode"]) > 0 and card["episode"][0] != "E":
        card["episode"] = "EP"+card["episode"]
    id_to_card[card["id"]] = card
    if card["name"] not in name_to_ids:
        name_to_ids[card["name"]] = set()
    name_to_ids[card["name"]].add(card["id"])

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
