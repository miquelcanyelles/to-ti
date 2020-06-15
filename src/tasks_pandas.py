import pandas as pd
import os
from datetime import datetime


def create_task_db(file=None):
    if 'tasks.csv' in os.listdir():
        print('tasks.csv exists. Remove it to create again.')
    else :
        f = open('tasks.csv', 'w')
        f.write('ID, DATE, STATUS, PARENT ID, TASK')
        f.close()

def load_task_db(file='tasks.csv'):
    db = pd.DataFrame(pd.read_csv(file))
    if (db.columns == pd.Index(['ID', ' DATE', ' STATUS', ' PARENT ID', ' TASK'], dtype='object')).all:
        return db
    else :
        print('The database should contain the following header:\n\'ID, DATE, STATUS, PARENT ID, TASK\'')
        return None


def add_task(db, status, date, task, parent_id=None):
    last_id = int(db.iloc[-1]['ID'])
    if date.lower() == 'today':
        date = str(pd.to_datetime('today').strftime('%Y-%m-%d'))

    db = db.append({'ID': last_id + 1,
                ' DATE' : date,
                ' STATUS' : status,
                ' PARENT' : parent_id,
                ' TASK' : task },
            ignore_index=True)

    return db

def print_task_id(db, task_id):
    task = db[db['ID'] == task_id]
    print(task)

def print_task_date(db, date):
    task = db[db[' DATE'] == date]
    print(task)

def remove_task(db, task_id):
    db = db.drop(db[db['ID'] == task_id].index)
    return db
