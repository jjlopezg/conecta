# -*- encoding: utf-8 -*-
###########################################################################
#
# © 2016 Juan Jose Lopez Garcia <jjlopezg74@gmail.com>.
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
###########################################################################
from openerp import models, fields, api, _
#from hr_contract_afi import create_file_afi
from datetime import datetime

class HrRedAfi(models.Model):
    _name = 'hr.red.afi'
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

    user_create = fields.Char(compute='compute_create_user', string='Creado', readonly=True, size=256, store=False)
    user_last = fields.Char(compute='compute_last_user', string='Modificado', readonly=True, size=256, store=False)
    contract_id = fields.Many2one('hr.contract', string='Contrato', default=lambda self: self.env.context.get('contract_id'), required=False)
    company_id = fields.Many2one(related='contract_id.company_id', string="Compañia", required=False)
    employee_id = fields.Many2one(related='contract_id.employee_id', string='Empleado', default=lambda self: self.env.context.get('employee_id'), required=False)

    date_start = fields.Date('Fecha Comunicacion', required=True, readonly=False)
    date_end = fields.Date('Termino', required=False, readonly=False)

    date_contract = fields.Date(related='contract_id.date_start', string='Fecha Inicio Contrato', readonly=True, store=True)

    datetime_send = fields.Datetime('Fecha/Hora proceso', default=datetime.today().strftime('%Y-%m-%d %H:%M:%S'), readonly=True)
    #time_send = fields.Float('Hora proceso', default=float_time_convert(datetime.today().strftime('')), readonly=True)

    move_id = fields.Many2one('hr.red.afi.move', 'Movimiento', required=True)
    position_id = fields.Many2one('hr.red.afi.position', 'Situacion', required=True)
    ####################################################################################################################################
    # TODO: FCT
    ####################################################################################################################################
    holiday_end = fields.Date(string="Fecha fin vacaciones", required=False, )
    ####################################################################################################################################
    # TODO: FAB
    ####################################################################################################################################
    ind_print = fields.Selection([
                                (' ', 'Sin Impresion'),
                                ('S', 'Impresion'),
                                ('C', 'Impresion+IDCl'),
                                ('I', 'IDC'),
                                ],
                                string='Indic. Impresion',
                                default='S',
                                required=True,
                                readonly=False)
    desem_id = fields.Many2one('hr.red.afi.desem', 'Desempleado', required=False)
    colec_id = fields.Many2one('hr.red.afi.colec', 'Colectivo', required=False)
    mujer_id = fields.Many2one('hr.red.afi.mujer', 'Mujer Reincorporada', required=False)
    mujer_sub = fields.Selection([
                                ('S', 'Si'),
                                ('N', 'No'),
                                ],
                                string='Mujer subrepresentada',
                                default='N',
                                required=True,
                                readonly=False)
    ####################################################################################################################################
    # TODO: DAM
    ####################################################################################################################################
    # RESPUESTA
    error = fields.Char("Cod. Error", required=False, readonly=True, size=5)
    otros = fields.Char("Otros textos", required=False, readonly=True, size=128)




    state = fields.Selection([
                                ('draft', 'Por enviar'),
                                ('send', 'Esperando respuesta'),
                                ('done', 'Aceptado'),
                                ('cancel', 'Rechazado'),
                                ],
                                string='Estado',
                                default='draft',
                                required=True,
                                readonly=False)





class HrRedAfiDesem(models.Model):
    _name = "hr.red.afi.desem"

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

class HrRedAfiColec(models.Model):
    _name = "hr.red.afi.colec"

    active = fields.Boolean('Activo', default=True)
    code = fields.Char('Codigo', size=3, required=True)
    description = fields.Char('Descipcion', size=200, required=True)
    name = fields.Char(compute='_compute_name', size=256)

    _sql_constraints = [
        ("code_unique", "unique(code)", "Codigo duplicado"),
    ]

    @api.one
    @api.depends('name')
    def _compute_name(self):
        self.name = "%s-%s" % (self.code, self.description)

class HrRedAfiMujer(models.Model):
    _name = "hr.red.afi.mujer"

    active = fields.Boolean('Activo', default=True)
    code = fields.Char('Codigo', size=1, required=True)
    description = fields.Char('Descipcion', size=200, required=True)
    name = fields.Char(compute='_compute_name', size=256)

    _sql_constraints = [
        ("code_unique", "unique(code)", "Codigo duplicado"),
    ]

    @api.one
    @api.depends('name')
    def _compute_name(self):
        self.name = "%s-%s" % (self.code, self.description)

class HrRedAfiPosition(models.Model):
    _name = "hr.red.afi.position"

    active = fields.Boolean('Activo', default=True)
    code = fields.Char('Codigo', size=7, required=True)
    description = fields.Char('Descipcion', size=200, required=True)
    note = fields.Text(string="Anotaciones", required=False)
    name = fields.Char(compute='_compute_name', size=256)

    _sql_constraints = [
        ("code_unique", "unique(code)", "Codigo duplicado"),
    ]

    @api.one
    @api.depends('name')
    def _compute_name(self):
        self.name = "%s-%s" % (self.code, self.description)


class HrARedfiMove(models.Model):
    _name = 'hr.red.afi.move'

    active = fields.Boolean('Activo', default=True)
    code = fields.Char('Codigo', size=7, required=True)
    description = fields.Char('Descipcion', size=200, required=True)
    name = fields.Char(compute='_compute_name', inverse='_inverse_name', size=256)

    _sql_constraints = [
        ("code_unique", "unique(code)", "Codigo duplicado"),
    ]

    @api.one
    @api.depends('name')
    def _compute_name(self):
        self.name = "%s-%s" % (self.code, self.description)