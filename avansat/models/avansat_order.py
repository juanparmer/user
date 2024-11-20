# -*- coding: utf-8 -*-

from odoo import api, fields, models


class AvansatOrder(models.Model):
    _name = "avansat.order"
    _description = "Listado de ordenes"

    def _default_currency_id(self):
        return self.env.company.currency_id

    currency_id = fields.Many2one("res.currency", default=_default_currency_id)
    name = fields.Char(related="remesa", copy=False, readonly=True, string="Nombre")
    avansat_id = fields.Many2one("avansat.avansat")
    # avansat_id = fields.Many2one(compute="_compute_avansat_id")

    # @api.depends("remesa")
    # def _compute_avansat_id(self):
    #     Avansat = self.env["avansat.avansat"]
    #     for record in self:
    #         avansat = Avansat.search([("remesa", "=", record.remesa)])
    #         record.avansat_id = avansat and avansat or False

    remesa = fields.Char("Remesa")
    nro_remision = fields.Char("Nro.remision")
    nro_autorizacion = fields.Char("Nro. Autorizacion")
    tipo_remesa = fields.Char("Tipo Remesa")
    agencia = fields.Char("Agencia")
    origen = fields.Char("Origen")
    destino = fields.Char("Destino")
    mercancia = fields.Char("Mercancía")
    tipo = fields.Char("Tipo")
    estado = fields.Char("Estado")
    impreso = fields.Char("Impreso")
    nit = fields.Char("Nit")
    cliente = fields.Char("Cliente")
    unidad_servicio = fields.Char("Unidad Servicio")
    valor_remesa_inicial = fields.Monetary("Valor Remesa Inicial")
    valor_declarado = fields.Monetary("Valor Declarado")
    seguro = fields.Char("% Seguro")
    valor_seguro = fields.Monetary("Valor Seguro")
    valor_total = fields.Monetary("Valor Total")
    no_factura = fields.Char("No. Factura")
    valor_unitario = fields.Monetary("Valor Unitario")
    valor_facturado = fields.Monetary("Valor Facturado")
    fecha_de_emision = fields.Datetime("Fecha De Emision")
    manifiesto = fields.Char("Manifiesto")
    creado_por = fields.Char("Creado Por")
    fecha = fields.Date("Fecha")
    orden_cargue = fields.Char("Orden Cargue")
    pedido = fields.Char("Pedido")
    observaciones_cierre = fields.Char("Observaciones Cierre")
    fecha_cierre = fields.Date("Fecha Cierre")
    usuario_cierre = fields.Char("Usuario Cierre")
    radicado_salida_de_cargue = fields.Char("Radicado Salida De Cargue")
    radicado_llegada_a_descargue = fields.Char("Radicado Llegada A Descargue")
    cumplido = fields.Char("Cumplido")
    entrega_final = fields.Char("Entrega Final")
    costo_remesa = fields.Char("Costo Remesa")
    sellos = fields.Char("Sellos")

    @api.model_create_multi
    def create(self, list_vals):
        Avansat = self.env["avansat.avansat"]
        for vals in list_vals:
            avansat = Avansat.search([("remesa", "=", vals.get("remesa"))])
            avansat_id = avansat and avansat.id or False
            vals.update(avansat_id=avansat_id)
        return super().create(vals)
