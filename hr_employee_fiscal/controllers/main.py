# -*- encoding: utf-8 -*-
###########################################################################
#
# © 2016 Juan Jose Lopez Garcia <jjlopezg74@gmail.com>.
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
###########################################################################
from openerp.addons.web import http
from openerp.addons.web.http import request, WebRequest, JsonRequest
from werkzeug import exceptions

from fdfgen import forge_fdf
from PyPDF2 import PdfFileReader, PdfFileWriter


import openerp
import subprocess
from StringIO import StringIO
import time
import base64

try:
    import json
except ImportError:
    import simplejson as json


def content_disposition(filename):
    return request.registry['ir.http'].content_disposition(filename)

class conecta_report(http.Controller):

    @http.route('/conecta/employee/<ids>', type='http', auth="user", website=False)
    def conecta(self, ids):
        print "controller ---------------------------------------------------------"
        self.cr, self.uid, self.pool = request.cr, request.uid, request.registry

        ids = eval(ids)
        def append_pdf(input, output):
            [output.addPage(input.getPage(page_num)) for page_num in range(input.numPages)]

        print ids
        if ids:
            print "HOLA"
            employees = request.env['hr.employee'].sudo().search([('id', 'in', ids)])

            combined = StringIO()
            output = PdfFileWriter()
            pdf_form = PdfTemplate()  # ? template. contract.type_id_template

            for employee in employees:
                fields = [
                    ('dato.nif.1', employee.fiscal_last_id.employee_id.identification_id), # dni empleado
                    ('dato.1', employee.name),  # nombre empleado
                    ('dato.2', time.strftime('%Y', time.strptime(employee.birthday, '%Y-%m-%d'))),  # nombre empleado
                    ('dato.3', 1 if employee.fiscal_last_id.situation == '1' else 0), # situacion
                    ('dato.4', 1 if employee.fiscal_last_id.situation == '2' else 0),  # situacion
                    ('dato.nif.2', employee.fiscal_last_id.conyuge_nif if employee.fiscal_last_id.situation == '2' else ''),  # situacion
                    ('dato.6', 1 if employee.fiscal_last_id.situation == '3' else 0), # situacion:
                    ('dato.7', 1 if employee.fiscal_last_id.minus == '3' else 0), # minusvalia: Entre 33% y 65%,
                    ('dato.7', 1 if employee.fiscal_last_id.minus == 'A' else 0), # minusvalia: Entre 33% y 65%, con asistencia
                    ('dato.9', 1 if employee.fiscal_last_id.minus == 'A' or employee.fiscal_last_id.minus == 'B' else 0), # minusvalia: Entre 33% y 65%, con asistencia
                    ('dato.8', 1 if employee.fiscal_last_id.minus == '6' else 0), # minusvalia Igual/Superior a 65%
                    ('dato.8', 1 if employee.fiscal_last_id.minus == 'B' else 0), # minusvalia: Igual/Superior a 65%, con asistencia
                    #('dato.9', 1 if employee.fiscal_last_id.minus == 'B' else 0), # minusvalia: Igual/Superior a 65%, con asistencia

                    ('dato.10', time.strftime('%d/%m/%Y', time.strptime(employee.fiscal_last_id.geo_date, '%Y-%m-%d')) if employee.fiscal_last_id.geo_move == 'S' else ''),  # fecha movilidad
                    ('dato.11', 0),  # rendimientos periodo superior 2 años
                    ('dato.53', 1 if employee.fiscal_last_id.loan == 'S' else 0),  # vivienda
                    ('dato.54', employee.home_city),  # employee city
                    ('dato.55', time.strftime('%d', time.strptime(employee.fiscal_last_id.date_from, '%Y-%m-%d'))),  # fecha movilidad
                    ('dato.56', time.strftime('%B', time.strptime(employee.fiscal_last_id.date_from, '%Y-%m-%d'))),  # fecha movilidad
                    ('dato.57', time.strftime('%Y', time.strptime(employee.fiscal_last_id.date_from, '%Y-%m-%d'))),  # fecha movilidad
                    ('dato.58', employee.name),  # Empleado
                    ('dato.59', employee.company_id.name),  # company
                    ('dato.60', employee.company_id.city),  # company city
                    ('dato.61', time.strftime('%d', time.strptime(employee.fiscal_last_id.date_from, '%Y-%m-%d'))),  # fecha movilidad
                    ('dato.62', time.strftime('%B', time.strptime(employee.fiscal_last_id.date_from, '%Y-%m-%d'))),  # fecha movilidad
                    ('dato.63', time.strftime('%Y', time.strptime(employee.fiscal_last_id.date_from, '%Y-%m-%d'))),  # fecha movilidad

                    ('dato.64', employee.company_id.manager_id.name),  # Manager
                 ]
                i = 0
                for fam in employee.fiscal_last_id.fam_ids:
                    if fam.type in ['2', '6']:
                        fields.append(('dato.'+str(12+i), time.strftime('%Y', time.strptime(fam.birthday, '%Y-%m-%d')) if fam.birthday!=False else ''))
                        fields.append(('dato.'+str(13+i), time.strftime('%Y', time.strptime(fam.date_adoption, '%Y-%m-%d')) if fam.date_adoption!=False else ''))
                        fields.append(('dato.'+str(14+i), 1 if fam.minus == '3' else 0)) # minusvalia:  Entre 33% y 65%,
                        fields.append(('dato.'+str(14+i), 1 if fam.minus == 'A' else 0))  # minusvalia: Entre 33% y 65%, con asistencia
                        fields.append(('dato.'+str(16+i), 1 if fam.minus == 'A' or fam.minus == 'B' else 0))  # minusvalia: Entre 33% y 65%, con asistencia
                        fields.append(('dato.'+str(15+i), 1 if fam.minus == '6' else 0)) # minusvalia:Igual/Superior a 33% e inferior 65%
                        fields.append(('dato.'+str(15+i), 1 if fam.minus == 'B' else 0)) # minusvalia: Igual/Superior a 65%, con asistencia
                        fields.append(('dato.'+str(17+i), 1 if fam.factor == '3' else 0)) # computo: totalidad del minimo
                        i += 6

                i = 0
                for fam in employee.fiscal_last_id.fam_ids:
                    if fam.type in ['11']:
                        fields.append(('dato.'+str(40+i), time.strftime('%Y', time.strptime(fam.birthday, '%Y-%m-%d')) if fam.birthday!=False else ''))
                        fields.append(('dato.'+str(41+i), 1 if fam.minus == '3' else 0)) # minusvalia:  Entre 33% y 65%,
                        fields.append(('dato.'+str(41+i), 1 if fam.minus == 'A' else 0))  # minusvalia: Entre 33% y 65%, con asistencia
                        fields.append(('dato.'+str(42+i), 1 if fam.minus == 'A' or fam.minus == 'B' else 0))  # minusvalia: Entre 33% y 65%, con asistencia
                        fields.append(('dato.'+str(43+i), 1 if fam.minus == '6' else 0)) # minusvalia:Igual/Superior a 33% e inferior 65%
                        fields.append(('dato.'+str(43+i), 1 if fam.minus == 'B' else 0)) # minusvalia: Igual/Superior a 65%, con asistencia
                        fields.append(('dato.'+str(44+i), fam.conviven if fam.conviven != '0' else 0)) # computo: totalidad del minimo
                        i += 6

                result = pdf_form.render(fields, "G:\odoo\V9\conecta\hr_employee_fiscal\pdfs\Mod145.pdf")
                append_pdf(PdfFileReader(StringIO(result)), output)

            output.write(combined)

            pdfhttpheaders = [
                ('Content-Type', 'application/pdf'),
                ('Content-Length', len(combined.getvalue())),
                ('Content-Disposition', content_disposition('Mod145'+'.pdf')),
            ]

            return request.make_response(combined.getvalue(), headers=pdfhttpheaders)
        else:
            raise exceptions.HTTPException(description='NOT implemented.')


    """
    # TODO: esto estaria bien que fuera generico, reciba un json para montar el report, mirar el otro fichero
    #@http.route('/conecta/report/', type='json', auth='user', website=False)
    @http.route('/conecta/employee/<ids>', type='http', auth="user", website=False)
    def conecta(self, ids):
        print "CONTROLLER ##########################################################"
        self.cr, self.uid, self.pool = request.cr, request.uid, request.registry

        def append_pdf(input, output):
            [output.addPage(input.getPage(page_num)) for page_num in range(input.numPages)]

        if isinstance(ids, unicode):
            ids = eval(ids)  # (int(i) for i in ids.split(','))
            contracts = request.env['hr.employee'].sudo().search([('id', 'in', ids)])

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
    """


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