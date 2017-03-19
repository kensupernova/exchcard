import re

re_pattern = re.compile(r'name[ \t\r\n]*=[ \t\r\n]*\"[A-ZAa-z-0-9]+\"')
infile = open("urls-text.txt", "r")
content = infile.read()
url_names= re_pattern.findall(content)

for name in url_names:
    name = name.replace("name", "")
    name = name.replace("=", "")
    name = name.replace('"', "")
    print '"{}":reverse("{}", request=request, format=format),'.format(name, name)


# for line in infile:
#     print re_pattern.findall(line)