# coding=utf-8
# Download the Willibrordvertaling
#
# Run with python 2 and pip for the HTMLParser and requests:
# $ virtualenv work
# $ work/bin/pip install Requests
# $ work/bin/pip install HTMLParser


from HTMLParser import HTMLParser
import re
import requests

WEBSERVICE = 'https://rkbijbel.nl/cms/webservice.php'
t = "\t"
vertalingtag = 'willibrord1975'
htmlParser = HTMLParser()
cleanr = re.compile('<.*?>')


# title     tag key ch  v   word
# Genesis	Ge	1	1	1	In the beginning God created the heaven and the earth.

def clean(text):
    if text:
        cleaned = re.sub(cleanr, '', text)
        cleaned = htmlParser.unescape(cleaned)
        cleaned = cleaned.replace(u'/', '')
        cleaned = cleaned.replace(u'\\', '')
        cleaned = cleaned.replace(u'*', '')
        cleaned = cleaned.replace(u'­', '')
        cleaned = cleaned.replace("\n", '')
        cleaned = cleaned.replace("\r", '')
        return cleaned.encode('utf-8')
    else:
        return None


url = WEBSERVICE + '?mode=boeken'
json = {"vertalingtag": vertalingtag}
boeken = requests.post(url, json=json).json()
for boek in boeken:
    boek_titel = clean(boek['stitel'])
    boek_tag = clean(boek['stag'])
    boek_key = boek['ikey']

    url = WEBSERVICE + '?mode=hoofdstukken'
    json = {"boektag": "genesis", "vertalingtag": vertalingtag}
    hoofdstukken = requests.post(url, json=json).json()
    for hoofdstuk in hoofdstukken:
        hoofdstuknr = hoofdstuk['ihoofdstuk']

        url = WEBSERVICE + '?mode=versen'
        json = {"boektag": boek_tag, "hoofdstuknr": hoofdstuknr, "vertalingtag": vertalingtag}
        versen = requests.post(url, json=json).json()
        if len(versen) > 1:
            for vers in versen:

                vers_nummer = vers['iversnummer']
                vers_titel = clean(vers['stitel'])
                vers_tekst = clean(vers['stekst'])

                if vers_nummer:
                    try:
                        print("{}\t{}\t{}\t{}\t{}\t{}".format(boek_titel, boek_tag[:3], boek_key, hoofdstuknr, vers_nummer, vers_tekst))
                    except UnicodeDecodeError as e:
                        print(u"{}\t{}\t{}\t{}\t{}\t{}".format(boek_titel, boek_tag[:3], boek_key, hoofdstuknr, vers_nummer, '?'))
                else:
                    print 'No verse number found'