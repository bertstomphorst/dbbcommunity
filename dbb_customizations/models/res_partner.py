# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # region Bungalownummer

    x_dbb_bungalownummer = fields.Char('Bungalownummer')
    x_dbb_relatienummer = fields.Integer('Relatienummer SnelStart', help='Relatienummer SnelStart')

    @api.depends('parent_id')
    def _change_bungalownummer(self):
        """ Push bungalownummer to descending partner's """
        for rec in self:
            for child in rec.child_ids:
                if child.x_dbb_bungalownummer == rec._origin.x_dbb_bungalownummer:
                    child.x_dbb_bungalownummer = rec.x_dbb_bungalownummer

    # endregion
