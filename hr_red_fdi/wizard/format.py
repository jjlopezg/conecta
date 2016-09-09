# -*- encoding: utf-8 -*-
#-*- coding:utf-8 -*-
###########################################################################
#
# © 2016 Juan Jose Lopez Garcia <jjlopezg74@gmail.com>.
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
###########################################################################
from base_line import BaseLine

        #ETI
        #EMP
        #RZS
        #EXC
        #FCE
        #PES
        # for id in ids
            #TRA
            #AYN
            #DOM
            #LDD
            #FAB
            #DAM
            #OTD
            #DSC
            #DRA
            #FCT
            #PIT
        #end for
        #ETF

# Cabecera del fichero (Line_1)

class ETI(BaseLine):
    fields = (
                ('cab', 3, 'ETI'),            #1#3# Cabecera de segmento
                ('idmen', 3, 'AFI6'), 	    #4#4# Identificador de sintaxis de mensaje
                ('ver', 1, '1'),	        #8#1# Versión de sintaxis de mensaje
                ('sintax', 3, 'WS74'), 	    #9#4# Identificador de sintaxis de proceso
                ('idsintax', 1, '0'),	        #13#1# Variable en función de la versión de WinSuite32.
                ('password', 8, ' '),            #14#8# Clave de Autorización
                ('supplier', 3, ' '),	        #22#3# Proveedor de nómina
                ('resva', 5, ' '),	            #25#5# Reservado
                ('date', 8, '*'),	            #30#8# Fecha de preparación
                ('time', 4, '*'),	            #38#4# Hora de preparación
                ('filename', 8, '*'),            #42#8# Referencia de control de intercambio / Nombre fichero
                ('file_ext', 3, '*'),         	#50#3# Sufijo / Extension
                ('priority', 1, 'N'),      	#53#1# Código de prioridad de procesado
                ('test', 1, 'P'),	            #54#1# Indicador de prueba
                                                    # (un spacio) Envío en real
                                                    # P Pruebas
                                                    # N No sustitución
                ('year', 2, '0'),                 #55#2# Número de identificación de Registro / año
                ('month', 2, '0'),                #57#2# Número de identificación de Registro / mes
                ('serial', 1, '0'),               #59#1# Número de identificación de Registro / serie
                ('send', 5, '0'),                 #60#5# Número de identificación de Registro / envio
                ('doc', 4, '0'),                  #65#4# Número de identificación de Registro / documento
                ('tgss', 1, ' '),	             #69#1# Reservado TGSS / Asignado por el programa de la TGSS
                ('resvb', 1, ' '),	             #70#1# Reservado
    )

"""
    EMP
    3#1# Cabecera de segmento
    4#4# Código de Cuenta de Cotización / regimen
    2#8# Código de Cuenta de Cotización / provincia
    9#10# Código de Cuenta de Cotización / numero ccc sin provincia
    1#19# Tipo de identificación
    3#20# País 724
    14#23# Número de identificación de empresario / Ajuste a derecha, relleno a ceros por empresario izquierda
    2#37# Calificador de código de empresario
    4#39# Código de Cuenta de Cotización / regimen2
    2#43# Código de Cuenta de Cotización / provincia2
    9#45# Código de Cuenta de Cotización / numero ccc sin provincia
    13#54# Reservado Recaudación
    3#67# Acción
    1#69# Reservado
"""
class EMP(BaseLine):
    fields = (
                ('cab',	3,'EMP'),       #1# Cabecera de segmento
                ('rega', 4, '*'),       #4# Código de Cuenta de Cotización / regimen
                ('prova', 2, '*'),      #8# Código de Cuenta de Cotización / provincia
                ('ccca', 9, '*'),        #10# Código de Cuenta de Cotización / numero ccc sin provincia
                ('ident', 1, '*'),       #19# Tipo de identificación
                ('country', 3, '*'),     #20# País 724
                ('vat', 14, '0'),         #23# Número de identificación de empresario / Ajuste a derecha, relleno a ceros por empresario izquierda
                ('code_emp', 2, '*'),    #37# Calificador de código de empresario
                ('regb', 4, '*'),	    #39# Código de Cuenta de Cotización / regimen2
                ('provb', 2, '*'),     #43# Código de Cuenta de Cotización / provincia2
                ('cccb', 9, '*'),	    #45# Código de Cuenta de Cotización / numero ccc sin provincia2
                ('resva', 13, '*'),	    #54# Reservado Recaudación
                ('action', 3, '*'),      #67# Acción
                ('resvb', 1, '*'),	    #69# Reservado
    )

