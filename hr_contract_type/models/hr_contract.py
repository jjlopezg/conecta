# -*- encoding: utf-8 -*-
###########################################################################
#
# © 2016 Juan Jose Lopez Garcia <jjlopezg74@gmail.com>.
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
###########################################################################
from openerp import models, fields, api, _
import time

class HrContract(models.Model):
    _inherit = 'hr.contract'

    type_id = fields.Many2one('hr.contract.type', 'Tipo Contrato', default=False, required=True)

    @api.onchange('type_id')
    def onchange_type(self):
        types = self.env['hr.contract.type'].search([
                ('date_start', '<=',  time.strftime('%Y-%m-%d')),
                '|',
                ('date_end', '=', False),
                ('date_end', '>=',  time.strftime('%Y-%m-%d')),
            ])
        ids = map(int, types)
        return {'domain':
                        {'type_id': [('id','in', ids)],}
                }

    """
    @api.multi
    # function definition is in odoo v8 format
    def export_file(self):
        data = self.browse(self.id)[0]

        datas = {
            'ids': self.id,
            'model': "hr.contract",
            'form': data,
            'context': self._context
        }
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'hr_contract.report_contracts',
            'datas': datas
        }
    """