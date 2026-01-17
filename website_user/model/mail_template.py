# -*- coding: utf-8 -*-

from odoo import models


class MailTemplate(models.Model):
    _inherit = 'mail.template'

    def run_website_branding(self):
        templates = self.search([('body_html', 'ilike', 'Powered by ')])
        for template in templates:
            body_html = template.body_html
            body_html = body_html.replace('Powered by', '<!-- Powered by')
            body_html = body_html.replace('Powered by', 'Odoo</a> -->')
            template.write({'body_html': body_html})
