# -*- encoding: utf-8 -*-
###########################################################################
#
# © 2016 Juan Jose Lopez Garcia <jjlopezg74@gmail.com>.
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
###########################################################################
from openerp import models, fields, api, _
import time


class HrContract(models.Model):
    _inherit = 'hr.contract'

    type_id = fields.Many2one('hr.contract.type', 'Tipo Contrato', default=False, required=True)

    @api.onchange('type_id')
    def onchange_type(self):
        types = self.env['hr.contract.type'].search([
                ('date_from', '<=',  time.strftime('%Y-%m-%d')),
                '|',
                ('date_to', '=', False),
                ('date_to', '>=',  time.strftime('%Y-%m-%d')),
            ])
        ids = map(int, types)
        return {'domain':
                        {'type_id': [('id','in', ids)],}
                }

    @api.multi
    def printer(self, ids):
        """
        import urllib2
        try:
            import json
        except ImportError:
            import simplejson as json


        contracts = self.search([('id', 'in', self.ids)])
        params = []
        for contract in contracts:
            fields = [
                ('ID_EMPR', contract.company_id.vat),
                ('Texto4', contract.company_id.manager_id.name),
                ('Texto5', contract.company_id.manager_id.identification_id),
            ]
            params.append({
                        "id": contract.id,
                        "model": contract._name,
                        "template": contract.type_id.template,
                        "filename": 'testhttp.pdf',
                        "fields": fields}
            )
        report = {"jsonrpc": "2.0",
                  'id': 0,
                  "params": {
                      "ids": self.ids,
                      "models": params}
                  }

        try:
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            content = urllib2.urlopen(
                urllib2.Request(
                    "http://127.0.0.1:8069/conecta/report/",
                    json.dumps(report),
                    headers),
                timeout=10000000)
        except urllib2.HTTPError, e:
            print e.code
            print _("Error: %s, %s" % (e.code, e.message))
        """
        return {'type': 'ir.actions.act_url', 'url': "/conecta/report/%s" % (self.ids), 'target': 'self'}









"""
    @api.multi
    def action_view_all_rating(self):

        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'name': "Redirect to the Website Projcet Rating Page",
            'target': 'self',
            'url': "/project/rating/%s" % (self.id,)
        }

    @api.multi
    def _website_url(self, field_name, arg):
        res = dict()
        for project in self:
            res[project.id] = "/project/rating/%s" % project.id
        return res
"""