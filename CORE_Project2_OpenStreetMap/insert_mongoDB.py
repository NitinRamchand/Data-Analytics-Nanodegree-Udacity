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

#db.Japan.delete_many({})
# 
# counter = 0
with open('Toulouse.json') as f:
    data = json.loads(f.read())
    db.Toulouse.insert(data)
