import psycopg2, requests

url_base = 'https://api.warframe.market/v2/'
itemsInDB = list()
isSet = False

json = requests.get(url_base+"items").json()

conection = psycopg2.connect(user=username, password=senha, dbname="inventario")
cursor = conection.cursor()

cursor.execute("SELECT slug FROM itens;")
itemsInDB = cursor.fetchall()

for x in range(len(json["data"])):
    if 'prime' in json["data"][x]["tags"] and json["data"][x]["slug"] not in itemsInDB and 'mod' not in json["data"][x]["tags"]:
        if 'component' in json["data"][x]["tags"]:
            isSet = False
        else:
            isSet = True

        