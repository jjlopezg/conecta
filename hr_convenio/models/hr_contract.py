# -*- coding: utf-8 -*-
###########################################################################
#
# © 2016 Juan Jose Lopez Garcia <jjlopezg74@gmail.com>.
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
###########################################################################
from openerp import models, fields, api, _

class HrContract(models.Model):
    _inherit = "hr.contract"

    convenio_id = fields.Many2one("hr.convenio", string="Convenio", required=True)
    catg_id = fields.Many2one('hr.convenio.catg.cov', string='Categoria', required=True)


    @api.model
    @api.onchange('company_id')
    def onchange_company(self):
        self.convenio_id = False
        self.catg_id = False

    @api.model
    @api.onchange('convenio_id')
    def onchange_convenio(self):
        self.catg_id = False