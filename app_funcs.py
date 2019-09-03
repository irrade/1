import uuid
import random
from datetime import datetime, timedelta
import pandas as pd
import click
import sys
import json
import os

PATH = 'c:\IKI\_test_conductor'
STORAGE_FILE_NAME = 'data_storage.json'
TERMS_FILE_NAME = 'phrases_ns.csv'


def _download_terms(path=PATH):
    """
    This func to download terms for random assignment
    :type path: path where the file with term is located
    """
    terms = pd.read_csv(os.path.join(path, TERMS_FILE_NAME), header=None, skiprows=1)
    terms_l = terms[0].tolist()
    return terms_l


def _append_to_data_storage(entry):
    """
    This func add search to data_storage
    :param entry: new search
    :return: add new serach
    """
    path_ = os.path.join(PATH, STORAGE_FILE_NAME)
    if not os.path.isfile(path_):
        with open(path_, 'w') as f:
            f.write(json.dumps([]))

    with open(path_, 'ab+') as f:
        f.seek(0, 2)
        if f.tell() == 0:
            f.write(json.dumps([entry]).encode())
        else:
            f.seek(-1, 2)
            f.truncate()
            f.write(','.encode())
            f.write(json.dumps(entry).encode())
            f.write(']'.encode())

           
def _load_data_storage(path=PATH):
    path_ = os.path.join(path, STORAGE_FILE_NAME)
    with open(path_, 'r') as f:
        dicts = json.load(f)
    return dicts
    


def _date_range(term_datetime, time_measurement, value):
    """
    this func check whether the datetime is in range based on minutes or seconds
    :return: true or false
    """
    timedelta_ = timedelta(seconds=value) if time_measurement == 'seconds' else timedelta(minutes=value)
    end_date = datetime.now()
    start_date = end_date - timedelta_
    condition = start_date <= term_datetime <= end_date
    return condition


def _count_terms(time_type, value_=1):
    """
    this func is used for num_arbitrary_lookback(seconds) and num_last_minute()
    :param time_type: seconds or minutes
    :param value_: should be int which refer to minutes or seconds
    :return:
    """
    time_ = 'minutes' if time_type == 'minutes' else 'seconds'
    dicts = _load_data_storage()
    counter = 0
    for current_dict in dicts:
        term_datetime = datetime.fromtimestamp(current_dict['timestamp'])
        date_range = _date_range(term_datetime=term_datetime, time_measurement=str(time_), value=int(value_))
        if date_range:
            counter += 1
    return counter


@click.group()
def main():
    pass


@click.option('--path_', default=PATH, help='Add the path to the file of terms location')
@main.command()
def increment(path_=PATH):
    terms_l = _download_terms(path_)
    for i in range(0,len(terms_l)):
        entry = {'term': str(random.choice(terms_l)), 'id': str(uuid.uuid1()), 'timestamp': datetime.now().timestamp()}
        _append_to_data_storage(entry)
    print('Data generated')
    sys.exit(0)


@main.command()
def num_last_minute():
    counter = _count_terms(time_type='minutes', value_=1)
    print(counter)
    sys.exit(0)


@click.argument('seconds')
@main.command()
def num_arbitrary_lookback(seconds):
    counter = _count_terms(time_type='seconds', value_=int(seconds))
    print(counter)
    sys.exit(0)


@click.argument('seconds')
@click.option('--dicts', default=_load_data_storage(), help='Add dictionary')
@main.command()
def most_common_term(seconds, dicts=_load_data_storage()):
    terms = []
    for current_dict in dicts:
        term_datetime = datetime.fromtimestamp(current_dict['timestamp'])
        date_range = _date_range(term_datetime=term_datetime, time_measurement='seconds', value=int(seconds))
        if date_range:
            terms.append(current_dict['term'])
    term = max(set(terms), key=terms.count)
    print(term)
    sys.exit(0)


if __name__ == "__main__":
    main()
