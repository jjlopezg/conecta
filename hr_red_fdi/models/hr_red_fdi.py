# -*- encoding: utf-8 -*-
###########################################################################
#
# © 2016 Juan Jose Lopez Garcia <jjlopezg74@gmail.com>.
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
###########################################################################
from openerp import models, fields, api, _
from dateutil.relativedelta import relativedelta
from datetime import datetime, date


class HrRedFdiType(models.Model):
    _name = "hr.red.fdi.type"

    active = fields.Boolean('Activo', default=True)
    code = fields.Char('Codigo', size=7, required=True)
    description = fields.Char('Descipcion', size=200, required=True)
    name = fields.Char(compute='_compute_name', size=256)

    _sql_constraints = [
        ("code_unique", "unique(code)", "Codigo duplicado"),
    ]

    @api.one
    @api.depends('name')
    def _compute_name(self):
        self.name = "%s-%s" % (self.code, self.description)


class HrRedFdiTypeTo(models.Model):
    _name = 'hr.red.fdi.type.to'

    active = fields.Boolean('Activo', default=True)
    code = fields.Char('Codigo', size=7, required=True)
    description = fields.Char('Descipcion', size=200, required=True)
    name = fields.Char(compute='_compute_name', size=256)

    _sql_constraints = [
        ("code_unique", "unique(code)", "Codigo duplicado"),
    ]

    @api.one
    @api.depends('name')
    def _compute_name(self):
        self.name = "%s-%s" % (self.code, self.description)

class HrRedFdiStatus(models.Model):
    _name = 'hr.red.fdi.status'
    _order = 'date desc'
    _rec_name = 'code'

    fdi_id = fields.Many2one('hr.red.fdi', string="Mensaje FDI", required=False, readonly=False)
    code = fields.Char('Codigo', size=4, default='0000', required=False)
    description = fields.Char('Descipcion', size=200, required=False)
    date = fields.Date(string='Fecha', required=False)
    state = fields.Selection([
                            ('done', 'Aceptado'),
                            ('refuse', 'Rechazado'),
                            ],
                            string='Estado',
                            default='',
                            required=True,
                            readonly=False)

    _sql_constraints = [
        ("code_unique", "unique(code)", "Codigo duplicado"),
    ]

    @api.one
    @api.depends('name')
    def _compute_name(self):
        self.name = "%s-%s" % (self.code, self.description)

class HrRedFdi(models.Model):
    _name = 'hr.red.fdi'
    _order = 'date_start desc'

    @api.one
    def compute_create_user(self):
        self.user_create = "%s:%s" % (self.create_uid.login.split('@')[0],
                                      datetime.strptime(self.create_date, '%Y-%m-%d %H:%M:%S').strftime(
                                          '%d-%m-%Y-%H:%M:%S'))

    @api.one
    def compute_last_user(self):
        self.user_last = "%s:%s" % (self.write_uid.login.split('@')[0],
                                    datetime.strptime(self.write_date, '%Y-%m-%d %H:%M:%S').strftime(
                                        '%d-%m-%Y-%H:%M:%S'))

    @api.one
    @api.depends('date_from')
    def compute_cumplim(self):
        if self.date_from:
            self.days_365 = datetime.strptime(self.date_from, '%Y-%m-%d') + relativedelta(days=365)

    @api.one
    @api.depends('name')
    def _compute_name(self):
        self.name = "%s-%s-%s" % (datetime.strptime(self.date_from, '%Y-%m-%d').strftime(
                                        '%d-%m-%Y'), self.action, self.type_id.name)

    user_create = fields.Char(compute='compute_create_user', string='Creado', readonly=True, size=256, store=False)
    user_last = fields.Char(compute='compute_last_user', string='Modificado', readonly=True, size=256, store=False)
    name = fields.Char(compute='_compute_name', size=256)
    contract_id = fields.Many2one('hr.contract', string='Contrato', default=lambda self: self.env.context.get('contract_id'), required=True)
    company_id = fields.Many2one(related='contract_id.company_id', string="Compañia", required=False)
    employee_id = fields.Many2one(related='contract_id.employee_id', string='Empleado', default=lambda self: self.env.context.get('employee_id'), required=False)

    date_start = fields.Date(string='Fecha Comunicacion', required=True, readonly=False)
    date_end = fields.Date(string='Termino', required=False, readonly=False)

    type_id = fields.Many2one('hr.red.fdi.type', string='Contingencia', required=True, readonly=False)
    date_from = fields.Date(string='Fecha baja', required=False, readonly=False)
    relapse = fields.Selection([
                                ('S', 'Si'),
                                ('N', 'No'),
                                ],
                                string='Recaida',
                                default='N',
                                required=True)

    type_to_id = fields.Many2one('hr.red.fdi.type.to', string='Causa Alta', required=False)
    date_to = fields.Date(string='Fecha alta', required=False, readonly=False)

    date_part = fields.Date(string='Fecha de parte', required=False, readonly=False)
    part_number = fields.Char(string="Nº de parte", size=2, required=False, readonly=False)

    date_at_ep = fields.Date(string='Fecha AT/EP', required=False, readonly=False)
    colg_number = fields.Char(string="Nº colegiado", size=8, required=True, readonly=False)
    state_id = fields.Many2one("res.country.state", string='Provincia', required=True)
    cias_number = fields.Char(string="C.I.A.S", size=10, required=False, readonly=False)
    days_from = fields.Char(string="Dias de baja", size=10, required=False, readonly=False)
    # FIXME: calcula 365 dias desde la fecha de baja, store debe de ser True??
    days_365 = fields.Date(compute='compute_cumplim', string='Cumplim. 365 dias', store=False)
    days_to = fields.Char(string='Dias Prob. Baja', required=False, readonly=False)

    # FIXME: este campo se debe de coger de otro sitio para obtener la base de cotizacion
    dc = fields.Char(string="Dias Cotizados", required=False, )
    base = fields.Float(string="Base Cotizacion", required=False, )
    base_sum = fields.Float(string="Suma Bases Cotizacion", required=False)
    old_year = fields.Float(string="Cot. año ant.h.extras", required=False)
    old_year_otther = fields.Float(string="Base Ant.Año Otros", required=False)

    action = fields.Selection([
                            ('PB', 'Comunicar Baja'),
                            ('PC', 'Comunicar Parte Confirmacion'),
                            ('PA', 'Comunicar Alta'),
                            ],
                            string='Accion',
                            default='',
                            required=True,
                            readonly=False)

    state = fields.Selection([
                                ('none', 'No Comunicar'),
                                ('draft', 'Por enviar'),
                                ('send', 'Esperando respuesta'),
                                ('done', 'Cerrado'),
                                ],
                                string='Estado',
                                default='draft',
                                required=True,
                                readonly=False)

    status_ids = fields.One2many('hr.red.fdi.status', 'fdi_id', string='Mensajes FDI', required=False)
