import pymongo
from pymongo import MongoClient
from pprint import pprint
from bunch import bunchify
import pandas as pd



class Opakovka:
    def __init__(self, firm_id: int, name_op:str, quantity:float):
        self.firm_id = firm_id
        self.name_op = name_op
        self.quantity = quantity

class Kashon:
    def __init__(self, firm_id: int, name_ka:str, quantity:float):
        self.firm_id = firm_id
        self.name_ka = name_ka
        self.quantity = quantity



class RawProduct:
    def __init__(self, firm_id:int, name:str, quantity:float):
        self.firm_id = firm_id
        self.name = name
        self.quantity = quantity


class PF:
    def __init__(self):
        self.firm_id = None
        self.name = None
        self.quantity = 1
        self.recept = []

    def fill_info_file(self):
        path_to_recept = "C:/Order_Warehouse_Grivas/data/Recepts_input/recept.xlsx"
        recept_form_file = pd.read_excel(path_to_recept)
        # print(recept)
        self.firm_id = int(recept_form_file.iloc[[0]]["Код ПФ"])
        self.name = recept_form_file.iloc[[0]]["Име полуфабрикат"][0]
        recept_form_file = recept_form_file[["Код", "Продукт/материал", "Количество"]]
        recept = []
        for row in recept_form_file.index:
            id_mat = int(recept_form_file.at[row, "Код"])
            name_mat = recept_form_file.at[row, "Продукт/материал"]
            quantity_mat = float(recept_form_file.at[row, "Количество"])
            current_mat = {}
            current_mat["firm_id"] = id_mat
            current_mat["name"] = name_mat
            current_mat["quantity"] = quantity_mat
            self.recept.append(current_mat)


        # while True:
        #     print("Въведете фирмено id на ПФ или напишете 'end' за прекратяване на въвеждането")
        #     id = int(input())
        #     if id == "end":
        #         break
        #     print(f"Въведете името на ПФ с id {id} или напишете 'end' за прекратяване на въвеждането")
        #     name = input()
        #     if name == "end":
        #         break
        #     count = 0
        #     while True:
        #         count += 1
        #         print(f"Моля въведете фирмено id за продукт {count} от рецептата на ПФ {id} {name} . 'end' за край")
        #         id_prod = int(input())
        #         if id_prod == "end":
        #             break
        #         print(f"Моля въведете име на основен продукт с фирмено id{id_prod},  {count} от рецептата на ПФ {id} {name}. 'end' за край ")
        #         name_prod = input()
        #         if name_prod == "end":
        #             break
        #         print(f"Моля въведете количество основен продукт {id_prod} {name_prod} ,{count} от рецептата на ПФ {id} {name}. 'end' за край ")
        #         quant_prod = float(input())
        #         if quant_prod == "end":
        #             break
        #         current_pf_product = RawProduct(id_prod, name_prod, quant_prod)
        #         self.recept.append(current_pf_product)


    def real_quantity(self):
        for prod in self.recept:
            prod.quantity = prod.quantity * self.quantity



class Product_full:
    def __init__(self, firm_id:int, name_p : str, number_in_box : int, weight_one : float):
        self.firm_id = firm_id
        self.name_p = name_p
        self.number_in_box = number_in_box
        self.weight_one = weight_one
        self.raw_products = []
        self.pf_products = []
        self.kashon = []
        self.opakovka = []



pf = PF()
pf.fill_info_file()
print(f"Добавено име {pf.name}")
print(f"Добавено номер {pf.firm_id}")
print(f"Добавено количество {pf.quantity}")
print(f"Добавена рецепта {pf.recept}")
post = pf.__dict__




cluster = MongoClient("mongodb+srv://admin:admin@cluster0-r3p5k.mongodb.net/test?retryWrites=true&w=majority")

db = cluster["Recepts"]
collection = db["PF"]
seqs = db['seqs']


# #  For monitoring id
# seqs.insert_one({
#     'collection' : 'RawProducts',
#      'id' : 0
#  })
# seqs.fin
#
def insert_doc(doc):
     doc['_id'] = str(seqs.find_and_modify(
         query={'collection': 'RawProducts'},
         update={'$inc': {'id': 1}},
         fields={'id': 1, '_id': 0},
         new=True
     ).get('id'))

     try:
         collection.insert_one(doc)

     except pymongo.errors.DuplicateKeyError as e:
         insert_doc(doc)

c = collection.count_documents({"firm_id": pf.firm_id})
if c > 0:
    print("Съществува Полуфабрикат с такъв номер")
else:
    insert_doc(post)
    print("Успешно въведохте в базата данни полуфабриката")





#
#     print("Успешно въведен продукт")
#     print("Въведете основен продукт или напишете 'end' за прекратяване на въвеждането")
#     command = input()