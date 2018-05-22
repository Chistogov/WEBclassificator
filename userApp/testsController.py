# -*- coding: utf-8 -*-
from flask import render_template, request, redirect, url_for
from userApp import *
from userApp.dbc import User, db, Testresults, Datasets, Category, Confirmed, Picture, Symptom, Recognized, Usertests, Tests
from flask_login import login_required, current_user
import datetime
import logging, collections


@userApp.route('/tests', methods=['GET'])
@login_required
def tests():
    logging.info("tests")
    message = ""
    if ('message' in request.args):
        message = request.args['message']
    tests = db.session.query(Datasets.Datasets)
    user_tests = db.session.query(Tests.Tests).filter(Tests.Tests.user_id==current_user.id, Tests.Tests.results==None)
    if(current_user.admin):
        test_results = db.session.query(Tests.Tests).filter(Tests.Tests.results!=None)
    else:
        test_results = db.session.query(Tests.Tests).filter(Tests.Tests.results != None, Tests.Tests.user_id==current_user.id)
    return render_template('tests/index.pug', admin=current_user.admin, message=message, tests = tests,
                           results = test_results, user_tests=user_tests, user=current_user)

@userApp.route('/tests/<int:test>/<int:page>', methods=['GET'])
@login_required
def test_view(test, page):
    logging.info("tests")
    dataset=Datasets.Datasets.query.get(test)
    test_pics=db.session.query(Usertests.Usertests.pic_id).filter(Usertests.Usertests.dataset_id==dataset.id)
    pics = db.session.query(Picture.Picture).filter(Picture.Picture.id.in_(test_pics))
    count = len(list(pics))
    pics = get_pics_for_page(page, pics)
    pagination = Pagination.Pagination(page, PER_PAGE, count)
    return render_template('tests/test.pug', admin=current_user.admin, pictures=pics, pagination=pagination,
                           dataset=dataset, testid=test)


@userApp.route('/tests', methods=['POST'])
@login_required
def tests_add   ():
    if not(current_user.admin):
        return redirect('/')
    if(current_user.user_name == "demo"):
        return redirect(url_for('tests', message="Demo user, read only"))
    logging.info("Users Post")
    form = request.form
    if (form['testname'] == ""):
        return redirect(url_for('tests', message="Введите название теста"))
    dataset = Datasets.Datasets()
    dataset.dataset_name = form['testname']
    db.session.add(dataset)
    db.session.commit()
    return redirect(url_for('tests'))

@userApp.route('/tests/change/<int:page>', methods=['GET'])
@login_required
def tests_change(page):
    logging.info("tests_change")
    message = ""
    if ('message' in request.args):
        message = request.args['message']
    pics = db.session.query(Picture.Picture).filter(Confirmed.Confirmed.pic_id == Picture.Picture.id, Confirmed.Confirmed.user_id == current_user.id)
    count = len(list(pics))
    pics = get_pics_for_page(page, pics)
    pagination = Pagination.Pagination(page, PER_PAGE, count)
    tests = db.session.query(Datasets.Datasets)
    return render_template('tests/change.pug', admin=current_user.admin, message=message, tests = tests,
                           pagination=pagination, pictures=pics)

@userApp.route('/tests/<int:pic>/<int:test>/add')
@login_required
def tests_add_pic(pic, test):
    if (current_user.user_name == "demo"):
        return redirect(request.referrer)
    if not(current_user.admin):
        return redirect('/')

    confirmed = db.session.query(Confirmed.Confirmed).filter(Confirmed.Confirmed.pic_id == pic, Confirmed.Confirmed.user_id==current_user.id)
    for conf in confirmed:
        new_tag = Usertests.Usertests()
        new_tag.pic_id=pic
        new_tag.user_id=current_user.id
        rec = Recognized.Recognized.query.get(conf.rec_id)
        new_tag.symp_id=rec.symp_id
        new_tag.dataset_id=test
        exist = db.session.query(Usertests.Usertests).filter(Usertests.Usertests.pic_id == pic,
                                                             Usertests.Usertests.symp_id==rec.symp_id, Usertests.Usertests.dataset_id==test)
        if (len(list(exist)) == 0):
            db.session.add(new_tag)
    db.session.commit()

    return redirect(request.referrer)

