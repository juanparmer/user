# -*- coding: utf-8 -*-

import requests
import json

from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    zoominfo_password = fields.Char()
    zoominfo_user = fields.Char()

    def zoominfo_authenticate(self):

        username = self.zoominfo_user or 'jlp@d-3.com.au'
        password = self.zoominfo_password or 'xdq1vqp1duq*HNH4qjx'

        protocol = 'https'
        url = 'api.zoominfo.com'
        url = f'{protocol}://{url}/authenticate'

        payload = json.dumps({
            'username': username,
            'password': password,
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request('POST', url, headers=headers, data=payload)
        response_json = response.json()
        jwt = response_json.get('jwt')

        # TODO
        # if not jwt

        return jwt
