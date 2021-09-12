#import logging
#from uuid import uuid4
import requests
import json
from pymongo import MongoClient
from pprint import pprint
from blacklist import get_blacklist
import datetime

mongo_client = MongoClient("mongodb+srv://lunarwhale:dD87Jhy@cluster0.xryw5.mongodb.net/")
db = mongo_client.api
serverStatusResult=db.command("serverStatus")
pprint(serverStatusResult)

db_names_before_drop = mongo_client.database_names()
print("db count:", len(db_names_before_drop))
print("Names of databases\n", db_names_before_drop)
col_list = db.list_collection_names()
print ("collections:", col_list)

api = "http://api.vulcanforged.com/getAllArts"
r = requests.get(api)
data = json.loads(r.text)
rlist = data['data']
print("Tokens: ", len(rlist))
blacklist = get_blacklist()
print("Blacklist: ", len(blacklist))
for a in blacklist:
    for token in rlist:
        if a == token['id']:
            rlist.remove(token)
print("Updated Tokens: ", len(rlist))
print("Converting List")
tokens = []
for a in rlist:
    data = json.loads(a['ipfs_data_json'])
    a['ipfs_data_json'] = data
    tokens.append(a)
print("New list: ", len(tokens))
print("Dropping tokens collection")
#mongo_client.drop_database('api')
db.tokens.drop()
col_list = db.list_collection_names()
print ("collections:", col_list)
print("Uploading List")
db.tokens.insert_many(tokens)
total_count = db.tokens.count_documents({})
print("Total number of documents : ", total_count)
print("Find token #2")
pprint(db.tokens.find_one({"id": 2}))
db.tokens.drop_indexes()

vulcanites = ['Tomyios', 'Aelio', 'Thunder', 'Kopis', 'Asterion',
    'Phearei', 'Alpha', 'Soter', 'Velosina', 'Chiron', 'Venomtail',
    'Syna', 'Chthonius', 'Nemean', 'Numatox', 'Wolfshadow', 'Trapjaw',
    'Medusa', 'Lost Shade', 'Blubberjaw', 'Charon']

vulcaniteslist = []
print("Make vulcanites list ", len(vulcanites))
for a in vulcanites:
    s = f"^{a}$"
    s2 = f" ^{a}$"
    s3 = f"^{a}$ "
    tfields = {"$or": [
        {"ipfs_data_json.Title": {"$regex": s, "$options": "i"}},
        {"ipfs_data_json.title": {"$regex": s, "$options": "i"}},
        {"ipfs_data_json.Name": {"$regex": s, "$options": "i"}},
        {"ipfs_data_json.name": {"$regex": s, "$options": "i"}},
        {"ipfs_data_json.Title": {"$regex": s2, "$options": "i"}},
        {"ipfs_data_json.title": {"$regex": s2, "$options": "i"}},
        {"ipfs_data_json.Name": {"$regex": s2, "$options": "i"}},
        {"ipfs_data_json.name": {"$regex": s2, "$options": "i"}},
        {"ipfs_data_json.Title": {"$regex": s3, "$options": "i"}},
        {"ipfs_data_json.title": {"$regex": s3, "$options": "i"}},
        {"ipfs_data_json.Name": {"$regex": s3, "$options": "i"}},
        {"ipfs_data_json.name": {"$regex": s3, "$options": "i"}}
        ]}
    dappfield = {"$or": [
        {"ipfs_data_json.dappid": int(3)},
        {"ipfs_data_json.dappid": str(3)}
        ]}
    r = db.tokens.find({"$and": [tfields, dappfield]}, {"_id": 0}).sort("id").limit(1)
#    print(f"count {a}: ", len(r))
    for z in r:
        b = z['id']
    c = z['ipfs_data_json']
    url = a.replace(" ", "+")
    vulcaniteslist.append({'id': b, 'Title': a, 'image': c['image'], 'url': url})
print("vulcanites upload")
db.vulcanites.drop()
db.vulcanites.insert_many(vulcaniteslist)

gods = ['Zeus', 'Poseidon', 'Ares', 'Hermes', 'Apollo',
    'Aphrodite', 'Hera', 'Demeter', 'Cronus', 'Hyperion', 'Coeus',
    'Crius', 'Iapetus', 'Oceanus', 'Rhea', 'Tethys', 'Dionysus']

