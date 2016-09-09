# -*- encoding: utf-8 -*-
###########################################################################
#
# © 2016 Juan Jose Lopez Garcia <jjlopezg74@gmail.com>.
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
###########################################################################
from openerp import models, fields, api, _

class HrSchoolLanguage(models.Model):

    _name = "hr.school.language"

    name = fields.Char('Idioma', size=128, required=True)
    is_read = fields.Boolean('Leido')
    is_write = fields.Boolean('Escrito')
    is_speak = fields.Boolean('Hablado')
    notes = fields.Text('Anotaciones')
    employee_id = fields.Many2one('hr.employee', string='Empleado')
