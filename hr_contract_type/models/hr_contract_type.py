# -*- encoding: utf-8 -*-
###########################################################################
#
# © 2016 Juan Jose Lopez Garcia <jjlopezg74@gmail.com>.
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
###########################################################################
from openerp import models, fields, api, _
import time

class HrContractTypeTelcolbo(models.Model):
    _name = "hr.contract.type.telcolbo"

    @api.one
    @api.depends('name')
    def compute_name(self):
        self.name = "%s-%s" % (self.code, self.description)

    code= fields.Char('code', size=3, required=True)
    description= fields.Char('Descripcion', size=128, required=True)
    name = fields.Char(compute='compute_name', size=128, store=True)
    date_start= fields.Date('Inicio')
    date_end= fields.Date('Termino')

    _sql_constraints = [
        ("code_unique", "unique(code)", "Codigo duplicado"),  
    ]

class HrContractTypeLey(models.Model):
    _name = "hr.contract.type.ley"

    code = fields.Char('code', size=128, required=True)
    name = fields.Text('Descripcion')
    date_start = fields.Date('Inicio', default= time.strftime('%Y-%m-%d'))
    date_end = fields.Date('Termino')

    _sql_constraints = [
        ("code_unique", "unique(code)", "Codigo duplicado"),
    ]

class HrContractTypeRd(models.Model):
    _name = "hr.contract.type.rd"

    code = fields.Char('code', size=128, required=True)
    name = fields.Text('Descripcion')
    date_start = fields.Date('Inicio', default= time.strftime('%Y-%m-%d'))
    date_end = fields.Date('Termino')

    _sql_constraints = [
        ("code_unique", "unique(code)", "Codigo duplicado"),
    ]


class HrContractTypeRd(models.Model):
    _name = "hr.contract.type.rd"

    code = fields.Char('code', size=128, required=True)
    name = fields.Text('Descripcion')
    date_start = fields.Date('Inicio', default= time.strftime('%Y-%m-%d'))
    date_end = fields.Date('Termino')

    _sql_constraints = [
        ("code_unique", "unique(code)", "Codigo duplicado"),
    ]

class HrContractTypeRules(models.Model):
    _name = "hr.contract.type.rules"

    @api.one
    @api.depends(
        'model_names',
    )
    def get_type(self):
        return [(lang, lang) for lang in self.model_names.fields_get()]

    code = fields.Char('code', size=128, required=True)
    name = fields.Char('Descripcion', size=128, required=True)

    model_names = fields.Many2one('ir.model', 'Model to use')
    field_names = fields.Many2one('ir.model.fields', string='Fields to use', domain="[('model_id', '=', model_names )]")

    value = fields.Char('Valor', size=128, required=True)
    alert = fields.Text('Alerta')

    _sql_constraints = [
        ("code_unique", "unique(code)", "Codigo duplicado"),
    ]

    @api.onchange('model_names')
    def do_stuff(self):
          self.field_names=False

class HrContractType(models.Model):
    _inherit = 'hr.contract.type'
    _order = 'code'

    code = fields.Char("Code", required=True, size=5)
    description = fields.Char('Descripcion', size=128, required=True)
    name = fields.Char(compute='_compute_name', size=256)

    sepe =  fields.Char("SEPE", required=False, size=3)
    date_start =  fields.Date('Inicio', default= time.strftime('%Y-%m-%d'),  required = True)
    date_end =  fields.Date('Termino', required = True)
    partner_alert =  fields.Char("Preav. Empresa", required=False, size=2)
    employee_alert =  fields.Char("Preav. Empleado", required=False, size=2)
    ley_id = fields.Many2one('hr.contract.type.ley', 'Ley aplicable', required=False)
    rd_id = fields.Many2one('hr.contract.type.rd', 'Real Decreto', required=False)

    schema = fields.Binary(string="Esquema validacion", required=False)
    type = fields.Selection([
                                 ('IJC','Indefinido Jornada Completa'),
                                 ('IJP','Indefinido Jornada Parcial'),
                                 ('DDJC','Duracion Determinada Jornada Completa'),
                                 ('DDJP','Duracion Determinada Jornada Parcial'),
                                 ('F','Formacion'),
                                 ('I','Interinidad'),
                                 ('PR','Practicas'),
                                 ('R','Relevo'),
                                 ('TC','Transformacion T. Completo'),
                                 ('TP','Transformacion T. Parcial'),
                                ], 'Tipo Contrato', required=False)

    bonificado_id = fields.Many2one('hr.contract.type.telcolbo', 'Colectivo bonificado', required=False)
    bonificado  = fields.Selection([
            ('N','No Bonificado'),
            ('B','Bonificado'),
            ('R','Reducido'),
            ], 'Bonificacion', required=False)
                
    cargo = fields.Selection([
            ('I','SEPE'),
            ('SS','S.S'),
            ], 'a Cargo', required=False)

    #'trial': fields.integer('Periodo de prueba', required=True),
    #duracion =  fields.integer('Max. Duracion (Meses)', required=False)
    #min_edad =  fields.integer('Min. Edad (Años)', required=False)
    #max_edad =  fields.integer('Max. Edad (Años)', required=False)
    #min_minus =  fields.integer('Min. Minusvalia (%)', required=False)
    #max_prog =  fields.integer('Numero Max. Prorrogas', required=False)
    #gender =  fields.selection([
    #                                ('male', 'Male'),
    #                                ('female', 'Female'),
    #                            ], 'Gender')


    cl_ad = fields.Html('Body', translate=True, sanitize=False, help="Rich-text/HTML version of the message (placeholders may be used here)")

    rule_ids = fields.Many2many('hr.contract.type.rules', 'contract_rules_rel', 'type_id', 'rule_id', string='Reglas', required=False)
    note = fields.Text('Anotaciones')


    _sql_constraints = [
        ("code_unique", "unique(code)", "Codigo duplicado."),
    ]

    @api.one
    @api.depends('code','description','name')
    def _compute_name(self):
        self.name = "%s-%s" % (self.code, self.description)



