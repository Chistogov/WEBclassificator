# -*- coding: utf-8 -*-
from flask import render_template, request, redirect, url_for
from userApp import *
from userApp import Pagination
from userApp.dbc import User, db, Picture, Symptom, Recognized, Appoint, Cnnrec
from userApp.Service import appointService, journalService
from flask_login import login_required, current_user
import logging, datetime


@userApp.route('/appoint', methods=['GET'])
@login_required
def appoint():
    if not(current_user.admin):
        return redirect('/')
    message = ""
    if('message' in request.args):
        message = request.args['message']
    logging.info("appoint")
    all_pics = db.session.query(Picture.Picture).all()
    app_pics = db.session.query(Appoint.Appoint).all()
    rec_pics = db.session.query(Recognized.Recognized.pic_id).group_by(Recognized.Recognized.pic_id)
    pics_by_symp = db.session.query(Symptom.Symptom.symptom_name, Symptom.Symptom.ear, Symptom.Symptom.throat, Symptom.Symptom.nose, db.func.count(Recognized.Recognized.pic_id))\
        .join(Recognized.Recognized)\
        .group_by(Symptom.Symptom.symptom_name, Symptom.Symptom.nose, Symptom.Symptom.throat, Symptom.Symptom.ear)

    infoForm.all_pics = len(list(all_pics))
    infoForm.rec_pics = len(list(rec_pics))
    infoForm.app_pics = len(list(app_pics))
    infoForm.wait_pics = infoForm.all_pics-infoForm.rec_pics
    users = User.User.query.all()
    cnnrec_symps = db.session.query(Symptom.Symptom).filter(Cnnrec.Cnnrec.symp_id==Symptom.Symptom.id).group_by(Symptom.Symptom.id)
    for item in cnnrec_symps:
        print item.symptom_name
    return render_template('appoint.pug', infoForm=infoForm, pics_by_symp=pics_by_symp, users=users, message=message, admin=current_user.admin, cnnrec_symps=cnnrec_symps)

@userApp.route('/appoint', methods=['POST'])
@login_required
def appoint_post():
    if not(current_user.admin):
        return redirect('/')
    if(current_user.user_name == "demo"):
        return redirect(url_for('appoint', message="Demo user, read only"))
    form = request.form
    if(appointService.validateForm(form)):
        message = appointService.validateForm(form)
        return redirect(url_for('appoint', message=message))
    forUser = form['forUser']
    count = form['count']
    in_app = db.session.query(Appoint.Appoint.pic_id).filter(Appoint.Appoint.user_id == forUser)
    alredyrec = db.session.query(Recognized.Recognized.pic_id).filter(Recognized.Recognized.user_id == forUser)
    toCnnConf = False
    for item in form:
        if (item == 'fromRec'):
            if (form['fromUser'] != "0"):
                # oe = list(db.session.query(Recognized.Recognized.pic_id).filter(
                #     Recognized.Recognized.symp_id.in_([23, 37, 49, 53])))
                # rec = db.session.query(Recognized.Recognized.pic_id).filter(
                #     # Recognized.Recognized.user_id == form['fromUser'])
                #     Recognized.Recognized.symp_id == 20,
                #     db.func.DATE(Recognized.Recognized.date) > "2018-05-10")
                # pics = db.session.query(Picture.Picture).filter(Picture.Picture.id.in_(rec),
                #                                                 ~Picture.Picture.id.in_(in_app),
                #                                                 Picture.Picture.id.notin_(oe),
                #                                                 Picture.Picture.id.notin_(alredyrec)).limit(count)
                # appointService.toAppDb(pics, forUser)
                # return redirect('/appoint')
                rec = db.session.query(Recognized.Recognized.pic_id).filter(
                    Recognized.Recognized.user_id == form['fromUser'])
                pics = db.session.query(Picture.Picture).filter(Picture.Picture.id.in_(rec),
                                                                ~Picture.Picture.id.in_(in_app)).limit(count)
                appointService.toAppDb(pics, forUser, toCnnConf)
                return redirect('/appoint')
            else:
                rec = db.session.query(Recognized.Recognized.pic_id)
                pics = db.session.query(Picture.Picture).filter(Picture.Picture.id.in_(rec), ~Picture.Picture.id.in_(in_app)).limit(count)
                appointService.toAppDb(pics, forUser, toCnnConf)
                return redirect('/appoint')
        if (item == 'fromApp'):
            app = db.session.query(Appoint.Appoint.pic_id)
            pics = db.session.query(Picture.Picture).filter(Picture.Picture.id.in_(app), ~Picture.Picture.id.in_(in_app)).limit(count)
            appointService.toAppDb(pics, forUser, toCnnConf)
            return redirect('/appoint')
        if (item.isdigit()):
            if(form['cnnConf'] != 0):
                toCnnConf = True
                print 'toCnnConf'
            rec = db.session.query(Recognized.Recognized.pic_id)
            app = db.session.query(Appoint.Appoint.pic_id)
            ear = db.session.query(Cnnrec.Cnnrec.pic_id).filter(Cnnrec.Cnnrec.symp_id == item)
            pics = db.session.query(Picture.Picture).filter(~Picture.Picture.id.in_(rec), ~Picture.Picture.id.in_(app),
                                                            ~Picture.Picture.id.in_(in_app), Picture.Picture.id.in_(ear), Picture.Picture.skipped==False).limit(count)
            appointService.toAppDb(pics, forUser, toCnnConf)
            return redirect('/appoint')
    rec = db.session.query(Recognized.Recognized.pic_id)
    app = db.session.query(Appoint.Appoint.pic_id)
    pics = db.session.query(Picture.Picture).filter(~Picture.Picture.id.in_(rec), ~Picture.Picture.id.in_(app), ~Picture.Picture.id.in_(in_app)).limit(count)
    appointService.toAppDb(pics, forUser, toCnnConf)
    # journalService.newMessaage(forUser, "Назначены новые снимки (" + str(len(list(pics))) + " шт.)")
    #--------------------------------------
    # cnnrec = db.session.query(Cnnrec.Cnnrec.pic_id).filter(Cnnrec.Cnnrec.symp_id == 20)
    # recbad = list(db.session.query(Recognized.Recognized.pic_id).filter(Recognized.Recognized.symp_id.in_([23, 37, 49, 53])))
    # recnose = list(db.session.query(Recognized.Recognized.pic_id).filter(Recognized.Recognized.symp_id.in_([20])))
    # picnice = db.session.query(Picture.Picture.id).filter(Picture.Picture.id.notin_(recbad), Picture.Picture.id.in_(recnose))
    # rec = db.session.query(Recognized.Recognized.pic_id).filter(Recognized.Recognized.user_id == form['fromUser'], Recognized.Recognized.pic_id.in_(cnnrec), Recognized.Recognized.pic_id.in_(picnice))
    # pics = db.session.query(Picture.Picture).filter(Picture.Picture.id.in_(rec)).limit(1000)
    # appointService.toAppDb(pics, forUser)
    # journalService.newMessaage(forUser, "Назначены новые снимки (" + str(len(list(pics))) + " шт.)")
    #----------------------------------------
    return redirect('/appoint')

