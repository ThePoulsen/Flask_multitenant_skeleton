## -*- coding: utf-8 -*-

from app import app, mail
from flask import g, flash, session, redirect, url_for, abort, render_template
from models import language, message, messageBody, messageGroup
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
import requests, json, re
from wtforms import widgets, validators
from functools import wraps

def getLang():
    try:
        lang = language.query.filter_by(abbr=g.lang).first()
    except:
        lang = language.query.filter_by(abbr='dk').first()
    return lang

def messageText(msg):
    try:
        lang = getLang()
        mesg = message.query.filter_by(title=msg).first()
        text = messageBody.query.filter_by(message_id=mesg.id, language_id=lang.id).first().text
        return text
    except:
        pass

# Setup auth token
ts = URLSafeTimedSerializer(app.config['SECRET_KEY'])

# SendMail
def sendMail(subject, sender, recipients, text_body, html_body):
    mesg = Message(subject, sender=sender, recipients=recipients)
    mesg.body = text_body
    mesg.html = html_body
    mail.send(mesg)

def flashMessage(msg):
    lang = getLang()
    try:
        mesg = message.query.filter_by(title=msg).first()
        grp = messageGroup.query.filter_by(id=mesg.messageGroup_id).first()
        grpmsg = message.query.filter_by(title=grp.name).first()
        header = messageBody.query.filter_by(message_id=grpmsg.id, language_id=lang.id).first().text
        text = messageBody.query.filter_by(message_id=mesg.id, language_id=lang.id).first().text
        return flash(text, (grp.name, header))
    except:
        grp = messageGroup.query.filter_by(name='error').first()
        grpmsg = message.query.filter_by(title=grp.name).first()
        header = messageBody.query.filter_by(message_id=grpmsg.id, language_id=lang.id).first().text
        return flash('Fejl', (grp.name, header))


def errorFlash(E):
    lang = getLang()
    grp = messageGroup.query.filter_by(name='error').first()
    grpmsg = message.query.filter_by(title=grp.name).first()
    header = messageBody.query.filter_by(message_id=grpmsg.id, language_id=lang.id).first().text
    return flash(str(E), (grp.name, header))

def requiredValidator(form, field):
    lang = getLang()
    msg = message.query.filter_by(title='validateRequired').first()
    text = messageBody.query.filter_by(message_id=msg.id, language_id=lang.id).first().text
    if not field.data:
        raise validators.ValidationError(text)

def emailValidator(form, field):
    lang = getLang()
    msg = message.query.filter_by(title='validateEmail').first()
    text = messageBody.query.filter_by(message_id=msg.id, language_id=lang.id).first().text
    if not re.match(r"[^@]+@[^@]+\.[^@]+", field.data):
        raise validators.ValidationError(text)

# Select2 widget
class select2Widget(widgets.Select):
    def __call__(self, field, **kwargs):
        kwargs.setdefault('data-role', u'select2')

        allow_blank = getattr(field, 'allow_blank', False)
        if allow_blank and not self.multiple:
            kwargs['data-allow-blank'] = u'1'

        return super(select2Widget, self).__call__(field, **kwargs)

# Select2 multiple widget
class select2MultipleWidget(widgets.Select):
    def __call__(self, field, **kwargs):
        kwargs.setdefault('data-role', u'select2')

        allow_blank = getattr(field, 'allow_blank', False)
        if allow_blank and not self.multiple:
            kwargs['data-allow-blank'] = u'1'

        return super(select2MultipleWidget, self).__call__(field, multiple = True, **kwargs)

def getRoles():
    headers = {'platform': 'StrategyDeployment',
                       'content-type': 'application/json',
                       'token':session['token']}

    url = 'http://192.168.87.118:5000/api/getRoles'
    r = requests.post(url, headers=headers)
    req = json.loads(r.text)
    if 'error' in req:
        return False
    else:
        return req['roles']

# flask view decorators
def requiredRole(*role):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if not 'token' in session:
                return redirect(url_for('authBP.loginView', lang=lang))
            roles = getRoles()
            if roles:
                if role[0] not in roles:
                    return abort(403)
            return f(*args, **kwargs)
        return wrapped
    return wrapper

def loginRequired(f):
    if session:
        if 'lang' in session:
            lang = session['lang']
    else:
        lang = 'dk'
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not 'token' in session:
            return redirect(url_for('authBP.loginView', lang=lang))
        headers = {'platform': 'StrategyDeployment',
                       'content-type': 'application/json',
                       'token':session['token']}

        url = 'http://192.168.87.118:5000/api/checkPassword'
        r = requests.post(url, headers=headers)
        req = json.loads(r.text)
        if 'error' in req:
            return abort(403)

        return f(*args, **kwargs)
    return decorated_function

def logoutUser():
    session.clear()
    flashMessage('logoutSuccess')

def breadCrumbs(view):
    breadcrumbs = []
    lang = getLang()
    msg = message.query.filter_by(title=view).first()
    data = [view]
    for i in xrange(10):
        try:
            code = 'parent = msg.parent{}.title'.format('.parent'*i)
            exec code
            data.append(parent)
        except Exception as E:
            pass
    for r in list(reversed(data)):
        msg = message.query.filter_by(title=r).first()
        text = messageBody.query.filter_by(message_id=msg.id, language_id=lang.id).first().text

        url = url_for(r, lang=lang.abbr)

        breadcrumbs.append({'url':url, 'text':text})
    return breadcrumbs

def columns(list):
    data = []
    lang = getLang()
    for r in list:
        mesg = message.query.filter_by(title=r).first()
        text = messageBody.query.filter_by(message_id=mesg.id, language_id=lang.id).first().text
        data.append(text)
    return data

#Error handlers
@app.errorhandler(403)
def forbidden(e):
    lang = getLang()
    kwargs = {'title':messageText('notAuthorized')}
    return render_template(lang.abbr+'/errors/403.html', **kwargs)

@app.errorhandler(404)
def notFound(e):
    lang = getLang()
    kwargs = {'title':messageText('notFound')}
    return render_template(lang.abbr+'/errors/404.html', **kwargs)
