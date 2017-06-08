#coding: utf-8

# 用户的活动类别
USER_ACTIVITY_TYPES = {
    #------- user make action initially, each action has a subject, and something being done
    # activity_type_id, activity_type, short_name, description
    "SP": {
        'activity_type_id':'1',
        'activity_type':'SP',
        'short_name':'Sent Postcard',
        'description':'sent a postcard to someone but without card photo'
    },
    'RPP': {'activity_type_id': '4',
        'description': '..........',
        'short_name': 'Receive postcard with photo',
        'activity_type': 'RPP'},
    'RP': {'activity_type_id': '3', 'description': '..........',
           'short_name': 'Receive Postcard', 'activity_type': 'RP'},
    'MC': {'activity_type_id': '6', 'description': '..........',
           'short_name': 'Make comment', 'activity_type': 'MC'},
    'SPP': {'activity_type_id': '2', 'description': '..........',
            'short_name': 'Sent Postcard with Photo', 'activity_type': 'SPP'},
    'MDZ': {'activity_type_id': '7', 'description': '..........',
            'short_name': 'Make dian Zan', 'activity_type': 'MDZ'},
    'UPP': {'activity_type_id': '5', 'description': '..........',
            'short_name': 'Upload postcard photo', 'activity_type': 'UPP'}
}

print USER_ACTIVITY_TYPES['UPP']['activity_type_id']