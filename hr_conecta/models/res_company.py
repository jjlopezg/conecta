#-*- coding:utf-8 -*-
###########################################################################
#
# © 2016 Juan Jose Lopez Garcia <jjlopezg74@gmail.com>.
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
###########################################################################
from openerp import models, fields, api, _

class ResCompany(models.Model):
    _inherit = 'res.company'

    @api.one
    @api.depends('ccc')
    def _compute_ccc(self):
        self.ccc = '%s/%s/%s' % (self.ccc_prov, self.ccc_cod, self.ccc_dc)

    ccc = fields.Char(compute='_compute_ccc', size=11, string='Cuenta Cotizacion')
    ccc_prov = fields.Char(string='Prov. Cuenta Cotizacion', size=2, required=True)
    ccc_cod = fields.Char(string="Cod. Cuenta Cotizacion", size=7, required=True)
    ccc_dc = fields.Char("Dig. Control Cuenta Cotizacion", size=2, required=True)
    office = fields.Char(string="Oficina Empleo", size=128, required=True)
    cnae_id = fields.Many2one("res.cnae", string="Codigo actividades economicas", required=True, domain="[('code', '=ilike', '_____')]")
    mutua_id = fields.Many2one("res.mutua", string="Mutua Accidentes", required=True)
    regimen_id = fields.Many2one("res.regimen", string="Regimen de cotizacion", required=True)
    manager_id = fields.Many2one('hr.employee', string='Representante legal', required=True)
    cotiza_id = fields.Many2one('res.cotiza', string='Tipo de Cotizacion', required=True)

    # TODO: necesario para los AFI TGSS - Tipo de Empresario Tabla-8
    emp_type = fields.Selection([
            ('1', 'Individual'),
            ('2', 'Colectivo'),
            ('3', 'Sin personalidad jurídica'),
            ('4', 'Entidad u Organismo de las Admones.Públicas'),
            ],
            string='Tipo de Empresario',
            required=True,
            default='1',
            readonly=False)

    # TODO: añadir cuenta analitica o centro de costes
    # TODO: añadir convenio colectivo

    # TODO: necesario para los AFI TGSS - Tipo de identificación de empresario Tabla-3
    vat_type = fields.Selection([
            ('1', 'D.N.I., N.I.F.'),
            ('6', 'Número de Identificación de Extranjero'),
            ('9', 'Código de Identificación Fiscal'),
            ('K', 'Españoles sin DNI < 14 años'),
            ('L', 'Españoles sin DNI'),
            ('M', 'Extranjeros sin NIF'),
            ],
            string='Tipo Ident. Empresario',
            required=True,
            default='1',
            readonly=False)