godslist = []
print("Make gods list ", len(gods))
for a in gods:
    s = f"^{a}$"
    s2 = f" ^{a}$"
    s3 = f"^{a}$ "
    tfields = {"$or": [
        {"ipfs_data_json.Title": {"$regex": s, "$options": "i"}},
        {"ipfs_data_json.title": {"$regex": s, "$options": "i"}},
        {"ipfs_data_json.Name": {"$regex": s, "$options": "i"}},
        {"ipfs_data_json.name": {"$regex": s, "$options": "i"}},
        {"ipfs_data_json.Title": {"$regex": s2, "$options": "i"}},
        {"ipfs_data_json.title": {"$regex": s2, "$options": "i"}},
        {"ipfs_data_json.Name": {"$regex": s2, "$options": "i"}},
        {"ipfs_data_json.name": {"$regex": s2, "$options": "i"}},
        {"ipfs_data_json.Title": {"$regex": s3, "$options": "i"}},
        {"ipfs_data_json.title": {"$regex": s3, "$options": "i"}},
        {"ipfs_data_json.Name": {"$regex": s3, "$options": "i"}},
        {"ipfs_data_json.name": {"$regex": s3, "$options": "i"}}
        ]}
    dappfield = {"$or": [
        {"ipfs_data_json.dappid": int(8)},
        {"ipfs_data_json.dappid": str(8)}
        ]}
    r = db.tokens.find({"$and": [tfields, dappfield]}, {"_id": 0}).sort("id").limit(1)
    for z in r:
        b = z['id']
    c = z['ipfs_data_json']
    godslist.append({'id': b, 'Title': a, 'image': c['image']})
print("gods upload")
db.gods.drop()
db.gods.insert_many(godslist)

berserk = ['Sunfire Strike', 'Velosina of the Sacred Stables',
    'Gift of the Great Green Ones', 'Snares of the Fae', 'Stranglevines',
    'Summer Palace', 'Pipes of Pan', 'Centaur Warband', 'Summer Storms',
    'Bushwhack Wolf', 'The Fortress of Winds', 'The Breath of Boreas',
    "Hippolyta's Bow", 'Panoply of Minos', 'Hilltop Fort of the Amazons',
    'Claws of the Harpy', 'Cantankerous Mammoth', 'Sudden Snowdrifts',
    'Rip and Rend', 'Cyclops Rock Rain', 'Edge of Night', 'Cerberus',
    'Hound of Hades', 'Funeral Barge of Acheron', 'A Storm of Strix',
    'The Hymn of Thanatos', 'A Mustering of Souls', 'Sepurchral Armour',
    'Javelins of Thanatos', 'Trapjaw', 'Shade Warrior',
    'Blood of the Cockatrice', 'Myrmidon Warrior', 'Shield of Achilles',
    'The Spear of Achilles', 'Sandstorm', 'Scorpion Stance',
    'Venomtail', 'Desert Winds', 'Storm Surge', 'The Ones Who Drink']

berserklist = []
print("Make berserk list ", len(berserk))
for a in berserk:
    s = f"^{a}$"
    s2 = f" ^{a}$"
    s3 = f"^{a}$ "
    tfields = {"$or": [
        {"ipfs_data_json.Title": {"$regex": s, "$options": "i"}},
        {"ipfs_data_json.title": {"$regex": s, "$options": "i"}},
        {"ipfs_data_json.Name": {"$regex": s, "$options": "i"}},
        {"ipfs_data_json.name": {"$regex": s, "$options": "i"}},
        {"ipfs_data_json.Title": {"$regex": s2, "$options": "i"}},
        {"ipfs_data_json.title": {"$regex": s2, "$options": "i"}},
        {"ipfs_data_json.Name": {"$regex": s2, "$options": "i"}},
        {"ipfs_data_json.name": {"$regex": s2, "$options": "i"}},
        {"ipfs_data_json.Title": {"$regex": s3, "$options": "i"}},
        {"ipfs_data_json.title": {"$regex": s3, "$options": "i"}},
        {"ipfs_data_json.Name": {"$regex": s3, "$options": "i"}},
        {"ipfs_data_json.name": {"$regex": s3, "$options": "i"}}
        ]}
    dappfield = {"$or": [
        {"ipfs_data_json.dappid": int(11)},
        {"ipfs_data_json.dappid": str(11)}
        ]}
    r = db.tokens.find({"$and": [tfields, dappfield]}, {"_id": 0}).sort("id").limit(1)
    for z in r:
        b = z['id']
    c = z['ipfs_data_json']
    url = a.replace(" ", "+")
    berserklist.append({'id': b, 'Title': a, 'image': c['image'], 'url': url})
print("berserk upload")
db.berserk.drop()
db.berserk.insert_many(berserklist)

coddlepets = ['Oversizedhat', 'Kaida', 'Iseran',
    'Wyvernie', 'Mergess', 'Lavender', 'Spudfire', 'Skandy', 'Bleu',
    'Khione', 'Zeekeez', 'Ash', 'Jade', 'Aquadra', 'Ember', 'Comet',
    'Eira', 'Podgy', 'Lotus', 'Chase', 'Farasha', 'Aye-aye', 'Salana',
    'Fleta', 'Yukio', 'Augino OG', 'Pink Juni Leaf', 'Blue Juni Leaf']

