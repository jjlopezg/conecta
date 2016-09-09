#-*- coding:utf-8 -*-
###########################################################################
#
# © 2016 Juan Jose Lopez Garcia <jjlopezg74@gmail.com>.
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
###########################################################################
{
    'name': 'Prevencion riesgos laborales',
    'version': '1.0.0',
    'author': 'Juan Jose Lopez Garcia',
    'website': 'http://',
    'license': 'AGPL-3',
    'category': 'Human Resources',
    'summary': '',
    'description': """
    """,
    'images': ['images/prl.jpeg'],
    "depends" : ['base','hr'],
    "data" : [
        # poner fichero para crear grupo de prevencion
        "security/ir.model.access.csv",
        'views/hr_prl_view.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
