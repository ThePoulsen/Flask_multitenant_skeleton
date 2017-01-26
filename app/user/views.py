## -*- coding: utf-8 -*-
from flask import Blueprint, session, render_template, url_for, jsonify, json, g, redirect
from app.admin.services import flashMessage, errorFlash, messageText, loginRequired, requiredRole, breadCrumbs
from forms import changePasswordForm
import requests

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


    headers = {'platform': 'StrategyDeployment',
               'content-type': 'application/json',
               'token':str(session['token'])}
    form = changePasswordForm()

    if form.validate_on_submit():

        url = 'http://192.168.87.118:5000/api/changePassword'

        dataDict = {'password':form.password.data}

        r = requests.post(url, headers=headers, data=json.dumps(dataDict, ensure_ascii=True))

        req = json.loads(r.text)
        return str(req)
#        flashMessage('passwordChanged')

    return render_template(lang+'/user/changePasswordForm.html', form=form, **kwargs)

# Reset password
@userBP.route('/<string:lang>/resetPassword', methods=['GET','POST'])
@requiredRole('User')
@loginRequired
def resetPasswordView(lang='dk'):
    g.lang = lang
    pass
