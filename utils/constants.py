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
    "SPP": ('2','SPP', 'Sent Postcard with Photo', '..........'),
    "RP": ('3', 'RP', 'Receive Postcard', '..........'),
    "RPP": ('4', 'RPP', 'Receive postcard with photo', '..........'),
    "UPP": ('5', 'UPP', 'Upload postcard photo', '..........'),
    #-------- Feedback on above actions, each has a subject
    "MC": ('6', 'MC', 'Make comment', '..........'), #
    "MDZ": ('7', 'MDZ', 'Make dian Zan', '..........'), #
}