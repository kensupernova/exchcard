import re

def url_name():
    re_pattern = re.compile(r'name[ \t\r\n]*=[ \t\r\n]*\"[A-ZAa-z-0-9]+\"')
    infile = open("urls-text.txt", "r")
    content = infile.read()
    url_names= re_pattern.findall(content)

    for name in url_names:
        name = name.replace("name", "")
        name = name.replace("=", "")
        name = name.replace('"', "")
        print '"{}":reverse("{}", request=request, format=format),'.format(name, name)

    for line in infile:
        print re_pattern.findall(line)

# datetime.datetime.strptime('2017-05-29T12:50:33.495153Z', '%Y-%m-%dT%H:%M:%S.%fZ')
# print item['created']
# 2017-05-29T12:50:33.495153Z
# 2017-05-31T07:55:23.112844Z
# time in local timezone
# >> > datetime.datetime.now()
# datetime.datetime(2017, 6, 5, 13, 13, 23, 103926)
# time in UTC
# >> > datetime.datetime.utcnow()
# datetime.datetime(2017, 6, 5, 5, 13, 30, 287766)
# timestamp in micro seconds
# >> > time.time()
# 1496639972.792231



types = {
    "SPP": ('2','SPP', 'Sent Postcard with Photo', '..........'),
    "RP": ('3', 'RP', 'Receive Postcard', '..........'),
    "RPP": ('4', 'RPP', 'Receive postcard with photo', '..........'),
    "UPP": ('5', 'UPP', 'Upload postcard photo', '..........'),
    #-------- Feedback on above actions, each has a subject
    "MC": ('6', 'MC', 'Make comment', '..........'), #
    "MDZ": ('7', 'MDZ', 'Make dian Zan', '..........'), #
}

types2 = {}
for key, val in types.items():
    types2[key] = {}
    types2[key]['activity_type_id'] = val[0]
    types2[key]['activity_type'] = val[1]
    types2[key]['short_name'] = val[2]
    types2[key]['description'] = val[3]

print(types2)

if __name__ == "__main__":
    pass