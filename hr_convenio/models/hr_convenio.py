# -*- coding: utf-8 -*-
###########################################################################
#
# © 2016 Juan Jose Lopez Garcia <jjlopezg74@gmail.com>.
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
###########################################################################
from openerp import models, fields, api, _
from datetime import datetime

class HrConvenio(models.Model):
    _name = "hr.convenio"

    @api.one
    def _compute_create_user(self):
        self.user_create = "%s:%s" % (self.create_uid.login.split('@')[0],
                                      datetime.strptime(self.create_date, '%Y-%m-%d %H:%M:%S').strftime('%d-%m-%Y-%H:%M:%S'))

    @api.one
    def _compute_last_user(self):
        self.user_last = "%s:%s" % (self.write_uid.login.split('@')[0],
                                    datetime.strptime(self.write_date, '%Y-%m-%d %H:%M:%S').strftime('%d-%m-%Y-%H:%M:%S'))

    @api.depends('name')
    def _compute_name(self):
        self.name = "%s-%s" % (self.code, self.description)

    @api.one
    def _get_catg(self):
        print "DEFAULT CAT ***********************************"
        return

    user_create = fields.Char(compute='_compute_create_user', string='Creado', readonly=True, size=256, store=False)
    user_last = fields.Char(compute='_compute_last_user', string='Modificado', readonly=True, size=256, store=False)
    company_id = fields.Many2one('res.company', string="Company", required=True, readonly=False)

    code = fields.Char("Codigo", required=True, size=20)
    description = fields.Char("Descripcion", required=True, size=250)
    name = fields.Char(compute='_compute_name', size=256)

    date_start = fields.Date('Inicio', required = True)
    date_end = fields.Date('Termino', required=True)
    max_legal = fields.Boolean('Exceder maximo legal', help="El convenio colectivo permite la contratacion por una duracion mayor que la legalmente establecidad")

    #'days_ap': fields.integer('Asuntos (Dias)', help="Dias permitidos y retribuidos"),
    hours_year = fields.Float('Horas jornada anual', digits=(4, 2))
    hours_week = fields.Float('Horas jornada semanal', digits=(4, 2))
    hours_month = fields.Float('Horas jornada mensual', digits=(4, 2))
    hours_day = fields.Float('Horas jornada diaria', digits=(4, 2))

    catg_ids = fields.One2many('hr.convenio.catg.cov', 'convenio_id', string='Categorias', readonly=False)

    state = fields.Selection([
                            ('draft', 'Borrador'),
                            ('active', 'Vigente'),
                            ('done', 'Finalizado')],
                            string='Estado',
                            default='draft',
                            readonly=True)


    _sql_constraints = [
        ("code_unique", "unique(code)", "Codigo duplicado"),
    ]

    @api.one
    def do_draft(self):
        self.write({'state': 'draft'})

    @api.one
    def do_active(self):
        self.write({'state': 'active'})

    @api.one
    def do_done(self):
        self.write({'state': 'done'})
