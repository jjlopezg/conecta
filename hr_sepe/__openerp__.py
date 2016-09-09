# -*- encoding: utf-8 -*-
###########################################################################
#
# © 2016 Juan Jose Lopez Garcia <jjlopezg74@gmail.com>.
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
###########################################################################

{
    'name': 'Proyecto Conecta - Contrat@',
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
Servicion Empleo Publico Español
==========================================
* COMUNICACIONES
* EVALUACION DE LAS COMUNICACIONES

""",
    "depends" : [
                'hr',
                'hr_employee',
                'hr_contract',
                'hr_contract_es',
                'report_xml',
                ],
    "data" : [
#        "security/ir.model.access.csv",
        'data/hr.sepe.terrores.csv',

        'views/hr_sepe_view.xml',
        'views/hr_contract_view.xml',

        'report/report_contract.xml',
        'report/report_prorogation.xml',

        "wizard/hr_sepe_create_view.xml",
        "wizard/hr_sepe_eval_view.xml",
    ],
}
