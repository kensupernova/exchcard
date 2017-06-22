#coding: utf-8

import random
import datetime
import time

from exchcard import settings
from exchcard.models_main import Card
import string


def generateToken(username):
    return "I am a token"


def generateUniquePostcardName():
    start = "POST"
    digit = int(random.random()*1000000)
    card_name = '{0}{1}'.format(start, digit)

    if Card.objects.filter(card_name=card_name).exists():
        generateUniquePostcardName()
    else:
        return card_name


def count_arrive_travel(cards):
    ## total = len(cards)
    arrive = 0
    travel = 0
    for card_url in cards:
        card_str = str(card_url)
        length = len(card_str)
        card_str = card_str[: length-1]
        index_of_last_slash = card_str.rindex("/")
        card_id = int(card_str[index_of_last_slash+1:])
        ## print card_id
        try:
            card_obj = Card.objects.get(pk=card_id)
            if card_obj.has_arrived:
                arrive = arrive + 1
            else:
                travel = travel + 1

        except Card.DoesNotExit:
            print ("%s does not exit" % card_id)

    total = arrive + travel
    return (total, arrive, travel)


def get_sae_bucket():
    # from sae.storage import Bucket
    from sae.storage import Connection
    from exchcard import settings
    connection = Connection(accesskey=settings.DATABASES.MYSQL_USER,
                                    secretkey=settings.DATABASES.MYSQL_PASS,
                                    account="exchcard2", retries=3)

    bucket = connection.get_bucket(settings.STORAGE_BUCKET_NAME)
    bucket.post(acl=".r:*", metadata={"expires":"1d"})

    return bucket


def handle_uploaded_file_sae_s3(title, f):
    """
    Handle the file uploaded from the UploadFileForm and upload to SAE BUCKET
    :param title: The title of the file
    :param f: The file
    :return:
    """

    bucket = get_sae_bucket()
    bucket.put_object("%s-avatar.jpg" % title, f)

    ## only when the folder of source code is writable
    with open(settings.MEDIA_ROOT+'card_photos/'+f.name, "wb+") as destination:
        #Looping over UploadedFile.chunks()
        #instead of using read() ensures that large
        # files don’t overwhelm your system’s memory.
        for chunk in f.chunks():
            destination.write(chunk)


def hash_file_name(fname):
    parts = fname.split(".")

    fileFormat = ".%s" % parts[-1]

    try:
        now = datetime.datetime.now()
        ms = str(now.microsecond)

        newName = ("{0}{1}{2}{3}{4}{5}{6}"+fileFormat).\
            format(now.year, now.month, now.day, now.hour, now.minute, now.second, ms)

    except:
        # time.time()整数是秒，*1000，才是毫秒
        timestamp = int(time.time()*1000) ## 毫秒，millsecond
        newName = ("{0}"+fileFormat).format(timestamp)

    return newName


def hash_email_to_username_fool(email):
    email = email.replace("@", "at")
    email = email.replace(".", "dot")

    return email


def compare_created_early_to_late(a, b):
    """
    两个datetime比早晚， 从早到晚！！！
    :param a: 包含a['created'] has datetime string, like '2017-05-31T07:55:23.112844Z', UTC
    :param b:
    :return:
    """
    atime = datetime.datetime.strptime(a['created'], '%Y-%m-%dT%H:%M:%S.%fZ')
    btime = datetime.datetime.strptime(b['created'], '%Y-%m-%dT%H:%M:%S.%fZ')

    # 从大到小, 从早到晚
    dtime = btime - atime # datetime.timedelta
    return int(dtime.total_seconds()) >= 0


def get_random_int_chars(y):
    """
    Get random string, contains [0-9a-zA-Z]
    :param y: The length of the random characters
    :return:
    """
    choices = string.letters
    choices += string.digits
    # print("choices {0}".format(choices))

    return u"".join([random.choice(choices) for i in range(y)])


# -------------------------------------------------
# testing

# if __name__ == "main":
#     # print hash_file_name("20160607_190736.jpg")
#     pass