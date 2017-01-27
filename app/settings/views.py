## -*- coding: utf-8 -*-
## project/app/settings/views.py

from flask import Blueprint, render_template, url_for, g, request, redirect, session, json
from app.admin.services import requiredRole, breadCrumbs, messageText, flashMessage, errorFlash, columns, loginRequired
from app import db
from forms import companyForm
from authAPI import authAPI

settingsBP = Blueprint('settingsBP', __name__, template_folder='templates')

@settingsBP.route('/<string:lang>/company')
@requiredRole(u'Administrator')
@loginRequired
def companyView(lang=None):
    g.lang = lang
    form = companyForm()
    kwargs = {'title':messageText('companyTitle'),
              'formWidth':'350',
              'breadcrumbs': breadCrumbs('settingsBP.companyView')}
    return render_template(lang+'/settings/companyView.html', form=form, **kwargs)

@settingsBP.route('/<string:lang>/settings')
@requiredRole(u'Administrator')
@loginRequired
def settingsView(lang=None):
    g.lang = lang
    kwargs = {'title':messageText('settingsTitle'),
              'formWidth':'350',
              'breadcrumbs': breadCrumbs('settingsBP.settingsView')}
    return render_template(lang+'/settings/settingsView.html', **kwargs)
