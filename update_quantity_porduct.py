
from pymongo import MongoClient

from idustrial_platform.products_ import Product

cluster = MongoClient("mongodb+srv://admin:admin@cluster0-r3p5k.mongodb.net/test?retryWrites=true&w=majority")


db = cluster["Recepts"]
collection = db["Products"]




def len_prod():
    return len(list(collection.find()))


_id_product = len_prod() + 1


result = collection.find_one({"_id": 38})

data_id = 1
product = Product(data_id)



for key in result:
    if key == "contragent":
        contragent = result[key]
        product.contragent = contragent
    elif key == "order_id":
        order_id = result[key]
        product.order_id = order_id
    elif key == "order_date":
        order_date = result[key]
        product.order_date = order_date
    elif key == "end_date":
        end_date = result[key]
        product.end_date = end_date


    elif key == "product_id":
        product_id = result[key]
        product.product_id = product_id
    elif key == "product_name":
        product_name = result[key]
        product.product_name = product_name
    elif key == "box_num":
        box_num = result[key]
        product.box_num = box_num
    elif key == "number_in_box":
        number_in_box = result[key]
        product.number_in_box = number_in_box
    elif key == "weight_one":
        weight_one = result[key]
        product.weight_one = weight_one
    elif key == "quantity_product":
        quantity_product = result[key]
        product.quantity_product = quantity_product
    elif key == "status":
        status = result[key]
        product.status = status

    elif key == "opakovka":
        opakovka = result[key]
        product.opakovka = opakovka

    elif key == "kashon":
        kashon = result[key]
        product.kashon = kashon


    elif key == "surovina":
        surovina = result[key]
        product.surovina = surovina
    elif key == "pf_1":
        pf_1 = result[key]
        product.pf_1 = pf_1
    elif key == "pf_2":
        pf_2 = result[key]
        product.pf_2 = pf_2




print(product.pf_2[0]['quantity'])
kg_product = 10

print(product.pf_1)

product.quantity_update(10)
print(product.pf_1)