@userApp.route('/appointed/', defaults={'page': 0})
@userApp.route('/appointed/<path:path>/<int:page>')
@login_required
def app_view(path, page):
    app_user = path
    pics = db.session.query(Picture.Picture.pic_name, Picture.Picture.id, User.User.user_name)\
        .join(Appoint.Appoint, User.User) \
        .filter(Appoint.Appoint.user_id == app_user, Picture.Picture.id == Appoint.Appoint.pic_id) \
        .group_by(Picture.Picture.pic_name,  Picture.Picture.id,  User.User.user_name)
    count = len(list(pics))
    pics = get_pics_for_page(page, app_user)
    message = ""
    pagination = Pagination.Pagination(page, PER_PAGE, count)
    user = User.User.query.get(app_user)
    return render_template('/appoint/viewer.pug', admin=current_user.admin, pictures=pics, pagination=pagination, user=user)

@userApp.route('/appoint/<int:user>/<int:pic>')
@login_required
def user_pic_app(user, pic):
    if (current_user.user_name == "demo"):
        return redirect(request.referrer)
    if not(current_user.admin):
        return redirect('/')

    app = Appoint.Appoint()
    app.user_id = user
    app.secondary = True
    app.pic_id = pic
    app.date = datetime.datetime.now().date()
    db.session.add(app)
    db.session.commit()

    return redirect(request.referrer)

PER_PAGE = 21

def get_pics_for_page(page, app_user):
    pics = db.session.query(Picture.Picture.pic_name, Picture.Picture.id, User.User.user_name)\
        .join(Appoint.Appoint, User.User) \
        .filter(Appoint.Appoint.user_id == app_user, Picture.Picture.id == Appoint.Appoint.pic_id) \
        .group_by(Picture.Picture.pic_name,  Picture.Picture.id,  User.User.user_name)
    print str(len(list(pics)))
    if PER_PAGE:
        pics = pics.limit(PER_PAGE)
    print str(len(list(pics)))
    if page:
        pics = pics.offset(page * PER_PAGE)
    print str(len(list(pics)))
    return pics

@userApp.route('/pics/<int:pic>/<int:user>/appclear')
@login_required
def appclear_pic(pic, user):
    if (current_user.user_name == "demo"):
        return redirect(request.referrer)
    if not(current_user.admin):
        return redirect('/')

    db.session.query(Appoint.Appoint).filter(Appoint.Appoint.pic_id==pic, Appoint.Appoint.user_id==user).delete()
    db.session.commit()

    return redirect(request.referrer)

class infoForm():
    rec_pics = 0
    all_pics = 0
    wait_pics = 0
    app_pics = 0




