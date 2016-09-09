# -*- coding: utf-8 -*-
###########################################################################
#
# © 2016 Juan Jose Lopez Garcia <jjlopezg74@gmail.com>.
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
###########################################################################
from openerp import models, fields, api, exceptions, _
from datetime import datetime
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT as OE_DFORMAT

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    @api.one
    @api.depends('home_street_name', 'home_street_number')
    def _get_street(self):
        self.street = '%s, %s' % (self.home_street_name, self.home_street_number)

    @api.one
    @api.onchange('birthday')
    def _compute_age(self):
         if self.birthday:
            dBday = datetime.strptime(self.birthday, OE_DFORMAT).date()
            dToday = datetime.now().date()
            self.age = (dToday - dBday).days / 365

    @api.one
    def _compute_ssnid(self):
        self.ssnid = '%s/%s/%s' % (self.ssnid_p, self.ssnid_n, self.ssnid_dc)

    company_id = fields.Many2one('res.company', string="Compañia", select=True, required=True, readonly=False)
    employee = fields.Boolean(string='Es Empleado', default=True) # FIXME: ODOO MOBILE
    id_employee = fields.Char(string='Id.Empleado', default='/')

    ssnid = fields.Char(compute='_compute_ssnid', string='Nº Seguridad Social', size=12)
    ssnid_p = fields.Char(string='Prov.NASS', size=2, required=True)
    ssnid_n = fields.Char(string='Nº NASS', size=8, required=True)
    ssnid_dc = fields.Char(compute='_numss', string='Dc.NASS', size=2, required=True)

    identification_id = fields.Char(string='Identification No', size=14, required=False)
    identification = fields.Many2one('hr.identification', string='Tipo Identificacion')

    age = fields.Integer(compute="_compute_age", string='Edad', size=3, readonly=True)
    gender = fields.Selection([
                            ('male', 'Male'),
                            ('female', 'Female'),
                            ],
                            string='Gender',
                            default = '',
                            required = True)

    home_street = fields.Char(compute='_get_street', string='Domicilio', store=True)

    home_street_name = fields.Char('Street name', required=True)
    home_street_number = fields.Char('Street number', required=True)
    home_zip = fields.Char('C.P', change_default=True, size=5, required=True)
    home_city = fields.Char('Municipio', required=True)
    home_state_id = fields.Many2one("res.country.state", 'Provincia', required=True, domain="[('country_id', '=', country_id)]")
    home_country_id = fields.Many2one('res.country', 'Pais', required=True)
    home_better_zip_id = fields.Many2one('res.better.zip', string='Location', select=1)
    home_phone = fields.Char('Telefono', readonly=False)
    home_mobile = fields.Char('Movil', readonly=False)
    home_email = fields.Char('Correo', size=128)

    status = fields.Selection([
                            ('draft', 'Candidato'),
                            ('active', 'Activo'),
                            ('inactive', 'Baja'),
                            ],
                            'Status',
                            default='draft',
                            readonly=True)



    _sql_constraints = [
        ('id_employee_uniq', 'unique(id_employee)', 'Numero de empleado debe de ser unico.'),
        ('identification_id_uniq', 'unique(identification_id)', 'Numero de identificacion debe de ser unico.'),
        ('ssnid_uniq', 'unique(ssnid)', 'El NASS debe de ser unico.'),
    ]

    @api.model
    def create(self, vals):
        print "CREATE---------------------------------------------------"
        vals['id_employee'] = self.env['ir.sequence'].next_by_code('id.employee')  or '/'
        vals['name'] = vals['name'].upper()
        return super(HrEmployee, self).create(vals)

    @api.multi
    def write(self, vals):
        print "WRITE---------------------------------------------------"

        return super(HrEmployee, self).write(vals)

    @api.multi
    def unlink(self):
        print "UNLINK---------------------------------------------------"
        if self.status not in ['draft']:
            raise exceptions.Warning(_("Only in 'draft' state can be removed"))

        print self.name_id.unlink()
        #FIXME: no deja borrar, porque ????
        return super(HrEmployee, self).unlink()


    @api.one
    @api.onchange('identification_id')
    def _onchange_identification_id(self):
        if self.identification_id:
            self.identification_id = ''.join(self.identification_id.upper().split())

    @api.one
    @api.onchange('home_better_zip_id')
    def on_change_city(self):
        if self.home_better_zip_id:
            self.home_zip = self.home_better_zip_id.name
            self.home_city = self.home_better_zip_id.city
            self.home_state_id = self.home_better_zip_id.state_id
            self.home_country_id = self.home_better_zip_id.country_id


    @api.multi
    def onchange_state(self, state_id):
        if state_id:
            state = self.env['res.country.state'].browse(state_id)
            return {'value': {'country_id': state.country_id.id}}
        return {}

    @api.one
    @api.onchange('ssnid_p', 'ssnid_n')
    def _numss(self):
        if self.ssnid_p and self.ssnid_n:
            NumSS = self.ssnid_p + self.ssnid_n
            print NumSS
            dc = '--'
            if NumSS:
                if len(NumSS) == 9 or len(NumSS) == 10:
                    print NumSS[2:3]
                    print "p1"
                    if NumSS[2:3] == '0':
                        print "p2"
                        NumSS = NumSS[0:2] + NumSS[2:len(NumSS)-3]
                    dc = int(NumSS) % 97
                    print "dc", dc
                    if dc <= 9:
                        dc = '0' + str(dc)
                    if dc > 9:
                        self.ssnid_dc = str(dc)
                # TODO: Descomentar en produccion, con las tablas limpias
                #else:
                     #raise exceptions.ValidationError("Longuitud incorrecta");
            self.ssnid_dc = str(dc)

