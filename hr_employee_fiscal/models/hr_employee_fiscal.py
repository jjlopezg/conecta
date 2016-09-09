# -*- encoding: utf-8 -*-
###########################################################################
#
# © 2016 Juan Jose Lopez Garcia <jjlopezg74@gmail.com>.
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
###########################################################################
from openerp import models, fields, api, exceptions, _
from datetime import datetime
import logging
import subprocess
import os
from lxml import etree
from openerp import tools


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

class HrEmployeeFiscalModif(models.Model):
    _name = "hr.employee.fiscal.modif"

    code = fields.Char('Codigo', size=7, required=True)
    description = fields.Char('Descipcion', size=200, required=True)
    name = fields.Char(compute='_compute_name', size=256)

    _sql_constraints = [
        ("code_unique", "unique(code)", "Codigo duplicado"),
    ]

    @api.one
    @api.depends('name')
    def _compute_name(self):
        self.name = "%s-%s" % (self.code, self.description)


class HrEmployeeFiscalkey(models.Model):
    _name = 'hr.employee.fiscal.key'

    code = fields.Char('Codigo', size=7, required=True)
    description = fields.Char('Descipcion', size=200, required=True)
    name = fields.Char(compute='_compute_name', size=256)

    _sql_constraints = [
        ("code_unique", "unique(code)", "Codigo duplicado"),
    ]

    @api.one
    @api.depends('name')
    def _compute_name(self):
        self.name = "%s-%s" % (self.code, self.description)

