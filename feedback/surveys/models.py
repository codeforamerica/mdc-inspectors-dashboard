# -*- coding: utf-8 -*-
from feedback.database import (
    Column, db, Model
)
from feedback.surveys.constants import (
    ROLES, PERMIT_TYPE
)


class Stakeholder(Model):
    ''' Stakeholder model - each field contains a
    string of e-mails separated by commas.
    '''
    __tablename__ = 'stakeholders'

    id = Column(db.Integer, primary_key=True, index=True)
    email_list = Column(db.String(200), nullable=True)
    label = Column(db.String(50), unique=True, nullable=True)

    def __repr__(self):
        return '<Stakeholder(id:{0})>'.format(self.id)


class Survey(Model):
    ''' Survey model is the now the base for the PIC
    feedback survey. This is the result of ETLs from
    both Typeform and TextIt, both English and Spanish
    versions. We've decided to do it this way also
    because there now needs to be a record to save every
    time a form is filled.
    '''
    __tablename__ = 'survey'

    id = Column(db.Integer, primary_key=True, index=True)
    source_id = Column(db.String(50), nullable=False)
    lang = Column(db.String(2), nullable=False, default='en')
    method = Column(db.String(3), nullable=False)
    date_submitted = Column(db.DateTime, nullable=False, index=True)
    role = Column(db.Integer, nullable=False)
    rating = Column(db.Integer, nullable=False)
    get_done = Column(db.Boolean(), default=False)
    contact = Column(db.String(500), nullable=True)
    more_comments = Column(db.String(2000), nullable=True)
    follow_up = Column(db.Boolean(), default=False)
    permit_type = Column(db.Integer, nullable=True)
    know_to_pass = Column(db.Boolean(), default=False)

    @property
    def permit_type_en(self):
        try:
            return PERMIT_TYPE[self.permit_type]
        except KeyError:
            return self.permit_type

    @property
    def role_en(self):
        try:
            return ROLES[self.role]
        except KeyError:
            return self.role

    def __repr__(self):
        return '<Survey(id:{0} tracking:{1})>'.format(self.id, self.source_id)


def get_en(x, x_other, X_DICT):
    if x_other is None:
        try:
            return X_DICT[x]
        except KeyError:
            return x
    else:
        return x_other