coddlepetslist = []
print("Make coddlepets list ", len(coddlepets))
for a in coddlepets:
    s = f"^{a}$"
    s2 = f" ^{a}$"
    s3 = f"^{a}$ "
    tfields = {"$or": [
        {"ipfs_data_json.Title": {"$regex": s, "$options": "i"}},
        {"ipfs_data_json.title": {"$regex": s, "$options": "i"}},
        {"ipfs_data_json.Name": {"$regex": s, "$options": "i"}},
        {"ipfs_data_json.name": {"$regex": s, "$options": "i"}},
        {"ipfs_data_json.Title": {"$regex": s2, "$options": "i"}},
        {"ipfs_data_json.title": {"$regex": s2, "$options": "i"}},
        {"ipfs_data_json.Name": {"$regex": s2, "$options": "i"}},
        {"ipfs_data_json.name": {"$regex": s2, "$options": "i"}},
        {"ipfs_data_json.Title": {"$regex": s3, "$options": "i"}},
        {"ipfs_data_json.title": {"$regex": s3, "$options": "i"}},
        {"ipfs_data_json.Name": {"$regex": s3, "$options": "i"}},
        {"ipfs_data_json.name": {"$regex": s3, "$options": "i"}}
        ]}
    dappfield = {"$or": [
        {"ipfs_data_json.dappid": int(7)},
        {"ipfs_data_json.dappid": str(7)}
        ]}
    r = db.tokens.find({"$and": [tfields, dappfield]}, {"_id": 0}).sort("id").limit(1)
    for z in r:
        b = z['id']
    c = z['ipfs_data_json']
    url = a.replace(" ", "+")
    coddlepetslist.append({'id': b, 'Title': a, 'image': c['image'], 'url': url})
print("coddlepets upload")
db.coddlepets.drop()
db.coddlepets.insert_many(coddlepetslist)

featured = ['The Death Dealer', 'Helm of the Death Dealer',
    'Sword of the Death Dealer', 'Shield of the Death Dealer']

featuredlist = []
print("Make featured list ", len(featured))
for a in featured:
    s = f"^{a}$"
    s2 = f" ^{a}$"
    s3 = f"^{a}$ "
    tfields = {"$or": [
        {"ipfs_data_json.Title": {"$regex": s, "$options": "i"}},
        {"ipfs_data_json.title": {"$regex": s, "$options": "i"}},
        {"ipfs_data_json.Name": {"$regex": s, "$options": "i"}},
        {"ipfs_data_json.name": {"$regex": s, "$options": "i"}},
        {"ipfs_data_json.Title": {"$regex": s2, "$options": "i"}},
        {"ipfs_data_json.title": {"$regex": s2, "$options": "i"}},
        {"ipfs_data_json.Name": {"$regex": s2, "$options": "i"}},
        {"ipfs_data_json.name": {"$regex": s2, "$options": "i"}},
        {"ipfs_data_json.Title": {"$regex": s3, "$options": "i"}},
        {"ipfs_data_json.title": {"$regex": s3, "$options": "i"}},
        {"ipfs_data_json.Name": {"$regex": s3, "$options": "i"}},
        {"ipfs_data_json.name": {"$regex": s3, "$options": "i"}}
        ]}
    r = db.tokens.find(tfields, {"_id": 0}).sort("id")
    b = r[0]
    c = b['ipfs_data_json']
    url = a.replace(" ", "+")
    featuredlist.append({'id': b['id'], 'Title': a, 'image': c['image'], 'url': url})
print("featured upload")
db.featured.drop()
db.featured.insert_many(featuredlist)

print("Making recent list")
r = db.tokens.find({}, {"_id": 0}).sort("id", -1).limit(12)
rlist = []
for a in r:
    b = a['ipfs_data_json']
    rlist.append({'id': a['id'], 'image': b['image']})
print("recent list upload")
db.recent.drop()
db.recent.insert_many(rlist)

print("Making recentlong list")
r = db.tokens.find({}, {"_id": 0}).sort("id", -1).limit(60)
rlist = []
for a in r:
    b = a['ipfs_data_json']
    rlist.append({'id': a['id'], 'image': b['image']})
print("recentlong list upload")
db.recentlong.drop()
db.recentlong.insert_many(rlist)

print("Making database stats")
stats = {}
count = db.tokens.find({}).count()
r = db.tokens.find({})
owners = []
for a in r:
    owners.append(a['owner'])
totalowners = list(dict.fromkeys(owners))
print("count: ", count, "\nOwners: ", len(totalowners))

dappfield = {"$or": [
        {"ipfs_data_json.dappid": int(3)},
        {"ipfs_data_json.dappid": str(3)}
        ]}
