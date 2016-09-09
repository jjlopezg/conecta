# -*- encoding: utf-8 -*-
###########################################################################
#
# © 2016 Juan Jose Lopez Garcia <jjlopezg74@gmail.com>.
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
###########################################################################
{
    'name': 'Proyecto Conecta -Tipos de Contratos',
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
Tipos de Contratos
==========================================

* Impresion de modelos


""",
    "depends" : [
        'hr',
        'hr_contract',
        'hr_contract_es',
    ],
    "data" : [
#        "security/ir.model.access.csv",
        'data/hr.contract.type.csv',
        'data/hr.contract.type.telcolbo.csv',

        'wizard/hr_contract_type_print_view.xml',

        'report/template_contracts.xml',
        'report/template_contracts_tp_page1.xml',
        'report/template_contracts_tp_page2.xml',
        'report/template_contracts_tp_page3.xml',
        'report/template_contracts_tp_page4.xml',
        'report/template_contracts_tp_page5.xml',
        'report/template_contracts_tp_page6.xml',
        'report/template_contracts_tp_page22.xml',
        'report/template_contracts_cb.xml',

        'views/hr_contract_view.xml',
        'views/hr_contract_type_view.xml',
        'views/hr_contract_type_telcolbo.xml',
    ],
}
