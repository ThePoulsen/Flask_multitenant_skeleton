## -*- coding: utf-8 -*-
## project/app/admin/views.py

from app import db
from models import messageGroup, message, messageBody, language
from forms import messageGroupForm, messageForm
from flask import Blueprint, render_template, request, redirect, url_for, session, g
from services import requiredRole, breadCrumbs, messageText, flashMessage, errorFlash, columns, loginRequired

adminBP = Blueprint('adminBP', __name__, template_folder='templates')

# Admin view
@adminBP.route('/<string:lang>')
@requiredRole(u'siteAdmin')
@loginRequired
def adminView(lang=None):
    g.lang = lang
    kwargs = {'title':messageText('adminTitle'),
              'breadcrumbs': breadCrumbs('adminBP.adminView')}

    return render_template(lang+'/admin/adminView.html', **kwargs)

# Message groups
@adminBP.route('/<string:lang>/messageGroup', methods=['GET'])
@adminBP.route('/<string:lang>/messageGroup/<string:function>', methods=['GET', 'POST'])
@adminBP.route('/<string:lang>/messageGroup/<string:function>/<int:id>', methods=['GET', 'POST'])
@requiredRole(u'siteAdmin')
@loginRequired
def messageGroupView(lang=None, id=None, function=None):
    g.lang = lang
    kwargs = {'title':messageText('adminTitle'),
              'width':'250',
              'formWidth':'350',
              'breadcrumbs': breadCrumbs('adminBP.messageGroupView')}

    if function == None:
        kwargs['tableColumns'] =columns(['msgGroupCol'])
        data = messageGroup.query.all()
        kwargs['tableData'] = [[r.id,r.name] for r in data]
        return render_template(lang+'/listView.html', **kwargs)
    elif function == 'delete':
        try:
            grp = messageGroup.query.filter_by(id=request.form['id']).first()
            db.session.delete(grp)
            db.session.commit()
            flashMessage('grpDeleted')
        except Exception as E:
            errorFlash(E)
        return redirect(url_for('adminBP.messageGroupView', lang=lang))
    else:
        if function == 'update':
            grp=messageGroup.query.filter_by(id=id).first()
            form = messageGroupForm(messageGroup=grp.name)
            kwargs['contentTitle'] = messageText('updateMsgGrpTitle')

            if form.validate_on_submit():
                try:
                    grp.name = form.messageGroup.data
                    db.session.commit()
                    flashMessage('grpUpdated')
                except Exception as E:
                    if 'unique constraint' in str(E):
                        db.session.rollback()
                        flashMessage('grpExists')
                    else:
                        errorFlash(E)
                return redirect(url_for('adminBP.messageGroupView', lang=lang))

        elif function == 'new':
            kwargs['contentTitle'] = messageText('newMsgGrpTitle')
            form = messageGroupForm()
            if form.validate_on_submit() and request.method == 'POST':
                try:
                    db.session.add(messageGroup(name=form.messageGroup.data))
                    db.session.commit()
                    flashMessage('grpNew')
                except Exception as E:
                    if 'unique constraint' in str(E):
                        db.session.rollback()
                        flashMessage('grpExists')
                    else:
                        errorFlash(E)
                return redirect(url_for('adminBP.messageGroupView', lang=lang))

        return render_template(lang+'/admin/messageGroupForm.html', form=form, **kwargs)