@userApp.route('/tests/<int:pic>/<int:symp>/<int:dataset>/remove')
@login_required
def symp_remove_test(pic, symp, dataset):
    if (current_user.user_name == "demo"):
        return redirect(request.referrer)
    if not(current_user.admin):
        return redirect('/')
    db.session.query(Usertests.Usertests).filter(Usertests.Usertests.pic_id == pic,
                                                             Usertests.Usertests.symp_id==symp, Usertests.Usertests.dataset_id==dataset).delete()
    db.session.commit()
    return redirect(request.referrer)

# /tests/"~pic.id~"/"~dataset.id~"/pic_data_remove

@userApp.route('/tests/<int:pic>/<int:dataset>/pic_data_remove')
@login_required
def dataset_remove_test(pic, dataset):
    if (current_user.user_name == "demo"):
        return redirect(request.referrer)
    if not(current_user.admin):
        return redirect('/')
    db.session.query(Usertests.Usertests).filter(Usertests.Usertests.pic_id == pic, Usertests.Usertests.dataset_id==dataset).delete()
    db.session.commit()
    return redirect(request.referrer)

@userApp.route('/tests/users', methods=['GET'])
@login_required
def tests_users():
    logging.info("tests_users")
    message = ""
    if ('message' in request.args):
        message = request.args['message']
    tests = db.session.query(Datasets.Datasets)
    users = db.session.query(User.User)
    return render_template('tests/users.pug', admin=current_user.admin, message=message, tests = tests,users=users)\

@userApp.route('/tests/users', methods=['POST'])
@login_required
def tests_users_app():
    logging.info("tests_users")
    if (current_user.user_name == "demo"):
        return redirect(request.referrer)
    if not(current_user.admin):
        return redirect('/')
    form = request.form
    exists = db.session.query(Tests.Tests).filter(Tests.Tests.user_id==form['forUser'], Tests.Tests.dataset_id==form['test'], Tests.Tests.results==None)
    if(len(list(exists))!=0):
        return redirect(url_for('tests_users', message="Тест уже назначен"))
    new_tag = Tests.Tests()
    new_tag.user_id=form['forUser']
    new_tag.dataset_id = form['test']
    new_tag.date=datetime.datetime.now()
    db.session.add(new_tag)
    db.session.commit()
    return redirect('/tests/users')

