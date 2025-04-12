from fastapi import *
from fastapi.responses import FileResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles
import mysql.connector, json
from typing import Optional
from pydantic import BaseModel
import jwt
import datetime
import json
from dotenv import load_dotenv
import os

dbconfig = {
    "user":"root",
    "password":"1234",
    "host":"localhost",
    "database":"tpe_trip"
    }
cnx = mysql.connector.connect(pool_name = "pool", pool_size = 10, **dbconfig)

load_dotenv("/Users/qiuhouan/Desktop/WeHelp/Intermediate/week1/taipei-day-trip/shiba.env")
env_key = os.getenv("secret_key")
secret_key = env_key

app=FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# Static Pages (Never Modify Code in this Block)
@app.get("/", include_in_schema=False)
async def index(request: Request):
	return FileResponse("./static/index.html", media_type="text/html")
@app.get("/attraction/{id}", include_in_schema=False)
async def attraction(request: Request, id: int):
	return FileResponse("./static/attraction.html", media_type="text/html")
@app.get("/booking", include_in_schema=False)
async def booking(request: Request):
	return FileResponse("./static/booking.html", media_type="text/html")
@app.get("/thankyou", include_in_schema=False)
async def thankyou(request: Request):
	return FileResponse("./static/thankyou.html", media_type="text/html")



@app.get("/api/attractions")
async def get_attractions(page: int, keyword: Optional[str] = None):
	
	try:

		cnx = mysql.connector.connect(pool_name = "pool")
		cursor = cnx.cursor(dictionary=True, buffered = True)

		if keyword is None:

			last_index = page*12
			cursor.execute("SELECT COUNT(*) FROM attractions")
			count = cursor.fetchone()
			row_count = count["COUNT(*)"]


			if row_count - last_index >= 12:
				cursor.execute("SELECT * FROM attractions LIMIT 12 OFFSET %s", (last_index,) )
				attractions_per_page = cursor.fetchall()

				for i in range(12):
					attractions_per_page[i]["images"] = json.loads(attractions_per_page[i]["images"])

				cnx.close()	
				return{
				"nextPage": page + 1,
				"data": attractions_per_page
			}

			elif 0 < row_count - last_index < 12:

				final_page_data_count = row_count - last_index
				cursor.execute("SELECT * FROM attractions LIMIT %s OFFSET %s", (final_page_data_count,last_index) )
				attractions_per_page = cursor.fetchall()

				for i in range(final_page_data_count):
					attractions_per_page[i]["images"] = json.loads(attractions_per_page[i]["images"])

				cnx.close()	
				return{
				"nextPage": None,
				"data": attractions_per_page
				}


		
		if keyword is not None:

			last_index = page*12
			cursor.execute("SELECT COUNT(*) FROM attractions WHERE mrt = %s OR name LIKE %s", (keyword, f"%{keyword}%"))
			count = cursor.fetchone()
			row_count = count["COUNT(*)"]
			
			if row_count - last_index >= 12:
				cursor.execute("SELECT * FROM attractions WHERE mrt = %s OR name LIKE %s LIMIT 12 OFFSET %s",
				   (keyword, f"%{keyword}%", last_index))
				attractions_per_page = cursor.fetchall()

				for i in range(12):
					attractions_per_page[i]["images"] = json.loads(attractions_per_page[i]["images"])

				cnx.close()	
				return{
					"nextPage": page + 1,
					"data": attractions_per_page
				}

			elif 0 < row_count - last_index < 12:

				final_page_data_count = row_count - last_index
				cursor.execute("SELECT * FROM attractions WHERE mrt = %s OR name LIKE %s LIMIT %s OFFSET %s",
				   (keyword, f"%{keyword}%", final_page_data_count, last_index))
				attractions_per_page = cursor.fetchall()

				for i in range(final_page_data_count):
					attractions_per_page[i]["images"] = json.loads(attractions_per_page[i]["images"])

				cnx.close()	
				return{
					"nextPage": None,
					"data": attractions_per_page
				}


	
	except:
		cnx.close()
		return JSONResponse(
        status_code =500,
        content = {
			"error": True,
			"message": "Internal Server Error"
		})




