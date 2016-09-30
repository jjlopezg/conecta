# -*- coding: utf-8 -*-
###########################################################################
#
# © 2016 Juan Jose Lopez Garcia <jjlopezg74@gmail.com>.
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
###########################################################################
{
    'name': 'Proyecto Conecta - Fiscal',
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
Datos Fiscales y familiares
===========================
Base para calculo IRPF
Modelo 145
    """,
    "depends" : [
        'base',
        'hr',
        'report_xml',
    ],
    "data" : [
        "data/hr.employee.fiscal.key.csv",
        "data/hr.employee.fiscal.modif.csv",

        "security/ir.model.access.csv",

        "views/hr_employee_view.xml",
        "views/hr_family_view.xml",
        "views/hr_employee_fiscal_view.xml",
    ],
}