@userApp.route('/tests/testing/<int:test>', methods=['GET'])
@login_required
def testing(test):
    logging.info('primary_rec')
    message = ""
    test_u = Tests.Tests.query.get(test)
    if(test_u.user_id != current_user.id):
        return redirect('/')
    dataset = db.session.query(Tests.Tests).filter(Tests.Tests.id == test).first()
    results = db.session.query(Testresults.Testresults.pic_id).filter(Testresults.Testresults.test_id == test)
    pics_in_wait = db.session.query(Picture.Picture).filter(Picture.Picture.id == Usertests.Usertests.pic_id,
                                                            Usertests.Usertests.dataset_id == dataset.dataset_id,
                                                            Picture.Picture.id.notin_(results))
    all_pics = db.session.query(Picture.Picture).filter(Picture.Picture.id == Usertests.Usertests.pic_id,
                                                            Usertests.Usertests.dataset_id == dataset.dataset_id)
    if(len(list(pics_in_wait))==0):
        test_c = Tests.Tests.query.get(test)
        test_result = Tests.Tests.query.get(test)
        all_test_pics = db.session.query(Usertests.Usertests.pic_id).filter(
            Usertests.Usertests.dataset_id == test_result.dataset_id).group_by(Usertests.Usertests.pic_id)
        i = 0
        summary_percentage_d = 0.0
        for pic in list(all_test_pics):

            test_app_d = db.session.query(Symptom.Symptom.symptom_name).filter(
                Usertests.Usertests.symp_id == Symptom.Symptom.id,
                Usertests.Usertests.dataset_id == test_result.dataset_id,
                Usertests.Usertests.pic_id == pic.pic_id,
                Symptom.Symptom.diagnos == True)

            user_result_d = db.session.query(Symptom.Symptom.symptom_name).filter(
                Testresults.Testresults.symp_id == Symptom.Symptom.id,
                Testresults.Testresults.test_id == test,
                Testresults.Testresults.pic_id == pic.pic_id,
                Symptom.Symptom.diagnos == True)

            minus_d = list(set(list(test_app_d)) - set(list(user_result_d)))
            plus_d = list(set(list(user_result_d)) - set(list(test_app_d)))
            trues_d = list(set(list(user_result_d)) & set(list(test_app_d)))

            percentage_d = (100 / (len(list(minus_d)) + len(list(plus_d)) + len(list(trues_d)))) * len(
                list(trues_d))
            if (percentage_d > 0):
                percentage_d = 100
            i += 1
            summary_percentage_d = summary_percentage_d + percentage_d

        summary_percentage_d = summary_percentage_d / i
        summary_percentage_d = round(summary_percentage_d, 2)
        test_c.results = summary_percentage_d
        test_c.date = datetime.datetime.now()
        db.session.commit()
        message="Тестирование завершено"
    symptoms = Symptom.Symptom.query.order_by(Symptom.Symptom.id)
    categories = Category.Category.query.order_by(Category.Category.id).all()

    if ('message' in request.args):
        message = request.args['message']
    return render_template('tests/testing.pug', symptoms=symptoms,
                           admin=current_user.admin,
                           message=message, categories=categories,
                           picture = pics_in_wait.first(), pic_wait=len(list(pics_in_wait)),
                           pic_ready=len(list(all_pics))-len(list(pics_in_wait)))

@userApp.route('/tests/testing/<int:test>', methods=['POST'])
@login_required
def testing_post(test):
    if(current_user.user_name == "demo"):
        return redirect(url_for('sec_rec', message="Demo user, read only"))
    form = request.form
    if(form.has_key('picture')):
        for item in form:
            if(item.isdigit()):
                new_tag = Testresults.Testresults()
                new_tag.user_id=current_user.id
                new_tag.symp_id=item
                new_tag.pic_id=form['picture']
                new_tag.test_id=test
                new_tag.timer=form['timer']
                new_tag.date=datetime.datetime.now()
                db.session.add(new_tag)
        db.session.commit()


    return redirect('/tests/testing/'+str(test))

