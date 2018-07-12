# -*- coding: utf-8 -*-
from flask import render_template, redirect, url_for, request
from userApp import *
from userApp.dbc import User, db, Recognized, Consilium, Appoint, Category, Usertests, Testresults, Tests, Datasets, Picture, Cnnrec, Confirmed, Symptom, Consnames, Consdata, Usercons
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
    # if not(current_user.admin):
    #     return redirect(request.referrer)
    # experts = db.session.query(User.User.id).filter(User.User.expert == True)
    hideTest = False
    hideConf = False
    hideApp = False
    hideSecRec = False

    if (request.args.has_key('hideTest')):
        if request.args.get('hideTest') == 'True':
            hideTest = True

    if (request.args.has_key('hideConf')):
        if request.args.get('hideConf') == 'True':
            hideConf = True

    if (request.args.has_key('hideApp')):
        if request.args.get('hideApp') == 'True':
            hideApp = True

    if (request.args.has_key('hideSecRec')):
        if request.args.get('hideSecRec') == 'True':
            hideSecRec = True

    usercons = db.session.query(Usercons.Usercons.cons_num).filter(Usercons.Usercons.user_id==current_user.id, Usercons.Usercons.manager==True)
    consdata = db.session.query(Consdata.Consdata).filter(Consdata.Consdata.cons_num.in_(usercons))
    users_cons = db.session.query(Usercons.Usercons.user_id).filter(Usercons.Usercons.cons_num.in_(usercons))
    pics1 = consdata.filter(Consdata.Consdata.pic_id==Recognized.Recognized.pic_id,
                                                             Recognized.Recognized.user_id.in_(users_cons)).group_by(Consdata.Consdata.id)
    pics = list()
    for pic in pics1:
        pics.append(pic.pic_id)
    iForm = infoForm()

    hidden_pics = db.session.query(Usertests.Usertests.pic_id)
    if(hideTest):
        iForm.sec_app = len(list(db.session.query(Picture.Picture).filter(Appoint.Appoint.secondary == True,
                                                   Picture.Picture.id == Appoint.Appoint.pic_id,
                                                   Picture.Picture.id.notin_(hidden_pics),
                                                   Appoint.Appoint.pic_id.in_(pics)).group_by(Picture.Picture.id)))
        iForm.cons_count = len(list(db.session.query(Picture.Picture).filter(Picture.Picture.id == Consilium.Consilium.pic_id, Picture.Picture.id.notin_(hidden_pics)).group_by(Consilium.Consilium.pic_id, Picture.Picture.id)))

    else:
        iForm.sec_app = len(list(db.session.query(Picture.Picture).filter(Appoint.Appoint.secondary == True,
                                                                          Picture.Picture.id == Appoint.Appoint.pic_id,
                                                                          Appoint.Appoint.pic_id.in_(pics)).group_by(Picture.Picture.id)))
        iForm.cons_count = len(list(db.session.query(Picture.Picture).filter(Picture.Picture.id == Consilium.Consilium.pic_id).group_by(Consilium.Consilium.pic_id, Picture.Picture.id)))
    pics = db.session.query(Picture.Picture).filter(Picture.Picture.id.in_(pics))

    if hideTest:
        pics = pics.filter(Picture.Picture.id.notin_(hidden_pics))
    if hideConf:
        hiddenConf = db.session.query(Consilium.Consilium.pic_id).group_by(Consilium.Consilium.pic_id)
        pics = pics.filter(Picture.Picture.id.notin_(hiddenConf))
    if hideApp:
        hiddenApp = db.session.query(Appoint.Appoint.pic_id).filter(Appoint.Appoint.secondary == True).group_by(
            Appoint.Appoint.pic_id)
        pics = pics.filter(Picture.Picture.id.notin_(hiddenApp))

    if hideSecRec:
        hiddenSecRec = db.session.query(Recognized.Recognized.pic_id).filter(Recognized.Recognized.secondary==True).group_by(Recognized.Recognized.pic_id)
        pics = pics.filter(Picture.Picture.id.in_(hiddenSecRec))
        print 'Not yet'

    conss = db.session.query(Consilium.Consilium.pic_id)
    picsto = pics.filter(Picture.Picture.id.notin_(conss))

    iForm.cons_to_rec = len(list(picsto))
    count = len(list(pics))
    pics = get_pics_for_page(page, pics)
    pagination = Pagination.Pagination(page, PER_PAGE, count)
    pics_list = list()
    message = ""
    print '4'
    if ('message' in request.args):
        message = request.args['message']
    for pic in pics:
        form = picsForm()
        form.pic = pic
        symp_ids = list()
        secondary = False
        for item in db.session.query(Recognized.Recognized.symp_id, Recognized.Recognized.secondary).filter(
                Recognized.Recognized.pic_id == pic.id, Recognized.Recognized.user_id.in_(
                    users_cons)).group_by(Recognized.Recognized.user_id,
                                                                 Recognized.Recognized.symp_id, Recognized.Recognized.secondary):
            symp_ids.append(item.symp_id)
            if(item.secondary==True):
                secondary=True
        form.secondary=secondary
        user_rec = db.session.query(User.User).filter(User.User.id == Recognized.Recognized.user_id,
                                                                          Recognized.Recognized.pic_id == pic.id,
                                                                          Recognized.Recognized.user_id.in_(
                                                                          users_cons)).group_by(
                                                                          Recognized.Recognized.user_id).group_by(User.User.id)
        # user_rec = db.session.query(User.User).filter(User.User.id.in_(user_rec), User.User.expert == True)

        symptoms = db.session.query(Symptom.Symptom).filter(Symptom.Symptom.id.in_(symp_ids))
        symptom_list = list()
        diagnoses = db.session.query(Symptom.Symptom.id).filter(Symptom.Symptom.diagnos == True)
        count_users = len(list(user_rec))
        count_diagnoses = len(list(
            db.session.query(Recognized.Recognized.user_id).filter(Recognized.Recognized.pic_id == pic.id,
                                                                   Recognized.Recognized.symp_id.in_(
                                                                   diagnoses),Recognized.Recognized.user_id.in_(
                                                                   users_cons)).group_by(
                                                                   Recognized.Recognized.user_id)))
        app_users = db.session.query(User.User).filter(User.User.id.in_(users_cons),
                                                       User.User.id == Appoint.Appoint.user_id,
                                                       Appoint.Appoint.pic_id == pic.id)
        for symptom in symptoms:
            symp = picSymps()
            users = db.session.query(User.User).filter(User.User.id.in_(users_cons), User.User.id==Recognized.Recognized.user_id, Recognized.Recognized.symp_id==symptom.id, Recognized.Recognized.pic_id==pic.id)
            symp.users=list()
            for usr in users:
                symp.users.append(usr)
            symp.app_users = list()
            for usr in app_users:
                symp.app_users.append(usr.id)
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
    print '5'
    return render_template('/consilium/index.pug', admin=current_user.admin, pagination=pagination, pictures=pics_list,
                           message=message, hideTest=hideTest, hideConf=hideConf, info=iForm, hideApp=hideApp, hideSecRec=hideSecRec)

