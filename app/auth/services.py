## -*- coding: utf-8 -*-

import requests
import json
from app.admin.services import messageText

# Get cvr data
def cvrapi(cvr):
    data = ' \
    { "from" : 0, "size" : 1, \
      "query": { \
        "term": { \
          "cvrNummer": %s \
        } \
      } \
    } \
    ' % cvr
    response = requests.post('http://distribution.virk.dk/cvr-permanent/_search',
                             data=data,
                             auth=('Meta_Bogfoering_CVR_I_SKYEN',
                                   '4f0031f1-9b51-499b-b88f-319b25e204f1'))
    firmaNavn = json.loads(response.text)[u'hits'][u'hits'][0]['_source']['Vrvirksomhed']['virksomhedMetadata']['nyesteNavn']['navn']
    return  {'firmaNavn':firmaNavn}

# Validate CVR sijax
def validateCVR(obj_response, cvr):
    try:
        companyName = cvrapi(cvr)['firmaNavn']
    except Exception as E:
        companyName = messageText('cvrCheckError')
    obj_response.attr('#companyName', 'readonly', False)
    obj_response.attr('#companyName', 'value', companyName)
    obj_response.attr('#companyName', 'readonly', True)
