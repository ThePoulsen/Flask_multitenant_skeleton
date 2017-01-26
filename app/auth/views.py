## -*- coding: utf-8 -*-
from flask import Blueprint, session, render_template, url_for, jsonify, json, g, redirect
from app.admin.services import ts, sendMail, flashMessage, errorFlash, messageText, loginRequired, logoutUser, requiredRole, breadCrumbs
from forms import registerForm, setPasswordForm, loginForm
from services import validateCVR
import requests
import flask_sijax
from authAPI import authAPI

authBP = Blueprint('authBP', __name__, template_folder='templates')

# register
@flask_sijax.route(authBP, '/<string:lang>/register')
def registerView(lang='dk'):
    if not 'token' in session:
        # universal variables
        form = registerForm()
        kwargs = {'formWidth':400,
                  'breadcrumbs': breadCrumbs('authBP.registerView')}

        if g.sijax.is_sijax_request:
            g.sijax.register_callback('validate', validateCVR)
            return g.sijax.process_request()

        if form.validate_on_submit():
            dataDict = {'regNo' : form.regNo.data,
                        'companyName' : form.companyName.data,
                        'userName' : form.userName.data,
                        'email' : form.email.data,
                        'password' : form.password.data}

            req = authAPI('register', method='post', dataDict=dataDict)

            if r.status_code == 409:
                flashmessage('accountExists')
            elif r.status_code == 404:
                flashmessage('cvrCheckError')
            elif 'error' in req:
                if req['error'] == 'Not valid email-address':
                    flashMessage('validateEmail')
            elif 'success' in req:
                # send email confirmation
                subject = u'Bekræft tilmelding'
                tok = req['token']
                email = req['email']
                confirm_url = url_for('authBP.confirmEmailView',token=tok, _external=True, lang=lang)
                html = render_template(lang+'/email/verify.html', confirm_url=confirm_url)
    #
                sendMail(subject=subject,
                         sender='Henrik Poulsen',
                         recipients=[email],
                         html_body=html,
                         text_body = None)
                flashMessage('loginSuccess')
                return redirect(url_for('indexView', lang=lang))

        return render_template(lang+'/auth/registerForm.html', form=form, **kwargs)
    else:
        flashMessage('alreadyRegistered')
        return redirect(url_for('indexView', lang=lang))

# Confirmation mail redirect
@authBP.route('/<string:lang>/confirm/<token>')
def confirmEmailView(token, lang='dk'):
    g.lang = lang
    req = authAPI('confirm', method='post', token=token)
    if 'error' in req:
        if req['error'] == 'User already confirmed':
            flashMessage('alreadyConfirmed')

    elif 'success' in req:
        if req['mustSetPass'] == 'True':
            return redirect(url_for('authBP.setPasswordView', lang=lang, token=req['token']))
        else:
            session['token'] = req['token']
            flashMessage('profileConfirmed')
    return redirect(url_for('indexView', lang=lang))

# Set password

@authBP.route('/<string:lang>/setPassword/<string:tok>', methods=['GET','POST'])
@loginRequired
@requiredRole('User')
def setPasswordView(lang='dk', tok=None):
    g.lang = lang
    kwargs = {'formWidth':300,
              'contentTitle':str(tok),
              'title':messageText('setPasswordTitle'),
              'breadcrumbs': breadCrumbs('authBP.setPasswordView')}

    form = setPasswordForm()

    if form.validate_on_submit():
        req = authAPI('setPassword', method='post', dataDict=dataDict, token=session['token'])
        if r.status_code == 404:
            flashMessage('userDoesNotExist')
        elif 'success' in req:
            flashMessage('passwordSet')

    return render_template(lang+'/auth/setPasswordForm.html', form=form, **kwargs)

# Login
@authBP.route('/<string:lang>/login', methods=['GET','POST'])
def loginView(lang='dk'):
    if not 'token' in session:
        g.lang = lang
        kwargs = {'formWidth':300,
                  'contentTitle':messageText('newPassword'),
                  'breadcrumbs': breadCrumbs('authBP.loginView')}

        form = loginForm()
        if form.validate_on_submit():
            regNo = form.regNo.data
            email = form.email.data
            password = form.password.data

            dataDict = {'regNo':regNo,
                        'email':email,
                        'password':password}

            req = authAPI('login', method='post', dataDict=dataDict)
            if 'success' in req:
                session['token'] = req['token']
                session['email'] = req['email']
                session['roles'] = req['roles']
                flashMessage('loginSuccess')
                return redirect(url_for('indexView', lang=lang))
            else:
                print req
                flashMessage('loginError')

        return render_template(lang+'/auth/loginForm.html', form=form, **kwargs)
    else:
        flashMessage('alreadyLoggedIn')
        return redirect(url_for('indexView', lang=lang))

# Change password
# Logout
@authBP.route('/<string:lang>/logout', methods=['GET','POST'])
def logoutView(lang='dk'):
    logoutUser()
    return redirect(url_for('indexView', lang=lang))
