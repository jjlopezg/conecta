# -*- encoding: utf-8 -*-
###########################################################################
#
# © 2016 Juan Jose Lopez Garcia <jjlopezg74@gmail.com>.
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
###########################################################################

from openerp import models, fields, api, _
from openerp.exceptions import Warning
from StringIO import StringIO
from lxml import etree
from openerp import tools
from datetime import date, datetime
import logging
import base64


logger = logging.getLogger(__name__)

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

class HrSepeCreate(models.TransientModel):
    _name = "hr.sepe.create"

    file       = fields.Binary("file", readonly=True)
    file_name = fields.Char('file name', size=64)
    note       = fields.Text('Log')
    sepe_ids   = fields.Many2many('hr.sepe', 'hr_sepe_rel', 'contract_id', 'sepe_id', string='Comunicaciones', required=False)

    real = fields.Boolean('Aplicar cambios')
    schem = fields.Boolean('Aplicar esquema')

    type = fields.Selection([
                            ('FICHERO_CONTRATOS', 'Contrato'),
                            ('FICHERO_PRORROGAS', 'Prorroga'),
                            ('transfor', 'Transformacion'),
                            ('ring', 'Llamamiento'),
                            ('basic', 'Copia Basica')
                            ],
                            string='Tipo Comunicacion',
                            required=True,
                            readonly=False,
                            default='FICHERO_CONTRATOS')

    state = fields.Selection([
                            ('draft', 'Borrador'),
                            ('fail', 'Error'),
                            ('done','Realizado'),
                            ],
                            string='Estado',
                            required=True,
                            default='draft',
                            readonly=False)

    @api.multi
    def do_process(self):
        sepe_ids = []

        for id in self.sepe_ids:
            sepe_ids.append(id.id)

        if sepe_ids:
            self.create_file(sepe_ids)

        return self.do_reload()

    @api.model
    def create_file(self, sepe_ids):
        log = Log()
        log.add(_("Resumen:\n"))

        xml = self.env['report'].get_html(self, self.env.ref('hr_sepe.report_' + self.type).report_name)
        tree = etree.fromstring(xml, etree.XMLParser(remove_blank_text=True))
        xml = etree.tostring(tree, pretty_print=True, encoding="iso-8859-1")

        if self.schem:
            schema = etree.XMLSchema(etree.parse(tools.file_open(
                    "EsquemaContratos50.xsd", subdir="addons/hr_sepe/data")))
            try:
                schema.assertValid(etree.fromstring(xml))
            except Exception, e:
                log.add(_("Error de esquema:\n"))
                log.add(_(e))
                log.add(_(schema.error_log))
                self.write({
                    'note': log(),
                    'file': False,
                    'file_name': False,
                    'state': 'fail'
                })

        if self.state != 'fail':
            sepe_file = xml
            file_name = (_(self.type + '_'  + datetime.today().strftime('%Y%m%d_%H%M%S') + '.xml')).replace('-', '')

            file = base64.b64encode(sepe_file)

            self.env['ir.attachment'].create({
                    'name': file_name,
                    'datas': file,
                    'datas_fname': file_name,
                    'res_model': self._name,
                    })


            self.write({
                    'note': log(),
                    'file': file,
                    'file_name': file_name,
                    'state': 'done',
                })


    @api.multi
    def do_back(self):
        self.write({
            'file': False,
            'file_name': False,
            'state': 'draft'
        })

        return self.do_reload()

    @api.multi
    def do_reload(self):

        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'view_type': 'form',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
        }


    @api.model
    def do_real(self, sepe):
        if self.real and sepe.state == 'draft':
            sepe.write({
                'state': 'send',
            })
            self.sepe_ids = [(2, sepe.id,)]