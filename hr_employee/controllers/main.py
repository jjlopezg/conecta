# -*- encoding: utf-8 -*-
###########################################################################
#
# © 2016 Juan Jose Lopez Garcia <jjlopezg74@gmail.com>.
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
###########################################################################
from openerp.addons.web import http
from openerp.addons.web.http import request
from werkzeug import exceptions

from fdfgen import forge_fdf
from PyPDF2 import PdfFileReader, PdfFileWriter


import openerp
import subprocess
from StringIO import StringIO
import base64

try:
    import json
except ImportError:
    import simplejson as json


def content_disposition(filename):
    return request.registry['ir.http'].content_disposition(filename)

class report_contract(http.Controller):
    # TODO: esto estaria bien que fuera generico, reciba un json para montar el report, mirar el otro fichero
    #@http.route('/conecta/report/', type='json', auth='user', website=False)
    @http.route('/conecta/report/<ids>', type='http', auth="user", website=False)
    def conecta(self, ids):
        print "CONTROLLER ##########################################################"
        self.cr, self.uid, self.pool = request.cr, request.uid, request.registry

        def append_pdf(input, output):
            [output.addPage(input.getPage(page_num)) for page_num in range(input.numPages)]

        if isinstance(ids, unicode):
            ids = eval(ids)  # (int(i) for i in ids.split(','))
            contracts = request.env['hr.contract'].sudo().search([('id', 'in', ids)])

            combined = StringIO()
            output = PdfFileWriter()
            pdf_form = PdfTemplate()  # ? template. contract.type_id_template

            for contract in contracts:
                fields = [
                    ('ID_EMPR', contract.company_id.vat),
                    ('Texto4', contract.company_id.manager_id.name),
                    ('Texto5', contract.company_id.manager_id.identification_id),
                    ('Texto6', 'APODERADO'),
                    ('Texto7', contract.company_id.name),
                    ('Texto8', contract.company_id.street),
                    ('Texto9', u'ESPAÑA'),
                    ('Texto10', '724'),

                    ('NOM_TRA', contract.employee_id.name_id.firstname),
                    ('APE1_TRA', contract.employee_id.name_id.lastname),
                    ('APE2_TRA', contract.employee_id.name_id.lastname2),
                ]

                result = pdf_form.render(fields, contract.type_id.template)
                append_pdf(PdfFileReader(StringIO(result)), output)
                for clause in contract.clause_ids:
                    append_pdf(PdfFileReader(StringIO(base64.b64decode(clause.file))), output)

            output.write(combined)

            pdfhttpheaders = [
                ('Content-Type', 'application/pdf'),
                ('Content-Length', len(combined.getvalue())),
                ('Content-Disposition', content_disposition('Contratos'+'.pdf')),
            ]
            return request.make_response(combined.getvalue(), headers=pdfhttpheaders)
        else:
            raise exceptions.HTTPException(description='NOT implemented.')



class PdfTemplate(object):
    pdftk_bin = None

    def __init__(self):
        self.set_pdftk_bin()

    def render(self, context=None, file=None):
        if context is None:
            context = {}
            print file

        context = context#.items()
        output, err = self.fill_form(context, file)
        if err:
            raise Warning(err)
        return output

    def fill_form(self, fields, src):
        fdf_stream = forge_fdf(fdf_data_strings=fields)

        cmd = [self.pdftk_bin, src, 'fill_form', '-', 'output', '-', 'flatten']
        cmd = ' '.join(cmd)

        return self.run_cmd(cmd, fdf_stream)

    def dump_data_fields(self, file=None):
        cmd = [self.pdftk_bin, file, 'dump_data_fields']
        cmd = ' '.join(cmd)

        output, err = self.run_cmd(cmd, None)
        if err:
            raise Warning(err)
        return output

    def run_cmd(self, cmd, input_data):
        try:
            process = subprocess.Popen(cmd, stdin=subprocess.PIPE,
                                       stdout=subprocess.PIPE, shell=True)
            if input_data:
                return process.communicate(input=input_data)
            else:
                return process.communicate()
        except OSError, e:
            return None, e

    def set_pdftk_bin(self):
        if self.pdftk_bin is None:
            config = openerp.tools.config

            if not config['pdftk']:
                msg = "PDF generation requires pdftk " \
                      "(http://www.pdflabs.com/tools/pdftk-the-pdf-toolkit). " \
                      "Edit your PDFTK_BIN settings accordingly."
                raise Warning(msg)
            self.pdftk_bin = config['pdftk']

    def version(self):
        cmd = [self.pdftk_bin, '--version']
        cmd = ' '.join(cmd)

        output, err = self.run_cmd(cmd, None)
        if err:
            raise Warning(err)
        return output