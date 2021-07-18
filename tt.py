import argparse
import pymongo
import shelve

parser = argparse.ArgumentParser()
parser.add_argument("verb", help="The action", choices=['add', 'get', 'update', 'remove', 'select'])
# parser.add_argument("type", help="The type name, like: task, project", default="task")
parser.add_argument("-a", "--all", help="All option, like: get --all", action="store_true", default=True)
parser.add_argument("--desc", help="Specify the description")
parser.add_argument("-o", "--objective", help="The related objective name")
parser.add_argument("-p", "--project", help="The related project name")
parser.add_argument("-n", "--name", help="Specify the name")
args = parser.parse_args()

# mongo db
if(args.verb in ['add', 'get', 'update', 'remove']): 
    client = pymongo.MongoClient("") # mango db url + secret here
    db = client.test
    collection = db.task

# shelve db
d = shelve.open('shelvedb')

def printSelectedInfo(): 
    if('selected' in d): 
        (selected_project, selected_objective) = d['selected']
        print(f"Selected project: {selected_project}, objective: {selected_objective}")
        
# main program
printSelectedInfo()

if(args.verb == "get"): 

    if(args.all): 
        for item in collection.find():
            print(item["_id"])
            print(item["name"])
            
if(args.verb == "add"):
    if(args.name != None): 
        collection.insert_one({"name": args.name, "description": args.desc, "project": args.project})

if(args.verb == "update"):
    collection.delete({"name": "foo 2"})
    
if(args.verb == "remove"):
    collection.delete_one({"name": "foo 2"})
    
if(args.verb == "select"):
    d['selected'] = (args.project, args.objective)
    
    printSelectedInfo()
    
# after main program
d.close() 