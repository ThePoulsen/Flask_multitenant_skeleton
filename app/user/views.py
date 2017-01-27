## -*- coding: utf-8 -*-
from flask import Blueprint, session, render_template, url_for, jsonify, json, g, redirect
from app.admin.services import flashMessage, errorFlash, messageText, loginRequired, requiredRole, breadCrumbs, columns
from forms import changePasswordForm, userManagementForm, groupForm
import requests
from authAPI import authAPI

userBP = Blueprint('userBP', __name__, template_folder='templates')

# User profile
@userBP.route('/<string:lang>/profile', methods=['GET'])
@requiredRole('User')
@loginRequired
def userProfileView(lang='dk'):
    g.lang = lang
    kwargs = {'title':messageText('userProfileTitle'),
              'breadcrumbs':breadCrumbs('userBP.userProfileView')}

    return render_template(lang+'/user/userProfileView.html', **kwargs)

@userBP.route('/<string:lang>/changePassword', methods=['GET','POST'])
@requiredRole('User')
@loginRequired
def changePasswordView(lang='dk'):
    g.lang = lang
    kwargs = {'formWidth':300,
              'contentTitle':messageText('changePassword'),
              'breadcrumbs':breadCrumbs('userBP.changePasswordView')}

    form = changePasswordForm()

    if form.validate_on_submit():

        dataDict = {'password':form.password.data}

        req = authAPI(endpoint='changePassword', method='put', dataDict=dataDict, token=session['token'])
        flashMessage('passwordChanged')

    return render_template(lang+'/user/changePasswordForm.html', form=form, **kwargs)

# Reset password
@userBP.route('/<string:lang>/resetPassword', methods=['GET','POST'])
@requiredRole('User')
@loginRequired
def resetPasswordView(lang='dk'):
    g.lang = lang
    pass

@userBP.route('/<string:lang>/user', methods=['GET'])
@userBP.route('/<string:lang>/user/<string:function>', methods=['GET', 'POST'])
@userBP.route('/<string:lang>/user/<string:function>/<int:id>', methods=['GET', 'POST'])
@requiredRole(u'Administrator')
@loginRequired
def userView(lang=None, id=None, function=None):
    # universal variables

    g.lang = lang
    form = userManagementForm()
    kwargs = {'title':messageText('usersTitle'),
              'width':'',
              'formWidth':'',
              'breadcrumbs': breadCrumbs('userBP.userView')}
    if function == None:
        kwargs['tableColumns'] =columns(['userNameCol','emailCol'])

        req = authAPI(endpoint='user', method='get', token=session['token'])

        kwargs['tableData'] = [[r['id'],r['name'],r['email']] for r in req['users']]

        return render_template(lang+'/listView.html', **kwargs)

    return render_template(lang+'/listView.html', **kwargs)

# Group View
@userBP.route('/<string:lang>/group', methods=['GET'])
@userBP.route('/<string:lang>/group/<string:function>', methods=['GET', 'POST'])
@userBP.route('/<string:lang>/group/<string:function>/<int:id>', methods=['GET', 'POST'])
@loginRequired
@requiredRole(u'Administrator')
def groupView(function=None, id=None, lang=None):
    # global variables
    g.lang = lang
    kwargs = {'title':messageText('userGrpTitle'),
              'width':'600',
              'formWidth':'350',
              'breadcrumbs': breadCrumbs('userBP.groupView')}

    if function == None:
        # perform API request
        req = authAPI(endpoint='userGroup', method='get', token=session['token'])

        # set data for listView
        kwargs['tableColumns'] =columns(['usrGroupCol'])
        kwargs['tableData'] = [[r['id'],r['name']] for r in req['groups']]

        # return view
        return render_template(lang+'/listView.html', **kwargs)
    elif function == 'delete':
        pass
    else:
        if function == 'update':
            pass
        elif function == 'new':
            form = groupForm()
            return render_template('')
