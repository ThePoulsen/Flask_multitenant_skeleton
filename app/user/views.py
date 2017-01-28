## -*- coding: utf-8 -*-
from flask import Blueprint, session, render_template, url_for, jsonify, json, g, redirect
from app.admin.services import flashMessage, errorFlash, messageText, loginRequired, requiredRole, breadCrumbs, columns
from forms import changePasswordForm, userForm, groupForm
import requests
from authAPI import authAPI
from groupCRUD import getGroups, postGroup, deleteGroup, getGroup, putGroup
from userCRUD import getUsers, getUser, postUser, putUser, deleteUser

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
    form = userForm()
    kwargs = {'title':messageText('usersTitle'),
              'width':'',
              'formWidth':'400',
              'breadcrumbs': breadCrumbs('userBP.userView')}

    # Get users
    if function == None:
        users = getUsers()
        kwargs['tableColumns'] =columns(['userNameCol','emailCol'])
        kwargs['tableData'] = [[r['id'],r['name'],r['email']] for r in users]

        return render_template(lang+'/listView.html', **kwargs)
    elif function == 'delete':
        delUsr = deleteUser(id)

        if 'error' in delUsr:
            errorFlash(delUsr['error'])
        elif 'success' in delUsr:
            flashMessage('userDeleted')

        return redirect(url_for('userBP.userView', lang=lang))
    else:
        if function == 'update':
            # Get single user
            usr = getUser(id, includes=['includeRoles', 'includeGroups'])

            form = userForm(name = usr['name'],
                            email = usr['email'],
                            phone = usr['phone'],
                            groups = [str(r['id']) for r in usr['groups']])

            if 'roles' in usr:
                for r in usr['roles']:
                    if r['title'] == 'Administrator':
                        form.isAdmin.checked = True
                    if r['title'] == 'Superuser':
                        form.isSuperuser.checked = True
#
            # Get all groups
            form.groups.choices = [(str(r['id']),r['name']) for r in getGroups()]

            if form.validate_on_submit():
                dataDict = {'name':form.name.data,
                            'email':form.email.data,
                            'phone':form.phone.data}

                roles = []
                if form.isAdmin.data:
                    roles.append('Administrator')
                if form.isSuperuser.data:
                    roles.append('Superuser')
                dataDict['roles'] = roles
                dataDict['groups'] = form.groups.data
                updateUser = putUser(dataDict=dataDict, id=id)
                if 'error' in updateUser:
                    errorFlash(updateUser['error'])
                elif 'success' in updateUser:
                    flashMessage('userUpdated')

                return redirect(url_for('userBP.userView', lang=lang))

            return render_template(lang+'/user/userForm.html', form=form, **kwargs)
        elif function == 'new':
            form = userForm()
            groups = [(str(r['id']),r['name']) for r in getGroups()]
            form.groups.choices = groups

            if form.validate_on_submit():
                dataDict = {'name':form.name.data,
                            'email':form.email.data,
                            'phone':form.phone.data}
                roles = []
                if form.isAdmin.data:
                    roles.append('Administrator')
                if form.isSuperuser.data:
                    roles.append('Superuser')
                dataDict['roles'] = roles
                dataDict['groups'] = form.groups.data
                newUser = postUser(dataDict)
                if 'error' in newUser:
                    if newUser['error'] == 'User already exist':
                        flashMessage('userExists')
                    else:
                        errorFlash(newUser['error'])
                elif 'success' in newUser:
                    flashMessage('userCreated')

                return redirect(url_for('userBP.userView', lang=lang))
            return render_template(lang+'/user/userForm.html', form=form, **kwargs)

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
        req = getGroups(includes=['includeUsers'])

        # set data for listView
        kwargs['tableColumns'] =columns(['usrGroupCol', 'usersCol'])
        kwargs['tableData'] = [[r['id'],r['name'],len(r['users'])] for r in req]

        # return view
        return render_template(lang+'/listView.html', **kwargs)
    elif function == 'delete':
        delGroup = deleteGroup(id)

        if 'error' in delGroup:
            if delGroup['error'] == 'Group has users':
                flashMessage('grpHasUsers')
            else:
                errorFlash(delGroup['error'])
        elif 'success' in delGroup:
            flashMessage('grpDeleted')

        return redirect(url_for('userBP.groupView', lang=lang))

    else:
        if function == 'update':
            # Get single group
            grp = getGroup(id, includes=['includeUsers'])
            form = groupForm(name=grp['name'],
                             desc=grp['desc'],
                             users = [str(r['id']) for r in grp['users']])
            form.users.choices = [(str(r['id']),r['email']) for r in getUsers()]
            if form.validate_on_submit():
                dataDict = {'name':form.name.data,
                            'desc':form.desc.data,
                            'users':[int(r) for r in form.users.data]}
                updateGroup = putGroup(dataDict=dataDict, id=id)
                if 'error' in updateGroup:
                    if updateGroup['error'] == 'Group already exist':
                        flashMessage('grpUpdated')
                    else:
                        errorFlash(updateGroup['error'])
                elif 'success' in updateGroup:
                    flashMessage('grpNew')

                return redirect(url_for('userBP.groupView', lang=lang))

        elif function == 'new':
            form = groupForm()
            form.users.choices = [(str(r['id']),r['email']) for r in getUsers()]

            if form.validate_on_submit():
                dataDict = {'name':form.name.data,
                            'desc':form.desc.data,
                            'users':[int(r) for r in form.users.data]}
                newGroup = postGroup(dataDict)

                if 'error' in newGroup:
                    if newGroup['error'] == 'Group already exist':
                        flashMessage('grpExists')
                    else:
                        errorFlash(newGroup['error'])
                elif 'success' in newGroup:
                    flashMessage('grpNew')

                return redirect(url_for('userBP.groupView', lang=lang))
        return render_template(lang+'/user/groupForm.html', form=form)
