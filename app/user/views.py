## -*- coding: utf-8 -*-
from flask import Blueprint, session, render_template, url_for, jsonify, json, g, redirect
from app.admin.services import flashMessage, errorFlash, messageText, loginRequired, requiredRole, breadCrumbs
from forms import changePasswordForm
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