class HrEmployeeFiscal(models.Model):
    _name = 'hr.employee.fiscal'
    _order = 'date_start desc'

    @api.one
    def _compute_create_user(self):
        self.user_create = "%s:%s" % (self.create_uid.login.split('@')[0],
                                      datetime.strptime(self.create_date, '%Y-%m-%d %H:%M:%S').strftime(
                                          '%d-%m-%Y-%H:%M:%S'))

    @api.one
    def _compute_last_user(self):
        self.user_last = "%s:%s" % (self.write_uid.login.split('@')[0],
                                    datetime.strptime(self.write_date, '%Y-%m-%d %H:%M:%S').strftime(
                                        '%d-%m-%Y-%H:%M:%S'))
    @api.one
    @api.onchange('wage','wage_total', 'css', 'otther', 'wage_bruto','min_per', 'min_fam')
    def _compute(self):
        self.base_liquid = self.wage_total - (self.css + self.otther)
        self.variables_var = self.wage_total - self.wage
        self.min_per_fam = (self.min_per + self.min_fam)
        try:
            self.calculado = (self.wage_total / self.java) * 100
        except:
            pass

    user_create = fields.Char(compute='_compute_create_user', string='Creado', readonly=True, size=256, store=False)
    user_last = fields.Char(compute='_compute_last_user', string='Modificado', readonly=True, size=256, store=False)
    employee_id = fields.Many2one('hr.employee', 'Empleado', required=False)

    date_start = fields.Date('Inicio', required=True, readonly=False)
    date_end = fields.Date('Termino', required=True, readonly=False)

    country_id = fields.Many2one('res.country', related='employee_id.country_id', string="Nacionalidad (País)", readonly=True, store=True)
    identification_id = fields.Char(related='employee_id.identification_id', string='Nº identificación', readonly=True, store=True)
    currency_id = fields.Many2one('res.currency', string='Currency', readonly=True, states={'draft': [('readonly', False)]},
                                  default=lambda self: self.env.user.company_id.currency_id)

    # FIZME: si cambiar las direcciones corregir
    #home_state_id = fields.Char(related='employee_id.home_state_id.name', string='Provincia', readonly=True, store=False)
    modif_id = fields.Many2one('hr.employee.fiscal.modif', 'Modificador IRPF', required=True)
    key_id = fields.Many2one('hr.employee.fiscal.key', 'Clave percepcion', required=True)
    marital = fields.Selection(related='employee_id.marital', string="Estado civil", readonly=True, store=False)
    situation = fields.Selection([
                                ('1', 'Monoparental'),
                                ('2', 'Con coyuge a cargo'),
                                ('3', 'Otras situacion'),
                                ],
                                string='Situacion familiar',
                                default='',
                                required=True,
                                readonly=False)
    minus = fields.Selection([
                            ('0', 'Sin Minusvalia'),
                            ('3', 'Igual/Superior a 33% e inferior 65%'),
                            ('A', 'Entre 33% y 65%, con asistencia'),
                            ('6', 'Igual/Superior a 65%')],
                            string='Minusvalia',
                            default='0',
                            required=False)

    geo_move = fields.Selection([
                                ('S', 'Si'),
                                ('N', 'No'),
                                ],
                                string='Movilida geofrafica',
                                default='N',
                                required=False)

    loan = fields.Selection([
                                ('S', 'Si'),
                                ('N', 'No'),
                                ],
                                string='Prestamo vivienda',
                                default='N',
                                required=False)

    regular = fields.Selection([
                                ('0', '0'),
                                ('1', '1'),
                                ],
                                string='Regularizacion',
                                default='1',
                                required=True,
                                readonly=False)

    calculado = fields.Float(compute='_compute', string="Ptje. Aplicado", default=0, readonly=True) #16 es el wage_total / devuelto por java * 100
    aplicado = fields.Float("Ptje. Calculado", default=0, readonly=True, size=5) # 31
    previo = fields.Float("Ptje. Previo", default=0, readonly=True, size=5) #11 porcentaje nomina anterior
    paysheet = fields.Float("Ptje. Nomina", default=0, readonly=True, size=5) # 31

    fam_qty = fields.Integer(related='employee_id.fam_qty', string="Familiares", store=False)
    fam_qty_des = fields.Integer(related='employee_id.fam_qty_des', string="Familiares Des.", store=False)
    fam_qty_asc = fields.Integer(related='employee_id.fam_qty_asc', string="Familiares Asc.", store=False)

    java = fields.Monetary(string='java')  # campo devulto desde java

    otther = fields.Monetary(string='Otras Reducciones')  #5 , compute='_compute_base_amount'
    pago_esp = fields.Monetary(string='Pago Especie')  #13
    irreg18_2 = fields.Monetary(string='Rend. Irreg. 18.2')  #14 Rendimiento irregular 18.2
    irreg18_3 = fields.Monetary(string='Rend. Irreg. 18.3')  # 15 Rendimiento irregular 18.3
    pension = fields.Monetary(string='Pension comp.')  # 32
    alimen = fields.Monetary(string='Alimentos')  # 33



    css = fields.Monetary(string='Cot. Seg. Social') #4 , compute='_compute_base_amount'
    base_liquid = fields.Monetary(compute='_compute', string='Base Liquidacion') #3 (wage_total - css - otther) = base_liquid


    wage = fields.Monetary(string='Salario Bruto')  # 0 - diferencia entre salario teorico wage_total - wage) prima de acc. por convenio
    wage_total = fields.Monetary(string='Retrib. Totales') #1 El total que se cobrara al año (Salario Bruto 12 meses)
    wage_bruto = fields.Monetary(string='Salario percibido')  # 10 El total que se lleva cobrado
    variables_var = fields.Monetary(compute='_compute', string='Variables var.')  # 2 ( wage_total -  wage) prima de acc. por convenio)
    wage_retn = fields.Monetary(string='Retenciones') #12 Retenciones

    min_per = fields.Monetary(string='Minimo Personal') #17 Finimo Personal
    min_fam = fields.Monetary(string='Minimo Familiar') #18 Minimo familiar
    minus_trab_act = fields.Monetary(string='Discapacidad Trab. Activo') #19 minimo trabajador activo
    minus_trab_no_act = fields.Monetary(string='Discapacidad Trab. no Activo') #20 minimo trabajador no activo
    min_per_fam = fields.Monetary(compute='_compute', string='Minimo Pers. Fam.') #21 Minimo personal familiar min_per_fam = (min_per + min_fam)

    state = fields.Selection([
                                ('N', 'Normalizado'),
                                ('R', 'Regularizar'),
                                ],
                                string='Estado',
                                default='N',
                                required=True,
                                readonly=False)


    @api.one
    def compute_irpf(self):
        log = Log()
        log.add(_("Resumen:\n"))

        def _run_java(command):
            # call = [['java','-jar','temp.jar']]
            print command
            res = subprocess.call(command, stdout=None, stderr=None)
            if res > 0:
                log.add(_("\nWarning - result was %d" % res))
            else:
                log.add(_("\nDone - result was %d" % res))
            return res

        def _compute():
            path = os.path.realpath(os.path.dirname(__file__))
            path += '/../java/'
            file_name_in = open(path + 'Ret.xml', 'w+')
            file_name_in.write(xml_irpf)
            file_name_in.close()


            call = 'java -jar ' + path + 'ModRet2016.jar /E:' + path + 'ret.xml /R:' + path + 'erroresRet.xml /S:' + path + 'salidaRet.xml'
            log.add(_(call))
            _run_java(call)
            return 'test'#

        report = self.env.ref('hr_employee_fiscal.report_compute_irpf')
        fiscal = self.env["hr.employee.fiscal"].browse([self.id])

        xml_irpf = self.env['report'].get_html(fiscal, report.report_name)

        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.fromstring(xml_irpf)#, parser)

        xml_irpf = xml_irpf.decode("utf-8").encode("iso-8859-1")
        xml_irpf = etree.tostring(tree, pretty_print=True, encoding="iso-8859-1")

        log.add(xml_irpf)

        xml_irpf = _compute()

        # FIXME; pensar quitar espacios en blanco (fichero pese menos)
        # FIXME; recoger si existe algun error y avisar y guardar
        #raise UserError(_('Calculo Realizado.'))
        raise exceptions.Warning(_(log()))
        # FIXME; abrir wizrard para dar opcion de regularizar mes o otros



