#-*- coding:utf-8 -*-
###########################################################################
#
# © 2016 Juan Jose Lopez Garcia <jjlopezg74@gmail.com>.
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
###########################################################################
from openerp import models, fields, api, _

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    @api.one
    def _compute_fam(self):
        # FIXME: type 'NewId'
        if not isinstance(self.id, models.NewId):
            self.fam_qty = self.env['hr.family'].search_count([('id', '=', self.id)])
            fam_ids = [x.id for x in self.fam_ids]
            self.fam_qty_des = self.env['hr.family'].search_count([('id', 'in', fam_ids), ('type', '=', '2')])
            self.fam_qty_asc = self.env['hr.family'].search_count([('id', 'in', fam_ids), ('type', '=', '11')])

    fam_ids = fields.One2many('hr.family', 'employee_id', string='Familiares')

    fam_qty = fields.Integer(compute="_compute", default=0, string="Familiares", store=False)
    fam_qty_des = fields.Integer(compute="_compute_fam", default=0, string="Familiares Des.", store=False)
    fam_qty_asc = fields.Integer(compute="_compute_fam", default=0, string="Familiares Asc.", store=False)

    # ('1', 'Conyuge'),
    # ('2', 'Descendiente'),
    # ('6', 'Descendiente adoptivo'),
    # ('10', 'Conyuge divorciado'),
    # ('11', 'Ascendiente')
