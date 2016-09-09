# -*- encoding: utf-8 -*-
###########################################################################
#
# © 2016 Juan Jose Lopez Garcia <jjlopezg74@gmail.com>.
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
###########################################################################
from openerp import models, fields, api, exceptions, _


class HrContractWage(models.Model):
    _name = "hr.contract.wage"

    @api.one
    @api.depends('name')
    def _compute_name(self):
        self.name = "%s.%s" % (self.code, self.name)

    name = fields.Char(compute='_compute_name', size=128)
    code = fields.Char(string='Code',
            help="The code that can be used in the salary rules to identify ")

    contract_id = fields.Many2one('hr.contract', 'Contrato', default=lambda self: self.env.context.get('contract_id'), required=True)

    currency_id = fields.Many2one('res.currency', string='Currency', readonly=True, default=lambda self: self.env.user.company_id.currency_id)
    amount_fix = fields.Float(string="Importe",  required=False)
    pay = fields.Selection([
            ("D", "Diario"),
            ("M", "Mensual"),
            ("A", "Anual"),
        ],
        string="Intervalo",
        default='',
        required=False)



