# -*- coding: utf-8 -*-
###########################################################################
#
# © 2016 Juan Jose Lopez Garcia <jjlopezg74@gmail.com>.
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
###########################################################################
from openerp import models, fields, api, _
from datetime import datetime

SELECTION_TIME = [
    ('00', 'Al ir al trabajo'),
    ('01', 'Hora 1'),
    ('02', 'Hora 2'),
    ('03', 'Hora 3'),
    ('04', 'Hora 4'),
    ('05', 'Hora 5'),
    ('06', 'Hora 6'),
    ('07', 'Hora 7'),
    ('08', 'Hora 8'),
    ('09', 'Hora 9'),
    ('98', 'Hora 10'),
    ('98', 'Al volver del trabajo'),
]


SELECTION_CLASS_ACC = [
    ('1', 'En el centro o lugar de trabajo habitual'),
    ('2', 'Al desplazarse durante su jornada laboral'),
    ('3', 'Al ir o volver del trabajo ("in itinere")'),
    ('4', 'En otro lugar o centro de trabajo'),
]

SELECTION_YES_NO = [
    ('0', 'No'),
    ('1', 'Si'),
]

SELECTION_ASSISTANCE = [
    ('1', 'Hospitalaria'),
    ('2', 'Ambulatoria'),
]

SELECTION_DEGREE = [
    ('1', 'Leve'),
    ('2', 'Grave'),
    ('3', 'Muy Grave'),
    ('4', 'Grave'),
]


