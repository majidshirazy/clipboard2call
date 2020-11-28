#!/usr/bin/env python3
import sys
import string
import clipboard
import pyperclip
import os
import re
from asterisk.ami import AMIClient, SimpleAction
from unidecode import unidecode

username = "mami-username"
password = "ami-password"
astsrv = "asterisk-ip-address"
agent = 602
port = 5038
area_code = '0604'
country_code = '+1'

sip = AMIClient(address=astsrv, port=port)
sip.login(username=username, secret=password)


def normalize(dst):
    # Normalize Destination number remove non digit charachters
    # and remove Country code followed by '+'
    if dst.startswith(country_code):
        dst = ('0' + dst[3:]).replace(" ", "")
    dst = re.sub("[^0-9]", "", dst)
    return dst


def call_to(dst):
    call = SimpleAction(
        'Originate',
        Channel="SIP/"+str(agent),
        Exten=dst,
        Priority=1,
        Context='from-internal',
        CallerID="From CRM<"+dst+">",
    )
    sip.send_action(call)
    sip.logoff()


if (len(sys.argv) > 1):
    dst = unidecode(''.join(sys.argv[1:]))
    dst = normalize(dst)


elif (clipboard.paste()):
    dst = unidecode(clipboard.paste().replace(" ", ""))
    dst = normalize(dst)

else:
    sip.logoff()
    print("Error")
    exit()

call_to(dst)
