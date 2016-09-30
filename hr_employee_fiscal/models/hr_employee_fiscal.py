# -*- encoding: utf-8 -*-
###########################################################################
#
# © 2016 Juan Jose Lopez Garcia <jjlopezg74@gmail.com>.
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
###########################################################################
from openerp import models, fields, api, exceptions, _
from datetime import datetime
import logging

logger = logging.Logger(__name__)

class HrEmployeeFiscal(models.Model):
    _name = 'hr.employee.fiscal'
    _order = 'date_from desc'

    @api.one
    def _compute_create_user(self):
        self.user_create = "%s:%s" % (self.create_uid.login.split('@')[0],
                                      datetime.strptime(self.create_date, '%Y-%m-%d %H:%M:%S').strftime(
                                          '%d-%m-%Y-%H:%M:%S'))

    @api.one
    def _compute_last_user(self):
        self.user_last = "%s:%s" % (self.write_uid.login.split('@')[0],
                                    datetime.strptime(self.write_date, '%Y-%m-%d %H:%M:%S').strftime(
                                        '%d-%m-%Y %H:%M:%S'))


    user_create = fields.Char(compute='_compute_create_user', string='Creado', readonly=True, size=68, store=False)
    user_last = fields.Char(compute='_compute_last_user', string='Modificado', readonly=True, size=68, store=False)
    employee_id = fields.Many2one('hr.employee', 'Empleado', required=False)
    # TODO: poner company_id, obtener company
    company_id = fields.Many2one(related='employee_id.company_id', string='Compañia', required=False)

    date_from = fields.Date('Inicio', default=datetime.today().strftime('%Y-%m-01'), required=True, readonly=False)
    date_to = fields.Date('Termino', default=datetime.today().strftime('%Y-%m-30'), required=True, readonly=False)

    country_id = fields.Many2one('res.country', related='employee_id.country_id', string="Nacionalidad (País)", readonly=True, store=True)

    #home_state_id = fields.Char(related='employee_id.home_state_id.name', string='Provincia', readonly=True, store=False)
    date_irpf = fields.Datetime('Fecha Calculo', required=False, readonly=True)
    modif_id = fields.Many2one('hr.employee.fiscal.modif', 'Modificador IRPF', required=True)
    key_id = fields.Many2one('hr.employee.fiscal.key', 'Clave percepcion', required=True)
    marital = fields.Selection(related='employee_id.marital', string="Estado civil", readonly=True, store=False)
    situation = fields.Selection([
                                ('1', 'Monoparental'),
                                ('2', 'Con conyuge a cargo'),
                                ('3', 'Otras situacion'),
                                ],
                                string='Situacion familiar',
                                default='',
                                required=True,
                                readonly=False)
    conyuge_nif = fields.Char(string="DNI/NIF Conyuge",size=12, required=False, )
    minus = fields.Selection([
                            ('0', 'Sin Minusvalia'),
                            ('3', 'Igual/Superior a 33% e inferior 65%'),
                            ('A', 'Entre 33% y 65%, con asistencia'),
                            ('6', 'Igual/Superior a 65%'),
                            ('B', 'Igual/Superior a 65%, con asistencia'),
                            ],
                            string='Minusvalia',
                            default='0',
                            required=False)

    geo_move = fields.Selection([
                                ('S', 'Si'),
                                ('N', 'No'),
                                ],
                                string='Movilidad geografica',
                                default='N',
                                required=False)
    geo_date = fields.Date(string="Fecha Movilidad", required=False, )

    loan = fields.Selection([
                                ('S', 'Si'),
                                ('N', 'No'),
                                ],
                                string='Prestamo vivienda',
                                default='N',
                                required=False)


class HrEmployeeFiscalModif(models.Model):
    _name = "hr.employee.fiscal.modif"

    @api.one
    @api.depends('name')
    def _compute_name(self):
        self.name = "%s-%s" % (self.code, self.description)

    code = fields.Char('Codigo', size=7, required=True)
    description = fields.Char('Descipcion', size=200, required=True)
    name = fields.Char(compute='_compute_name', size=256)

    _sql_constraints = [
        ("code_unique", "unique(code)", "Codigo duplicado"),
    ]

class HrEmployeeFiscalkey(models.Model):
    _name = 'hr.employee.fiscal.key'

    @api.one
    @api.depends('name')
    def _compute_name(self):
        self.name = "%s-%s" % (self.code, self.description)

    code = fields.Char('Codigo', size=7, required=True)
    description = fields.Char('Descipcion', size=200, required=True)
    name = fields.Char(compute='_compute_name', size=256)

    _sql_constraints = [
        ("code_unique", "unique(code)", "Codigo duplicado"),
    ]


