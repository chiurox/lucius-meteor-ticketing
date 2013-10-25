#!/usr/bin/env python

import timeit
import csv
import urllib2
import json

def formatTransactionsFromCSV(file_name):
    """
    This function imports a csv file where each row is a transaction. Parses it and returns a formatted array
    """
    print(file_name)
    s3_url = 'https://paguemob.s3.amazonaws.com/'
    file_suffix = '-medium.png'
    fb_url = 'https://graph.facebook.com/'
    fb_suffix = '/picture?width=150&height=150&redirect=false'
    image_placeholder = '<img height="100" width="100" src="./lucius-festival-dos-deuses_files/placeholder-user.png">'
    with open(file_name, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for fields in reader:
            row = []
            row.append(fields[0])  #transaction group id
            row.append(fields[1]) #user name
            row.append('R$' + '{:,.2f}'.format(float(fields[2]))) #amount
            if fields[3] is not '': #image uploaded to s3
                # row.append('"' + s3_url + fields[3] + file_suffix)
                row.append((fields[3] + file_suffix).split('/')[-1])
            elif fields[4] != '': #image coming from facebook social profile
                request = urllib2.urlopen(fb_url + fields[4] + fb_suffix)
                avatar = json.load(request)['data']['url']
                row.append(avatar.split('/')[-1])
            else: #user does not have an avatar 
                row.append('"https://paguemob.s3.amazonaws.com/placeholder-user.png"')
            row.append(fields[5]) # purchase date
            print row

    return
if (__name__ == "__main__"):
    """
    Main
    """
    # try:
    t = timeit.Timer(setup='from __main__ import formatTransactionsFromCSV', stmt='formatTransactionsFromCSV(sys.argv[1])')
    print "\n" + str(t.timeit(1)) + " seconds"
    # except:
    print """
            Usage: python file_name.py
            """