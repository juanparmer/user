from odoo import models, fields, api


class avansat(models.TransientModel):
    _name = 'avansat.wizard'
    _description = 'Wizard'

    def _default_avasant_id (self):
        return self.env.context.get('active_id')

    avansat_id = fields.Many2one("avansat.avansat", default=_default_avasant_id)