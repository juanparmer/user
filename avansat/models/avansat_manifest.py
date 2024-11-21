# -*- coding: utf-8 -*-

from odoo import api, fields, models


class AvansatManifest(models.Model):
    _name = "avansat.manifest"
    _description = "Listado de manifiestos"

    def _default_currency_id(self):
        return self.env.company.currency_id

    currency_id = fields.Many2one("res.currency", default=_default_currency_id)
    name = fields.Char(related="manifiesto", copy=False, readonly=True, string="Nombre")
    avansat_id = fields.Many2one("avansat.avansat")

    manifiesto = fields.Char("Manifiesto")
    no_radicado = fields.Integer("No. Radicado")
    fecha_creacion = fields.Date("Fecha Creación")
    creado_por = fields.Char("Creado por")
    agencia_despacho = fields.Char("Agencia Despacho")
    agencia_pago = fields.Char("Agencia Pago")
    origen = fields.Char("Origen")
    ciudad_intermedia = fields.Char("Ciudad Intermedia")
    destino = fields.Char("Destino")
    placa = fields.Char("Placa")
    tipo_manifiesto = fields.Char("Tipo Manifiesto")
    tipo_vinculacion = fields.Char("Tipo Vinculación")
    cliente = fields.Char("Cliente")
    tenedor = fields.Char("Tenedor")
    documento_tenedor = fields.Integer("Documento Tenedor")
    conductor = fields.Char("Conductor")
    documento = fields.Integer("Documento")
    licencia = fields.Integer("Licencia")
    vencimiento_licencia = fields.Date("Vencimiento Licencia")
    soat = fields.Char("SOAT")
    vencimiento_soat = fields.Date("Vencimiento SOAT")
    segundo_conductor = fields.Char("2º Conductor")
    identificacion = fields.Integer("Identificación")
    fecha_emision = fields.Date("Fecha de Emisión")
    valor_informativo_liquidacion = fields.Monetary("Valor informativo en liquidación")
    valor_flete = fields.Monetary("Valor Flete")
    retef = fields.Monetary("Retef")
    ica = fields.Monetary("ICA")
    anticipo = fields.Monetary("Anticipo")
    comprobante = fields.Integer("Comprobante")
    sobreanticipos = fields.Monetary("Sobreanticipo(s)")
    comprobantes = fields.Monetary("Comprobante(s)")
    estado = fields.Char(string="Estado")
    modificado_por = fields.Char("Modificado por")
    fecha_modificacion = fields.Date("Fecha Modificación")
    fecha_radicacion_rndc = fields.Datetime("Fecha Radicación RNDC")
    nro_radicado_rndc = fields.Integer("Nro. Radicado RNDC")
    motivo_anulacion = fields.Text("Motivo de Anulación")
    observacion_anulacion = fields.Text("Observación de Anulación")
    fecha_anulacion_rndc = fields.Datetime("Fecha Anulación RNDC")
    nro_anulacion_rndc = fields.Integer("Nro. Anulación RNDC")
    fecha_cumplido_rndc = fields.Datetime("Fecha Cumplido RNDC")
    fecha_anulacion_cumplido_rndc = fields.Integer("Fecha Anulación Cumplido RNDC")
    nro_anulacion_cumplido_rndc = fields.Integer("Nro. Anulación Cumplido RNDC")
    tipo_cumplido_rndc = fields.Char("Tipo Cumplido RNDC")
    motivo_suspension_rndc = fields.Text("Motivo Suspensión RNDC")
    consecuencia_suspension_rndc = fields.Text("Consecuencia de Suspensión RNDC")
    fecha_manifiesto_transbordo = fields.Date("Fecha Manifiesto Transbordo")
    nro_manifiesto_transbordo = fields.Integer("Nro. Manifiesto Transbordo")
    manifiesto_paqueteo = fields.Char("Manifiesto Paqueteo")
    nro_remesa_paqueteo = fields.Char("Nro. Remesa Paqueteo")

