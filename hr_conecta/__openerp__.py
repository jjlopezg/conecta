#-*- coding:utf-8 -*-
###########################################################################
#
# © 2016 Juan Jose Lopez Garcia <jjlopezg74@gmail.com>.
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
###########################################################################
{
    'name': 'Proyecto Conecta',
    'version': '9.0.1.0.0',
    'author': 'JJLopezG',
    'website': 'http://www.tuconecta.es/',
    'license': 'AGPL-3',
    'category': 'Human Resources',
    'summary': '',
    'installable': True,
    'application': False,
    'auto_install': False,
    'description': """ """,
    "depends" : [
        'base',
        'base_iso3166',
        'base_location_geonames_import',
        'hr',
    ],
    "data" : [
        "data/res.cnae.csv",
        "data/res.mutua.csv",
        "data/res.regimen.csv",

        "security/ir.model.access.csv",

        'views/res_company_view.xml',
        "views/res_cnae_view.xml",
        "views/res_mutua_view.xml",
        "views/res_regimen_view.xml",
    ],
}
