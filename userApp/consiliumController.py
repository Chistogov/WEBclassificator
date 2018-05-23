# -*- coding: utf-8 -*-
from flask import render_template, redirect, url_for, request
from userApp import *
from userApp.dbc import User, db, Recognized, Appoint, Journal, Category, Usertests, Testresults, Tests, Datasets, Picture, Cnnrec, Confirmed, Symptom
from flask_login import login_required, current_user
import datetime
import logging


@userApp.route('/consilium/<int:pic_id>')
@login_required
def consilium(pic_id):
    # ***
    recognized = db.session.query(Recognized.Recognized).filter(Recognized.Recognized.pic_id == pic_id)
    symp_ids = list()
    for item in db.session.query(Recognized.Recognized.symp_id).filter(Recognized.Recognized.pic_id == pic_id).group_by(Recognized.Recognized.user_id, Recognized.Recognized.symp_id):
        symp_ids.append(item.symp_id)
    user_rec = db.session.query(Recognized.Recognized.user_id).filter(Recognized.Recognized.pic_id == pic_id).group_by(Recognized.Recognized.user_id)
    user_rec = db.session.query(User.User).filter(User.User.id.in_(user_rec))
    recognized_count = db.session.query(db.func.count(Recognized.Recognized.symp_id)).filter(Recognized.Recognized.pic_id == pic_id).group_by(Recognized.Recognized.symp_id)
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

@userApp.route('/consilium/<int:pic_id>', methods=['POST'])
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

@userApp.route('/user_day_rec/<int:user_id>/<string:date>', methods=['GET'])
@login_required
def user_day_rec(user_id, date):
    if not(current_user.admin):
        return redirect(request.referrer)
    if(current_user.user_name == "demo"):
        return redirect(url_for('rejection', message="Demo user, read only"))
    print user_id
    print date
    pics = db.session.query(Picture.Picture).join(Recognized.Recognized)
    pics = pics.filter(Recognized.Recognized.user_id == user_id)
    date = datetime.datetime.strptime(date, "%Y-%m-%d")
    pics = pics.filter(db.func.DATE(Recognized.Recognized.date) == date)
    picslist = list()
    for item in pics:
        picslist.append(item.id)
    print "user_day_rec " + str(user_id)
    return redirect(url_for('rejection_search', page=0, p=picslist, user_owner=user_id))

class picSymps():
    symptom = None
    count = 0