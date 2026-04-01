import psycopg2, requests
from time import sleep

url_base = 'https://api.warframe.market/v2/'
itemsInDB = list()
item_type = ""
sets = list()
req_counter = 1

def try_req(counter: int):
    counter += 1
    if counter == 3:
        sleep(1)
        counter = 0
    return counter
    



json = requests.get(url_base+"items").json()

with open("./user_info.txt", "r") as info:
    username = info.readline().strip()
    password = info.readline().strip()
    db = info.readline().strip()

conection = psycopg2.connect(user=username, password=password, dbname=db)
cursor = conection.cursor()

cursor.execute("SELECT slug FROM itens;")
itemsInDB = [x[0] for x in cursor.fetchall()]

for x in range(len(json["data"])):
    if 'prime' in json["data"][x]["tags"] and json["data"][x]["slug"] not in itemsInDB and 'mod' not in json["data"][x]["tags"]:
        if 'component' in json["data"][x]["tags"]:
            item_type = "part"
        elif 'set' in json["data"][x]["tags"]:
            item_type = "set"
            sets.append(json["data"][x]["slug"])

        cursor.execute(f"INSERT INTO itens(slug, name, price, type, amount) VALUES ('{json["data"][x]["slug"]}', '{json["data"][x]['i18n']['en']["name"]}', 0, '{item_type}', 0);")

for set in sets:
    req_counter = try_req(req_counter)
    json = requests.get(url_base+f"item/{set}/set").json()
    print(set)
    for parte in json["data"]['items']:
        if parte['slug'] != set:
            cursor.execute(f"INSERT INTO set_parts(set_slug, part_slug, amount) VALUES ('{set}','{parte['slug']}', {parte['quantityInSet']})")

conection.commit()
cursor.execute("SELECT slug FROM itens;")
itemsInDB = [x[0] for x in cursor.fetchall()]

cont = 0 
for item in itemsInDB:
    cont +=1
    req_counter = try_req(req_counter)
    json = requests.get(url_base+f"orders/item/{item}/top").json()
    if len(json['data']['buy']) == 0:
        price = 0
    else:
        price = sum([order['platinum'] for order in json['data']['buy']])/len(json['data']['buy'])
    print(f"Item {item} is worth {price} platinum. ({cont}/{len(itemsInDB)})")
    cursor.execute(f"UPDATE itens SET price = {price} WHERE itens.slug = '{item}';")

conection.commit()
conection.close()