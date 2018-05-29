# -*- coding: utf-8 -*-
from flask import render_template, redirect, url_for, request
from userApp import *
from userApp.dbc import User, db, Recognized, Consilium, Appoint, Category, Usertests, Testresults, Tests, Datasets, Picture, Cnnrec, Confirmed, Symptom
from flask_login import login_required, current_user
import datetime
from userApp.Service import journalService
import logging


@userApp.route('/consilium/pic/<int:pic_id>')
@login_required
def consilium(pic_id):
    # ***
    experts = db.session.query(User.User.id).filter(User.User.expert == True)
    recognized = db.session.query(Recognized.Recognized).filter(Recognized.Recognized.pic_id == pic_id, Recognized.Recognized.user_id.in_(experts))
    symp_ids = list()
    for item in db.session.query(Recognized.Recognized.symp_id).filter(Recognized.Recognized.pic_id == pic_id).group_by(Recognized.Recognized.user_id, Recognized.Recognized.symp_id):
        symp_ids.append(item.symp_id)
    user_rec = db.session.query(Recognized.Recognized.user_id).filter(Recognized.Recognized.pic_id == pic_id, Recognized.Recognized.user_id.in_(experts)).group_by(Recognized.Recognized.user_id)
    user_rec = db.session.query(User.User).filter(User.User.id.in_(user_rec), User.User.expert == True)
    recognized_count = db.session.query(db.func.count(Recognized.Recognized.symp_id)).filter(Recognized.Recognized.pic_id == pic_id, Recognized.Recognized.user_id.in_(experts)).group_by(Recognized.Recognized.symp_id)
    symptoms = db.session.query(Symptom.Symptom).filter(Symptom.Symptom.id.in_(symp_ids))
    symptom_list = list()
    diagnoses = db.session.query(Symptom.Symptom.id).filter(Symptom.Symptom.diagnos == True)
    count_users = len(list(user_rec))
    count_diagnoses = len(list(db.session.query(Recognized.Recognized.user_id).filter(Recognized.Recognized.pic_id == pic_id, Recognized.Recognized.symp_id.in_(diagnoses)).group_by(Recognized.Recognized.user_id)))
    for symptom in symptoms:
        symp = picSymps()
        symp.symptom=symptom
        if (symptom.ismedical and not(symptom.primary)):
            symp.count = (100 / count_users) * symp_ids.count(symptom.id)
        if(symptom.diagnos):
            symp.count=(100/count_diagnoses)*symp_ids.count(symptom.id)
        symptom_list.append(symp)
    # ***
    pic = Picture.Picture.query.get(pic_id)
    # ***
    neural = db.session.query(Cnnrec.Cnnrec).filter(Cnnrec.Cnnrec.pic_id == pic_id)
    # ***
    datasets = db.session.query(Datasets.Datasets)
    return render_template('pics_viewer/consilium.pug', admin=current_user.admin, neural=neural, pic=pic, user_rec=user_rec, recognized=recognized, datasets=datasets
                           , recognized_count=recognized_count, symptom_list=symptom_list)

@userApp.route('/consilium/pic/<int:pic_id>', methods=['POST'])
@login_required
def consilium_post(pic_id):
    if not(current_user.admin):
        return redirect(request.referrer)
    if (current_user.user_name == "demo"):
        return redirect(url_for('/'))
    form = request.form
    print int(form['pic'])
    if (form.has_key('pic')):
        for item in form:
            if("test" in item):
                test = form[item]
                for symp in form:
                    if (symp.isdigit()):
                        new_tag = Usertests.Usertests()
                        new_tag.pic_id = pic_id
                        new_tag.user_id = current_user.id
                        new_tag.dataset_id = test
                        new_tag.symp_id = symp
                        print "pic_id - " + str(pic_id)
                        print "symp - " + str(symp)
                        print "test - " + str(test)
                        exist = db.session.query(Usertests.Usertests).filter(Usertests.Usertests.pic_id == pic_id, Usertests.Usertests.symp_id == symp, Usertests.Usertests.dataset_id == test)
                        print str(len(list(exist)))
                        if (len(list(exist)) == 0):
                            db.session.add(new_tag)
                        else:
                            for i in exist:
                                print "exists id=" + str(i.id)
                                print "exists pic_id=" + str(i.pic_id)
                                print "exists symp_id=" + str(i.symp_id)
                                print "exists dataset_id=" + str(i.dataset_id)
                db.session.commit()

    return redirect(request.referrer)


PER_PAGE = 12

