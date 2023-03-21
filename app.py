import uvicorn
from fastapi import FastAPI, BackgroundTasks, status
from fastapi.responses import JSONResponse
from typing import Union

from utils import update_db_server, update_count, get_station_count, fetch_stations
from models import Refill, RefillOut


app = FastAPI()


@app.on_event("startup")
async def startup_events():
    # init/update station_db
    fetch_stations()


@app.get("/v1/flow/total_flow")
async def get_staion_total_flow():
    print(f"Fetching total flow...")
    result = get_station_count(0)
    response = {"stationId": 0,
                "quantity": result}
    return JSONResponse(response)


@app.get("/v1/flow/{station_id}")
async def get_station_flow(station_id: int):
    print(f"Fetching flow for station {station_id}...")
    result = get_station_count(station_id)
    response = {"stationId": station_id,
                "quantity": result}
    return JSONResponse(response)


@app.post("/v1/flow/refill", response_model=RefillOut)
async def add_refill(request: Refill, background_tasks: BackgroundTasks):
# async def add_refill(request: Refill, background_tasks: BackgroundTasks):
    # Send Data to MySQL DB Server
    background_tasks.add_task(update_db_server, request.dict())

    # Send Data to Local DB
    background_tasks.add_task(update_count, request.dict())

    # return JSONResponse(request, status_code=status.HTTP_201_CREATED)
    return request

if __name__ == "__main__":
    uvicorn.run(app)