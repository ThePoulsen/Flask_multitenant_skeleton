from flask import session, json
from authAPI import authAPI

def getUsers():
    return authAPI(endpoint='user', method='get', token=session['token'])['users']

def getUser(id, includes=None):
    if includes:
        includeString = '?'
        for r in includes:
            includeString = includeString + str(r) + str('=True&')
        return authAPI(endpoint='user/'+str(id)+includeString, method='get', token=session['token'])
    else:
        return authAPI(endpoint='user/'+str(id), method='get', token=session['token'])

def postUser(dataDict):
    return authAPI(endpoint='user', method='post', dataDict=dataDict, token=session['token'])

def putUser(dataDict, id):
    return authAPI(endpoint='user/'+str(id), method='put', dataDict=dataDict, token=session['token'])

def deleteUser(id):
    return authAPI(endpoint='user/'+str(id), method='delete', token=session['token'])
