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

class HrEmployeeName(models.Model):
    _name = "hr.employee.name"

    firstname = fields.Char(string="Nombre", default='')
    lastname = fields.Char(string="Primer apellido", default='')
    lastname2 = fields.Char(string="Segundo apellido", default='')
    tc2 = fields.Char(compute='_compute_tc2', string='Nombre tc2', default='')
    name = fields.Char(compute='_compute_name', string='Nombre completo')

    @api.one
    def _compute_name(self):
        self.name = '%s %s, %s' % (self.lastname, self.lastname2, self.firstname)

    @api.one
    def _compute_tc2(self):
        self.tc2 = '%s%s%s' % (self.lastname[:2], self.lastname2[:2], self.firstname[:1])


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    @api.model
    def _name_parts(self, vals):
        parts = []
        if vals.get('name') != False:
            if ',' in vals.get('name'):
                lastname, firstname = vals.get('name').split(",", 1)  # si hay coma parte en dos
                parts = [firstname.upper().strip()] + lastname.upper().strip().split(" ", 1)  # lastname lo parte en dos por los espacios
            else:
                parts = vals.get('name').split(' ', 2)  # lo parte en dos por los espacios

        while len(parts) < 3:
            parts.append('')

        return {"firstname": parts[0],
                "lastname": parts[1],
                "lastname2": parts[2]}

    name_id = fields.Many2one('hr.employee.name', string='Detalle', required=False)

    @api.model
    def create(self, vals):
        vals['name_id'] = self.env['hr.employee.name'].create(self._name_parts({'name': vals.get('name')})).id


        return super(HrEmployee, self).create(vals)

    @api.multi
    def write(self, vals):
        if vals.has_key('name'):
            self.name_id.write(self._name_parts({'name': vals['name']}))
            vals['name'] = self.name_id.name

        return super(HrEmployee, self).write(vals)

