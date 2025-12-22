from fastapi import FastAPI
import time
#import asyncio to simulate an synchronous I/O operation (like an API call).

import asyncio

app = FastAPI()

#1. Synchronous Endpoint (CPU-bound example)
#Note: Since this is fast, the difference is minimal, but conceptually,
#CPU-bound tasks are run in thread pool. 

@app.get("/sync-task")
def sync_task():
    return {"message":"Sync task finished immediately. "}

#2. Asynchronous Endpoint (I/O-bound simulation)
#This simulates waiting for a database query or external service.

@app.get("/async-task")
async def async_task():
    print ("Async task started waiting...")
    #await is mandatory when calling an asychronous function (like asyncio.sleep)
    #The main thread yields control here to handle other requests.
    await asyncio.sleep(2) #Simulates a 2-second I/O delay, main thread yeilds control to other requests
    print("Async task resumed and finished. ")
    return {"message":"Async task finished after 2s delay."}
# async is used for tasks that are I/O bound (waitining for external systems, db or API)
#You must use await in these functions 