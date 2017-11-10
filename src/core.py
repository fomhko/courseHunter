import xml.etree.ElementTree as ET
import requests
from sendemail import sendEmail
from time import sleep
import datetime
import os
from pytz import timezone

#course = {'department': 'CS', 'number': 225, 'crn': 35917}

def check_open(course):
    url = 'http://courses.illinois.edu/cisapp/explorer/schedule/2018/spring/{}/{}/{}.xml'.format(course['department'], course['number'], course['crn'])
    r = requests.get(url)
    xml = r.text

    # For testing with localXML #
    # with open('test.xml', 'r') as xml:
    #     xml = xml.read()

    try:
        root = ET.fromstring(xml)
    except ET.ParseError:
        print "Class doesn't exist :("
        return
    avail = root.find('enrollmentStatus').text
    if avail == "Closed" or avail == "UNKNOWN":
        return 0
    else:
        return 1

def notify(course):
    open('log.txt', 'w').close()
    course_open = 0
    f = open('log.txt', 'r+')
    logtext = ''
    while 1:
        print 'RUNNNING ' + str(course['number'])
        prelog = datetime.datetime.now(timezone('US/Central')).strftime("%m/%d %I:%M:%S %p: ")
        if check_open(course):
            if course_open == 0:
                logtext = "{}Opened\n".format(prelog)
                sendEmail("Your class has opened.")
                sleep(5)
                sendEmail(str(course['crn']))
                course_open = 1
        else:
            logtext = "{}Closed\n".format(prelog)
            if course_open == 1:
                sendEmail("Your class has closed")
            course_open = 0
        f.write(logtext)
        f.flush()
        os.fsync(f.fileno())
        sleep(300)
    f.close()