@app.get("/api/attraction/{attractionId}")
async def get_attraction_by_id(attractionId:int):

	try:
		cnx = mysql.connector.connect(pool_name = "pool")
		cursor = cnx.cursor(dictionary=True)
		cursor.execute("SELECT * FROM attractions WHERE id = %s", (attractionId,))
		attraction_data = cursor.fetchone()

		if attraction_data is not None:
			attraction_data["images"] = json.loads(attraction_data["images"])
			cnx.close()
			return{
			"data": attraction_data
		}

		else:
			cnx.close()
			return JSONResponse(
        	status_code = 400,
        	content = {
			"error": True,
			"message": "Invalid attraction ID."
		})
		
	
	except:
		cnx.close()
		return JSONResponse(
        status_code =500,
        content = {
			"error": True,
			"message": "Internal Server Error"
		})
	

@app.get("/api/mrts")
async def get_mrts_desc():
	try:
		cnx = mysql.connector.connect(pool_name = "pool")
		cursor = cnx.cursor()
		cursor.execute("SELECT mrt FROM attractions GROUP BY mrt ORDER BY COUNT(mrt) DESC")
		mrts = cursor.fetchall()
		mrts.pop()
		
		mrt_list = []
		for mrt in mrts:
			mrt_list.append(mrt[0])
		
		cnx.close()

		return{
			"data":mrt_list
		}
	
	except:
		cnx.close()
		return JSONResponse(
        status_code =500,
        content = {
			"error": True,
			"message": "Internal Server Error"
		})
	

class SignUpData(BaseModel):
    name: str
    email: str
    password: str

@app.post("/api/user")
async def user_signup(user_data:SignUpData):
	try:
		cnx = mysql.connector.connect(pool_name = "pool")
		cursor = cnx.cursor(buffered = True)
		cursor.execute("SELECT email FROM user_data WHERE email = %s", (user_data.email,))
		email = cursor.fetchone()
		if email is None:
			cursor.execute("INSERT INTO user_data(name, email, password) VALUES(%s, %s, %s)", (user_data.name, user_data.email, user_data.password))
			cnx.commit()
			cnx.close()
			return{"ok": True}
		if email is not None:
			cnx.close()
			return JSONResponse(
				status_code = 400,
				content = {
				"error": True,
				"message": "Email 已被註冊"
			})
	except:
		cnx.close()
		return JSONResponse(
        status_code =500,
        content = {
			"error": True,
			"message": "Internal Server Error"
		})



class SignInData(BaseModel):
    email: str
    password: str	

@app.put("/api/user/auth")
def user_signIn(user_data:SignInData, response:Response):
	
	try:
		cnx = mysql.connector.connect(pool_name = "pool")
		cursor = cnx.cursor(buffered = True)
		cursor.execute("SELECT email, password FROM user_data WHERE email = %s AND password = %s", (user_data.email, user_data.password))
		matched_user = cursor.fetchone()
		if matched_user is None:
			cnx.close()
			return JSONResponse(
				status_code = 400,
				content = {
				"error": True,
				"message": "帳號或密碼輸入錯誤"
			})
		if matched_user is not None:
			cursor = cnx.cursor(buffered = True, dictionary = True)
			cursor.execute("SELECT id, name, email FROM user_data WHERE email = %s", (user_data.email,))
			matched_user_data = cursor.fetchone()

			payload = {
				"sub": f"{matched_user_data["id"]}",
				"name": matched_user_data["name"],   
				"email": matched_user_data["email"],
				"iat": datetime.datetime.now().timestamp(),
				"exp": (datetime.datetime.now() + datetime.timedelta(days=7)).timestamp()
			}

			# generate token
			token = jwt.encode(payload, secret_key, algorithm="HS256")
			return {"token": token}
	
	except:
		cnx.close()
		return JSONResponse(
        status_code =500,
        content = {
			"error": True,
			"message": "Internal Server Error"
		})
	


@app.get("/api/user/auth")
def check_user_status(request: Request):
	
	auth_header = request.headers.get("Authorization")
	token = auth_header.split(" ")[1]
	try:
		payload = jwt.decode(token, secret_key, algorithms=["HS256"])
		return{
			"data":{
				"id": int(payload["sub"]),
				"name": payload["name"],
				"email": payload["email"]
			}
		}
	except jwt.InvalidTokenError:
		return{
			"data": None
		}
	except jwt.ExpiredSignatureError:
		return{
			"data": None
		}


class booking_data(BaseModel):
	attractionId: int
	date: str
	time: str
	price: int


