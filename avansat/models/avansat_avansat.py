# -*- coding: utf-8 -*-

from odoo import fields, models


class AvansatAvansat(models.Model):
    _name = "avansat.avansat"
    _description = "Avansat"

    def _default_currency_id(self):
        return self.env.company.currency_id

    currency_id = fields.Many2one("res.currency", default=_default_currency_id)
    name = fields.Char(related="manifiesto", copy=False, readonly=True, string="Nombre")
    line_ids = fields.One2many("account.move.line", "avansat_id")
    avansat_ids = fields.One2many("avansat.order", "avansat_id")

    # Verde
    manifiesto = fields.Char(string="Manifiesto")
    fecha_manifiesto = fields.Date(string="Fecha Manifiesto")
    placa = fields.Char(string="Placa")
    val_inicial_remesa = fields.Monetary(string="Val. Inicial Remesa")
    val_declarado_remesa = fields.Monetary(string="Val. Declarado Remesa")
    val_ser_esp_rem = fields.Monetary(string="Val. Ser. Esp. Rem.")
    facturado_a = fields.Char(string="Facturado A")
    origen = fields.Char(string="Origen")
    destino = fields.Char(string="Destino")
    destinatario = fields.Char(string="Destinatario")
    # Rojo
    tn_pedido = fields.Float(string="(Tn) Pedido")
    tn_cumplido = fields.Float(string="(Tn) Cumplido")
    flete_manifiesto = fields.Float(string="Flete Manifiesto")
    retefuente_manifiesto = fields.Float(string="Retefuente Manifiesto")
    ica_manifiesto = fields.Float(string="ICA Manifiesto")
    anticipo = fields.Float(string="Anticipo")
    # Azul
    nombre_ser_especial = fields.Char(string="Nombre del Ser. Especial")
    val_ser_esp_man = fields.Monetary(string="Val. Ser. Esp. Man.")
    ser_especial_manifiesto = fields.Integer(string="Ser. Especial Manifiesto")
    # Blanco
    remolque = fields.Char(string="Remolque")
    configuracion = fields.Char(string="Configuración")
    contenedor_1 = fields.Char(string="Contenedor 1")
    contenedor_2 = fields.Char(string="Contenedor 2")
    tipo_vinculacion = fields.Char(string="Tipo Vinculación")
    orden_cargue = fields.Char(string="Orden de Cargue")
    remesa = fields.Char(string="Remesa")
    remisiones = fields.Char(string="Remisiones")
    fecha_remesa = fields.Date(string="Fecha Remesa")
    fecha_salida_despacho = fields.Date(string="Fecha Salida Despacho")
    fecha_llegada_despacho = fields.Date(string="Fecha Llegada Despacho")
    cumplida = fields.Date(string="Cumplida")
    fecha_llegada_cargue = fields.Datetime(string="Fecha Llegada de Cargue")
    fecha_salida_cargue = fields.Datetime(string="Fecha Salida de Cargue")
    fecha_llegada_descargue = fields.Datetime(string="Fecha Llegada de Descargue")
    fecha_salida_descargue = fields.Datetime(string="Fecha Salida de Descargue")
    factura = fields.Char(string="factura")
    fecha_factura = fields.Date(string="Fecha Factura")
    fecha_vencimiento = fields.Date(string="Fecha Vencimiento")
    val_facturado_x_separado = fields.Monetary(string="Val. Facturado x Separado")
    val_facturado_remesa = fields.Monetary(string="Val. Facturado Remesa")
    nombre_ser_especial = fields.Char(string="Nombre Ser. Especial")
    aplica_rentabilidad = fields.Char(string="Aplica Rentaabilidad")
    val_servicios = fields.Monetary(string="Val. Servicios")
    val_produccion = fields.Monetary(string="Val. Producción")
    cantidad_facturada = fields.Float(string="Cantidad Facturada")
    costo_unitario = fields.Float(string="Costo Unitario")
    retefuente_factura = fields.Float(string="Retefuente Factura")
    ica_factura = fields.Float(string="ICA Factura")
    iva_factura = fields.Float(string="IVA Factura")
    sede = fields.Char(string="Sede")
    asesor_comercial = fields.Char(string="Asesor Comercial")
    agencia_despacho = fields.Char(string="Agencia Despacho")
    remitente = fields.Char(string="Remitente")
    empaque = fields.Char(string="Empaque")
    unidad_servicio = fields.Char(string="Unidad Servicio")
    tn_o_cargue = fields.Float(string="(Tn) O.Cargue")
    tn_remesa = fields.Float(string="(Tn) Remesa")
    pendiente = fields.Float(string="Pendiente")
    cantidad_cumplida = fields.Integer(string="Cantidad Cumplida")
    usuario_cumplido_manifiesto = fields.Char(string="Usuario Cumplido Manifiesto")
    fecha_cumplido_manifiesto = fields.Datetime(string="Fecha Cumplido Manifiesto")
    tiquete_cargue = fields.Char(string="Tiquete Cargue")
    tiquete_descargue = fields.Char(string="Tiquete Descargue")
    nro_anticipos = fields.Integer(string="Nro. Anticipos")
    nro_comprob_1 = fields.Integer(string="Nro. Comprob")
    valor_flete_liquidacion = fields.Monetary(string="Valor Flete Liquidación")
    valor_liquidado = fields.Monetary(string="Valor Liquidado")
    retefuente_liquid = fields.Integer(string="Retefuente Liquid")
    ica_liquid = fields.Integer(string="ICA Liquid")
    cree_liquid = fields.Integer(string="CREE Liquid")
    fecha_liquid = fields.Date(string="Fecha Liquid.")
    nro_comprob_2 = fields.Integer(string="Nro. Comprob.")
    faltantes_por_liquidacion = fields.Integer(string="Faltantes por Liquidación")
    novedad_reportada = fields.Integer(string="Novedad Reportada")
    valor_a_descontar = fields.Monetary(string="Valor a Descontar")
    descripcion_nov_cum = fields.Integer(string="Descripción Nov. Cum.")
    servicio_integral = fields.Integer(string="Servicio Integral")
    aplica_rentabilidad = fields.Char(string="Aplica Rentabilidad")
    valor_pagado = fields.Monetary(string="Valor Pagado")
    fecha_pago = fields.Date(string="Fecha Pago")
    nro_comprob_3 = fields.Integer(string="Nro. Comprob")
    banco = fields.Char(string="Banco")
    cuenta_bancaria = fields.Integer(string="Cuenta Bancaria")
    nro_cheque = fields.Integer(string="Nro. Cheque")
    tipo_pago = fields.Char(string="Tipo Pago")
    producto = fields.Char(string="Producto")
    conductor = fields.Char(string="Conductor")
    cc_conductor = fields.Integer(string="C.C Conductor")
    celular = fields.Integer(string="Celular")
    poseedor = fields.Char(string="Poseedor")
    cc_nit_poseedor = fields.Integer(string="C.C o Nit Poseedor")
    nro_pedido = fields.Integer(string="Nro. Pedido")
    campo1_opcional = fields.Char(string="Campo1 (Opcional)")
    observacion_llegada = fields.Text(string="Observación de Llegada")
    orden_servicio = fields.Integer(string="Orden de Servicio")
    vlr_tarifa_cotizacion_cliente = fields.Integer(
        string="Vlr. Tarifa Cotización - Cliente"
    )
    descripcion_tarifa = fields.Char(string="Descripción de Tarifa")
    fecha_recaudo = fields.Date(string="Fecha de Recaudo")
    nro_comprobante_recaudo = fields.Integer(string="Nro. Comprobante Recaudo")
    creado_por = fields.Char(string="Creado por")
    estado = fields.Char(string="Estado")
    documento_destinatario = fields.Integer(string="Documento destinatario")
    remesa_padre = fields.Char(string="Remesa Padre")
    costo_produccion = fields.Integer(string="Costo Producción")
    prorrateo_costo_estimado_propio = fields.Float(
        string="Prorrateo Costo Estimado Propio"
    )
    prorrateo_costo_estimado_tercero = fields.Float(
        string="Prorrateo Costo Estimado Tercero"
    )
    prorrateo_utilidad_estimada = fields.Integer(string="Prorrateo Utilidad Estimada")
    fecha_hora_entrada_cargue = fields.Datetime(string="Fecha y Hora Entrada al Cargue")
    fecha_hora_entrada_descargue = fields.Datetime(
        string="Fecha y Hora Entrada al Descargue"
    )
    manifiesto_paqueteo = fields.Char(string="Manifiesto Paqueteo")
    nro_remesa_paqueteo = fields.Char(string="Nro. Remesa Paqueteo")
    tipo_manifiesto = fields.Char(string="Tipo de Manifiesto")

    def campos_verde(self):
        self.ensure_one()
        return {
            "manifiesto": self.manifiesto,
            "fecha_manifiesto": fields.Date.to_string(self.fecha_manifiesto),
            "placa": self.placa,
            "val_inicial_remesa": self.val_inicial_remesa,
            "val_declarado_remesa": self.val_declarado_remesa,
            "val_ser_esp_rem": self.val_ser_esp_rem,
            "facturado_a": self.facturado_a,
            "origen": self.origen,
            "destino": self.destino,
            "destinatario": self.destinatario,
        }

    # TODO
    def campos_rojo(self):
        self.ensure_one()
        return {
            "tn_pedido": self.tn_pedido,
            "tn_cumplido": self.tn_cumplido,
            "flete_manifiesto": self.flete_manifiesto,
            "retefuente_manifiesto": self.retefuente_manifiesto,
            "ica_manifiesto": self.ica_manifiesto,
            "anticipo": self.anticipo
        }

    def campos_azul(self):
        self.ensure_one()
        return {
            "nombre_ser_especial": self.nombre_ser_especial,
            "val_ser_esp_man" : self.val_ser_esp_man,
            "ser_especial_manifiesto" : self.ser_especial_manifiesto
        }

    def campos_blanco(self):
        self.ensure_one()
        return {
            "remolque": self.remolque,
            "configuracion": self.configuracion,
            "contenedor_1": self.contenedor_1,
            "contenedor_2": self.contenedor_2,
            "tipo_vinculacion": self.tipo_vinculacion,
            "orden_cargue": self.orden_cargue,
            "remisiones": self.remisiones,
            "fecha_remesa": self.fecha_remesa,
            "fecha_salida_despacho": self.fecha_salida_despacho,
            "fecha_llegada_despacho": self.fecha_llegada_despacho,
            "cumplida": self.cumplida,
            "fecha_llegada_cargue": self.fecha_llegada_cargue,
            "fecha_salida_cargue": self.fecha_salida_cargue,
            "fecha_llegada_descargue": self.fecha_llegada_descargue,
            "fecha_salida_descargue": self.fecha_salida_descargue,
            "factura": self.factura,
            "fecha_factura": self.fecha_factura,
            "fecha_vencimiento": self.fecha_vencimiento,
            "val_facturado_x_separado": self.val_facturado_x_separado,
            "val_facturado_remesa": self.val_facturado_remesa,
            "nombre_ser_especial": self.nombre_ser_especial,
            "aplica_rentabilidad": self.aplica_rentabilidad,
            "val_servicios": self.val_servicios,
            "val_produccion": self.val_produccion,
            "cantidad_facturada": self.cantidad_facturada,
            "costo_unitario": self.costo_unitario,
            "retefuente_factura": self.retefuente_factura,
            "ica_factura": self.ica_factura,
            "iva_factura": self.iva_factura,
            "sede": self.sede,
            "asesor_comercial": self.asesor_comercial,
            "agencia_despacho": self.agencia_despacho,
            "remitente": self.remitente,
            "empaque": self.empaque,
            "unidad_servicio": self.unidad_servicio,
            "tn_o_cargue": self.tn_o_cargue,
            "tn_remesa": self.tn_remesa,
            "pendiente": self.pendiente,
            "cantidad_cumplida": self.cantidad_cumplida,
            "usuario_cumplido_manifiesto": self.usuario_cumplido_manifiesto,
            "fecha_cumplido_manifiesto": self.fecha_cumplido_manifiesto,
            "tiquete_cargue": self.tiquete_cargue,
            "tiquete_descargue": self.tiquete_descargue,
            "nro_anticipos": self.nro_anticipos,
            "nro_comprob_1": self.nro_comprob_1,
            "valor_flete_liquidacion": self.valor_flete_liquidacion,
            "valor_liquidado": self.valor_liquidado,
            "retefuente_liquid": self.retefuente_liquid,
            "ica_liquid": self.ica_liquid,
            "cree_liquid": self.cree_liquid,
            "fecha_liquid": self.fecha_liquid,
            "nro_comprob_2": self.nro_comprob_2,
            "faltantes_por_liquidacion": self.faltantes_por_liquidacion,
            "novedad_reportada": self.novedad_reportada,
            "valor_a_descontar": self.valor_a_descontar,
            "descripcion_nov_cum": self.descripcion_nov_cum,
            "servicio_integral": self.servicio_integral,
            "aplica_rentabilidad": self.aplica_rentabilidad,
            "valor_pagado": self.valor_pagado,
            "fecha_pago": self.fecha_pago,
            "nro_comprob_3": self.nro_comprob_3,
            "banco": self.banco,
            "cuenta_bancaria": self.cuenta_bancaria,
            "nro_cheque": self.nro_cheque,
            "tipo_pago": self.tipo_pago,
            "producto": self.producto,
            "conductor": self.conductor,
            "cc_conductor": self.cc_conductor,
            "celular": self.celular,
            "poseedor": self.poseedor,
            "cc_nit_poseedor": self.cc_nit_poseedor,
            "nro_pedido": self.nro_pedido,
            "campo1_opcional": self.campo1_opcional,
            "observacion_llegada": self.observacion_llegada,
            "orden_servicio": self.orden_servicio,
            "vlr_tarifa_cotizacion_cliente": self.vlr_tarifa_cotizacion_cliente,
            "descripcion_tarifa": self.descripcion_tarifa,
            "fecha_recaudo": self.fecha_recaudo,
            "nro_comprobante_recaudo": self.nro_comprobante_recaudo,
            "creado_por": self.creado_por,
            "estado": self.estado,
            "documento_destinatario": self.documento_destinatario,
            "remesa_padre": self.remesa_padre,
            "costo_produccion": self.costo_produccion,
            "prorrateo_costo_estimado_propio": self.prorrateo_costo_estimado_propio,
            "prorrateo_costo_estimado_tercero": self.prorrateo_costo_estimado_tercero,
            "prorrateo_utilidad_estimada": self.prorrateo_utilidad_estimada,
            "fecha_hora_entrada_cargue": self.fecha_hora_entrada_cargue,
            "fecha_hora_entrada_descargue": self.fecha_hora_entrada_descargue,
            "manifiesto_paqueteo": self.manifiesto_paqueteo,
            "nro_remesa_paqueteo": self.nro_remesa_paqueteo,
            "tipo_manifiesto": self.tipo_manifiesto
        }
