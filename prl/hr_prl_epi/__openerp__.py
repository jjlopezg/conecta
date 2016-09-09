#-*- coding:utf-8 -*-
###########################################################################
#
# © 2016 Juan Jose Lopez Garcia <jjlopezg74@gmail.com>.
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
###########################################################################
{
    'name': 'Prevencion riesgos laborales - Accion Formativa',
    'version': '1.0.0',
    'author': 'Juan Jose Lopez Garcia',
    'website': 'http://',
    'license': 'AGPL-3',
    'category': 'Human Resources',
    'summary': '',
    'description': """
    """,
    'images': ['images/training.jpeg'],
    "depends" : ['base','hr','hr_employee'],
    "data" : [
        "security/ir.model.access.csv",
        #'data/hr.school.csv',
        #'data/hr.academy.csv',
        #'views/hr_employee_view.xml',
        #'views/hr_school_view.xml',
        #'views/hr_academy_view.xml',
        #'views/hr_language_view.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
