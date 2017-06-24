#coding: utf-8

with open('sae_ips.txt') as f:
    ips = ""
    for line in f:
        print line
        ips = ips +"," + line.strip()

    print ips


if __name__=="__main__":
    """

    :return:
    """







