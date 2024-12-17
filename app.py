import sys, os, certifi
import pymongo
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.utils.main_utils.utils import load_object
from networksecurity.pipeline.training_pipeline import TrainingPipeline
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile,Request
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse
import pandas as pd

from networksecurity.constants.training_pipeline import DATA_INGESTION_COLLECTION_NAME
from networksecurity.constants.training_pipeline import DATA_INGESTION_DATABASE_NAME
from networksecurity.components.model_trainer import NetworkModel
from dotenv import load_dotenv
load_dotenv()
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, File, UploadFile

mongo_db_url = os.getenv("MONGO_DB_URL")
print(mongo_db_url)
ca =certifi.where()
client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)

collection = client[DATA_INGESTION_COLLECTION_NAME]
database = client[DATA_INGESTION_DATABASE_NAME]



app =FastAPI()
origins=["*"]
templates = Jinja2Templates(directory="./templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:
        train_pipeline=TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response("Trainig is Successful")
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
@app.get("/predict")
async def predict_route(request:Request, file: UploadFile=File(...)):

    try:
        df =pd.read_csv(file.file)
        preprocessor=load_object("final_model/preprocessor.pkl")
        final_model=load_object("final_model/model.pkl")
        network_model=NetworkModel(preprocessor=preprocessor,model=final_model)
        print(df.iloc[0])
        y_pred = network_model.predict(df)
        print(y_pred)
        df["predicted_column"] =y_pred
        print(df["predicted_column"])
        df.to_csv("predicted_output/output.csv")
        table_html = df.to_html(classes='tble table-striped')
        return templates.TeamplateResponse("table.html", {"request": request, "table": table_html})



    except Exception as e:
        raise NetworkSecurityException(e, sys)


if __name__=="__main__":
    app_run(app, host="localhost", port=8000)