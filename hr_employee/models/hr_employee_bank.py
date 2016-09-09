# -*- coding: utf-8 -*-
###########################################################################
#
# © 2016 Juan Jose Lopez Garcia <jjlopezg74@gmail.com>.
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
###########################################################################
from openerp import models, fields, api, exceptions, _
from datetime import datetime

class HrEmployeeBank(models.Model):
    _name = 'hr.employee.bank'
    _inherit = "res.partner.bank"
    _order = 'date_start desc'

    @api.one
    def _compute_create_user(self):
        self.user_create = "%s:%s" % (self.create_uid.login.split('@')[0],
                                      datetime.strptime(self.create_date, '%Y-%m-%d %H:%M:%S').strftime('%d-%m-%Y-%H:%M:%S'))

    @api.one
    def _compute_last_user(self):
        self.user_last = "%s:%s" % (self.write_uid.login.split('@')[0],
                                    datetime.strptime(self.write_date, '%Y-%m-%d %H:%M:%S').strftime('%d-%m-%Y-%H:%M:%S'))

    user_create = fields.Char(compute='_compute_create_user', string='Creado', readonly=True, size=256, store=False)
    user_last = fields.Char(compute='_compute_last_user', string='Modificado', readonly=True, size=256, store=False)

    date_start = fields.Date('Inicio', required=True, readonly=False)
    date_end = fields.Date('Termino', required=False, readonly=False)
    employee_id = fields.Many2one('hr.employee', string='Empleado', default=lambda self: self.env.context.get('employee_id'), required=False, readonly=True)

    acc_payment = fields.Selection(string="Forma de pago",
                               selection=[('T', 'Transferencia'),
                                          ('C', 'Cheque'),
                                          ('P', 'Efectivo'),
                                          #('S', 'Sepa'),
                                          ],
                               default='T',
                               required=True, )

    state = fields.Selection(string="Estado",
                             selection=[
                                 ('draft', 'Borrador'),
                                 ('active', 'Activa'),
                                 ('cancel', 'Cancelada'),
                             ],
                             default='active',
                             required=True, )

    _sql_constraints = [
        ("code_unique", "unique(acc_number)", "Numero de cuenta duplicada"),
    ]


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    @api.one
    @api.depends('account_ids')
    def _latest_account(self):
        account_ids = self.env['hr.employee.bank'].search([('employee_id', '=', self.id)], order='date_start')
        self.bank_account_id = account_ids[-1:][0].id
        return self.bank_account_id

    @api.one
    def _compute_get_account(self):
        self.bank_account_id = self._latest_account()[0].id

    account_ids = fields.One2many('hr.employee.bank', 'employee_id', string='Cuentas bancarias', required=True, copy=False)

    bank_account_id = fields.Many2one(comodel_name='hr.employee.bank',
                                      computed='_latest_account',
                                      domain=[],
                                      context={},
                                      string="Nº Cuenta Bancaria",
                                      required=False,
                                      readonly=True,
                                      help='Este campo es heredado',
                                      copy=False)