@userApp.route('/tests/results/<int:test>/<int:page>', methods=['GET'])
@login_required
def test_results(test, page):
    logging.info("tests")
    test_result=Tests.Tests.query.get(test)
    test_user=User.User.query.get(test_result.user_id)
    dataset=Datasets.Datasets.query.get(test_result.dataset_id)
    all_test_pics=db.session.query(Usertests.Usertests.pic_id).filter(Usertests.Usertests.dataset_id==test_result.dataset_id).group_by(Usertests.Usertests.pic_id)
    mistakes = list()
    mistake_pics = list()
    i = 0
    summary_percentage_v = 0.0
    summary_percentage_d = 0.0
    for pic in list(all_test_pics):

        test_app = db.session.query(Symptom.Symptom.symptom_name).filter(
            Usertests.Usertests.symp_id == Symptom.Symptom.id,
            Usertests.Usertests.dataset_id == test_result.dataset_id,
            Usertests.Usertests.pic_id==pic.pic_id)
        user_result = db.session.query(Symptom.Symptom.symptom_name).filter(
            Testresults.Testresults.symp_id == Symptom.Symptom.id,
            Testresults.Testresults.test_id == test,
            Testresults.Testresults.pic_id==pic.pic_id)
        test_app_v = db.session.query(Symptom.Symptom.symptom_name).filter(
            Usertests.Usertests.symp_id == Symptom.Symptom.id,
            Usertests.Usertests.dataset_id == test_result.dataset_id,
            Usertests.Usertests.pic_id==pic.pic_id,
            Symptom.Symptom.diagnos == False)
        test_app_d = db.session.query(Symptom.Symptom.symptom_name).filter(
            Usertests.Usertests.symp_id == Symptom.Symptom.id,
            Usertests.Usertests.dataset_id == test_result.dataset_id,
            Usertests.Usertests.pic_id==pic.pic_id,
            Symptom.Symptom.diagnos == True)
        user_result_v = db.session.query(Symptom.Symptom.symptom_name).filter(
            Testresults.Testresults.symp_id == Symptom.Symptom.id,
            Testresults.Testresults.test_id == test,
            Testresults.Testresults.pic_id==pic.pic_id,
            Symptom.Symptom.diagnos == False)
        user_result_d = db.session.query(Symptom.Symptom.symptom_name).filter(
            Testresults.Testresults.symp_id == Symptom.Symptom.id,
            Testresults.Testresults.test_id == test,
            Testresults.Testresults.pic_id==pic.pic_id,
            Symptom.Symptom.diagnos == True)
        mistake = user_mistakes()
        mistake.pic_id=pic.pic_id
        mistake.minus = list(set(list(test_app)) - set(list(user_result)))
        mistake.plus = list(set(list(user_result)) - set(list(test_app)))
        mistake.trues = list(set(list(user_result)) & set(list(test_app)))

        minus_v = list(set(list(test_app_v)) - set(list(user_result_v)))
        plus_v = list(set(list(user_result_v)) - set(list(test_app_v)))
        trues_v = list(set(list(user_result_v)) & set(list(test_app_v)))

        minus_d = list(set(list(test_app_d)) - set(list(user_result_d)))
        plus_d = list(set(list(user_result_d)) - set(list(test_app_d)))
        trues_d = list(set(list(user_result_d)) & set(list(test_app_d)))

        mistake.percentage_v = (100/(len(list(minus_v))+len(list(plus_v))+len(list(trues_v))))*len(list(trues_v))
        i+=1
        summary_percentage_v = summary_percentage_v+mistake.percentage_v
        mistake.percentage_d = (100 / (len(list(minus_d)) + len(list(plus_d)) + len(list(trues_d)))) * len(list(trues_d))
        if(mistake.percentage_d>0):
            mistake.percentage_d = 100
        summary_percentage_d = summary_percentage_d + mistake.percentage_d
        if(len(mistake.plus) + len(mistake.minus) + len(mistake.trues) != 0):
            mistakes.append(mistake)
            mistake_pics.append(pic.pic_id)
    summary_percentage_v = summary_percentage_v/i
    summary_percentage_v = round(summary_percentage_v,2)
    summary_percentage_d = summary_percentage_d / i
    summary_percentage_d = round(summary_percentage_d, 2)
    pics = db.session.query(Picture.Picture).filter(Picture.Picture.id.in_(mistake_pics))
    count = len(list(pics))
    pics = get_pics_for_page(page, pics)
    pagination = Pagination.Pagination(page, PER_PAGE, count)
    testresult = db.session.query(db.func.max(Testresults.Testresults.date), db.func.min(Testresults.Testresults.date)).filter(
        Testresults.Testresults.test_id == test).first()
    time_rec = testresult[0] - testresult[1]

    return render_template('tests/results.pug', admin=current_user.admin, pictures=pics, pagination=pagination,
                           mistakes=mistakes, testid=test, dataset=dataset, rec_user=test_user, time_rec=time_rec,
                           summary_percentage_v=summary_percentage_v, summary_percentage_d=summary_percentage_d)

PER_PAGE = 12

def get_pics_for_page(page, pics):
    pics = pics.group_by(Picture.Picture.id)
    if PER_PAGE:
        pics = pics.limit(PER_PAGE)
    if page:
        pics = pics.offset(page * PER_PAGE)
    return pics

class user_mistakes():
    pic_id = ""
    minus = list()
    plus = list()
    trues = list()
    percentage_v = 0.0
    percentage_d = 0.0