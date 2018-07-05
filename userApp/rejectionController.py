# -*- coding: utf-8 -*-
from flask import render_template, request, redirect, url_for
from userApp import *
from userApp.dbc import User, db, Picture, Symptom, Recognized, Confirmed, Category, Appoint
from flask_login import login_required, current_user
import logging, datetime


@userApp.route('/rejection', methods=['GET'])
@login_required
def rejection():
    if not(current_user.admin):
        return redirect('/')
    message = ""
    if('message' in request.args):
        message = request.args['message']
    logging.info("appoint")
    symptoms = db.session.query(Symptom.Symptom)
    categories = Category.Category.query.order_by(Category.Category.id).all()
    users = User.User.query.all()
    return render_template('rejection.pug', symptoms=symptoms, users=users, message=message,
                           categories=categories,admin=current_user.admin)

@userApp.route('/rejection', methods=['POST'])
@login_required
def rejection_post():
    if not(current_user.admin):
        return redirect('/')
    if(current_user.user_name == "demo"):
        return redirect(url_for('rejection', message="Demo user, read only"))
    symptoms = list()
    form = request.form
    for item in form:
        if (item.isdigit()):
            symptoms.append(item)

    pics = db.session.query(Picture.Picture).join(Recognized.Recognized)
    if (len(symptoms) != 0):
        for item in symptoms:
            rec = list(db.session.query(Recognized.Recognized.pic_id).filter(Recognized.Recognized.symp_id == item))
            pics = pics.filter(Picture.Picture.id.in_(rec))
            print str(len(list(pics)))
    if (form.has_key('opticalExclude')):
        rec = list(db.session.query(Recognized.Recognized.pic_id).filter(Recognized.Recognized.symp_id.in_([23,37,49,53])))
        pics = pics.filter(Picture.Picture.id.notin_(rec))
    if (form.has_key('forUser')):
        pics = pics.filter(Recognized.Recognized.user_id == form['forUser'])
    if (form['dateRec']):
        date = datetime.datetime.strptime(form['dateRec'], "%Y-%m-%d")
        pics = pics.filter(db.func.DATE(Recognized.Recognized.date) == date)

    conf = db.session.query(Confirmed.Confirmed).filter(Confirmed.Confirmed.user_id==current_user.id)
    conflist = list()
    for item in conf:
        conflist.append(item.recognized.pic_id)
    # pics = pics.filter(Picture.Picture.id.notin_(conflist))

    picslist = list()
    for item in pics:
        picslist.append(item.id)
    symp_type = ""
    if (form['type']):
        symp_type = form['type']
    return redirect(url_for('rejection_search', page=0, p=picslist, symp_type=symp_type, user_owner=form['forUser']))


# @userApp.route('/rejection/submit/<int:pic>')
# @login_required
# def pic_submit(pic):
#     if (current_user.user_name == "demo"):
#         return redirect(request.referrer)
#     if not(current_user.admin):
#         return redirect('/')
#     recs = db.session.query(Recognized.Recognized).filter(Recognized.Recognized.pic_id == pic)
#
#     conf = db.session.query(Confirmed.Confirmed).filter(Confirmed.Confirmed.user_id == current_user.id)
#     for item in conf:
#         if (item.recognized.pic_id==pic):
#             print ("Double Click Error")
#             return redirect(request.referrer)
#
#     for rec in recs:
#         confirmed = Confirmed.Confirmed()
#         confirmed.user_id = current_user.id
#         confirmed.rec_id = rec.id
#         confirmed.date = datetime.datetime.now()
#         confirmed.pic_id = rec.pic_id
#         db.session.add(confirmed)
#         db.session.commit()
#     return redirect(request.referrer)

# @userApp.route('/rejection/submit/<int:pic>/<int:user_id>')
# @login_required
# def pic_submit_user(pic, user_id):
#     if (current_user.user_name == "demo"):
#         return redirect(request.referrer)
#     if not(current_user.admin):
#         return redirect('/')
#     recs = db.session.query(Recognized.Recognized).filter(Recognized.Recognized.pic_id == pic, Recognized.Recognized.user_id == user_id)
#
#     conf = db.session.query(Confirmed.Confirmed).filter(Confirmed.Confirmed.user_id == current_user.id)
#     for item in conf:
#         if (item.recognized.pic_id==pic):
#             print ("Double Click Error")
#             return redirect(request.referrer)
#
#     for rec in recs:
#         confirmed = Confirmed.Confirmed()
#         confirmed.user_id = current_user.id
#         confirmed.rec_id = rec.id
#         confirmed.date = datetime.datetime.now()
#         confirmed.pic_id = rec.pic_id
#         db.session.add(confirmed)
#         db.session.commit()
#     return redirect(request.referrer)

