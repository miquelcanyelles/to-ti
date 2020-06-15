import yaml
import os, sys
from tinydb import TinyDB, Query
from datetime import datetime, timedelta

def config(config_file='config.yaml'):
    configuration = yaml.safe_load(open(config_file))

    file   = open('commands.py', 'r').readlines()
    output = open('commands.py.tmp', 'w')

    if configuration['db_filename'] == str(None):
       configuration['db_filename'] = 'toti.json'


    for line in file:
        if line.find('db_filename = ') == 0:
            output.write('db_filename = \'' + configuration['db_filename'] + '\'\n')
        else :
            output.write(line)

    output.close()
    os.remove('commands.py')
    os.rename('commands.py.tmp', 'commands.py')

    sys.exit(0)

db_filename = 'toti.json'

db = TinyDB(db_filename)
db_tasks = db.table('tasks')
db_time  = db.table('time')

def hello(db_tasks=db_tasks, db_time=db_time, time='now'):
    if time == 'now':
        time = datetime.now().time().strftime('%H:%M')
    day  = datetime.today().strftime('%d-%m-%Y')

    db_time.insert(
        { 'day'   : day,
        'time'    : time,
        'type'    : 'hello',
        'task_id' : None
        }
    )

    DueToday = Query()

    print(db_tasks.search(DueToday.due == str(datetime.today().strftime('%d-%m-%Y'))))

def pause(db_tasks=db_tasks, db_time=db_time, time='now'):
    if time == 'now':
        time = datetime.now().time().strftime('%H:%M')
    day  = datetime.today().strftime('%d-%m-%Y')

    db_time.insert(
        { 'day'   : day,
        'time'    : time,
        'type'    : 'pause',
        'task_id' : None
        }
    )

def resume(db_tasks=db_tasks, db_time=db_time, time='now'):
    if time == 'now':
        time = datetime.now().time().strftime('%H:%M')
    day  = datetime.today().strftime('%d-%m-%Y')

    db_time.insert(
        { 'day'   : day,
        'time'    : time,
        'type'    : 'pause',
        'task_id' : None
        }
    )

def goodbye(db_tasks=db_tasks, db_time=db_time, time='now'):
    if time == 'now':
        time = datetime.now().time().strftime('%H:%M')

    day  = datetime.today().strftime('%d-%m-%Y')

    db_time.insert(
        {
        'day'     : day,
        'time'    : time,
        'type'    : 'goodbye',
        'task_id' : None
        }
    )

    DueToday = Query()

    times = db_time.search(DueToday.day == str(datetime.today().strftime('%d-%m-%Y')))
    loc = int(str(time).find(':'))
    time_sum = datetime(1,1,1,int(time[:loc]), int(time[loc+1:]))

    types = []
    for time in times:
        types.append(time['type'])

    if all(x in types for x in ('hello', 'goodbye')):
        resumes = (len([type for type in types if type not in ['hello', 'goodbye', 'pause']]) % 2)
        pauses  = (len([type for type in types if type not in ['hello', 'goodbye', 'resume']]) % 2)


        if resumes == pauses:
            pass
        elif pauses > resumes:
            print('One or more \'resume\' entrances are missing, please add it(them).')
            sys.exit(0)

        elif pauses < resumes:
            print('One or more \'pause\' entrances are missing, please add it(them).')
            sys.exit(0)


    elif all(x in types for x in ('goodbye')):
        print('\'Hello\' instance is missing, please add it.')
        sys.exit(0)

    for time in times:
        loc = int(str(time['time']).find(':'))
        if time['type'] in ('hello', 'resume'):
            time_sum = time_sum - timedelta(hours=int(time['time'][:loc]), minutes=int(time['time'][loc+1:]))

        elif time['type'] == 'pause':
            time_sum = time_sum + timedelta(hours=int(time['time'][:loc]), minutes=int(time['time'][loc+1:]))

    #if time_sum > timedelta(days=1):
    #    time_sum = time_sum - timedelta(days=1)

    time_sum = ' h '.join(str(time_sum).split(':')[:2]) + ' min'
    print(time_sum)

    db_time.insert(
        {
        'day'     : day,
        'time'    : time_sum,
        'type'    : 'total of day',
        'task_id' : None
        }
    )
