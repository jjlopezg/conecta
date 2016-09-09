# -*- coding: utf-8 -*-
###########################################################################
#
# © 2016 Juan Jose Lopez Garcia <jjlopezg74@gmail.com>.
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
###########################################################################
{
    'name': 'Proyecto Conecta - Contratos',
    'version': '9.0.1.0.0',
    'author': 'JJLopezG',
    'website': 'http://www.tuconecta.es',
    'license': 'AGPL-3',
    'category': 'Human Resources',
    'summary': '',
    'installable': True,
    'application': False,
    'auto_install': False,
    'description':""""
Contratos
==========================================

    """,
    "depends" : [
        'hr',
        'hr_contract',
    ],
    "update_xml" : [
        'data/terfircb.xml',
        'data/tbonvfor.xml',
        'data/teiinter.xml',
        'security/ir.model.access.csv',
        'hr_contract_sequence.xml',
        'views/hr_contract_view.xml',
    ],
}
