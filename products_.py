import uuid
from pprint import pprint
from datetime import date
import pandas as pd
import pymongo

from mongo_get_data import len_pf, get_pf_recept
from order_input import Oreder



class Oreder:
    def __init__(self,order_id=None, contragent=None, order_date=None):
        self.contragent = contragent
        self.order_id = order_id
        self.order_date = order_date
        self.order_products = []




class Product(Oreder):
    def __init__(self, _id : int, contragent=None, order_date=None):
        self.contragent = None
        self._id = _id
        self.order_id = None
        self.order_date = None
        self.end_date = None

        self.product_id = None
        self.product_name = None
        self.box_num = 1
        self.number_in_box = None
        self.weight_one = None
        self.quantity_product = None
        self.status = None

        self.opakovka = None
        self.kashon = None
        self.surovina = []
        self.pf_1 = [] # Списък на вложените ПФ
        self.pf_2 = []  #Списък на всички полуфабрикати


    def fill_info_file(self):
        path_to_recept = "C:/Order_Warehouse_Grivas/data/Product_full_recept_input/Product_recept.xlsx"
        recept_form_file = pd.read_excel(path_to_recept)
        pprint(recept_form_file)
        self.product_id = int(recept_form_file.iloc[[0]]["ID продукт"])
        self.product_name = recept_form_file.iloc[[0]]["Име продукт"][0]
        self.number_in_box = int(recept_form_file.iloc[[0]]["брой в кашон"][0])
        self.weight_one = float(recept_form_file.iloc[[0]]["маса на пакетче в кг"][0])
        self.quantity_product = self.box_num * self.weight_one * self.number_in_box
        recept_form_file = recept_form_file[["ID продукт/материал", "Продукт/материал", "Количество"]]

        for row in recept_form_file.index:
            current_id = int(recept_form_file.at[row, "ID продукт/материал"])
            current_name_product = recept_form_file.at[row, "Продукт/материал"]
            current_quantity = float(recept_form_file.at[row, "Количество"])
            if "Кашон" in current_name_product:
                box = Kashon(self.contragent, self.order_id, self.product_id, self.product_id,
                                self.product_name, current_id ,current_name_product,
                                current_quantity)
                self.kashon = box.__dict__
                print("намерен кашон. Присвоен!")
            elif "Опак." in current_name_product:
                opak = Opakovka(self.contragent, self.order_id, self.product_id, self.product_id,
                                self.product_name, current_id ,current_name_product,
                                current_quantity)
                self.opakovka = opak.__dict__
                print("намерена опаковка. Присвоен")
            elif "ПФ" in current_name_product:
                pf_recept_from_db = get_pf_recept(current_id)


                for pf_2_key in pf_recept_from_db:
                    if pf_2_key == "quantity":
                        pf_recept_from_db[pf_2_key] = current_quantity
                    if pf_2_key == "recept":
                        for recept in pf_recept_from_db['recept']:
                            for recept_key in recept:
                                if recept_key == "quantity":
                                    recept[recept_key] *= float(pf_recept_from_db['quantity'])

                self.pf_2.append(pf_recept_from_db)
                print("намерен полуфабрикат. Присвоен")
            else:
                surovina = Surovina(self.contragent, self.order_id, self.product_id, self.product_id,
                                self.product_name, current_id ,current_name_product,
                                current_quantity)
                self.surovina.append(surovina.__dict__)
                print("Намерена суровина. Да се присъедини към суровини")

    def quantity_update(self, boxes):
        self.box_num = boxes
        self.quantity_product = self.box_num * self.weight_one * self.number_in_box

        for opakovka_key in self.opakovka:
            if opakovka_key == "opakovka_quantity":
                self.opakovka[opakovka_key] *= self.box_num

        for kashon_key in self.kashon:
            if kashon_key == "kashon_quantity":
                self.kashon[kashon_key] *= boxes

        for surv in self.surovina:
            for surovina_key in surv:
                if surovina_key == "surovina_quantity":
                    surv[surovina_key] *= boxes






class Kashon:
    def __init__(self, contragent, order_number, for_product_firm_id,  material_id, product_name,
                 kashon_id:int, kashon_name:str, kashon_quantity:float, end_date=None ):
        self.contragent = None
        self.order_number = None
        self.end_date = end_date

        self.for_product_firm_id = for_product_firm_id


        self.material_id = material_id
        self.product_name = product_name
        self.kashon_id = kashon_id
        self.kashon_name = kashon_name
        self.kashon_quantity = kashon_quantity


class Opakovka:
    def __init__(self, contragent, order_number, for_product_firm_id, product_id, product_name,
                 opakovka_id:int, opakovka_name:str, opakovka_quantity:float, end_date = None):
        self.contragent = None
        self.order_number = None
        self.end_date = end_date

        self.for_product_firm_id = for_product_firm_id

        self.product_id = product_id
        self.product_name = product_name
        self.opakovka_id = opakovka_id
        self.opakovka_name = opakovka_name
        self.opakovka_quantity = opakovka_quantity


class Surovina:
    def __init__(self, contragent, order_number, for_product_firm_id,  product_id, product_name,
                 surovina_id:int, surovina_name:str, surovina_quantity:float, end_date=None):
        self.contragent = None
        self.order_number = None
        self.end_date = end_date

        self.for_product_firm_id = for_product_firm_id

        self.product_id = product_id
        self.product_name = product_name
        self.surovina_id = surovina_id
        self.surovina_name = surovina_name
        self.surovina_quantity = surovina_quantity



from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://admin:admin@cluster0-r3p5k.mongodb.net/test?retryWrites=true&w=majority")


db = cluster["Recepts"]
collection = db["Products"]




def len_prod():
    return len(list(collection.find()))


_id_product = len_prod() + 1

# print(get_pf_recept(7))

test_product = Product(_id_product)
test_product.fill_info_file()
#print(test_product.__dict__)





def insert_doc(doc):

    try:
        collection.insert_one(doc)

    except pymongo.errors.DuplicateKeyError as e:
        insert_doc(doc)


c = collection.count_documents({"firm_id": test_product.product_id})
if c > 0:
    print("Съществува Полуфабрикат с такъв номер")
else:
    insert_doc(test_product.__dict__)
    print("Успешно въведохте в базата данни полуфабриката")





# test = test_product.__dict__
#
# test = collection.find_one({"_id": 9})
#
# for t in test:
#     id = t
#     value = test[id]
#     if id == "contragent":
#         test[id] = "Promeneno"
#     if id == "box_num":
#         test[id] = 999
#     if id == "pf_2":
#         for prod in test[id]:
#             print(prod)


