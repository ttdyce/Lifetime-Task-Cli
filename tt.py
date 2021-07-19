import argparse
import pymongo
import shelve

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(help='The action', dest='verb', required=True)
parser_add = subparsers.add_parser('add', aliases=['a'], help='Add an item, e.g. default=task, objective, project')
parser_get = subparsers.add_parser('get', aliases=['g'], help='Get an item/items, default all items')
parser_update = subparsers.add_parser('update', aliases=['u'], help='Update an item')
parser_remove = subparsers.add_parser('remove', aliases=['r'], help='Remove an item')
parser_select = subparsers.add_parser('select', aliases=['s'], help='Select a Project/Objective')

parser_get.add_argument("-a", "--all", help="All option, like: get --all", action="store_true", default=True)

parser_add.add_argument("-d", "--desc", help="Specify the description")
parser_add.add_argument("-o", "--objective", help="The related objective name")
parser_add.add_argument("-p", "--project", help="The related project name")
parser_add.add_argument("-t", "--type", help="The type name, like: task, project", default="task")

parser.add_argument("-n", "--name", help="Specify the name")
parser.add_argument("-o", "--objective", help="The related objective name")
parser.add_argument("-p", "--project", help="The related project name")

def init_remote_db(): 
# mongo db
    client = pymongo.MongoClient("") # mango db url + secret here
    db = client.test
    collection = db.task

    return (db, collection)

def printSelectedInfo(): 
    if('selected' in d): 
        (selected_project, selected_objective) = d['selected']
        print(f"Selected project: {selected_project}, objective: {selected_objective}")
        
# each subcommand is a method call        
def get(args): 
    db, collection = init_remote_db()
    if(args.all): 
        for item in collection.find():
            print(item["_id"])
            print(item["name"])
            
def add(args): 
    db, collection = init_remote_db()
    if(args.name != None): 
        collection.insert_one({"name": args.name, "description": args.desc, "project": args.project})

def update(args): 
    db, collection = init_remote_db()
    collection.delete({"name": "foo 2"})
    
def remove(args): 
    db, collection = init_remote_db()
    collection.delete_one({"name": "foo 2"})
    
def select(args): 
    d['selected'] = (args.project, args.objective)
    printSelectedInfo()

parser_get.set_defaults(func=get)
parser_add.set_defaults(func=add)
parser_update.set_defaults(func=update)
parser_remove.set_defaults(func=remove)
parser_select.set_defaults(func=select)
args = parser.parse_args()

# shelve db
d = shelve.open('shelvedb')
    
# main program
    printSelectedInfo()
args.func(args)
    
# after main program
d.close() 