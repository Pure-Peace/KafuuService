# -*- coding: utf-8 -*-
'''
@author: PurePeace
@version: 0.10
@date: 2020-4-16

Utils everything
'''

import time, datetime
from os import getcwd

log_handle = True
log_path = f'{getcwd()}\\run.log'
with open(log_path, 'w', encoding='utf-8') as init_file:
    pass

# get now timeString or timeStamp
def getTime(needFormat=0, formatMS=True):
    if needFormat != 0:
        return datetime.datetime.now().strftime(f'%Y-%m-%d %H:%M:%S{r".%f" if formatMS else ""}')
    else:
        return time.time()


# timeString to timeStamp
def toTimeStamp(timeString):
    if '.' not in timeString: getMS = False
    else: getMS=True
    timeTuple = datetime.datetime.strptime(timeString, f'%Y-%m-%d %H:%M:%S{r".%f" if getMS else ""}')
    return float(f'{str(int(time.mktime(timeTuple.timetuple())))}' + (f'.{timeTuple.microsecond}' if getMS else ''))


# timeStamp to timeString
def toTimeString(timeStamp):
    if type(timeStamp) == int: getMS = False
    else: getMS = True
    timeTuple = datetime.datetime.utcfromtimestamp(timeStamp + 8 * 3600)
    return timeTuple.strftime(f'%Y-%m-%d %H:%M:%S{r".%f" if getMS else ""}')


def logg(text, dont_write=False):
    if log_handle == True:
        print(f'[{getTime(1)}] {text}')
    elif log_handle == 'write' and dont_write == False:
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(f'[{getTime(1)}] {text}\n')