@userApp.route('/user_day_rec/<int:user_id>/<string:date>', methods=['GET'])
@login_required
def user_day_rec(user_id, date):
    if not(current_user.admin):
        return redirect(request.referrer)
    if(current_user.user_name == "demo"):
        return redirect(url_for('rejection', message="Demo user, read only"))

    pics = db.session.query(Picture.Picture).join(Recognized.Recognized)
    pics = pics.filter(Recognized.Recognized.user_id == user_id)
    date = datetime.datetime.strptime(date, "%Y-%m-%d")
    pics = pics.filter(db.func.DATE(Recognized.Recognized.date) == date)
    picslist = list()
    for item in pics:
        picslist.append(item.id)

    return redirect(url_for('rejection_search', page=0, p=picslist, user_owner=user_id))

PER_PAGE = 12

@userApp.route('/rejection/search', methods=['POST'])
@login_required
def rejection_search_post():
    if (current_user.user_name == "demo"):
        return redirect(request.referrer)
    if not(current_user.admin):
        return redirect(request.referrer)
    form = request.form
    if (form.has_key('user') and form.has_key('message') and form.has_key('pic')):
        print "app"
        app = Appoint.Appoint()
        app.user_id = form['user']
        app.secondary = True
        app.pic_id = form['pic']
        app.date = datetime.datetime.now().date()
        app.message = form['message']
        db.session.add(app)
        db.session.commit()
        return redirect(request.referrer)
    if (form.has_key('rec_pic')):
        if(form.has_key('user')):
            for i in db.session.query(Recognized.Recognized).filter(Recognized.Recognized.user_id==form['user'], Recognized.Recognized.pic_id==form['rec_pic']):
                db.session.query(Confirmed.Confirmed).filter(Confirmed.Confirmed.rec_id == i.id).delete()
                db.session.commit()
        for item in form:
            if (item.isdigit()):
                confirmed = Confirmed.Confirmed()
                confirmed.user_id = current_user.id
                confirmed.rec_id = item
                print "qwr"+str(item)
                confirmed.date = datetime.datetime.now()
                confirmed.pic_id = form['rec_pic']
                db.session.add(confirmed)
                db.session.commit()
        return redirect(request.referrer)
    return redirect(request.referrer)


@userApp.route('/rejection/search', methods=['GET'])
@login_required
def rejection_search():
    page=int(request.args.get('page'))
    picslist = request.args.getlist('p')
    user_owner = request.args.get('user_owner')
    pics = db.session.query(Picture.Picture).filter(Picture.Picture.id.in_(picslist))
    # print "rejection_search " + user_owner
    count = len(list(pics))
    pics = get_pics_for_page(page, pics)
    picForms = list()
    for pic in pics:
        picForm = picsForm()
        picForm.pic=pic
        user = db.session.query(User.User).get(user_owner)
        picForm.symps = list()
        picForm.user = user
        picForm.recs = list()
        picForm.confRecs = list()
        recs = db.session.query(Recognized.Recognized).filter(Recognized.Recognized.user_id==user.id, Recognized.Recognized.pic_id == pic.id)
        recsids = list()
        for rec in recs:
            recsids.append(rec.id)
            picForm.recs = recs
        conf = db.session.query(Confirmed.Confirmed.rec_id).filter(Confirmed.Confirmed.rec_id.in_(recsids))
        recsids = list()
        for rec in conf:
            recsids.append(rec.rec_id)
        picForm.confRecs = recsids

        picForms.append(picForm)
    pagination = Pagination.Pagination(page, PER_PAGE, count)

    if not(user_owner):
        user_owner=0
    return render_template('/rejection/pics.pug', admin=current_user.admin, pictures=picForms,
                           pagination=pagination, request=request, user_owner=int(user_owner))

def get_pics_for_page(page, pics):
    pics = pics.group_by(Picture.Picture.id)
    if PER_PAGE:
        pics = pics.limit(PER_PAGE)
    if page:
        pics = pics.offset(page * PER_PAGE)
    return pics

class picsForm():
    pic = None
    user = None
    recs = list()
    confRecs = list()