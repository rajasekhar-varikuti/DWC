import app_modules.models
from fastapi import FastAPI, BackgroundTasks, Depends, HTTPException
from typing import List
from uuid import uuid4
from threading import Lock
import time
from sqlalchemy.orm import Session
from typing import Optional

from pydantic import BaseModel
from app_modules.models import get_db, Customers, Campaigns, TaskManger
from app_modules import utils
import logging


app = FastAPI()

#Cancel task request body model
class CancelTaskReqBody(BaseModel):
    task_id: str = None

#Campaigns model
class CampaignsResp(BaseModel):
    id: int = None
    status : str = None
    name : str = None
    budget : str = None
    start_date : str = None
    end_date : str = None

#Customers model
class CustomersResp(BaseModel):
    id : int = None
    name : str = None
    status : str = None
    email : str = None
    


#get data response model
class DataResp(BaseModel):
    campaings : Optional[CampaignsResp] = None
    customers : Optional[CampaignsResp] = None


    



@app.post('/webhook')
async def webhook(background_tasks: BackgroundTasks, db: Session= Depends(get_db)):
    task_id = str(uuid4())
    task_m = TaskManger(
            task_id=task_id,
            status="running"
        )
    db.add(task_m)
    db.commit()
    logging.info("Adding background tasks")
    try:
        background_tasks.add_task(utils.sync_crm_data, task_id, db)
        background_tasks.add_task(utils.sync_marketing_data, task_id, db)
    except:
        logging.error("Error while adding the background tasks in the webhook API")
    return {"status_code": 200,"message": "Sync started"}


@app.get('/data')
async def get_data(limit=10, offset=0, db: Session= Depends(get_db)):

    db_campaign_items = db.query(Campaigns).limit(limit).offset(offset)
    db_customer_items = db.query(Customers).limit(limit).offset(offset)
    all_items = []
    resp = DataResp()
    logging.info("Fetched records from campaigns and customers tables")
    camps : List[CampaignsResp] = []
    customers: List[CustomersResp] = []
    customers = []
    for camp in db_campaign_items:
        details = CampaignsResp()
        details.id = camp.id
        details.status = camp.status
        details.name = camp.name
        details.budget = camp.budget
        details.start_date = utils.get_date_str(camp.start_date)
        details.end_date = utils.get_date_str(camp.end_date)
        camps.append(details)
    for cust in db_customer_items:
        details = CustomersResp()
        details.id = cust.id
        details.status = cust.status
        details.name= cust.name
        details.email = cust.email
        customers.append(details)
    
    resp.campaings = camps
    resp.customers = customers
    return resp
    
    

@app.get('/sync/{source}')
async def sync_data(source: str, background_tasks: BackgroundTasks, db: Session= Depends(get_db)):
    
    if source == "crm":
        task_id = str(uuid4())
        task_m = TaskManger(
            task_id=task_id,
            status="running"
        )
        db.add(task_m)
        db.commit()
        try:
            background_tasks.add_task(utils.sync_crm_data, task_id, db)
        except:
            logging.error("Error while adding the background task in the sync crm api")
    elif source == "marketing":
        task_id = str(uuid4())
        task_m = TaskManger(
            task_id=task_id,
            status="running"
        )
        db.add(task_m)
        db.commit()
        try:
            background_tasks.add_task(utils.sync_marketing_data, task_id, db)
        except:
            logging.error("Error while adding the background task in the sync crm api")
    else:
        raise HTTPException(status_code=404, detail="Source not found")
    return {"status_code": 200,"message": "Sync started"}
    

@app.get('/tasks')
async def get_tasks(db: Session= Depends(get_db)):
    tasks = db.query(TaskManger).all()
    tasks = [{"task_id": task.task_id, "status": task.status } for task in tasks]
    return tasks

@app.post('/tasks/cancel')
async def cancel_task(body: CancelTaskReqBody, db: Session= Depends(get_db)):
    task_id = body.task_id
    db.query(TaskManger).filter(task_id==task_id).delete()
    return {"status_code": 200, "message": "Successfully removed the task"}
