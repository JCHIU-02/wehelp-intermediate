from fastapi import *
from fastapi.responses import FileResponse, JSONResponse
import mysql.connector, json
from typing import Optional

dbconfig = {
    "user":"root",
    "password":"1234",
    "host":"localhost",
    "database":"tpe_trip"
    }
cnx = mysql.connector.connect(pool_name = "pool", pool_size = 10, **dbconfig)


app=FastAPI()


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
		cursor = cnx.cursor(dictionary=True)

		if keyword is None:

			cursor.execute("SELECT * FROM attractions")
			attraction_list = cursor.fetchall()

			page_start_index = page*12
			page_end_index = (page+1)*12

			if page_start_index > len(attraction_list):
				
				cnx.close()
				return{
					"message":"No Data. Data index out of range."
				}
		
			elif page_end_index <= len(attraction_list):

				attractions_data = []

				for i in range(page_start_index, page_end_index):
					attraction_list[i]["images"] = json.loads(attraction_list[i]["images"])
					attractions_data.append(attraction_list[i])
				
				
				
				cnx.close()	
				return{
					"nextPage": page + 1,
					"data": attractions_data
				}
			
			elif len(attraction_list) - page_start_index < 12:

				attractions_data = []

				for i in range(page_start_index, len(attraction_list)):
					attraction_list[i]["images"] = json.loads(attraction_list[i]["images"])
					attractions_data.append(attraction_list[i])

				cnx.close()				
				return{
					"nextPage": None,
					"data": attractions_data
				}


		if keyword is not None:

			cursor.execute("SELECT * FROM attractions WHERE mrt = %s OR name LIKE %s", (keyword, f"%{keyword}%"))
			attraction_list = cursor.fetchall()

			page_start_index = page*12
			page_end_index = (page+1)*12

			if len(attraction_list) == 0:

				cnx.close()
				return{
					"message":"Can't find any matched data."
				}
					
			elif page_end_index <= len(attraction_list):

				attractions_data = []

				for i in range(page_start_index, page_end_index):
					attraction_list[i]["images"] = json.loads(attraction_list[i]["images"])
					attractions_data.append(attraction_list[i])

				cnx.close()
				return{
					"nextPage": page + 1,
					"data": attractions_data
				}
			
			elif 0 < len(attraction_list) - page_start_index < 12:

				attractions_data = []

				for i in range(page_start_index, len(attraction_list)):
					attraction_list[i]["images"] = json.loads(attraction_list[i]["images"])
					attractions_data.append(attraction_list[i])

				cnx.close()
				return{
					"nextPage": None,
					"data": attractions_data
				}

			else:
				return{
					"message": "No Data. Data index out of range."
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
		attraction_data["images"] = json.loads(attraction_data["images"])

		if attraction_data == None:
			cnx.close()
			return JSONResponse(
        	status_code = 400,
        	content = {
			"error": True,
			"message": "Id is out of range."
		})

		cnx.close()
		return{
			"data": attraction_data
		}
	
	
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