class ZRS(BaseLine):
    fields = (
                ('cab', 'ZRS'),     #1# Cabecera de segmento
                ('razon', 1),       #4# Indicador de Razón social
                ('type', 1),        #5# Tipo alfabético de empresario
                ('partner', 55),    #6# Razón social
                ('password', 8),    #61# Clave de Autorización
                ('resv', 2),	    #69# Reservado
    )

# Trabajador
# for id in ids: (Line_xx)
class TRA(BaseLine):
    fields = (
                ('cab', 3, 'TRA'),     #1# Cabecera de segmento
                ('cccp', 2, '*'),	    #4# Número de afiliación a la Seguridad Social (N.A.F.) / provincia
                ('ccc', 10, '*'),   	    #6# Número de afiliación a la Seguridad Social (N.A.F.) /  numero
                ('type',1, '*'),         #16# Identificador de Persona Física (IPF) / Tipo de Identificador
                ('country', 3, '*'),     #17# Identificador de Persona Física (IPF) / Pais
		        ('alfa', 14, '*'),       #20# Identificador de Persona Física (IPF) / Alfaclave
                ('resva', 3, '*'),  	    #34# Reservado respuesta afiliación
                ('control', 25, '*'), 	#37# Decodificación Código rotura de control
                ('country', 3, '*'),     #62# Nacionalidad
                ('resvb', 1, '*'),     	#65# Indicadores del trabajador / Futuro uso
                ('resvc', 5, '*'),       #66# Reservado
    )

# Apellidos y Nombre    	}
class AYN(BaseLine):
    fields = (
                ('cab', 3,'AYN'),     #1# Cabecera de segmento
                ('firstname', 20, '*'),  #4# Primer apellido
                ('lastname', 20, '*'),	#24# Segundo Apellido
                ('name', 15, '*'),	    #44# Nombre
                ('resv', 12, '*'),       #59# Reservado
    )

# Fechas de Alta Baja
class FAB(BaseLine):
    fields = (
                ('cab', 3, 'FAB'),  #1# Cabecera de segmento
                ('action',3),     	#4# Accion
                ('state',2),	    #7# situacion
                ('date',8),	        #9# Fecha real
                ('grp',2),	        #17# Grupo de cotización
                ('resva',3),        #19# Reservado respuesta afiliación
                ('contract',3),     #22# Clave de contrato de trabajo
                ('condicion',1),	#25# Condición de desempleado
                ('femalesub',1),    #26# Mujer subrepresentada / S= Sí; N=No
                ('coef',3),     	#27# Coeficiente tiempo parcial
                ('colec',3),     	#30# Colectivo de trabajador
                ('print',1),	    #33# Indicador impresión
                ('catg',7),	        #34# Categoría profesional / Obligatorio para Régimen 0911. Opcional para Régimen Especial de Trabajadores del Mar. No admisible par resto de regímenes.
                ('birth',8),	    #41# Fecha de nacimiento
                ('sex',1),	        #49# Sexo / 1 = hombre; 2 = mujer
                ('type',1),	        #50# Tipo de Inactividad
                ('exclu',1),     	#51# Exclusión de desempleo
                ('strike',3),     	#52# Coeficiente de actividad huelga parcia
                ('femalerei',1),    #55# Mujer reincorporada
                ('disabled',1),     #56# Incapacitado readmitido
                ('auto',1),	        #57# Trabajador de autónomo
                ('week',1),     	#58# 5JR/semana según convenio
                ('count',1),     	#56# Indicativo nº trabajadores empresa
                ('control',8),     	#60# Fecha de control
                ('social',1),     	#68# Exclusión social/Víctimas
                ('inser',1),     	#69# Renta activa de inserción
                ('alumb',1),     	#70# Trabajadoras contratadas en los 24 meses siguientes a la fecha de alumbramiento
    )
