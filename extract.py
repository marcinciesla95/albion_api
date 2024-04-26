import requests
import sqlite3
cout = 2

connect = sqlite3.connect('albion.db')
curs = connect.cursor()
curs.execute('''CREATE TABLE IF NOT EXISTS itemy
(
id INTEGER PRIMARY KEY AUTOINCREMENT,
item_id TEXT NOT NULL,
price INTEGER,
city TEXT NOT NULL)''')

sql = "INSERT INTO itemy (item_id, price, city) VALUES (?, ?, ?)"
while cout < 85:
    list = []
    with open(f"items/items{cout}.txt", "r") as itemy:
        for item in itemy:
            list.append(item.strip())
    list_str = ",".join(list)
    url = f'https://west.albion-online-data.com/api/v2/stats/prices/{list_str}.json?locations=Black Market,Bridgewatch&quality=2'

    response = requests.get(url)
    if response.status_code == 200:
        market_prices = response.json()
        correct_data = []
        for item in market_prices:
            response_body = {
                'item_id': item['item_id'],
                'price': item['sell_price_min'],
                'city': item['city'],
            }
            curs.execute(sql,(response_body['item_id'], response_body['price'], response_body['city']))



    cout+=1

connect.commit()
connect.close()