# Messages
@adminBP.route('/<string:lang>/message', methods=['GET'])
@adminBP.route('/<string:lang>/message/<string:function>', methods=['GET', 'POST'])
@adminBP.route('/<string:lang>/message/<string:function>/<int:id>', methods=['GET', 'POST'])
@requiredRole(u'siteAdmin')
@loginRequired
def messageView(lang='dk', id=None, function=None):
    g.lang = lang
    kwargs = {'title':messageText('adminTitle'),
              'formWidth':'350',
              'breadcrumbs': breadCrumbs('adminBP.messageView')}

    if function == None:
        tableData = []
        kwargs['tableColumns'] = columns(['msgCol','msgGroupCol', 'dkTextCol','enTextCol', 'parentCol'])
        mesg = message.query.all()
        for r in mesg:
            msg = messageBody.query.filter_by(message_id=r.id).all()
            msgGrp = messageGroup.query.filter_by(id=r.messageGroup_id).first()
            for m in msg:
                lan = language.query.filter_by(id=m.language_id).first().abbr
                if lan == 'dk':
                    dk = m.text
                elif lan == 'en':
                    en = m.text
            try:
                parent = message.query.filter_by(id=r.parent_id).first().title
            except:
                parent=''
            tableData.append([r.id, r.title, msgGrp.name, dk, en, parent])
        kwargs['tableData'] = tableData
        return render_template(lang+'/listView.html', **kwargs)
    elif function == 'delete':
        try:
            mesg = message.query.filter_by(id=request.form['id']).first()
            msgBody = messageBody.query.filter_by(message_id=mesg.id).all()
            for m in msgBody:
                db.session.delete(m)
                db.session.commit()
            db.session.delete(mesg)
            db.session.commit()
            flashMessage('msgDeleted')
        except Exception as E:
            errorFlash(E)
        return redirect(url_for('adminBP.messageView', lang=lang))

    else:
        if function == 'update':
            kwargs['contentTitle'] = messageText('updateMessageTitle')
            mesg = message.query.filter_by(id=id).first()
            en = language.query.filter_by(abbr='en').first().id
            dk = language.query.filter_by(abbr='dk').first().id
            msgGrp = messageGroup.query.filter_by(id=mesg.messageGroup_id).first()
            try:
                parent = str(mesg.parent_id)
            except:
                parent = ''
            form = messageForm(title=mesg.title,
                               messageGroup=str(msgGrp.id),
                               parent=str(mesg.parent_id),
                               en_text=messageBody.query.filter_by(message_id=mesg.id,
                                                                     language_id=en).first().text,
                               dk_text=messageBody.query.filter_by(message_id=mesg.id,
                                                                     language_id=dk).first().text)
            form.messageGroup.choices = [(str(r.id),r.name) for r in messageGroup.query.all()]
            viewGrp = messageGroup.query.filter_by(name='view').first()
            views = [(str(r.id), r.title) for r in message.query.filter_by(messageGroup_id=viewGrp.id).all()]
            views.insert(0,('',''))
            form.parent.choices = views
            if form.validate_on_submit():
                try:
                    mesg.title = form.title.data
                    mesg.messageGroup_id = form.messageGroup.data
                    msgBody = messageBody.query.filter_by(message_id=mesg.id).all()
                    for m in msgBody:
                        if m.language_id == en:
                            m.text = form.en_text.data
                        elif m.language_id == dk:
                            m.text = form.dk_text.data
                    if form.parent.data:
                        mesg.parent_id = form.parent.data
                    db.session.commit()
                    flashMessage('msgUpdated')
                except Exception as E:
                    if 'unique constraint' in str(E):
                        flashMessage('msgExists')
                    else:
                        errorFlash(E)
                return redirect(url_for('adminBP.messageView', lang=lang))

        elif function == 'new':
            kwargs['contentTitle'] = messageText('newMessageTitle')
            form = messageForm()

            grp = [(str(r.id), r.name) for r in messageGroup.query.all()]
            grp.insert(0,('',''))
            form.messageGroup.choices = grp
            viewGrp = messageGroup.query.filter_by(name='view').first()
            views = [(str(r.id), r.title) for r in message.query.filter_by(messageGroup_id=viewGrp.id).all()]
            views.insert(0,('',''))
            form.parent.choices = views
            if form.validate_on_submit() and request.method == 'POST':
                try:
                    mesg = message(title=form.title.data,
                                  messageGroup_id = form.messageGroup.data)
                    if form.parent.data:
                        mesg.parent_id = form.parent.data
                    db.session.add(mesg)

                    en = language.query.filter_by(abbr='en').first()
                    enMsgBody = messageBody(text=form.en_text.data,
                                       message_id=mesg.id,
                                       language_id=en.id)
                    db.session.add(enMsgBody)

                    dk = language.query.filter_by(abbr='dk').first()
                    enMsgBody = messageBody(text=form.dk_text.data,
                                       message_id=mesg.id,
                                       language_id=dk.id)
                    db.session.add(enMsgBody)
                    db.session.commit()

                    flashMessage('msgNew')
                except Exception as E:
                    if 'unique constraint' in str(E):
                        flashMessage('msgExists')
                    else:
                        errorFlash(E)
                return redirect(url_for('adminBP.messageView', lang='dk'))
        return render_template(lang+'/admin/messageForm.html', form=form, **kwargs)
