# -*- coding: utf-8 -*-
###########################################################################
#
# © 2016 Juan Jose Lopez Garcia <jjlopezg74@gmail.com>.
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
###########################################################################
from openerp import models, fields, api, _
from datetime import datetime

class ResCotiza(models.Model):
    _name = "res.cotiza"

    @api.one
    @api.depends('name')
    def _compute_name(self):
        self.name = "%s-%s" % (self.code, self.description)

    code = fields.Char("Codigo", required=True, size=2)
    description = fields.Char("Descripcion", required=True, size=128)
    name = fields.Char(compute='_compute_name', size=256)

    smi = fields.Float("S.M.I", required=False, )
    iprem = fields.Float("IPREM", required=False, )

    min_atep = fields.Float("Minimo A.T y E.P", required=False, )
    max_atep = fields.Float("Maximo A.T y E.P", required=False, )

    # Continguencias
        # Empresa
    ecc_comun = fields.Float(string="C. Comunes", required=False, )
    ecc_hextfue = fields.Float(string="Horas Ext. Fuerza Mayor", required=False, )
    ecc_hextres = fields.Float(string="Horas Ext. Resto", required=False, )
    ecc_mayor65 = fields.Float(string="Mayores 65<=38.5 o 67<=37", required=False,
                               help="Mayores de 65 (38.5 Años cotizados) o Mayores de 67 (37 Años cotizados)")
    ecc_mayor60 = fields.Float(string="Mayores 60", required=False, )
        # Trabajador
    tcc_ccomun = fields.Float(string="C. Comunes", required=False, )
    tcc_hextfue = fields.Float(string="Horas Ext. Fuerza Mayor", required=False, )
    tcc_hextres = fields.Float(string="Horas Ext. Resto", required=False, )
    tcc_mayor65 = fields.Float(string="Mayores 65<=38.5 o 67<=37", required=False,
                               help="Mayores de 65 (38.5 Años cotizados) o Mayores de 67 (37 Años cotizados)")
    tcc_mayor60 = fields.Float(string="Mayores 60", required=False, )

    # Desempleo
        # Empresa
    edesem_general = fields.Float(string="Tipo General", required=False, )
    edesem_tcompleto = fields.Float(string="Temporal Tiempo Parcial", required=False, )
    edesem_tparcial = fields.Float(string="Temporal Tiempo Completo", required=False, )
        # Trabajador
    tdesem_general = fields.Float(string="Tipo General", required=False, )
    tdesem_tcompleto = fields.Float(string="Temporal Tiempo Parcial", required=False, )
    tdesem_tparcial = fields.Float(string="Temporal Tiempo Completo", required=False, )

    # Otros
        # Empresa
    eot_fogasa = fields.Float(string="FOGASA", required=False, )
    eot_forma = fields.Float(string="Formacion", required=False, )
        # Trabajador
    tot_fogasa = fields.Float(string="FOGASA", required=False, )
    tot_forma = fields.Float(string="Formacion", required=False, )


    _sql_constraints = [
        ("code_unique", "unique(code)", "Codigo duplicado"),
    ]


