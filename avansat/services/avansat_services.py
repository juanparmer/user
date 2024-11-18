# -*- coding: utf-8 -*-

from odoo.addons.component.core import Component


class PingService(Component):
    _inherit = "base.rest.service"
    _name = "avansat.service"
    _usage = "avansat"
    _collection = "avansat.services"

    # pylint:disable=method-required-super
    def create(self, **params):
        Avansat = self.env['avansat.avansat']
        avansat = Avansat.create(params)
        return {"response": "POST called with message " + params.get("message", '')}
