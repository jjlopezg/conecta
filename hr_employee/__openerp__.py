# -*- coding: utf-8 -*-
###########################################################################
#
# © 2016 Juan Jose Lopez Garcia <jjlopezg74@gmail.com>.
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
###########################################################################
{
    'name': 'Proyecto Conecta - Empleados',
    'version': '9.0.1.0.0',
    'author': 'JJLopezG',
    'website': 'http://www.tuconecta.es',
    'license': 'AGPL-3',
    'category': 'Human Resources',
    'summary': '',
    'installable': True,
    'application': False,
    'auto_install': False,
    'description': """
Empleados
=========
    """,
    "depends" : [
        'base',
        'hr'
    ],
    "data" : [
        "security/ir.model.access.csv",

        "data/hr.identification.csv",

        "views/hr_employee_view.xml",
        "views/hr_employee_bank_view.xml",
        "views/hr_identification_view.xml",

        'hr_employee_sequence.xml',
    ],
}
