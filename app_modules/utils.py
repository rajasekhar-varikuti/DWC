import httpx
import logging
from datetime import datetime
from .models import Campaigns, Customers, TaskManger



async def fetch_data(url: str, api_key: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers={"X-API-Key": api_key})
        response = response.json()
        return response

async def sync_crm_data(task_id, db):
    url = "https://challenge.berrydev.ai/api/crm/customers"
    api_key = "rajasekhar-varikuti"
    all_data = []
    for page in range(1, 10):  # Adjust range for pagination
        limit = page*10
        offset = limit - 10
        data = await fetch_data(f"{url}?limit={limit}&offset={offset}", api_key)
        all_data.extend(data['customers'])
    # Store data in database
    all_data = list({v['id']:v for v in all_data}.values())
    for item in all_data:
        db.merge(Customers(
            id = item['id'],
            name = item['name'],
            email = item['email'],
            status = item['status'],
            source = "Crm"
        ))
    db.commit()
    task = db.query(TaskManger).filter(TaskManger.task_id == task_id).first()
    task.status = "Completed"
    db.commit()
    return data

async def sync_marketing_data(task_id, db):
    url = "https://challenge.berrydev.ai/api/marketing/campaigns"
    api_key = "rajasekhar-varikuti"
    data = await fetch_data(url, api_key)
    print(data)
    logging.info(data)
    # Store data in database
    for item in data['campaigns']:
        db.merge(Campaigns(
            id=item['id'],
            name=item['name'],
            status=item['status'],
            budget=item['budget'],
            start_date=get_date_time_obj(item['start_date']),
            end_date=get_date_time_obj(item['end_date']),
            source = "Campaigns"
            
        ))
    db.commit()
    task = db.query(TaskManger).filter(TaskManger.task_id == task_id).first()
    task.status = "Completed"
    db.commit()

    return data


def get_date_time_obj(date_string):
    date_time_obj = datetime.strptime(date_string, "%Y-%m-%d")
    return date_time_obj


def get_date_str(date_obj):
    date_time_str = datetime.strftime(date_obj, "%Y-%m-%d")
    return date_time_str