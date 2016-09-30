# -*- encoding: utf-8 -*-
###########################################################################
#
# © 2016 Juan Jose Lopez Garcia <jjlopezg74@gmail.com>.
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
###########################################################################

from openerp import models, fields, api, _
from StringIO import StringIO
#from PyPDF2 import PdfFileMerger, PdfFileReader

from datetime import date, datetime
import logging
import base64

try:
    from pdfjinja import PdfJinja
except Exception, e:
    print "Error en pdfjinja-> ", e


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

class HrContractTypePrint(models.TransientModel):
    _name = "hr.contract.type.print"

    company_ids = fields.Many2many('res.company', 'type_print_company_rel', 'print_id', 'company_id', string='Compañia', required=True)
    file = fields.Binary("file", readonly=True)
    file_name = fields.Char('file name', size=64)
    note = fields.Text('Log', default='Resumen\n')
    contract_ids = fields.Many2many(comodel_name='hr.contract',
                                      relation='hr_contract_printing_rel',
                                      columm1='printing_id',
                                      columm2='contract_id',
                                      string='Contratos',
                                      required=False)

    type = fields.Selection([
                            ('FICHERO_CONTRATOS', 'Contrato'),
                            ('FICHERO_PRORROGAS', 'Prorroga'),
                            ('transfor', 'Transformacion'),
                            ('ring', 'Llamamiento'),
                            ('basic', 'Copia Basica')
                            ],
                            string='Tipo',
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
        if self.contract_ids:
            self.process()
        return self.do_reload()

    @api.multi
    def get_anexo(self, o):
        self.note = self.note + o.name+"\n"
#        return 'hr_contract_type.template_contracts_tp_page1'
#<t t-call="#{ o.get_anexo(contract) }"/>



    @api.one
    def process(self):
        log = Log()
        log.add(_("Resumen:\n"))
        print "IMPRESION DE ", self.type


        report = self.env.ref('hr_contract_type.report_contracts')

        docs_ids = self.env["hr.contract.type.print"].browse(self._ids)

        result = StringIO()
        #merger = PdfFileMerger()
        #result = []

        for docs_id in docs_ids:
            print "creando contrato->", docs_id

        result.write(self.env['report'].get_pdf(docs_id, report.report_name))
        #print len(result)
        #for filename in result:
            #merger.append(PdfFileReader(StringIO(filename), 'rb'))

        #merger.write(combined)
        """
        combined = StringIO()
        merger = PdfFileMerger()
        for filename in filenames:
            merger.append(PdfFileReader(StringIO(result), 'rb')))

        merger.write(combined)
        #def append_pdf(input, output):
        #    [output.addPage(input.getPage(page_num)) for page_num in range(input.numPages)]

        output = PdfFileWriter()
        for id, result in self.files:
            append_pdf(PdfFileReader(StringIO(result)), output)


        output.write(combined)

        self.write({
            'state': 'get',
            'name': ('%s.%s' % (time.strftime("%Y%m%d%H%M%S"), 'pdf')),
            'data': base64.encodestring(combined.getvalue()),
        })
        """
        # ---------------------------------
        file = base64.b64encode(result.getvalue())
        file_name = (_(self.type + '_' + datetime.today().strftime('%Y%m%d_%H%M%S') + '.pdf'))

        self.env['ir.attachment'].create({
            'name': file_name,
            'datas': file,
            'datas_fname': file_name,
            'res_model': 'hr.contract',
            'res_id': 0,
        })

        self.write({
            #'note': log(),
            'file': file,
            'file_name': file_name,
            'state': 'done'
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


