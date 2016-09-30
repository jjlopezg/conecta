#-*- coding:utf-8 -*-
###########################################################################
#
# © 2016 Juan Jose Lopez Garcia <jjlopezg74@gmail.com>.
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
###########################################################################
from datetime import datetime
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT as OE_DFORMAT
from openerp import models, fields, api, _

class HrEmployeeFiscal(models.Model):
    _inherit = 'hr.employee.fiscal'

    # info: Obtener numero de miembros de la unidad familiar
    @api.one
    def _compute_fam(self):
        # TODO: 'NewId'
        if not isinstance(self.id, models.NewId):
            self.fam_qty = self.env['hr.family'].search_count([('id', '=', self.id)])
            fam_ids = [x.id for x in self.fam_ids]
            self.fam_qty_des = self.env['hr.family'].search_count([('id', 'in', fam_ids), ('type', 'in', ['2', '6'])])
            self.fam_qty_asc = self.env['hr.family'].search_count([('id', 'in', fam_ids), ('type', '=', '11')])
            # ('2', 'Descendiente'),
            # ('6', 'Descendiente adoptivo'),
            # ('11', 'Ascendiente')

    fam_ids = fields.One2many('hr.family', 'fiscal_id', string='Familiares')
    fam_qty = fields.Integer(compute="_compute", default=0, string="Familiares", store=False)
    fam_qty_des = fields.Integer(compute="_compute_fam", default=0, string="Familiares Des.", store=False)
    fam_qty_asc = fields.Integer(compute="_compute_fam", default=0, string="Familiares Asc.", store=False)

class HrFamily(models.Model):
    _name = 'hr.family'
    _order = 'birthday asc'

    @api.one
    @api.onchange('birthday')
    def _compute_age(self):
        if self.birthday:
            dBday = datetime.strptime(self.birthday, OE_DFORMAT).date()
            dToday = datetime.now().date()
            self.age = (dToday - dBday).days / 365

    fiscal_id = fields.Many2one('hr.employee.fiscal', string='Fiscal')
    name = fields.Char('Nombre', size=250, required=True)
    age = fields.Integer(compute="_compute_age", string='Edad', size=3, readonly=True)
    # FIXME: por letra de dni en mayusculas siempre
    ssnid = fields.Char('D.N.I/N.I.F', size=10, required=False)
    type = fields.Selection([
#                            ('1', 'Conyuge'),
                            ('2', 'Descendiente'),
                            ('6', 'Descendiente adoptivo'),
#                            ('10', 'Conyuge divorciado'),
                            ('11', 'Ascendiente')
                            ],
                            string='Miembro',
                            required=True)
    gender = fields.Selection([
                            ('male', 'Hombre'),
                            ('female', 'Mujer'),
                            ],
                            string='Sexo',
                            required=False)
    birthday = fields.Date('Fecha nacimiento', required=True)
    country_id = fields.Many2one('res.country', 'Nacionalidad')
    city = fields.Char('Lugar nacimiento', size=128)
    factor = fields.Selection([
                                ('1', 'Familiar no relevante para IRPF'),
                                ('2', 'Aplicacion minimo por defecto'),
                                ('3', 'Totalida del minimo'),
                                ('4', 'Mitad del minimo'),
                                ('10', '1/3 del minimo'),
                                ('11', '1/4 del minimo'),
                                ('12', '1/5 del minimo'),
                                ('13', '1/6 del minimo'),
                                ('14', '1/7 del minimo'),
                                ('15', '1/8 del minimo'),
                                ('16', '1/9 del minimo')
                            ],
                            string='Factor Familiar',
                            required=True)
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


    date_adoption = fields.Date('Fecha de adopcion')
    conviven = fields.Char('Nº Pers. Conviven con ascendiente', default='0', size=2, required=False)

