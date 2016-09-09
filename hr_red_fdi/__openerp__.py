# -*- encoding: utf-8 -*-
###########################################################################
#
# © 2016 Juan Jose Lopez Garcia <jjlopezg74@gmail.com>.
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
###########################################################################
{
    'name': 'Proyecto Conecta - Mensajes FDI',
    'version': '9.0.1.0.0',
    'author': 'JJLopezG',
    'website': 'http://www.tuconecta.es',
    'license': 'AGPL-3',
    'category': 'Human Resources',
    'summary': '',
    'installable': True,
    'application': False,
    'auto_install': False,
    'description':
"""
Sistema RED de la Seguridad Social
=====================================
* FDI
* COMUNICACION
* EVALUACION DE LA COMUNICACION

""",
    "depends" : [
                'hr',
                'hr_contract',
                'hr_contract_es',
                ],
    "data" : [
        'data/hr.red.fdi.type.csv',
        'data/hr.red.fdi.type.to.csv',
#        "security/ir.model.access.csv",
        'views/hr_red_view.xml',
        'views/hr_red_fdi_view.xml',
        'views/hr_contract_view.xml',

        'report/report_fdi.xml',

        'wizard/hr_red_create_fdi_view.xml',
        'wizard/hr_red_fdi_eval_view.xml',
    ],
}
