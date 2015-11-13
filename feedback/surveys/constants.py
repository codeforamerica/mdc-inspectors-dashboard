 # -*- coding: utf-8 -*-

SURVEY_DAYS = 30

ROLES = {}
# FIXME: VERIFY CONSTANTS AGAINST V4 TEXTIT
ROLES[1] = 'Contractor'
ROLES[2] = 'Architect/Engineer'
ROLES[3] = 'Permit Consultant'
ROLES[4] = 'Homeowner'
ROLES[5] = 'Business Owner'
ROLES['Contractor'] = 1
ROLES['Contratista'] = 1
ROLES['Architect/Engineer'] = 2
ROLES['Arquitecto/Ingeniero'] = 2
ROLES['Permit Consultant'] = 3
ROLES['Consultor de Permiso'] = 3
ROLES['Homeowner'] = 4
ROLES[u'Dueño/a de Casa'] = 4
ROLES['Business Owner'] = 5
ROLES[u'Dueño/a de Negocio'] = 5

TF = {}

TF['LANG_EN'] = 'list_13579055_choice'
TF['ROLE_EN'] = 'list_13579056_choice'
TF['ROLE_ES'] = 'list_13579060_choice'

TF['OPINION_EN'] = 'opinionscale_13579066'
TF['OPINION_ES'] = 'opinionscale_13579067'

TF['GETDONE_EN'] = 'yesno_13579068'
TF['GETDONE_ES'] = 'yesno_13579070'

TF['COMMENTS_EN'] = 'textarea_13579074'
TF['COMMENTS_ES'] = 'textarea_13579075'

TF['TYPE_EN'] = 'list_13579058_choice'
TF['TYPE_ES'] = 'list_13579062_choice'

TF['FOLLOWUP_EN'] = 'yesno_13579069'
TF['FOLLOWUP_ES'] = 'yesno_13579071'
TF['CONTACT_EN'] = 'textfield_13579072'
TF['CONTACT_ES'] = 'textfield_13579073'
