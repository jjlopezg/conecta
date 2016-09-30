# -*- encoding: utf-8 -*-
###########################################################################
#
# © 2016 Juan Jose Lopez Garcia <jjlopezg74@gmail.com>.
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
###########################################################################
from openerp import models, fields, api, _
import time
from datetime import datetime

class HrContractTypeTelcolbo(models.Model):
    _name = "hr.contract.type.telcolbo"

    @api.one
    @api.depends('name')
    def compute_name(self):
        self.name = "%s-%s" % (self.code, self.description)

    code= fields.Char('code', size=3, required=True)
    description= fields.Char('Descripcion', size=128, required=True)
    name = fields.Char(compute='compute_name', size=128, store=False)

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

    date_start = fields.Date('Inicio')
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

    @api.one
    def _compute_create_user(self):
        self.user_create = "%s:%s" % (self.create_uid.login.split('@')[0],
                                      datetime.strptime(self.create_date, '%Y-%m-%d %H:%M:%S').strftime('%d-%m-%Y-%H:%M:%S'))

    @api.one
    def _compute_last_user(self):
        self.user_last = "%s:%s" % (self.write_uid.login.split('@')[0],
                                    datetime.strptime(self.write_date, '%Y-%m-%d %H:%M:%S').strftime('%d-%m-%Y-%H:%M:%S'))

    @api.one
    @api.depends('code','description','name')
    def _compute_name(self):
        self.name = "%s-%s" % (self.code, self.description)

    code = fields.Char("Code", required=True, size=5)
    description = fields.Char('Descripcion', size=128, required=True)
    name = fields.Char(compute='_compute_name', size=256)
    user_create = fields.Char(compute='_compute_create_user', string='Creado', readonly=True, size=256, store=False)
    user_last = fields.Char(compute='_compute_last_user', string='Modificado', readonly=True, size=256, store=False)


    sepe =  fields.Char("SEPE", required=False, size=3)
    date_from =  fields.Date('Inicio', default= time.strftime('%Y-%m-%d'),  required = True)
    date_to =  fields.Date('Termino', required = True)
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
                                 ('R', 'Relevo'),
                                 ('FD', 'Fijo Discontinuo'),
                                 ('TC','Transformacion T. Completo'),
                                 ('TP','Transformacion T. Parcial'),
                                ], 'Tipo Contrato', required=False)
    # BONIFICACIONES
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
    mujer_sub = fields.Selection([
            ('S', 'Si'),
            ('N', 'No'),
            ],
            string='Mujer subrepresentada',
            default='N',
            required=True,
            readonly=False)


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


    #cl_ad = fields.Html('Body', translate=True, sanitize=False, help="Rich-text/HTML version of the message (placeholders may be used here)")
    # FIXME:  validar que no tenga espacios la ruta y el nombre del fichero
    template = fields.Char(string="Plantilla", )

    rule_ids = fields.Many2many('hr.contract.type.rules', 'contract_rules_rel', 'type_id', 'rule_id', string='Reglas', required=False)
    note = fields.Text('Anotaciones')


    _sql_constraints = [
        ("code_unique", "unique(code)", "Codigo duplicado."),
    ]

# FIXME:  validar que no tenga espacios la ruta y el nombre del fichero
"""
  @api.one
  @api.constrains('filename')
  def _check_filename(self):
      if self.file:
          if not self.filename:
  	        raise exceptions.ValidationError(_("no file"))
  	else:
          if self.filename:
  	        tmp = self.filename.split('.')
  	        ext = tmp[len(tmp)-1]
  	        if ext != 'xml':
      	        raise exceptions.ValidationError(_("xml file"))
  """


