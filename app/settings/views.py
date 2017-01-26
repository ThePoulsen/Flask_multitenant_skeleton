## -*- coding: utf-8 -*-
## project/app/settings/views.py

from flask import Blueprint, render_template, url_for, g, request, redirect, session, json
from app.admin.services import requiredRole, breadCrumbs, messageText, flashMessage, errorFlash, columns, loginRequired
from app import db
from forms import userManagementForm, groupForm, companyForm
import requests
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

@settingsBP.route('/<string:lang>/user', methods=['GET'])
@settingsBP.route('/<string:lang>/user/<string:function>', methods=['GET', 'POST'])
@settingsBP.route('/<string:lang>/user/<string:function>/<int:id>', methods=['GET', 'POST'])
@requiredRole(u'Administrator')
@loginRequired
def userManagementView(lang=None, id=None, function=None):
    # universal variables

    g.lang = lang
    form = userManagementForm()
    kwargs = {'title':messageText('usersTitle'),
              'width':'',
              'formWidth':'',
              'breadcrumbs': breadCrumbs('settingsBP.userManagementView')}
    if function == None:
        kwargs['tableColumns'] =columns(['userNameCol','emailCol'])

        req = authAPI(endpoint='user', method='get', token=session['token'])

        kwargs['tableData'] = [[r['id'],r['name'],r['email']] for r in req['users']]

        return render_template(lang+'/listView.html', **kwargs)

    return render_template(lang+'/listView.html', **kwargs)

# Group View
@settingsBP.route('/<string:lang>/group', methods=['GET'])
@settingsBP.route('/<string:lang>/group/<string:function>', methods=['GET', 'POST'])
@settingsBP.route('/<string:lang>/group/<string:function>/<int:id>', methods=['GET', 'POST'])
@loginRequired
@requiredRole(u'Administrator')
def groupView(function=None, id=None, lang=None):
    g.lang = lang
    form = groupForm()
    kwargs = {'title':messageText('userGrpTitle'),
              'width':'600',
              'formWidth':'350',
              'breadcrumbs': breadCrumbs('settingsBP.groupView')}
    return render_template(lang+'/settings/groupForm.html', form=form, **kwargs)
