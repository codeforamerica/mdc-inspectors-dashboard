# -*- coding: utf-8 -*-
# DO NOT DELETE
import re
import StringIO
import csv

import datetime
today = datetime.date.today()

from flask import (
    Blueprint, render_template,
    flash, request, redirect, url_for,
    make_response, json
)

from sqlalchemy import desc
from feedback.database import db
from feedback.decorators import requires_roles

from feedback.surveys.models import Stakeholder, Survey


blueprint = Blueprint(
    'surveys',
    __name__,
    url_prefix='/surveys',
    static_folder="../static")


def is_valid_email_list(value):

    value = [item.strip() for item in value.split(',') if item.strip()]
    email_list = list(set(value))

    for item in email_list:
        if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", item):
            flash("{0} is not a valid e-mail address.".format(item), "alert-danger")
            return False
    return True


def process_stakeholders_form(form):
    errors = False

    for i in range(1, 15):
        label = ROUTES[i]
        key = 'field-route-' + str(i)
        value = request.form[key]

        if is_valid_email_list(value):
            stakeholder = Stakeholder.query.filter_by(label=label).first()
            if not stakeholder:
                stakeholder = Stakeholder(
                    label=label,
                    email_list=value
                )
            else:
                stakeholder.update(
                    email_list=value
                )
            db.session.add(stakeholder)
        else:
            errors = True
            db.session.rollback()

    if not errors:
        db.session.commit()
        flash("Your settings have been saved!", "alert-success")
        return redirect(url_for('user.user_manage'))
    else:
        return redirect(url_for('user.user_manage'))


@blueprint.route('/', methods=['GET', 'POST'])
@requires_roles('admin')
def survey_index():
    # from here figure out if you posted the form
    if request.method == 'POST':
        return process_stakeholders_form(request.form)

    stakeholders = Stakeholder.query.order_by(Stakeholder.id).all()
    return render_template(
        "surveys/edit-stakeholders.html",
        routes=ROUTES,
        date=today.strftime('%B %d, %Y'),
        stakeholders=stakeholders)


@blueprint.route('/download')
def to_csv():
    csvList = []
    csvList.append([
        'date_submitted',
        'method',
        'language',
        'rating',
        'role',
        'get_done',
        'purpose',
        'improvement',
        'follow_up',
        'contact',
        'more_comments'])

    survey_models = Survey.query.order_by(desc(Survey.date_submitted)).all()
    for survey_model in survey_models:
        csvList.append([
            survey_model.date_submitted,
            survey_model.method,
            survey_model.lang,
            survey_model.rating,
            survey_model.role_en,
            survey_model.get_done,
            survey_model.purpose_en,
            survey_model.improvement,
            survey_model.follow_up,
            survey_model.contact,
            survey_model.more_comments])

    strIO = StringIO.StringIO()
    writer = csv.writer(strIO)
    writer.writerows(csvList)

    output = make_response(strIO.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
    return output


@blueprint.route("/webhook", methods=['GET', 'POST'])
def webhook():
    ''' How to test this on localhost, since I had to do some digging:
    1. Run the server locally in one tab (python manage.py server)
    2. In another tab try:
       curl -H "Content-Type: application/json" -X POST -d typeform-request.json http://127.0.0.1:9000/surveys/webhook
    TIP: Resty may help: https://github.com/micha/resty. Once you do that you can do the following:
    Tab 1: resty http://127.0.0.1:9000 -H "Content-Type: application/json"
    Tab 2: POST /surveys/webhook < typeform-request.json
    '''
    if request.method == 'POST':
        try:
            payload = json.loads(request.data)
            print ("HTTP/1.1 200 OK")
            print (payload)
            return 'OK'
        except:
            pass
    else:
        # Probably raise an error of some sort or redirect
        print ('GETS HERE FWIW')
