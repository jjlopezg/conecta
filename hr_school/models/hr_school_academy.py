#-*- coding:utf-8 -*-
###########################################################################
#
# © 2016 Juan Jose Lopez Garcia <jjlopezg74@gmail.com>.
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
###########################################################################
from openerp import models, fields, api, _

class HrSschoolAcademy(models.Model):

    _name = "hr.school.academy"
    
    code = fields.Char('Codigo', size=12, required=True)
    name = fields.Char('Descripcion', size=250, required=True)

    _sql_constraints = [
        ("code_unique", "unique(code)", "Codigo duplicado"),
    ]