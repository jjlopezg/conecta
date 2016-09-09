# -*- encoding: utf-8 -*-
###########################################################################
#
# © 2016 Juan Jose Lopez Garcia <jjlopezg74@gmail.com>.
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
###########################################################################
from openerp import models, fields, api, exceptions, _

class HrConvenioCatgCov(models.Model):
    _name = "hr.convenio.catg.cov"

    @api.one
    @api.depends('name')
    def _compute_name(self):
        self.name = "%s-%s" % (self.categoria_id.code, self.categoria_id.description)


    name = fields.Char(compute='_compute_name', size=256)
    categoria_id = fields.Many2one('hr.convenio.catg', string='Categoria', required=True)
    grp_id = fields.Many2one('hr.convenio.grpcot', string='Grp. Cotizacion', required=True)
    cno_id = fields.Many2one('res.cno', string='Codigo ocupacion', required=True)
    cno_modif_id = fields.Many2one('res.cno.modif', string='Modif. ocupacion', required=True)
    convenio_id = fields.Many2one('hr.convenio', string='Convenio', default=lambda self: self.env.context.get('convenio_id'), required=True, readonly=False)

    _sql_constraints = [
        ("code_unique", "unique(code)", "Codigo duplicado"),
    ]

class HrConvenioGrCot(models.Model):
    _name = "hr.convenio.grpcot"

    code = fields.Char("Code", required=True, size=2)
    description = fields.Char("Description", required=True, size=128)
    name = fields.Char(compute='_compute_name', size=256)

    min = fields.Float("Minimo", required=False, size=5)
    max = fields.Float("Maximo", required=False, size=5)
    type = fields.Selection([
                            ("D", "Dia"),
                            ("M", "Mes"),
                            ],
                            string="Tipo Cotizacion",
                            default='',
                            required=False)

    _sql_constraints = [
        ("code_unique", "unique(code)", "Codigo duplicado"),
    ]

    @api.one
    @api.depends('name')
    def _compute_name(self):
        self.name = "%s-%s" % (self.code, self.description)

class HrConvenioCatg(models.Model):
    _name = "hr.convenio.catg"

    code = fields.Char("Code", required=True, size=5)
    description = fields.Char("Description", required=True, size=250)
    name = fields.Char(compute='_compute_name', size=256)

    _sql_constraints = [
        ("code_unique", "unique(code)", "Codigo duplicado"),
    ]

    @api.one
    @api.depends('name')
    def _compute_name(self):
        self.name = "%s-%s" % (self.code, self.description)



