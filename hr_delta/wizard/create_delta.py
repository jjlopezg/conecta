# -*- coding: utf-8 -*-
###########################################################################
#
# © 2016 Juan Jose Lopez Garcia <jjlopezg74@gmail.com>.
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
###########################################################################

import base64
from openerp import api, fields, models, _
from openerp.exceptions import Warning as UserError
import logging
from lxml import etree
from datetime import datetime

logger = logging.Logger(__name__)


class Log(Exception):
    def __init__(self):
        self.content = ""
        self.error = False

    def add(self, s, error=True):
        self.content = self.content + s
        if error:
            self.error = error

    def __call__(self):
        return self.content

    def __str__(self):
        return self.content


class CreateDelta(models.TransientModel):
    _name = "create.delta"

    @api.one
    def compute_create_user(self):
        self.user_create = "%s:%s" % (self.create_uid.login.split('@')[0],
                                      datetime.strptime(self.create_date, '%Y-%m-%d %H:%M:%S').strftime(
                                          '%d-%m-%Y %H:%M:%S'))

    @api.one
    def compute_last_user(self):
        self.user_last = "%s:%s" % (self.write_uid.login.split('@')[0],
                                    datetime.strptime(self.write_date, '%Y-%m-%d %H:%M:%S').strftime(
                                        '%d-%m-%Y %H:%M:%S'))

    user_create = fields.Char(compute='compute_create_user', string='Creado', readonly=True, size=256, store=False)
    user_last = fields.Char(compute='compute_last_user', string='Modificado', readonly=True, size=256, store=False)
    delta = fields.Binary('Delt@ file', readonly=True)
    delta_fname = fields.Char("File name", size=64)
    note = fields.Text('Log')
    state = fields.Selection([('first', 'First'), ('second', 'Second')],
                             'State', readonly=True, default='first')

    @api.multi
    def create_delta_file(self):

        log = Log()
        delta_ids = self.env.context.get('active_ids', [])

        if not delta_ids or len(delta_ids) > 1:
            raise UserError(_('You can only select one to export'))

        delta = self.env['hr.delta'].browse(delta_ids[0])
        report = self.env.ref('hr_delta.report_delta')
        xml_delta = self.env['report'].get_html(delta, report.report_name)
        tree = etree.fromstring(xml_delta, etree.XMLParser(remove_blank_text=True))
        xml_delta = etree.tostring(tree, pretty_print=True, encoding="iso-8859-1")

        delta_file = xml_delta
        file_name = (_('delta' + '_'  + self.user_last)).replace('-', '')
        file_name = (file_name + '.xml').replace(':', '')

        file = base64.b64encode(delta_file)

        self.env['ir.attachment'].create({
            'name': file_name,
            'datas': file,
            'datas_fname': file_name,
            'res_model': 'hr.delta',
            'res_id': delta.id
        })
        log.add(_("Delt@ creado\n\nResumen:\nEmpleado: %s\n") %
                delta.employee_id.name)
        self.write({
            'note': log(),
            'delta': file,
            'delta_fname': file_name,
            'state': 'second'
        })
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'create.delta',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'views': [(False, 'form')],
            'target': 'new'
        }