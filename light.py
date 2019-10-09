#!/usr/bin/env python


import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import datetime
import time
from pytz import timezone
from ltr559 import LTR559
ltr559 = LTR559()

cred = credentials.Certificate('./credential.json')
firebase_admin.initialize_app(cred)
db = firestore.client()


def fetchData():
    for i in range(3):
        lux = ltr559.get_lux()
        prox = ltr559.get_proximity()
        time.sleep(0.5)
        formattedLux = '{:05.02f}'.format(lux)
        formattedProx = '{:05.02f}'.format(prox)

    return {'lux': formattedLux, 'prox': formattedProx}


def insertToDb(data):
    dtNow = datetime.datetime.now()
    dtNow = dtNow.astimezone(timezone('Asia/Tokyo'))
    docRef = db.collection(u'light').document()
    docRef.set({
        u'value': data['lux'],
        u'createdAt': dtNow
    })


data = fetchData()
insertToDb(data)
