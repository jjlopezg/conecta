#-*- coding:utf-8 -*-
###########################################################################
#
# © 2016 Juan Jose Lopez Garcia <jjlopezg74@gmail.com>.
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
###########################################################################
from openerp import models, fields, api, _

class ResCnae(models.Model):

    _name = "res.cnae"
    _parent_store = True

    code = fields.Char("Code", required=True, size=5)
    description = fields.Char("Description", required=True, size=250)
    name = fields.Char(compute='_compute_name', size=256)

    parent_id = fields.Many2one(_name, "Parent")
    parent_left = fields.Integer("Left parent")
    parent_right = fields.Integer("Right parent")
    child_ids = fields.One2many(_name, "parent_id")

    _sql_constraints = [
        ("code_unique", "unique(code)", "Codigo duplicado"),
    ]

    @api.one
    @api.depends('name')
    def _compute_name(self):
        self.name = "%s-%s" % (self.code, self.description)
