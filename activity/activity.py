import glob
import json
import os.path
from datetime import datetime

from fastapi import FastAPI, Response, status
from pydantic import BaseModel

app = FastAPI()
ACTIVITY_FOLDER = 'activity'


class Activity(BaseModel):
    id: int
    name: str
    date: datetime


def find_activity(activity_id=0):
    return glob.glob(os.path.join(ACTIVITY_FOLDER, f"*{activity_id if activity_id else ''}.json"))


def write_to_json(activity_id, activity):
    with open(os.path.join(ACTIVITY_FOLDER, f'activity_{activity_id}.json'), 'w') as file:
        file.write(activity.json())


@app.get('/activity/get/all')
def get_activities():
    res = []
    files = find_activity()
    if files:
        for file in files:
            with open(file) as f:
                data = f.read()
                activity = Activity(**json.loads(data))
                res.append(activity)
    return res


@app.get('/activity/get/{activity_id}')
def get_activity(activity_id: int, response: Response):
    file = find_activity(activity_id)
    if file:
        with open(file[0]) as f:
            data = f.read()
            return Activity(**json.loads(data))
    response.status_code = status.HTTP_404_NOT_FOUND
    return {}


@app.post('/activity/add/{activity_id}')
def add_activity(activity_id: int, activity: Activity, response: Response):
    file = find_activity(activity_id)
    if file:
        response.status_code = status.HTTP_302_FOUND
        return False
    else:
        write_to_json(activity_id, activity)
    return True


@app.put('/activity/update/{activity_id}')
def update_activity(activity_id: int, activity: Activity, response: Response):
    file = find_activity(activity_id)
    if file:
        with open(file[0]) as f:
            data = f.read()
            act = Activity(**json.loads(data))
            act.name = activity.name
            act.date = activity.date
            write_to_json(activity_id, activity)
        return True
    response.status_code = status.HTTP_404_NOT_FOUND
    return False


@app.delete('/activity/delete/{activity_id}')
def delete_activity(activity_id: int, response: Response):
    file = find_activity(activity_id)
    if file:
        os.remove(file[0])
        return True
    response.status_code = status.HTTP_404_NOT_FOUND
    return False




