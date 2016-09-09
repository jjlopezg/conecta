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


class HrRedFdiEval(models.TransientModel):
    _name = "hr.red.fdi.eval"

    #company_id = fields.Many2one('res.company', 'Compañia', default=lambda self: self.env.user.company_id, required=False)
    #workcenter_id = fields.Many2one('hr.workcenter', 'Centro de trabajo', required=True)

    file = fields.Binary(string="Fichero", default=False, required=False, readonly=False)
    filename = fields.Char(string='Fichero', size=64, default=False)
    note = fields.Text('Log')
    real = fields.Boolean('Aplicar cambios')

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
        log = Log()
        log.add(_("Resumen:\n"))

        if not (self.file and self.filename):
            raise exceptions.UserError(_("Falta fichero"))
        else:
            tmp = self.filename.split('.')
            ext = tmp[len(tmp) - 1]
            print "EXT->", ext
            if ext != 'TXT':
                raise exceptions.ValidationError(_("El fichero no es *.TXT"))

        try:
            stream = StringIO.StringIO(base64.decodestring(self.file))
        except Exception, e:
            raise exceptions.ValidationError(_("Error de Fichero: %s\n" % (e)))
        else:
            self.eval_afi(stream, log)

        return self.do_reload()

    @api.model
    def eval_fdi(self, stream, log):

        print stream.getvalue()
        lines = stream.readlines()
        print "----------------------------------------------------"
        print len(lines)

        #if cab == 'ETI':
         #   print "llamada a ETI"
        #elif cab == 'CAB':
         #   print "llamada a CAB"
        print lines[0]
        print lines[1]
        del lines[0]
        del lines[0]

        print lines
        i = 0
        print "----------------------------------------------------"
        while (lines[0][:3] != "ETF"):
            cab = lines[0][:3]
            print "CAB->", cab
            if cab == 'EMP':
                print "----------------------------------------------------"
                self.eval_emp(lines, log)
                print "----------------------------------------------------"
            del lines[0]

        print "----------------------------------------------------"
        print lines
        print len(lines)

        #print "llamada a ETF"



        print log()
        self.write({
            'note': log(),
            #'file':  file,
            #'filename': filename,
            'state': 'done'
        })

    @api.model
    def eval_emp(self, lines, log):
        print "EVAL EMP"

        while (lines[0][:3] != "EMP"):
            cab = lines[0][:3]
            print "CAB->", lines[0][:3]
            if cab == 'EMP':
                print "llamada a EMP"
                lines[0]
            elif cab == 'RZS':
                print "llamada a RZS"
                lines[0]
            elif cab == 'TRA':
                print "llamada a TRA"
                lines[0]
            elif cab == 'AYN':
                print "llamada a AYN"
                lines[0]
            elif cab == 'FAB':
                print "llamada a FAB"
                lines[0]
            elif cab == 'COD':
                print "llamada a COD"
                log.add(lines[0])
                lines[0]
            else:
                return



    @api.multi
    def do_back(self):
        self.write({
#            'file': False,
#            'filename': False,
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

