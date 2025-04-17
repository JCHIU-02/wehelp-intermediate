from fastapi import *
from fastapi.responses import FileResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles
import mysql.connector, json
from typing import Optional
from pydantic import BaseModel
import jwt
import datetime
import json
import requests
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

@app.post("/api/orders")
async def create_order_and_payment(request: Request):

	try:

		try:
			order_data = await request.json()

		except:
			return JSONResponse(
				status_code = 400,
				content={
					"error": True,
					"message": "Invalid or missing JSON body"
				}
			)

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
		
		# 產生 orderNumber (時間戳記+userid)
		try:
			user_id = payload["sub"]
			now_string = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
			order_number = f"{now_string}{user_id}"
				
			# 將 order data 存進資料庫 -> 狀態 Paid = N
			cnx = mysql.connector.connect(pool_name = "pool")
			cursor = cnx.cursor(buffered = True)
			cursor.execute("""INSERT INTO order_data(order_number, price, attraction_id, attraction_name, attraction_add, attraction_img, date, time, name, email, phone) 
					VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
						(order_number, order_data["order"]["price"], order_data["order"]["trip"]["attraction"]["id"], order_data["order"]["trip"]["attraction"]["name"], 
							order_data["order"]["trip"]["attraction"]["address"], order_data["order"]["trip"]["attraction"]["image"], 
							order_data["order"]["trip"]["date"], order_data["order"]["trip"]["time"],
							order_data["order"]["contact"]["name"], order_data["order"]["contact"]["email"], order_data["order"]["contact"]["phone"]))
			cnx.commit()
			cnx.close()
		except:
			return{"message": "failed to post data to DB"}

		# fetch tap pay api
		try:
			url = 'https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime'
			api_key = "partner_AzA78ymgW5U9c4KP07WhC8Lnl8NoN1l7yKY5ih34GbS3brBolXsIGM6d"

			headers = {
			"Content-Type": "application/json",
			"x-api-key": api_key
			}

			payload = {
			"prime": order_data["prime"],  
			"partner_key": api_key,
			"merchant_id": "musictalk_FUBON_POS_3",
			"details": "TapPay Test",
			"order_number": order_number,
			"amount": order_data["order"]["price"],
			"cardholder": {
				"name": order_data["order"]["contact"]["name"],
				"email": order_data["order"]["contact"]["email"],
				"phone_number": order_data["order"]["contact"]["phone"]
			},
			"remember": True
			}
			
			response = requests.post(url, headers=headers, json=payload, timeout=30)
			payment_data = response.json()
		
		except:
			return{"message":"failed to get response from TapPay"}

		# 等待 api response，將 response 中的 payment status 存到 orderdata 資料庫並 marked paid
		if payment_data["status"] == 0:
			cnx = mysql.connector.connect(pool_name = "pool")
			cursor = cnx.cursor(buffered = True)
			cursor.execute("UPDATE order_data SET paid = 'Y', status = 0 WHERE order_number = %s",(order_number,)) 
			cnx.commit()
			# 預定成功清空購物車
			cursor.execute("DELETE FROM booking_data WHERE user_id = %s", (user_id,))
			cnx.commit()
			cnx.close()
			return JSONResponse(status_code = 200, 
				content={
					"data": {
						"number": order_number,
						"payment": {
							"status": 0,
							"message": "付款成功"
						}
					}
				})
		else:
			cnx = mysql.connector.connect(pool_name = "pool")
			cursor = cnx.cursor(buffered = True)
			cursor.execute("UPDATE order_data SET status = %s WHERE order_number = %s",(payment_data["status"], order_number)) 
			cnx.commit()
			cnx.close()
			return JSONResponse(status_code = 200, 
				content={
					"data": {
						"number": order_number,
						"payment": {
							"status": 1,
							"message": "付款失敗"
						}
					}
				})
			
	except:
		return JSONResponse(status_code = 500, 
				content={
					"error": True,
					"message": "Internal Server Error"
				})

	# 將 order number response 給前端

@app.get("/api/order/{orderNumber}")
def getOrderbyNumber(orderNumber, request:Request):

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
		jwt.decode(token, secret_key, algorithms=["HS256"])

	except jwt.InvalidTokenError:
		return JSONResponse(
			status_code = 403,
			content = {
			"error": True,
			"message": "Login to get authorization."
			}
		)
	
	cnx = mysql.connector.connect(pool_name = "pool")
	cursor = cnx.cursor(buffered=True, dictionary=True)
	cursor.execute("SELECT * FROM order_data WHERE order_number = %s", (orderNumber,)) 
	orderData = cursor.fetchone()
	cnx.close()
	if orderData:
		return JSONResponse(status_code=200, content={
			"data": {
				"number": orderData["order_number"],
				"price": orderData["price"],
				"trip": {
				"attraction": {
					"id": orderData["attraction_id"],
					"name": orderData["attraction_name"],
					"address": orderData["attraction_add"],
					"image": orderData["attraction_img"]
				},
				"date": orderData["date"],
				"time": orderData["time"]
				},
				"contact": {
				"name": orderData["name"],
				"email": orderData["email"],
				"phone": orderData["phone"]
				},
				"status": orderData["status"]
			}
		})
	else:
		return{"data": None}
	


	

