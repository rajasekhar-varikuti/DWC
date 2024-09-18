To run the application:
    in local:
        1. install all the packages which are mentioned in the requirements.txt
        2. run the following cmd in terminal to run the application `uvicorn main:app --reload`

    using docker:
        1. run the following cmd in the terminal to run the application `sudo docker compose up --build`


API EndPoints:


1. POST  /webhook 
    requestbody : optional

    # This API fetches the data from crm and campaigns and stores in the database

2. GET /data
    # This returns customers and campains list based on the limit and offset
    # if limit and offset is not given by ddefault it will take limit = 10 and offset = 0

    sample response:
        {
    "campaings": [
        {
            "id": 1,
            "status": "paused",
            "name": "Campaign 1",
            "budget": "9842",
            "start_date": "2024-08-30",
            "end_date": "2024-10-26"
        }
    ],
    "customers": [
        {
            "id": 1,
            "name": "Customer 1",
            "status": "active",
            "email": "customer1@example.com"
        }
    ]
} 

3. GET /sync/{source}
    # This API Syncs the data into database based on the source e.g crm, campaigns

4. GET /tasks
    # This API returns all the background tasks 
    sample response:
    [
    {
        "task_id": "830599dd-cd11-4be7-9e72-2c72ef6cbcec",
        "status": "running"
    }
]


5. POST /tasks/cancel
    request body:
        {
            "task_id": "830599dd-cd11-4be7-9e72-2c72ef6cbcec"
        }
    # This API cancel/deletes the background task based on task id


