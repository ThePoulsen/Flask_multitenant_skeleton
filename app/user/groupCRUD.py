from flask import session
from authAPI import authAPI

def getGroups():
    return authAPI(endpoint='userGroup', method='get', token=session['token'])['groups']

def postGroup(dataDict):
    return authAPI(endpoint='userGroup', method='post', dataDict=dataDict, token=session['token'])
