from flask import session
from authAPI import authAPI

def getGroups(includes=None):
    if includes:
        includeString = '?'
        for r in includes:
            includeString = includeString + str(r) + str('=True&')
        return authAPI(endpoint='userGroup'+includeString, method='get', token=session['token'])
    else:
        return authAPI(endpoint='userGroup', method='get', token=session['token'])['groups']

def postGroup(dataDict):
    return authAPI(endpoint='userGroup', method='post', dataDict=dataDict, token=session['token'])

def putGroup(dataDict, id):
    return authAPI(endpoint='userGroup/'+str(id), method='put', dataDict=dataDict, token=session['token'])

def deleteGroup(id):
    return authAPI(endpoint='userGroup/'+str(id), method='delete', token=session['token'])

def getGroup(id, includes=None):
    if includes:
        includeString = '?'
        for r in includes:
            includeString = includeString + str(r) + str('=True&')
        return authAPI(endpoint='userGroup/'+str(id)+includeString, method='get', token=session['token'])
    else:
        return authAPI(endpoint='userGroup/'+str(id), method='get', token=session['token'])
