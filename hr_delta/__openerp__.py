# -*- coding: utf-8 -*-
###########################################################################
#
# © 2016 Juan Jose Lopez Garcia <jjlopezg74@gmail.com>.
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
###########################################################################
{
    'name': 'Declaración Electronica de Trabajadores Accidentados',
    'version': '9.0.1.0.0',
    'author': 'Juan Jose Lopez Garcia',
    'website': 'http://www.tuconecta.es',
    'license': 'AGPL-3',
    'category': 'Human Resources',
    'summary': '',
    'installable': True,
    'application': False,
    'auto_install': False,
    'description': """
    """,
    'images': [
        'images/delta.jpeg'
    ],
    "depends" : [
        'base',
        'hr',
        'hr_contract',
        'report_xml',
        'web_widget_timepicker',
    ],
    "data" : [
        'data/hr.delta.type.csv',
        'data/hr.delta.type.work.csv',
        'data/hr.delta.form.csv',
        'data/hr.delta.desv.csv',
        'data/hr.delta.agen.csv',
        'data/hr.delta.actv.csv',
        'security/ir.model.access.csv',

        "wizard/create_delta_view.xml",
        'report/report_delta.xml',
        'views/hr_delta_view.xml',

    ],
}