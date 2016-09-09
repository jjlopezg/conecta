# -*- encoding: utf-8 -*-
###########################################################################
#
# © 2016 Juan Jose Lopez Garcia <jjlopezg74@gmail.com>.
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
###########################################################################
from openerp import models, fields, api, exceptions, _
import logging
import base64

try:
    import cStringIO as StringIO
except ImportError:
    import StringIO

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

class HrRedCreateFdi(models.TransientModel):
    _name = "hr.red.create.fdi"

    #company_id = fields.Many2one('res.company', 'Compañia', default=lambda self: self.env.user.company_id, required=True)
    company_ids = fields.Many2many('res.company', 'fdi_company_rel', 'fdi_id', 'company_id', string='Compañia', required=True)

    password = fields.Char(string='Clave Auth.', size=8, required=True)
    # TODO: PONER FECHA Y HORA AUTOMATICO ????
    date = fields.Date(string='Fecha', required=True)
    time = fields.Float(string='Hora', required=True)
    file = fields.Binary(string="Fichero", readonly=False)
    filename = fields.Char(string='Fichero', size=12, required=False)
    user_filename = fields.Char(string='Nombre del Fichero', size=8, required=True)
    note = fields.Text('Log')
    fdi_ids = fields.Many2many('hr.red.fdi', 'hr_red_fdi_create_rel', 'fdi_id','contract_id', string='Comunicacion FDI')
    """
    status = fields.Selection([
                                ('2', 'Comunicar Bajas'),
                                ('3', 'Comunicar Partes Confirmacion'),
                                ('4', 'Comunicar Altas'),
                            ],
                            string='Comunicacion',
                            default='',
                            required=True,
                            readonly=False)
    """
    state = fields.Selection([
                            ('draft', 'Borrador'),
                            ('fail', 'Error'),
                            ('done','Realizado'),
                            ],
                            string='Estado',
                            required=True,
                            default='draft',
                            readonly=False)


    @api.model
    @api.onchange('company')
    def onchange_fdi(self):
        self.fdi_ids = False


    @api.multi
    def do_process(self):


        if self.fdi_ids:
            self.filename = self.user_filename
            self.create_fdi()


        return self.do_reload()

    @api.model
    def create_fdi(self):
        log = Log()
        log.add(_("Resumen:\n"))

        report = self.env['report'].get_html(self, self.env.ref('hr_red_fdi.report_fdi').report_name)

        lines = [arg.strip()[1:71] for arg in (report).split(",")]
        print lines
        print "----------------------------------------------------"

        for a in lines:
            print len(a)
        print "----------------------------------------------------"
        stream = StringIO.StringIO()

        for line in lines:
            print line
            stream.write(line.join('\n\r'))

        # TOFIX: el la cadena stream siempre al escribir el fichero pone un salto de linea? por que? se elimina con [1:0]
        file = base64.encodestring(stream.getvalue()[1:])
        stream.close()

        self.filename = ''.join('%s.%s' % (self.user_filename, 'fdi'))

        self.env['ir.attachment'].create({
            'name': self.filename,
            'datas': file,
            'datas_fname': self.filename,
            'res_model': self._name,
        })

        print log()

        self.write({
            'note': log(),
            'file': file,
            'filename': self.filename,
            'state': 'done'
        })



    @api.multi
    def do_back(self):
        self.write({
            'file': False,
            'filename': False,
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