# Datos Asociados al Movimiento
class DIT(BaseLine):
    fields = (
                 ('cab', 'DAM'),    # Cabecera de segmento
                 ('date', ''),	    # Fecha de inicio de contrato
                 ('fic', ''),	    # FIC específico
                 ('relation', ''),	# Relación laboral de carácter especial
                 ('nuss', ''),	    # NUSS del trabajador sustituido
                 ('causa', ''),	    # Causa sustitución
                 ('par_1', ''),	    # Permanencias / Parte entera del coeficiente
                 ('par_2', ''),	    # Permanencias / Parte decimal del coeficiente
                 ('par_3', ''),	    # Permanencias / Días de trabajo
                 ('par_4', ''),	    # Permanencias / Días a los que no se aplica el coeficiente
                 ('coe_red', ''),   # Coeficiente reductor de la edad de jubilación
                 ('relevo',	''),    # Relevo
                 ('days', ''),	    # Días trabajados
                 ('rev_1',	''),    # Reservado
                 ('change',	''),    # Cambio puesto de trabajo
                 ('perdida', ''),   # Indicativo pérdida de beneficios
                 ('vinculo', ''),   # Vínculo familiar
                 ('prg_fea', ''),   # Programa Fomento Empleo Agrario
                 ('Modalidad',''),  # Modalidad de cotización
                 ('garantia', ''),	# Beneficiario Sistema Nacional de Garantía Juvenil
                 ('ocupacion',''),	# Ocupación
                 ('excedente',''),	# Excedente sector industrial
                 ('reduce',	''),	# Reducción de jornada
                 ('coef_tp', ''),	# Coeficiente de tiempo parcial inicial
    )

# Datos de Incapacidad Temporal(FDI)
class DIT(BaseLine):
    fields = (
                ('cab', 'DIT'),	    #1# Cabecera de segmento
                ('action', ''),	    #4# Acción
                ('causa', ''),	    #7# Causa del alta
                ('contg', ''),	    #9# Contingencia / Obligatorio para acción PA, PB
                ('start', ''),	    #10# Fecha baja / Obligatorio para acción PA, PB y PC
	            ('end', ''),	    #18# Fecha alta / Obligatorio para acción PA
                ('atep', ''),	    #26# Fecha de AT y EP / Obligatorio para contingencias 3, 4 y 5
                ('prova', ''),	    #34# Número de colegiado / Provincia
                ('provb', ''),	    #36# Número de colegiado / Provincia
                ('coleg', ''),	    #38# Número de colegiado / Numero
                ('area', ''),	    #44# Código de Identificación de Área Sanitaria
                ('days', ''),	    #55# Duración probable de la baja / Dias
                ('month', ''),	    #58# Duración probable de la baja / Meses
                ('cagt', ''),	    #60# Categoría profesional / Sólo para régimen 0911
                ('reca', ''),	    #67# Recaida / S=Sí; N=No
                ('resva', ''),	    #68# Reservado
    )

# Otros Datos del Parte(FDI)
class OPD(BaseLine):
    fields = (
                ('cab', 'OPD'),	    #1# Cabecera de segmento
                ('date', 8),	    #4# Fecha del parte de confirmación
                ('pc', 2),		    #12# Número del parte de confirmación
                ('mutua', 3),	    #14# Entidad aseguradora de IT
                ('change', 8),	    #17# Fecha de cambio de entidad aseguradora de IT
                ('resv', 0),	    #25# Reservado
    )

