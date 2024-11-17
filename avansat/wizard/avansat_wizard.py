# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class avansat(models.TransientModel):
    _name = "avansat.wizard"
    _description = "Wizard"

    def _default_avansats_ids(self):
        return self.env.context.get("active_ids")

    avansats_ids = fields.Many2many("avansat.avansat", default=_default_avansats_ids)

    product_id = fields.Many2one("product.product")

    def action_confirm(self):
        # Se agrupan las lineas segun el tercero y se crean las facturas
        Avansat = self.env["avansat.avansat"]
        Move = self.env["account.move"]

        domain = [("id", "in", self.avansats_ids.ids)]
        fields = ["val_ser_esp_rem:sum"]
        groupby = ["facturado_a"]
        read_group = Avansat.read_group(domain, fields, groupby)

        # facturas_creadas = self.env["account.move"]

        for rg in read_group:
            partner = self.get_partner(rg.get("facturado_a"))
            avansats = self.avansats_ids.filtered(
                lambda a: a.facturado_a == rg.get("facturado_a")
            )
            invoice_vals = self.get_invoice(avansats, partner)
            invoice = Move.create(invoice_vals)
            # facturas_creadas |= invoice
            print(invoice)
        # TODO
        # Cretornar vista tree de las facturas
        # return {
        #     'type' : "ir.actions.act_window",
        #     "name" : "Facturas",
        #     "res_model" : "account.move",
        #     "view_mode" : "tree",
        #     'domain': [('id', 'in', facturas_creadas.ids)],  # Mostrar solo las facturas creadas 
        # }
        return True

    def get_partner(self, name):
        # Busca el asociado segun el nombre
        Partner = self.env["res.partner"]
        partner = Partner.search([("name", "=", name)], limit=1)
        if not partner:
            partner = Partner.search([("name", "ilike", name)], limit=1)
        if not partner:
            raise ValidationError("No se encontro tercero")
        return partner

    def get_invoice(self, avansats, partner):
        # Retorna un diccionario para crear la factura
        invoice_line_ids = self.get_invoice_line(avansats)
        return {
            "move_type": "out_invoice",
            "type_note": False,
            # "fe_type": '12',
            "partner_id": partner.id,
            # "invoice_date": ''
            "invoice_line_ids": invoice_line_ids,
        }

    def get_invoice_line(self, avansats):
        # Retorna una lista de tuplas para crear las lineas de la factura con el estilo [(0,0,{})]
        # Yo hago esta parte
        return [
            (
                0,
                0,
                {
                    "product_id": self.product_id.id,
                    "price_unit": a.val_ser_esp_rem,
                    # "consignment_ids": [(0,0,{
                    #     "consignment_id": a.remesa,
                    #     "transport_rec": "1",
                    #     "freight": a.val_inicial_remesa,
                    #     "quantity": 1,
                    #     "udm": "KGM",
                    #     "order_ref": "",
                    # })],
                },
            )
            for a in avansats
        ]
