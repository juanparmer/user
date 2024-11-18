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

    def action_move(self, mtype):
        # Se agrupan las lineas segun el tercero y se crean las facturas
        Avansat = self.env["avansat.avansat"]
        Move = self.env["account.move"]

        invoices = []

        domain = [("id", "in", self.avansats_ids.ids)]
        fields = ["val_ser_esp_rem:sum"]
        groupby = ["facturado_a"]
        read_group = Avansat.read_group(domain, fields, groupby)
        for rg in read_group:
            partner = self.get_partner(rg.get("facturado_a"))
            avansats = self.avansats_ids.filtered(
                lambda a: a.facturado_a == rg.get("facturado_a")
            )
            for avansat in avansats:
                if avansat.line_ids.filtered(lambda l: l.move_id.move_type == mtype):
                    raise ValidationError(
                        "La remesa %s ya esta facturada" % avansat.remesa
                    )

            invoice_vals = self.get_invoice(avansats, partner, mtype)
            invoice = Move.create(invoice_vals)
            invoices.append(invoice.id)

        return {
            "name": "Facturas",
            "type": "ir.actions.act_window",
            "view_type": "tree,form",
            "view_mode": "form",
            "res_model": "account.move",
            # "res_id": self.id,
            "domain": [("id", "in", invoices)],
        }

    def action_invoice(self):
        return self.action_move("out_invoice")

    def action_bill(self):
        return self.action_move("in_invoice")

    def action_payment(self):
        # Se crea un anticipo por cada una de las lineas
        Avansat = self.env["avansat.avansat"]
        Voucher = self.env["account.voucher"]

        voucher_list = []

        for avansat in self.avansats_ids:
            partner = self.get_partner(avansat.facturado_a)

            if avansat.line_ids.filtered(lambda l: l.move_id.voucher_id):
                raise ValidationError(
                    "La remesa %s ya tiene un anticipo" % avansat.remesa
                )

            vals = {
                "partner_type": "supplier",
                "voucher_type": 'advance',
                "voucher_reference": avansat.ser_especial_manifiesto,
                "partner_id": partner.id,
                "amount": avansat.val_ser_esp_man,
                "avansat_id": avansat.id,
            }
            voucher_list.append(vals)

        vouchers = Voucher.create(voucher_list)

        return {
            "name": "Anticipos",
            "type": "ir.actions.act_window",
            "view_type": "tree,form",
            "view_mode": "form",
            "res_model": "account.voucher",
            # "res_id": self.id,
            "domain": [("id", "in", vouchers.ids)],
        }

    def get_partner(self, name):
        # Busca el asociado segun el nombre
        Partner = self.env["res.partner"]
        partner = Partner.search([("name", "=", name)], limit=1)
        if not partner:
            partner = Partner.search([("name", "ilike", name)], limit=1)
        if not partner:
            raise ValidationError("No se encontro tercero")
        return partner

    def get_invoice(self, avansats, partner, mtype):
        # Retorna un diccionario para crear la factura
        invoice_line_ids = self.get_invoice_line(avansats)

        vals = {
            "move_type": mtype,
            "type_note": False,
            "partner_id": partner.id,
            "invoice_date": avansats[0].fecha_manifiesto,
            "invoice_line_ids": invoice_line_ids,
        }

        if mtype == "out_invoice":
            vals.update(
                {
                    "fe_type": "01",
                    "fe_operation_type": "12",
                }
            )

        return vals

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
                    "avansat_id": a.id,
                    "consignment_ids": [
                        (
                            0,
                            0,
                            {
                                "consignment_id": a.remesa,
                                "transport_rec": "1",
                                "freight": a.val_inicial_remesa,
                                "quantity": 1,
                                "udm": "KGM",
                                "order_ref": "",
                            },
                        )
                    ],
                },
            )
            for a in avansats
        ]