vulccount = db.tokens.find(dappfield).count()
r = db.tokens.find(dappfield)
owners = []
for a in r:
    owners.append(a['owner'])
vulcowners = list(dict.fromkeys(owners))
print("count: ", vulccount, "\nVulc Owners: ", len(vulcowners))

dappfield = {"$or": [
        {"ipfs_data_json.dappid": int(7)},
        {"ipfs_data_json.dappid": str(7)}
        ]}
coddlecount = db.tokens.find(dappfield).count()
r = db.tokens.find(dappfield)
owners = []
for a in r:
    owners.append(a['owner'])
coddleowners = list(dict.fromkeys(owners))
print("count: ", coddlecount, "\nCoddle Owners: ", len(coddleowners))

dappfield = {"$or": [
        {"ipfs_data_json.dappid": int(8)},
        {"ipfs_data_json.dappid": str(8)}
        ]}
vvcount = db.tokens.find(dappfield).count()
r = db.tokens.find(dappfield)
owners = []
for a in r:
    owners.append(a['owner'])
vvowners = list(dict.fromkeys(owners))
print("count: ", vvcount, "\nVV Owners: ", len(vvowners))
Ï
dappfield = {"$or": [
        {"ipfs_data_json.dappid": int(9)},
        {"ipfs_data_json.dappid": str(9)}
        ]}
geocatcount = db.tokens.find(dappfield).count()
r = db.tokens.find(dappfield)
owners = []
for a in r:
    owners.append(a['owner'])
geocatowners = list(dict.fromkeys(owners))
print("count: ", geocatcount, "\ngeocat Owners: ", len(geocatowners))

dappfield = {"$or": [
        {"ipfs_data_json.dappid": int(10)},
        {"ipfs_data_json.dappid": str(10)}
        ]}
plotcount = db.tokens.find(dappfield).count()
r = db.tokens.find(dappfield)
owners = []
for a in r:
    owners.append(a['owner'])
plotowners = list(dict.fromkeys(owners))
print("count: ", plotcount, "\nplot Owners: ", len(plotowners))

dappfield = {"$or": [
        {"ipfs_data_json.dappid": int(11)},
        {"ipfs_data_json.dappid": str(11)}
        ]}
berserkcount = db.tokens.find(dappfield).count()
r = db.tokens.find(dappfield)
owners = []
for a in r:
    owners.append(a['owner'])
berserkowners = list(dict.fromkeys(owners))
print("count: ", berserkcount, "\nberserk Owners: ", len(berserkowners))

dappfield = {"$or": [
        {"ipfs_data_json.dappid": int(1)},
        {"ipfs_data_json.dappid": str(1)}
        ]}
agoracount = db.tokens.find(dappfield).count()
r = db.tokens.find(dappfield)
owners = []
for a in r:
    owners.append(a['owner'])
agoraowners = list(dict.fromkeys(owners))
print("Agora count: ", agoracount, "\nAgora Owners: ", len(agoraowners))

dappfield = {"$or": [
        {"ipfs_data_json.dappid": int(11)},
        {"ipfs_data_json.dappid": str(11)}
        ]}
bbcount = db.tokens.find(dappfield).count()
r = db.tokens.find(dappfield)
owners = []
for a in r:
    owners.append(a['owner'])
bbowners = list(dict.fromkeys(owners))
print("BB count: ", bbcount, "\nBB Owners: ", len(bbowners))

stats = {'time': f"<< Activated {datetime.datetime.now()",
    stats: [
    f"Total Active NFTs: {count}",
    f"Total Unique NFT Owners: {len(totalowners)}",
    f"Agora NFTs: {agoracount}",
    f"Agora Owners: {len(agoraowners)}",
    f"Land NFTs: {plotcount}",
    f"Land Owners: {len(plotowners)}",
    f"Vulcanite NFTs: {vulccount}",
    f"Vulcanite Owners: {len(vulcowners)}",
    f"VulcanVerse Item NFTs: {vvcount}",
    f"VulcanVerse Item Owners: {len(vvowners)}",
    f"Berserk Card NFTs: {berserkcount}",
    f"Berserk Card Owners: {len(berserkowners)}",
    f"BlockBabies NFTs: {bbcount}",
    f"BlockBabies Owners: {len(bbowners)}",
    f"CoddlePets NFTs: {coddlecount}",
    f"CoddlePets Owners: {len(coddleowners)}",
    f"GeoCats NFTs: {geocatcount}",
    f"GeoCats Owners: {len(geocatowners)}"
    ]}

db.stats.drop()
db.stats.insert_one(stats)

col_list = db.list_collection_names()
print ("collections on the db:", col_list)

def main():
    pass

if __name__ == '__main__':
    main()