@userApp.route('/consilium/', methods=['POST'], defaults={'page': 0})
@userApp.route('/consilium/<int:page>', methods=['POST'])
@login_required
def consilium_view_post(page):
    if (current_user.user_name == "demo"):
        return redirect(request.referrer)
    if not(current_user.admin):
        return redirect(request.referrer)
    form = request.form
    if(form.has_key('hideForm')):
        hideTest = False
        hideConf = False
        hideApp = False
        hideSecRec = False
        if (form.has_key('hideTest')):
            hideTest = True
        if (form.has_key('hideConf')):
            hideConf = True
        if (form.has_key('hideApp')):
            hideApp = True
        if (form.has_key('hideSecRec')):
            hideSecRec = True
        return redirect(url_for('consilium_view', hideTest=hideTest, hideConf=hideConf, hideApp=hideApp, hideSecRec=hideSecRec))
    if (form.has_key('user') and form.has_key('message') and form.has_key('pic')):
        app = Appoint.Appoint()
        app.user_id = form['user']
        app.secondary = True
        app.pic_id = form['pic']
        app.date = datetime.datetime.now().date()
        app.message = form['message']
        db.session.add(app)
        db.session.commit()
        # hide = False
        # if (form.has_key('hide')):
        #     hide = form.has_key('hide')
        # return redirect(url_for('consilium_view', page=page, hidden=hide))
        return redirect(request.referrer)
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


@userApp.route('/consilium/stats')
@login_required
def consilium_stats():
    if not(current_user.admin):
        return redirect('/')
    logging.info("ConsiliumStats")
    usercons = db.session.query(Usercons.Usercons.user_id)
    cons_pics = db.session.query(Consdata.Consdata.pic_id).group_by(Consdata.Consdata.pic_id).all()
    cons_pics_count = len(list(db.session.query(Consdata.Consdata.pic_id).group_by(Consdata.Consdata.pic_id).all()))
    pics_by_cons = db.session.query(Consnames.Consnames.cons_name, db.func.count(Consdata.Consdata.pic_id))\
        .join(Consdata.Consdata).group_by(Consnames.Consnames.cons_name, Consnames.Consnames.id)

    pics_by_symp = db.session.query(Symptom.Symptom.symptom_name, db.func.count(Recognized.Recognized.id).label('total')) \
        .join(Recognized.Recognized)\
        .filter(Recognized.Recognized.pic_id.in_(cons_pics), Recognized.Recognized.user_id.in_(usercons),
                Symptom.Symptom.diagnos==True) \
        .group_by(Symptom.Symptom.symptom_name).order_by(db.desc('total'))

    return render_template('/consilium/stats.pug', cons_pics=cons_pics_count, pics_by_cons= pics_by_cons, pics_by_symp=pics_by_symp, admin=current_user.admin)

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
    app_users = list()
    count = 0

class picsForm():
    pic = None
    symps = picSymps()
    consilium = list()
    secondary = False

class infoForm():
    cons_count = 0
    sec_app = 0
    cons_to_rec = 0