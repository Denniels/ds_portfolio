from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List, Optional
import pandas as pd
import json
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="CO2 Emissions API",
    description="API para acceder a datos de emisiones de CO2 en Chile",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB connection
MONGODB_URL = os.getenv("MONGODB_URL")
client = AsyncIOMotorClient(MONGODB_URL)
db = client.emissions_db

@app.get("/")
async def root():
    return {"message": "CO2 Emissions API v1.0"}

@app.get("/api/v1/emissions/summary")
async def get_emissions_summary():
    """Obtener resumen general de emisiones"""
    try:
        summary = await db.summaries.find_one({"type": "general"})
        if summary:
            return summary
        return {"error": "No summary data available"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/emissions/by-region")
async def get_emissions_by_region():
    """Obtener emisiones por región"""
    try:
        regions = await db.regions.find({}).to_list(length=100)
        return regions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/emissions/top-emitters")
async def get_top_emitters(limit: int = Query(10, ge=1, le=50)):
    """Obtener principales emisores"""
    try:
        emitters = await db.emitters.find({}).limit(limit).to_list(length=limit)
        return emitters
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/emissions/geographical")
async def get_geographical_data():
    """Obtener datos geográficos de emisiones"""
    try:
        geo_data = await db.geographical.find({}).to_list(length=1000)
        return geo_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
