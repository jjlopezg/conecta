# -*- encoding: utf-8 -*-
###########################################################################
#
# © 2016 Juan Jose Lopez Garcia <jjlopezg74@gmail.com>.
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
###########################################################################
from openerp import models, fields, api, _

class HrPrlTraining(models.Model):

    _name = "hr.prl.training"

    name = fields.Char('Idioma', size=128, required=True)

    date_start = fields.Date(string='Fecha Inicio', required=False)
    time_start = fields.Float(string='Hora', required=True, default=False)
    date_end = fields.Date(string='Fecha Fin', required=False)

    employee_id = fields.Many2one('hr.employee', string='Empleado')
