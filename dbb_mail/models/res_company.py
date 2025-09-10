# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ResCompany(models.Model):
    _inherit = 'res.company'

    x_dbb_openingstijden = fields.Text('Openingstijden', translate=True)
    x_dbb_telefoontijden = fields.Char('Telefoontijden', translate=True)