class HrDelta(models.Model):
    _name ='hr.delta'
    _description = 'Delt@'
    _order ='date_start'

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
    @api.onchange('workers')
    def compute_workers(self):
        employees = 0
        employees = self.env['hr.employee'].search_count([])
        self.workers = employees # FIXME: contar numero empleados

    @api.one
    @api.onchange('base_month', 'days_month')
    def compute_base(self):
        try:
            self.base_reg = self.b_month / self.day_month

        except:
            self.base_reg = 0.0


        #self.b_reg_day = self.ba + self.bb
        self.subsidio_setenta_5 = self.b_reg_day * 75 / 100
        return {
            'warning': _(
                'test')
        }

    user_create = fields.Char(compute='compute_create_user', string='Creado', readonly=True, size=256, store=False)
    user_last = fields.Char(compute='compute_last_user', string='Modificado', readonly=True, size=256, store=False)
    #employee_id = fields.Many2one('hr.employee', string='Empleado', default=lambda self: self.env.context.get('employee_id'), required=True)
    employee_id = fields.Many2one('hr.employee', string='Empleado', required=True)
    date = fields.Datetime(string='Fecha/Hora datos', required=True, default=fields.Date.today)
    name = fields.Char(string='Delt@', size=12, default='000000000000', required=True)

    # PAGE  Accidente
    date_start = fields.Date(string='Fecha Baja', required=True)
    date_acc = fields.Date(string='Fecha accidente', required=True)
    time_acc = fields.Float('Hora accidente', required=True)

    #time_acc = fields.Float(string='Hora del Accidente.', required=True, default=False)
    type = fields.Selection([
                            ('1', 'Accidente'),
                            ('2', 'Recaida'),
                            ],
                            string='Tipo Acc.',
                            default='1',
                            required=True)

    time_trab = fields.Selection(SELECTION_TIME,
                                 string='Hora de Trabajo',
                                 default='',
                                 required=True)
    description = fields.Text('Descripcion Accidente', required=True)
    # FIXME: no obligatorio cuando es inetinere
    habt = fields.Selection(SELECTION_YES_NO,
                            string='Era su trabajo habitual',
                            required=False)
    # FIXME: no obligatorio cuando es inetinere
    eval = fields.Selection(SELECTION_YES_NO,
                            string='Evaluacion de riesgos',
                            required=False,
                            help='Indica si se ha realizado evaluación de riesgos')
    incident = fields.Selection(SELECTION_YES_NO,
                            string='Es un Incidente',
                            required=False)
    # PAGE. Ampliacion
    type_id = fields.Many2one('hr.delta.type', string='Tipo de lugar', required=True)
    work_id = fields.Many2one('hr.delta.type.work', string='Tipo de trabajo', required=True)
    actv_id = fields.Many2one('hr.delta.actv', string='Activida fisica', required=True)
    agen1_id = fields.Many2one('hr.delta.agen', string='Agente mat. act. fisica', required=True)
    desv_id = fields.Many2one('hr.delta.desv', string='Desviacion', required=True)
    agen2_id = fields.Many2one('hr.delta.agen', string='Agente mat. deviacion', required=True)
    form_id = fields.Many2one('hr.delta.form', string='Forma de contacto', required=True)
    agen3_id = fields.Many2one('hr.delta.agen', string='Agente mat. lesion', required=True)
    multi = fields.Selection(SELECTION_YES_NO,
                            string='Afecto a más trabajadores',
                            required=False)
    testigo = fields.Selection(SELECTION_YES_NO,
                            string='Hubo testigos',
                            required=False)
    testigo_text = fields.Text(string='Testigo', required=False)
    mode = fields.Text(string='Modo en el que se a lesionado', required=False)
    # END PAGE. ############################################3
    # PAGE. Lugar
    class_acc = fields.Selection(SELECTION_CLASS_ACC,
                            string='Clase Lugar',
                            default='',
                            required=True)
    traffic = fields.Selection(SELECTION_YES_NO,
                            string='Es de Trafico',
                            required=False)

    street = fields.Char(string='Direccion', size=128, required=False)
    via_km = fields.Char(string='Via Km', size=128, required=False)
    other = fields.Char(string='Otros', size=128, required=False)
    zip = fields.Char('C.P', change_default=True, size=5, required=False)
    city = fields.Char('Municipio', size=128, required=False)
    state_id = fields.Many2one("res.country.state", 'Provincia')
    country_id = fields.Many2one('res.country', 'Pais')
    better_zip_id = fields.Many2one('res.better.zip', string='Location', select=1)
    center = fields.Selection(SELECTION_YES_NO,
                            string='Centro coincide',
                            default='1',
                            required=False)
    in_center = fields.Selection(SELECTION_YES_NO,
                            string='Pertenece',
                            required=False)
    type_cif = fields.Selection([
        ('3', 'Otro tipo'),
        ('C', 'Empresa como contrata o subcontrata'),
        ('T', 'Empresa de trabajo temporal'),
    ],
        string='Tipo de C.I.F',
        required=False)

    #partner = fields.Char(string='Empresa', size=128, required=False)
    #partner_street = fields.Char(string='Direccion', size=128, required=False)
    #zip = fields.Char('Cod. postal', change_default=True, size=5, required=False)
    #city = fields.Char('Municipio', size=128, required=False)
    # state_id = fields.Many2one("res.country.state", 'Provincia', domain="[('country_id', '=', country_id)]")
    # phone = fields.Char(string='Telefono', size=128, required=False)
    #ccc = fields.Char('CCC Acidente', size=11, required=False)
    #cnae = fields.Char('CNAE', size=4, required=False)
    # END PAGE. ############################################
    # PAGE. Asistenciales
    # tipo lesion
    degree = fields.Selection(SELECTION_DEGREE,
                              string='Grado de la lesion',
                              required=True)
    # parte del cuerpo
    assistance = fields.Selection(SELECTION_ASSISTANCE,
                              string='Tipo asistencia sanitaria',
                              required=True)
    doctor = fields.Char(string='Nombre medico', size=128, required=False)
    doctor_street = fields.Char(string='Direccion', size=128, required=False)
    doctor_phone = fields.Char(string='Telefono', size=128, required=False)

    is_hospitalized = fields.Selection(SELECTION_YES_NO,
                               string='ha sido hospitalizado',
                               required=False)
    clinic = fields.Char(string='Centro hospitalario', size=128, required=False)

    # END PAGE. ############################################
    # PAGE. Economicos
    #base = fields.Monetary(string='Base', compute='_compute_base_amount')
    #amount = fields.Monetary()
    currency_id = fields.Many2one('res.currency', string='Currency', readonly=True, states={'draft': [('readonly', False)]},
                                  default=lambda self: self.env.user.company_id.currency_id)

    base_month = fields.Float(string='Base cotiz. mes ant.', digits=(16, 2), required=False, readonly=False)
    days_month = fields.Integer(string='Dias cotiz. mes ant.', readonly=False)

    hours_ext = fields.Float('B1 Horas Extra', digits=(16, 2), required=False, readonly=False)
    day_hours_ext = fields.Integer('Dias H Ext.', readonly=False)
    b2_other = fields.Float('B2 Otros', digits=(16, 2), required=False, readonly=False)
    real_salary = fields.Float('Salario Real', digits=(16, 2), required=False, readonly=False)
    # Funcionales
    ba = fields.Float('Base A', digits=(16, 2), readonly=False)
    bb = fields.Float('Base B', digits=(16, 2), readonly=False)
    b_b2 = fields.Float('B1+B2', digits=(16, 2), readonly=False)
    promedio_b = fields.Float('Promedio B', digits=(16, 2), readonly=False)
    b_reg = fields.Float('Base Reg.', digits=(16, 2), readonly=False)
    subsidio_setenta_5 = fields.Float(string='Subsidio 75%', digits=(16, 2), readonly=False)
    b_reg_day = fields.Float(string='Base Diaria', digits=(16, 2), readonly=False)

    """
    """
    # END PAGE. ############################################
    # PAGE. Adicionales
    job = fields.Char(string='Ocupacion', size=4, required=True)
    a_contract = fields.Selection([ # FIXME: poner la correspondencia
                        ('0', 'No'),
                        ('0', 'Si'),
                        ('0', 'No contesta'),
                        ],
                        default='0',
                        string='Contrata',
                        required=False)
    workers = fields.Integer(compute='compute_workers', string='Plantilla', readonly=True, size=10, store=True) # FIXME; poner status=alta
    # END PAGE. ############################################
    # PAGE. Actor
    name_send = fields.Char(string='Nombre Emisor', size=128, required=True)
    job_send = fields.Char(string='Cargo Emisor', size=128, required=True)
    state_send_id = fields.Many2one("res.country.state", 'Provincia')
    # END PAGE. ############################################

    #data_fname = fields.Char('Nombre Fichero', size=32)
    #data       = fields.Binary("Fichero", readonly=True)

    state = fields.Selection([
                            ('draft', 'Por enviar'),
                            ('send', 'Enviado'),
                            ('done', 'Aceptado'),
                            ('refuse', 'Rechazado'),
                            ('cancel', 'Cancelado'),
                        ],
                        string='Estado',
                        default='draft',
                        required=True)


    @api.onchange('better_zip_id')
    def on_change_city(self):
        if self.better_zip_id:
            self.zip = self.better_zip_id.name
            self.city = self.better_zip_id.city
            self.state_id = self.better_zip_id.state_id
            self.country_id = self.better_zip_id.country_id


    @api.multi
    def onchange_state(self, state_id):
        if state_id:
            state = self.env['res.country.state'].browse(state_id)
            return {'value': {'country_id': state.country_id.id}}
        return {}


