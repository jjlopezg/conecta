# -*- coding: utf-8 -*-
###########################################################################
#
# © 2016 Juan Jose Lopez Garcia <jjlopezg74@gmail.com>.
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
###########################################################################
from openerp import models, fields, api, _

WEEK_SELECTION = [
        ('Lunes','Lunes'),
        ('Martes','Martes'),
        ('Miercoles','Miercoles'),
        ('Jueves','Jueves'),
        ('Viernes','Viernes'),
        ('Sabado','Sabado'),
        ('Domingo','Domingo')
]

class hr_contract_tbonvfor(models.Model):
    _name = "hr.contract.tbonvfor"

    code = fields.Char('code', size=2, required=True)
    description = fields.Char("Descripcion", size=256, required=True)
    name = fields.Char(compute='_compute_name', size=259)

    _sql_constraints = [
        ("code_unique", "unique(code)", "Codigo duplicado"),
    ]

    @api.one
    @api.depends('name')
    def _compute_name(self):
        self.name = "%s-%s" % (self.code, self.description)


class hr_contract_teiinter(models.Model):
    _name = "hr.contract.teiinter"

    code = fields.Char('code', size=2, required=True)
    description = fields.Char("Descripcion", size=256, required=True)
    name = fields.Char(compute='_compute_name', size=259)
    date_start = fields.Date('Inicio', default=fields.Date.today , required=True)
    date_end = fields.Date('Termino')

    _sql_constraints = [
        ("code_unique", "unique(code)", "Codigo duplicado"),
    ]

    @api.one
    @api.depends('name')
    def _compute_name(self):
        self.name = "%s-%s" % (self.code, self.description)

class hr_contract_visa(models.Model):
    _name = "hr.contract.visa"
    _order = "date_start"
    _rec_name= "visa_no"

    permit_no = fields.Char('Numero permiso de trabajo', required=False, readonly=False)
    visa_no = fields.Char('Numero de visado', required=False, readonly=False)
    date_start = fields.Date('Inicio', default=fields.Date.today, required=True)
    date_end = fields.Date('Termino')
    contract_id = fields.Many2one('hr.contract', 'Contrato', default=lambda self: self.env.context.get('contract_id'), required=True)

    _sql_constraints = [
        ("visa_no_unique", "unique(visa_no)", "Codigo duplicado"),
        ("permit_no_unique", "unique(permit_no)", "Codigo duplicado"),
    ]


class hr_contract_terfircb(models.Model):
    _name = "hr.contract.terfircb"

    code = fields.Char('code', size=2, required=True)
    description = fields.Char("Descripcion", size=256, required=True)
    name = fields.Char(compute='_compute_name', size=259)

    _sql_constraints = [
        ("code_unique", "unique(code)", "Codigo duplicado"),
    ]

    @api.one
    @api.depends('name')
    def _compute_name(self):
        self.name = "%s-%s" % (self.code, self.description)