@userApp.route('/consilium/', defaults={'page': 0})
@userApp.route('/consilium/<int:page>', methods=['GET'])
@login_required
def consilium_view(page):
    if not(current_user.admin):
        return redirect(request.referrer)
    experts = db.session.query(User.User.id).filter(User.User.expert == True)
    pics1 = db.session.query(Recognized.Recognized.pic_id).filter(Recognized.Recognized.user_id.in_(experts)).group_by(Recognized.Recognized.pic_id)
    pics = list()
    for pic in pics1:
        tmppic = db.session.query(db.func.count(Recognized.Recognized.pic_id)).filter(Recognized.Recognized.pic_id == pic[0], Recognized.Recognized.user_id.in_(experts)).group_by(Recognized.Recognized.pic_id).first()
        if(tmppic[0]>2):
            pics.append(pic[0])
    pics = db.session.query(Picture.Picture).filter(Picture.Picture.id.in_(pics))
    count = len(list(pics))
    pics = get_pics_for_page(page, pics)
    pagination = Pagination.Pagination(page, PER_PAGE, count)
    pics_list = list()
    message = ""
    if ('message' in request.args):
        message = request.args['message']
    for pic in pics:
        form = picsForm()
        form.pic = pic

        symp_ids = list()
        for item in db.session.query(Recognized.Recognized.symp_id).filter(
                Recognized.Recognized.pic_id == pic.id, Recognized.Recognized.user_id.in_(
                                                                 experts)).group_by(Recognized.Recognized.user_id,
                                                                 Recognized.Recognized.symp_id):
            symp_ids.append(item.symp_id)
        user_rec = db.session.query(Recognized.Recognized.user_id).filter(Recognized.Recognized.pic_id == pic.id,
                                                                          Recognized.Recognized.user_id.in_(
                                                                          experts)).group_by(
                                                                          Recognized.Recognized.user_id)
        user_rec = db.session.query(User.User).filter(User.User.id.in_(user_rec), User.User.expert == True)

        symptoms = db.session.query(Symptom.Symptom).filter(Symptom.Symptom.id.in_(symp_ids))
        symptom_list = list()
        diagnoses = db.session.query(Symptom.Symptom.id).filter(Symptom.Symptom.diagnos == True)
        count_users = len(list(user_rec))
        count_diagnoses = len(list(
            db.session.query(Recognized.Recognized.user_id).filter(Recognized.Recognized.pic_id == pic.id,
                                                                   Recognized.Recognized.symp_id.in_(
                                                                   diagnoses),Recognized.Recognized.user_id.in_(
                                                                   experts)).group_by(
                                                                   Recognized.Recognized.user_id)))
        for symptom in symptoms:
            symp = picSymps()
            users = db.session.query(User.User).filter(User.User.expert==True, User.User.id==Recognized.Recognized.user_id, Recognized.Recognized.symp_id==symptom.id, Recognized.Recognized.pic_id==pic.id)
            symp.users=list()
            for usr in users:
                symp.users.append(usr)
            symp.symptom = symptom
            if (symptom.ismedical and not (symptom.primary)):
                symp.count = (100 / count_users) * symp_ids.count(symptom.id)
            if (symptom.diagnos):
                symp.count = (100 / count_diagnoses) * symp_ids.count(symptom.id)
            symptom_list.append(symp)
        form.symps=symptom_list
        cons = db.session.query(Consilium.Consilium.symp_id).filter(Consilium.Consilium.pic_id == pic.id)
        form.consilium = list()
        if(len(list(cons))>0):
            for cns in cons:
                form.consilium.append(cns.symp_id)
        pics_list.append(form)

    return render_template('/consilium/index.pug', admin=current_user.admin, pagination=pagination, pictures=pics_list, message=message)

@userApp.route('/consilium/', methods=['POST'], defaults={'page': 0})
@userApp.route('/consilium/<int:page>', methods=['POST'])
@login_required
def consilium_view_post(page):
    if (current_user.user_name == "demo"):
        return redirect(request.referrer)
    if not(current_user.admin):
        return redirect(request.referrer)
    form = request.form

    if (form.has_key('user') and form.has_key('message') and form.has_key('pic')):
        app = Appoint.Appoint()
        app.user_id = form['user']
        app.secondary = True
        app.pic_id = form['pic']
        app.date = datetime.datetime.now().date()
        app.message = form['message']
        db.session.add(app)
        db.session.commit()
        return redirect(url_for('consilium_view', page=page))
    if(form.has_key('pic')):
        db.session.query(Consilium.Consilium).filter(Consilium.Consilium.pic_id == form['pic']).delete()
    for item in form:
        if (item.isdigit()):
            new_tag = Consilium.Consilium()
            new_tag.user_id = current_user.id
            new_tag.symp_id = item
            new_tag.pic_id = form['pic']
            exist = db.session.query(Consilium.Consilium).filter(Consilium.Consilium.pic_id == form['pic'],
                                                                 Consilium.Consilium.symp_id == item)
            if (len(list(exist)) == 0):
                db.session.add(new_tag)
    db.session.commit()
    return redirect(request.referrer)

def get_pics_for_page(page, pics):
    pics = pics.group_by(Picture.Picture.id)
    if PER_PAGE:
        pics = pics.limit(PER_PAGE)
    if page:
        pics = pics.offset(page * PER_PAGE)
    return pics

class picSymps():
    symptom = None
    users = list()
    count = 0

class picsForm():
    pic = None
    symps = picSymps()
    consilium = list()