@app.post("/api/booking")
def create_booking(booking_data:booking_data, request:Request):

	try:

		auth_header = request.headers.get("Authorization")

		if not auth_header:
			return JSONResponse(
				status_code = 401,
				content = {
					"error": True,
					"message": "Authorization header is required."
				}
			)

		token = auth_header.split(" ")[1]

		try:
			payload = jwt.decode(token, secret_key, algorithms=["HS256"])

		except jwt.InvalidTokenError:
			return JSONResponse(
				status_code = 403,
				content = {
				"error": True,
				"message": "Invalid Token"
				}
			)

		user_id = payload["sub"]
		attraction_id = booking_data.attractionId

		cnx = mysql.connector.connect(pool_name = "pool")
		cursor = cnx.cursor(buffered = True)
		cursor.execute("SELECT * FROM booking_data WHERE user_id = %s",(user_id,))
		user_already_booked = cursor.fetchone()
		cursor.execute("SELECT * FROM attractions WHERE id = %s", (attraction_id,))
		attraction = cursor.fetchone()
		cnx.close()

		# 檢查景點 id 是否存在
		if attraction:
			
			# 檢查 user 是否已有預定資料
			if user_already_booked:
				cnx = mysql.connector.connect(pool_name = "pool")
				cursor = cnx.cursor(buffered = True)
				cursor.execute("""UPDATE booking_data SET attraction_id = %s, date = %s, time = %s, price = %s WHERE user_id = %s""",
				(booking_data.attractionId, booking_data.date, booking_data.time, booking_data.price, user_id))
				cnx.commit()
				cnx.close()
				return {"ok": True}
			
			else:
				cnx = mysql.connector.connect(pool_name = "pool")
				cursor = cnx.cursor(buffered = True)
				cursor.execute("""INSERT INTO booking_data(attraction_id, date, time, price, user_id)
				VALUES(%s, %s, %s, %s, %s)""",(booking_data.attractionId, booking_data.date, booking_data.time, booking_data.price, user_id))
				cnx.commit()
				cnx.close()
				return {"ok": True}

		else:
			return JSONResponse(
				status_code = 400,
				content = {
					"error": True,
					"message": "The attraction ID does not exist."
				}
			)
	
	except:
		cnx.close()
		return JSONResponse(
        status_code =500,
        content = {
			"error": True,
			"message": "Internal Server Error"
		})
		
	
	
@app.get("/api/booking")
def getbooking_data(request:Request):

    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return JSONResponse(
            status_code = 401,
            content = {
                "error": True,
                "message": "Authorization header is required."
            }
        )

    token = auth_header.split(" ")[1]

    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
    
    except jwt.InvalidTokenError:
        return JSONResponse(
            status_code = 403,
            content = {
                "error": True,
                "message": "Invalid Token"
            }
        )

    user_id = payload["sub"]

    cnx = mysql.connector.connect(pool_name = "pool")
    cursor = cnx.cursor(buffered = True, dictionary = True)
    cursor.execute("""SELECT booking_data.date, booking_data.time, booking_data.price, attractions.id, 
			attractions.name, attractions.address, attractions.images
			FROM booking_data 
			LEFT JOIN attractions ON booking_data.attraction_id = attractions.id
			WHERE booking_data.user_id = %s""", (user_id,))
    booking_data = cursor.fetchone()
    cnx.close()

    if not booking_data:
        return {
			"data": None
		}

    cover_image = json.loads(booking_data["images"])[0]

    return {
		"data": {
			"attraction": {
				"id": booking_data["id"],
				"name": booking_data["name"],
				"address": booking_data["address"],
				"image": cover_image
			},
			"date": booking_data["date"].strftime("%Y-%m-%d"),
			"time": booking_data["time"],
			"price": booking_data["price"]
		}
	}


@app.delete("/api/booking")
def deleteBookingData(request:Request):

	auth_header = request.headers.get("Authorization")

	if not auth_header:
		return JSONResponse(
            status_code = 401,
            content = {
                "error": True,
                "message": "Authorization header is required."
            }
        )
	
	token = auth_header.split(" ")[1]
	
	try:
		payload = jwt.decode(token, secret_key, algorithms=["HS256"])

	except jwt.InvalidTokenError:
		return JSONResponse(
			status_code = 403,
			content = {
			"error": True,
			"message": "Login to get authorization."
			}
		)
	
	user_id = payload["sub"]
	cnx = mysql.connector.connect(pool_name = "pool")
	cursor = cnx.cursor(buffered = True)
	cursor.execute("DELETE FROM booking_data WHERE user_id = %s", (user_id,))
	cnx.commit()
	cnx.close()

	return {"ok": True}

	


	