class HrDeltaType(models.Model):
    _name = "hr.delta.type"
    _description = 'Tipo de lugar'

    code = fields.Char('code', size=3, required=True)
    description = fields.Char("Descripcion", size=256, required=True)
    name = fields.Char(compute='_compute_name', size=256)

    _sql_constraints = [
        ("code_unique", "unique(code)", "Codigo duplicado"),
    ]

    @api.one
    @api.depends('name')
    def _compute_name(self):
        self.name = "%s-%s" % (self.code, self.description)

class HrDeltaTrab(models.Model):
    _name = "hr.delta.type.work"
    _description = 'Delt@-Tipo de trabajo'

    code = fields.Char('code', size=2, required=True)
    description = fields.Char("Descripcion", size=256, required=True)
    name = fields.Char(compute='_compute_name', size=256)

    _sql_constraints = [
        ("code_unique", "unique(code)", "Codigo duplicado"),
    ]

    @api.one
    @api.depends('name')
    def _compute_name(self):
        self.name = "%s-%s" % (self.code, self.description)

class HrDeltaActv(models.Model):
    _name = "hr.delta.actv"
    _description = 'Delt@-Tipo de actividad'

    code = fields.Char('code', size=2, required=True)
    description = fields.Char("Descripcion", size=256, required=True)
    name = fields.Char(compute='_compute_name', size=256)

    _sql_constraints = [
        ("code_unique", "unique(code)", "Codigo duplicado"),
    ]

    @api.one
    @api.depends('name')
    def _compute_name(self):
        self.name = "%s-%s" % (self.code, self.description)

class HrDeltaDesv(models.Model):
    _name = "hr.delta.desv"
    _description = 'Delt@-Tipo de desviacion'

    code = fields.Char('code', size=2, required=True)
    description = fields.Char("Descripcion", size=256, required=True)
    name = fields.Char(compute='_compute_name', size=256)

    _sql_constraints = [
        ("code_unique", "unique(code)", "Codigo duplicado"),
    ]

    @api.one
    @api.depends('name')
    def _compute_name(self):
        self.name = "%s-%s" % (self.code, self.description)

class HrDeltaForma(models.Model):
    _name = "hr.delta.form"
    _description = 'Delt@-Tipo de forma'

    code = fields.Char('code', size=2, required=True)
    description = fields.Char("Descripcion", size=256, required=True)
    name = fields.Char(compute='_compute_name', size=256)

    _sql_constraints = [
        ("code_unique", "unique(code)", "Codigo duplicado"),
    ]

    @api.one
    @api.depends('name')
    def _compute_name(self):
        self.name = "%s-%s" % (self.code, self.description)

class HrDeltaAgen(models.Model):
    _name = "hr.delta.agen"
    _description = 'Delt@-Tipo de agente'

    code = fields.Char('code', size=8, required=True)
    description = fields.Char("Descripcion", size=256, required=True)
    name = fields.Char(compute='_compute_name', size=256)

    _sql_constraints = [
        ("code_unique", "unique(code)", "Codigo duplicado"),
    ]

    @api.one
    @api.depends('name')
    def _compute_name(self):
        self.name = "%s-%s" % (self.code, self.description)