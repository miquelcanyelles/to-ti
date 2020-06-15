import numpy as np
import os
from datetime import datetime, timedelta


def create_db(file=None):
    '''
    Function for creating the database for the task.
    The database is a csv file.
    '''

    if 'tasks.csv' in os.listdir():
        print('tasks.csv exists. Remove it to create again.')
    else :
        f = open('tasks.csv', 'w')
        f.write('ID, DATE, STATUS, PARENT ID, TASK')
        f.close()

def load_db(file='tasks.csv'):
    '''
    Function that looks for and opens the database. It checks if it has the proper format (based on the header).
    '''

    db = np.loadtxt(file, delimiter=', ', dtype=str)

    if (db[0] == np.array(['ID', 'DATE', 'STATUS', 'PARENT', 'TASK'], dtype='<U13')).all():
        return db[1:]
    else :
        print('The database should contain the following header:\n\'ID, DATE, STATUS, PARENT ID, TASK\'')
        return None

def add_task(db, status, date, task, parent_id=None):
    '''
    Function for adding new tasks to the database.
    '''

    last_id = int(db[-1][0])

    if date.lower() == 'today':
        date = str(datetime.today().strftime('%Y-%m-%d'))
    elif date.lower() == 'tomorrow':
        date = str((datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d'))

    entry = [str(last_id + 1),
        date,
        status,
        parent_id,
        task]

    db = np.append(db, entry, axis=0)

    return db

def print_task_id(db, task_id):
    '''
    Function for printing a task based on its ID number
    '''
    for entry in db:
        if str(entry[0]) == str(task_id): print(entry)

def print_task_date(db, date):
    '''
    Function for printing tasks based on the due date.
    '''
    for entry in db:
        if str(entry[1]) == str(date): print(entry)

def remove_task(db, task_id):
    '''
    Function for removing tasks based on its ID.
    '''
    for entry in range(len(db)):
        if str(db[entry][1]) == str(task_id):
            np.delete(db, entry, axis=0)
