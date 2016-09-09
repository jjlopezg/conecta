# -*- encoding: utf-8 -*-
###########################################################################
#
# © 2016 Juan Jose Lopez Garcia <jjlopezg74@gmail.com>.
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
###########################################################################
from openerp import models, fields, api, _
from datetime import datetime

class HrSepeTerrores(models.Model):
    _name = "hr.sepe.terrores"
    _order = "code"

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


class HrSepe(models.Model):
    _name = 'hr.sepe'

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
    def compute_employee(self):
        self.employee_id = self.contract_id.employee_id

    user_create = fields.Char(compute='compute_create_user', string='Creado', readonly=True, size=256, store=False)
    user_last = fields.Char(compute='compute_last_user', string='Modificado', readonly=True, size=256, store=False)
    contract_id = fields.Many2one('hr.contract', string='Contrato', default=lambda self: self.env.context.get('contract_id'), required=False)
    company_id = fields.Many2one(related='contract_id.company_id', string="Compañia", required=False)
    employee_id = fields.Many2one(related='contract_id.employee_id', string='Empleado', default=lambda self: self.env.context.get('employee_id'), required=False)

    date_start = fields.Date('Inicio', required=True, readonly=False)
    date_end = fields.Date('Termino', required=False, readonly=False)
    type = fields.Selection([
                            ('FICHERO_CONTRATOS', 'Contrato'),
                            ('FICHERO_PRORROGAS', 'Prorroga'),
                            ('transfor', 'Transformacion'),
                            ('ring', 'Llamamiento'),
                            ('basic', 'Copia Basica'),
                            ],
                            string='Tipo Comunicacion',
                            default='FICHERO_CONTRATOS',
                            required=True,
                            readonly=False)

    name = fields.Char('Codigo Inem', size=17, default='E0000000000000000', readonly=False)
    date_send = fields.Date('Fecha Comunicacion', readonly=False)
    date_init = fields.Date('Fecha Alta', required=False, readonly=False)
    user_auth = fields.Char('Usuario Auth.', size=32, default=False, readonly=False)
    leybonif = fields.Char('Ley Bonificacion', size=2, default='00', readonly=False)
    leyfomento = fields.Char('Ley Fomento', size=2, default='00', readonly=False)
    leyreduccion = fields.Char('Ley Reduccion', size=2, default='00', readonly=False)
    leydeduccion = fields.Char('Ley Deduccion', size=2, default='00', readonly=False)
    terror_ids = fields.Many2many('hr.sepe.terrores', 'hr_sepe_terrores_rel', 'sepe_id', 'terror_id', string='Codigos',
                                    required=False, readonly=True, copy=False)
    basic_copy = fields.Selection([
                                    ('S', 'Si'),
                                    ('N', 'No'),
                                    ],
                                    string='Copia Basica',
                                    required=True,
                                    default='N',
                                    readonly=False)


    state = fields.Selection([
                        ('draft', 'Por enviar'),
                        ('send', 'Esperando respuesta'),
                        ('RECHAZADO', 'Rechazado'),
                        ('ACEPTADO', 'Aceptado'),
                        ('ACEPTADO CON ERRORES', 'Aceptado con errores'),
                        ],
                        string='Estado',
                        default='draft',
                        required=True,
                        readonly=False)


    @api.model
    @api.onchange('state')
    def onchange_state(self):
        if self.state in ['draft', 'send']:
            self.terror_ids = False