class HrContract(models.Model):

    _inherit = 'hr.contract'

    @api.model
    def _get_teiinter(self):
        res = []
        ids = self.env['hr.contract.teiinter'].search([])
        for id in ids:
            res.append((id.code, id.description))
        return res

    #id_employee = fields.Char(related='employee_id.id_employee', string='ID Empleado')
    #name_employee = fields.Char(related='employee_id.name', string='Empleado')
    company_id = fields.Many2one('res.company', string="Compañia", required=True, readonly=False)

    #company_id = fields.Many2one('res.company', 'Compañia', default=lambda self: self.env.user.company_id, required=True, readonly=True,
    #                             states={'draft': [('readonly', False)]})

    name = fields.Char('ID Contrato', size=32, default='/', required=True, readonly=True)

    visa_ids = fields.One2many('hr.contract.visa', 'contract_id', field_description='Visado')

    # Page Informacion
    date_signature = fields.Date('Fecha Firma', default=fields.Date.today, required = True)
    test_trial_units = fields.Integer('Periodo de Prueba', default=15, required=False)
    test_trial_type = fields.Selection([
                            ('day','Dias'),
                            ('Semanas','Semanas'),
                            ('Meses','Meses'),
                            ('year','Años')],
                            default='day',
                            string='Periodo',
                            required=False)
    # End Informacion

    # Page General
    prg_emp = fields.Boolean('Acoge el prog. de empleo')

    is_dist = fields.Boolean('A Distancia')
    is_dist_text = fields.Char('Calle/Numero/Localidad', size=250, required=False, readonly=False)
    time_work = fields.Float('Jornada de trabajo', default=0, required=True)
    of_days = fields.Selection(WEEK_SELECTION, 'prestadas de', required=False)
    to_days = fields.Selection(WEEK_SELECTION, 'a', required=False)
    jornada = fields.Selection([
                                ('D','al dia'),
                                ('S','a la semana'),
                                ('M','al mes'),
                                ('A','al año')
                                ],
                                string='Jornada',
                                required=False,
                                default='')
    coef_tp = fields.Float(string="Coeficiente",  required=False, )
    distribution = fields.Char('Distribucion de la jornada', size=250, required=False, readonly=False)

    por_jornada =  fields.Float('Jornada(%)', required=False)

    # Page obra Clausula personal
    cla_per =  fields.Text('Clausula adicional')
    # End Page

    # Page obra servicio
    obser = fields.Char('Obra/Servicio', size=100, required=False, readonly=False)
    # End Page

    # Page circunstacionas
    circuns = fields.Char('Circunstancias', size=100, required=False, readonly=False)
    # End Page

    # Page Interinidad
    teiinter = fields.Selection('_get_teiinter', field_description='Sustituir')
#    get_teiinter = fields.Many2one(related='teiinter')
    teiinter_id = fields.Many2one('hr.employee', field_description='Empleado', required=False, readonly=False)
    # End Page

    # Page anexo horas
    anexo_h = fields.Boolean('Anexo horas complementarias')
    max_hours = fields.Float('Maximo horas', required=False)
    por_hours = fields.Float('Horas complementarias(%)', required=False)
    pre_days = fields.Integer('Horas preaviso', size=2, required=False)
    # End Page

    # Formacion
    tbonvfor_id = fields.Many2one('hr.contract.tbonvfor', 'Nivel formativo')
    # End Formacion

    # Copia Basica
    is_alta_d = fields.Boolean('Contrato alta direccion')
    contract_write = fields.Boolean('Contrato escrito')
    terfircb_id = fields.Many2one('hr.contract.terfircb', string='Copia Basica')
    # End Copia Basica

    # Asistencia Legal
    legal_name = fields.Char('Asistente legal', size=100, required=False, readonly=False)
    legal_id = fields.Char('N.I.F/N.I.E', size=20, required=False, readonly=False)
    legal_type = fields.Char('En Calidad', size=100, required=False, readonly=False)
    # End Asistencia Legal

    # PRORROGA
    """
    type      = fields.Selection([('contract', 'Contrato'),
                                    ('extend', 'Prorroga')],
                                    'Tipo contrato', default='contract', required=False, readonly=False)

    extend      = fields.Selection([('1', 'PRIMERA'),
                                    ('2', 'SEGUNDA'),
                                    ('3', 'TERCERA'),
                                    ('4', 'CUARTA')],
                                    'Numero Prorroga', default=False, required=False, readonly=False)
    """
    # Otros
    state =  fields.Selection([
                            ('draft', 'Borrador'),
                            ('trial', 'Periodo de prueba'),
                            ('contract', 'Contratado'),
                            ('done', 'Finalizado')],
                            default='draft',
                            string='Estado',
                            readonly=True)
    """
    @api.multi
    def _needaction_domain_get(self):
        users_obj = self.pool.get('res.users')
        domain = []
        
        if users_obj.has_group(self._cr, self._uid, 'base.group_hr_manager'):
            domain = [('state', 'in', ['draft', 'trial', 'active'])]
            return domain
        return False
    """
    @api.model
    def create(self, vals):
        #if ('name' not in vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('id.contract') or '/'

        return super(HrContract, self).create(vals)


    """
    @api.onchange('date_begin')
    def _onchange_date_begin(self):
        if self.date_begin and not self.date_end:
            date_begin = fields.Datetime.from_string(self.date_begin)
            self.date_end = fields.Datetime.to_string(date_begin + timedelta(hours=1))
    """

    @api.one
    @api.onchange('date_start')
    def onchange_start(self):
        if self.date_start:
            self.date_signature = self.date_start


