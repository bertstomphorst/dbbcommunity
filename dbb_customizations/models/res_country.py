# -*- coding: utf-8 -*-

from odoo import fields, models


class ResCountry(models.Model):
    _inherit = 'res.country'
    _order = 'sequence, name'

    sequence = fields.Integer(default=10)
