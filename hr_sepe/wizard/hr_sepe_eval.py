# -*- encoding: utf-8 -*-
###########################################################################
#
# © 2016 Juan Jose Lopez Garcia <jjlopezg74@gmail.com>.
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
###########################################################################

from openerp import models, fields, api, exceptions, _
from StringIO import StringIO
from lxml import etree
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

class HrSepeEval(models.TransientModel):
    _name = "hr.sepe.eval"

    file = fields.Binary(string='Fichero', default=False, required=False, readonly=False)
    filename = fields.Char(string='Fichero', size=64, default=False)
    note = fields.Text('Log')

    real = fields.Boolean('Aplicar cambios')

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
        log = Log()
        log.add(_("Resumen:\n"))
        #namespaces = {'ns': 'http://www.sepe.es/CONTRATA'}  # add more as needed

        if not (self.file and self.filename):
            raise exceptions.UserError(_("Falta fichero"))
        else:
            tmp = self.filename.split('.')
            ext = tmp[len(tmp) - 1]
            if ext != 'xml':
                raise exceptions.ValidationError(_("El fichero no es un XML"))

        try:
            root = etree.parse(StringIO(base64.decodestring(self.file)))
        except Exception, e:
            raise exceptions.ValidationError(_("Error de Fichero: %s\n" % (e)))
        else:
            if self.type == 'FICHERO_CONTRATOS':
                self.eval_contrat(root, log)
            elif self.type == 'FICHERO_PRORROGAS':
                raise exceptions.ValidationError(_("No Implementado"))
            elif self.type == 'transfor':
                raise exceptions.ValidationError(_("No Implementado"))
            elif self.type == 'ring':
                raise exceptions.ValidationError(_("No Implementado"))
            elif self.type == 'basic':
                raise exceptions.ValidationError(_("No Implementado"))
            else:
                pass


        self.write({
            'note': log(),
            'state': 'done'
        })

        return self.do_reload()

    @api.model
    def eval_contrat(self, root, log):
        ns = 'http://www.sepe.es/CONTRATA'
        """
        ###############################################################################################
        # FIXME: hay que buscar el primerio y comparar si es del mismo tipo
        if root.tag != '{%s}%s' % (ns, self.type):
            raise exceptions.ValidationError(_("El fichero no es una respuesta del tipo: %s"%self.type))
        else:
            nodes = root.find('{%s}%s' % (ns, 'CONTRATOSPROCESADOS'))
            for a in nodes.getchildren():

            if node.tag == ('{%s}CONTRATOSPROCESADOS' % ns):
        ###############################################################################################
        """

        for node in root.findall('.//{%s}USOLIBRE_EMPRESA'%ns):
            if isinstance(node.text, basestring):
                try:
                    sid, contract_id, date_start = node.text.split(";")
                    sepe = self.env['hr.sepe'].browse(int(sid))
                except:
                    raise exceptions.ValidationError(_("Error al desempaquetar"))

                if not sepe:
                    log.add("Identificador de la comunicacion no encontrado\n")
                elif sepe.state != 'send' and self.real:
                    log.add("Imposible actualizar estado: Contrato: %s, Empleado: %s\n"%(sepe.contract_id.name, sepe.employee_id.name))
                else:
                    parent = node.getparent().getparent().getparent()
                    values = {
                        'id' : int(sid),
                        'state' : parent[1].find('{%s}RESULTADO'%ns).text,
                        'name' : parent[1].find('{%s}IDCONTRATO'%ns).text,
                        'date_send' : parent[1].find('{%s}FECHACOMUNICACION'%ns).text,
                        'user_auth' : parent[1].find('{%s}USUARIO'%ns).text,
                        'date_init' : parent[1].find('{%s}FECHAALTA'%ns).text,
                        'basic_copy' : parent[1].find('{%s}OBLIGCB'%ns).text,
                        'leybonif' : parent[1].find('{%s}LEYBONIF'%ns).text,
                        'leyfomento' : parent[1].find('{%s}LEYFOMENTO'%ns).text,
                        'leyreduccion' : parent[1].find('{%s}LEYREDUCCION'%ns).text,
                        'leydeduccion': parent[1].find('{%s}LEYDEDUCCION'% ns).text,
                        'terror_ids' : [],
                    }

                    log.add("%s - %s\n" % (values['name'], values['state']))
                    for error in parent[1].find('{%s}ERRORES'%ns).getchildren():
                        terror = self.env['hr.sepe.terrores'].search_read([('code', '=', error.text)], ['id'])
                        if terror:
                            values['terror_ids'] += [(4, terror[0]['id'])]
                        else:
                            log.add(_("Un codigo de repuesta no existe, por favor actualizar"))

                    if self.real:
                        sepe.write(values)


    @api.multi
    def do_back(self):
        self.write({
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

    """
    @api.one
    @api.constrains('filename')
    def _check_filename(self):
        if self.file:
            if not self.filename:
    	        raise exceptions.ValidationError(_("no file"))
    	else:
            if self.filename:
    	        tmp = self.filename.split('.')
    	        ext = tmp[len(tmp)-1]
    	        if ext != 'xml':
        	        raise exceptions.ValidationError(_("Txml file"))
    """