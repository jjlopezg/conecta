# -*- coding: utf-8 -*-
###########################################################################
#
# © 2016 Juan Jose Lopez Garcia <jjlopezg74@gmail.com>.
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
###########################################################################
from openerp import models, fields, api, exceptions, _

class HrEmployee(models.Model):
    _inherit = 'hr.employee'


    def _fiscal_last_id(self):
        self.fiscal_last_id = self.env['hr.employee.fiscal'].search([('employee_id', '=', self.id)], limit=1, order='date_from desc')

    fiscal_ids = fields.One2many('hr.employee.fiscal', 'employee_id', string='Datos Fiscales')
    fiscal_last_id = fields.One2many('hr.employee.fiscal', compute='_fiscal_last_id', string='Datos Fiscales')

    # info: Obtener el ultimo periodo fiscal
    @api.one
    def get_period_fiscal(self, date_from, date_to):
        print "GET PERIOD FISCAL ##############################################"
        fiscal = self.fiscal_ids.filtered(lambda x: (x.date_start >= date_from and x.date_end >= date_to ))

        result = fiscal.compute_irpf()
        if result:
            print "GET PERIOD: %s"%result[0]
            return result[0]
        else:
            raise exceptions.Warning("No Existe ningun periodo fiscal, para el calculo del IRPF")



        """
            self.env['hr.employee.fiscal'].search([
                                ('date_start', '>=' date_from),
                                ('date_end', '=', date_to),
                                ],
                                order='date_start', limit=1)
        """


    @api.multi
    def printer(self, ids):
        import urllib2
        try:
            import json
        except ImportError:
            import simplejson as json
        """
        print ids
        print self.ids
        employees = self.search([('id', 'in', self.ids)])
        params = []
        print employees
        for employee in employees:
            params.append({
                        "id": employee.id,
                        "model": employee._name,
                        "template": 'Modelo145.pdf',
                        "filename": 'test_json.pdf',
                        "fields": [
                            ('Texto4', employee.name),
                        ]
            })

        report = {"jsonrpc": "2.0",
                  'id': 0,
                  'method': 'call',
                  "params": {
                      "ids": self.ids,
                      "data": params}
                  }

        try:
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            urllib2.urlopen(
                urllib2.Request(
                    "http://127.0.0.1:8069/conecta/report/",
                    json.dumps(report),
                    headers),
                timeout=10000000)

        except urllib2.HTTPError, e:
            print e.code
            print _("Error: %s, %s" % (e.code, e.message))
        """
        return {'type': 'ir.actions.act_url', 'url': "/conecta/employee/%s" % (self.ids), 'target': 'self'}



