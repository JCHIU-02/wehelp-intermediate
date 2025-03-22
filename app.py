from fastapi import *
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
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


			else:
				cnx.close()	
				return{
					"message":"data out of range."
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

			else:
				cnx.close()	
				return{
					"message":"data out of range or no matched keyword."
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