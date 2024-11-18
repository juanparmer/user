# -*- coding: utf-8 -*-

from odoo.addons.base_rest.controllers import main


class MyRestController(main.RestController):
    _root_path = "/avansat_api/"
    _collection_name = "avansat.services"
    _default_auth = "user"
