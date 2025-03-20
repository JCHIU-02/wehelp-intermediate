import json
import mysql.connector

dbconfig = {
    "user":"root",
    "password":"1234",
    "host":"localhost",
    "database":"tpe_trip"
    }

def read_json_file():
    with open("data/taipei-attractions.json") as json_file:
        data = json.load(json_file)
        spots_data= data["result"]["results"]
        return spots_data
    
def filter_imgs(spot_img):
    file_string = spot_img
    split_url = file_string.split("https://")
    split_url = [p for p in split_url if p] #清除空item
    img_url = ["https://" + p for p in split_url if p.lower().endswith("jpg") or p.lower().endswith("png")]
    return img_url


#INSERT into DB
spots = read_json_file()
cnx = mysql.connector.connect(**dbconfig)
cursor = cnx.cursor()
# print('資料庫連線成功')
for spot in spots:
    name = spot["name"]
    category = spot["CAT"]
    description = spot["description"]
    address = spot["address"]
    transport = spot["direction"]
    mrt = spot["MRT"]
    latitude = spot["latitude"]
    longitude = spot["longitude"]
    images = json.dumps(filter_imgs(spot["file"]))

    cursor.execute("""
    INSERT INTO attractions(name, category, description, address, transport, mrt, lat, lng, images)
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                    (name, category, description, address, transport, mrt, latitude,longitude, images))
    cnx.commit()

cnx.close()
    



