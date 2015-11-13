"""
This script should run daily to:
"""
import arrow
import requests

from flask import render_template, current_app

from feedback.app import create_app
from feedback.settings import DevelopmentConfig
from feedback.surveys.models import Stakeholder
from feedback.surveys.serializers import (
    pic_schema, DataLoader
)

from feedback.surveys.constants import (
    TF, SURVEY_DAYS, ROLES
)
from feedback.dashboard.vendorsurveys import (
    fill_values
)
from feedback.utils import send_email


def date_to_db(str1):
    ''' Takes the string date format of various APIs
    to convert them into a format the postgres is
    okay with. Returns as a string.
    '''
    DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"
    return arrow.get(str1).strftime(DATE_FORMAT)


def call_web(ts):
    ''' Call the WEB API, which in this case is
    Typeform. Accepts an timestamp (Arrow object)
    as an argument, then pulls Return the
    result in json.
    '''
    API = 'https://api.typeform.com/v0/form/' + current_app.config.get('TF_ID') + '?key=' + current_app.config.get('TF_KEY') + '&completed=true&since=' + str(ts.timestamp)
    print API
    response = requests.get(API)

    return response.json()


def etl_web_data(ts):
    ''' Take the Typeform API and ETL it to a common
    standard we can do dashboard stats for.

    Returns a list of objects, each object being
    a survey.
    '''
    data = []
    json = call_web(ts)

    for resp in json['responses']:
        answers_arr = resp['answers']

        obj = {'method': 'web'}
        if "English" in answers_arr[TF['LANG_EN']]:
            obj['lang'] = 'en'
        else:
            obj['lang'] = 'es'

        obj['source_id'] = 'WEB-' + resp['id']

        temp = resp['metadata']['date_submit']
        obj['date_submitted'] = date_to_db(temp)

        obj['get_done'] = fill_values(answers_arr, TF['GETDONE_EN'], TF['GETDONE_ES'])
        obj['rating'] = int(fill_values(answers_arr, TF['OPINION_EN'], TF['OPINION_ES']))

        obj['follow_up'] = fill_values(answers_arr, TF['FOLLOWUP_EN'], TF['FOLLOWUP_ES'])
        obj['permit_type'] = fill_values(answers_arr, TF['TYPE_EN'], TF['TYPE_ES'])
        obj['contact'] = fill_values(answers_arr, TF['CONTACT_EN'], TF['CONTACT_ES'])
        obj['more_comments'] = fill_values(answers_arr, TF['COMMENTS_EN'], TF['COMMENTS_ES'])
        obj['role'] = ROLES[
            fill_values(
                answers_arr,
                TF['ROLE_EN'],
                TF['ROLE_ES'])]

        data.append(obj)
    # print data
    return data


def follow_up(models):
    ''' Inputs a bunch of survey models, go through
    each of them, figuring out if they require
    follow-ups and then e-mail the appropriate
    directors.

    Returns ..?
    '''
    subj = 'Miami-Dade County Permit Inspection Center Survey'
    from_email = 'mdcfeedbackdev@gmail.com'
    for survey in models:

        if survey.follow_up:
            stakeholder = Stakeholder.query.get(survey.route)
            if stakeholder is None or stakeholder.email_list is None:
                current_app.logger.info(
                    'NOSTAKEHOLDER | Route: {}\nSurvey Submitted Date: {}\nSubject: {}'.format(
                        survey.route_en,
                        survey.date_submitted,
                        subj
                    )
                )
            else:
                send_email(
                    subj,
                    from_email,
                    stakeholder.email_list,
                    render_template(
                        'email/followup_notification.txt',
                        survey=survey
                    ),
                    render_template(
                        'email/followup_notification.html',
                        survey=survey
                    ))


def load_data():
    timestamp = arrow.utcnow()
    timestamp = timestamp.replace(days=-SURVEY_DAYS)

    tf = etl_web_data(timestamp)
    data = tf

    loader = DataLoader(pic_schema)

    for row in data:
        loader.slice_and_add(row)

    db_models = loader.save_models_or_report_errors()
    follow_up(db_models)


def run():
    app = create_app()
    with app.app_context():
        load_data()

if __name__ == '__main__':
    run()
