# -*- encoding: utf-8 -*-
###########################################################################
#
# © 2016 Juan Jose Lopez Garcia <jjlopezg74@gmail.com>.
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
###########################################################################

{
    'name': 'Proyecto Conecta - Convenio Colectivo',
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
Convenio Colectivo
==========================================

* Convenio colectivo
* Categoria laboral
* Grp. cotizacion

""",
    "depends" : [
        'base',
        'hr',
        'hr_contract',
    ],
    "data" : [
#        "security/ir.model.access.csv",
        "data/hr.convenio.catg.csv",
        "data/hr.convenio.grpcot.csv",
        "data/res.cno.csv",
        "data/res.cno.modif.csv",

        "views/hr_contract_view.xml",
        "views/hr_convenio_view.xml",
        "views/hr_convenio_catg_view.xml",
        "views/res_cno_view.xml",
    ],
}
