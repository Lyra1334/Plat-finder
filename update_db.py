import psycopg2, requests

url_base = 'https://api.warframe.market/v2/'
itemsInDB = list()

json = requests.get(url_base+"items").json()

conection = psycopg2.connect(user=username, password=senha, dbname="inventario")
cursor = conection.cursor()

cursor.execute("SELECT slug FROM itens;")
itemsInDB = cursor.fetchall()

for x in range(len(json["data"])):
    if 'prime' in json["data"][x]["tags"]:
        if 'component' in json["data"][x]["tags"]:
            pass #é parte
        if 'warframe' in json["data"][x]["tags"]:
            pass #é frame
        if 'primary' in json["data"][x]["tags"]:
            pass #é arma
        if 'secondary' in json["data"][x]["tags"]:
            pass #é auxiliar
        if 'melee' in json["data"][x]["tags"]:
            pass #é melee

        