import random
import datetime
import time

def mills2datetime(ms):
    """
    convert mill seconds to datetime
    :param ms: mill seconds
    :return: datetime
    """
    print ms
    if ms is None:
        return
    if ms == 0:
        return
    return datetime.datetime.fromtimestamp(int(ms/1000))

def datetime2milss(dt):
    """
    convert datetime to mill seconds
    :param dt: datetime object
    :return: mill seconds
    """
    return int(dt.strftime("%s") * 1000)