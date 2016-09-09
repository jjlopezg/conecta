# -*- coding: utf-8 -*-
###########################################################################
#
# © 2016 Juan Jose Lopez Garcia <jjlopezg74@gmail.com>.
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
###########################################################################
from openerp import models, fields, api

class HrIdentification(models.Model):

    _name = "hr.identification"
    _description = 'Tipo de Indentificacion'
   
    code = fields.Char("Codigo SEPE", size=1, required=True)
    description = fields.Char("Descripcion", size=128, required=True)
    tgss = fields.Char("Codigo TGSS", size=1, required=True)
    name = fields.Char(compute='_compute_name', size=256)

    _sql_constraints = [
        ("code_unique", "unique(code)", "Codigo duplicado"),
    ]

    @api.one
    @api.depends('name')
    def _compute_name(self):
        self.name = "%s" % (self.description)