# Datos Económicos(FDI)
class DEC(BaseLine):
    fields = (
                ('cab', 'DEC'),	    #1# Cabecera de segmento
                ('basea', ''),	    #4# Base de cotización / Parte entera
                ('baseb', ''),	    #10# Base de cotización / Parte decimal
                ('suma', ''),	    #12# Suma bases de cotización / Parte entera
                ('sumb', ''),	    #18# Suma bases de cotización / Parte decimal
                ('extraa', ''),	    #20# Cotización año anterior por horas extras / Parte entera
                ('extrab', ''),	    #26# Cotización año anterior por horas extras / Parte decimal
                ('yeara', ''),	    #28# Cotización año anterior por otros conceptos / Parte entera
                ('yearb', ''),	    #34# Cotización año anterior por otros conceptos / Parte decimal
                ('care', ''),	    #37# Carencia / Sólo para fichero FRI
                ('days', ''),	    #37# Días cotizados mes/Obligatorio para acción PB en todos los contratos excepto los de tiempo parcial y fijos discontinuos.
                ('sumdays', ''),    #39# Suma días cotizados/Obligatorio para acción PB en contratos de tiempo parcial y fijos discontinuos.
                ('resv', ''),	    #42# Reservado
    )

# Domicilio del trabajador
class DOM(BaseLine):
    fields = (
                 ('cab', 'DOM'),	#1# Cabecera de segmento
                 ('type', 1),		#4# Tipo de domicilio
                 ('via', ''),		#5# Domicilio postal/Tipo vía
                 ('name', ''),		#7# Domicilio postal/Nombre vía
                 ('number', ''),	#43# Domicilio postal/Numero
                 ('bis', ''),		#48# Domicilio postal/bis
                 ('blq', ''),		#50# Domicilio postal/bloque
                 ('esc', ''),		#52# Domicilio postal/escalera
                 ('pis', ''),		#54# Domicilio postal/piso
                 ('door', ''),	#56# Domicilio postal/puerta
                 ('sms', ''),		#59# Mensajes SMS/Sólo acción MA y MB.Para acción PB número de teléfono.
                 ('resv', ''),	#68# Reservado
    )

# Localidad del Domicilio Decodificado
class LDD(BaseLine):
    fields = (
                ('cab', 'LDD'),	#1# Cabecera de segmento
                ('zip', 4),		#4# Código Postal
                ('loca', 12),	#12# Localidad
                ('prov', 14),	#14# Provincia
                ('phone', 17),	#17# Telefono
                ('resv', 25),	#25# Reservado
    )
# end for
# Etiquetas de proceso
class ETF(BaseLine):
    fields = (
                ('cab', 3, 'ETF'),	    # Cabecera de segmento
                ('id', 4, 'AFI6'), # Identificador de sintaxis de mensaje
                ('ver', 1, '3'),   # Versión de sintaxis de mensaje
                ('sintax', 4, 'WS74'),# Identificador de sintaxis de proceso
                ('idsintax', 1, '0'),    # Identificador de sintaxis de proceso
                ('password', 8, '*'),	# Clave de Autorización
                ('resva', 8, '*'),     	# Reservado
                ('date', 8, '*'),     	# Fecha de preparación
                ('time', 4, '*'),	    # Hora de preparación
                ('control', 1, '*'),     # Referencia de control de intercambio
                ('Subfijo', 3, 'AFI'), # Sufijo
                ('priority', 1, 'N'),	# Código de prioridad de procesado
                ('test', 1, '1'),	    # Indicador de prueba
                ('counta', 1, '0'),	    # Contador de segmentos EMP
                ('countb', 1, '0'),     # Contador de segmentos totales, incluidas ETI y ETF
                ('resvb', 3, '*'),     	# Reservado
    )
