# -*- coding: utf-8 -*-

from odoo import models, fields, api


class resPartner(models.Model):
    _inherit = 'res.partner'

    salutation = fields.Char('Salutation')
