'''
Created on 29 may. 2019

@author: ramchand_n
'''
import json
import pymongo
try: 
    client = pymongo.MongoClient("mongodb://nitinramchand:4Ractxps@cluster0dataanalyticsnanodegree-shard-00-00-9pkgh.mongodb.net:27017,cluster0dataanalyticsnanodegree-shard-00-01-9pkgh.mongodb.net:27017,cluster0dataanalyticsnanodegree-shard-00-02-9pkgh.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0DataAnalyticsNanodegree-shard-0&authSource=admin&retryWrites=true&w=majority", ssl=True)
    print("Connected successfully!!!") 
except:   
    print("Could not connect to MongoDB")
    
db = client.database


perc_nodes = float(db.Toulouse.find({"type" : "node"}).count())/float(db.Toulouse.count())
perc_way = float(db.Toulouse.find({"type" : "way"}).count())/float(db.Toulouse.count())
print db.Toulouse.find_one()
print db.command("dbstats", "Toulouse")
print db.Toulouse.distinct("created.uid")
print db.Toulouse.find({"type" : "node"}).count()
print db.Toulouse.find({"type" : "way"}).count()
print db.Toulouse.count()
print perc_nodes
print perc_way
print db.Toulouse.distinct("cuisine")
print db.Toulouse.find({"created.uid" : u'39569'}).count()
print db.Toulouse.find({"created.uid" : {"$exists": True }}).count()
print db.Toulouse.find({"amenity" : {"$exists": True }}).count()
print db.Toulouse.distinct("amenity")
count_amenity = {}
count_user = {}
count_amenity_chart = {}
count_user_chart = {}
for amenity in db.Toulouse.distinct("amenity"):
    count_amenity[amenity] = db.Toulouse.find({"amenity" : amenity}).count()
print count_amenity
for k, v in count_amenity.items():
    if v >= 120:
        count_amenity_chart[k] = v
    else:
        if 'other' not in count_amenity_chart:
            count_amenity_chart['other'] = 0
        count_amenity_chart['other'] += v
print count_amenity_chart
 
 
import matplotlib.pyplot as plt
 
 
labels = count_amenity_chart.keys()
sizes = count_amenity_chart.values()
 
# Plot
plt.pie(sizes, labels=labels,
autopct='%1.1f%%', textprops={'fontsize': 7})
 
plt.axis('equal')
plt.show()
# 
for user in db.Toulouse.distinct("created.uid"):
    count_user[user] = db.Toulouse.find({"created.uid" : user}).count()
print count_user
for k, v in count_user.items():
    if v >= 1000:
        count_user_chart[k] = v
    else:
        if 'other' not in count_user_chart:
            count_user_chart['other'] = 0
        count_user_chart['other'] += v
print count_user_chart

labels_user = count_user_chart.keys()
sizes_user = count_user_chart.values()
 
# Plot
plt.pie(sizes_user, labels=labels_user,
autopct='%1.1f%%', textprops={'fontsize': 7})
 
plt.axis('equal')
plt.show()
 