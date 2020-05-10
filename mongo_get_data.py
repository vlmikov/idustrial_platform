from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://admin:admin@cluster0-r3p5k.mongodb.net/test?retryWrites=true&w=majority")


db = cluster["Recepts"]
collection = db["PF"]
seqs = db['seqs']


def len_pf():
    return len(list(collection.find()))


def get_pf_recept(current_id):
    result = collection.find_one({"firm_id" : current_id})
    return  result

