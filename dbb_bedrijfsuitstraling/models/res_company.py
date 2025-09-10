# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ResCompany(models.Model):
    _inherit = 'res.company'

    x_dbb_post_street = fields.Char('Postadres straat')
    x_dbb_post_zip = fields.Char('Postadres postcode')
    x_dbb_post_city = fields.Char('Postadres plaats')

    x_dbb_mobile2 = fields.Char('Mobiel 2')