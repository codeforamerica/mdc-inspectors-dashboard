# -*- coding: utf-8 -*-
# DO NOT DELETE
import re
import StringIO
import csv

import datetime
today = datetime.date.today()

from flask import (
    Blueprint, make_response
)

from sqlalchemy import desc

from feedback.surveys.models import Survey


blueprint = Blueprint(
    'surveys',
    __name__,
    url_prefix='/surveys',
    static_folder="../static")


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

