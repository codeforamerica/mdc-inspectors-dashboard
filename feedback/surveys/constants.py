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

PERMIT_TYPE = {}
PERMIT_TYPE[1] = 'Building / Roofing / Structural'
PERMIT_TYPE[2] = 'Electrical'
PERMIT_TYPE[3] = 'Environment (DERM)'
PERMIT_TYPE[4] = 'Fire'
PERMIT_TYPE[5] = 'Mechanical'
PERMIT_TYPE[6] = 'Plumbing'
PERMIT_TYPE[7] = 'Zoning'
PERMIT_TYPE['Building / Roofing / Structural'] = 1
PERMIT_TYPE['Electrical'] = 2
PERMIT_TYPE['Environment (DERM)'] = 3
PERMIT_TYPE['Fire'] = 4
PERMIT_TYPE['Mechanical'] = 5
PERMIT_TYPE['Plumbing'] = 6
PERMIT_TYPE['Zoning'] = 7
PERMIT_TYPE['Edificio / Techos'] = 1
PERMIT_TYPE[u'Eléctrico'] = 2
PERMIT_TYPE[u'Gestión de Recursos Ambientales (DERM)'] = 3
PERMIT_TYPE['Fuego'] = 4
PERMIT_TYPE[u'Mecánica'] = 5
PERMIT_TYPE[u'Plomería'] = 6
PERMIT_TYPE[u'Zonificación'] = 7
