# -*- coding: utf-8 -*-

from odoo import api, fields, models


class MassMailing(models.Model):
    """ Mass Mailing models the sending of emails to a list of recipients for a mass mailing campaign."""
    _inherit = 'mailing.mailing'

    email_from_company = fields.Many2one('res.company',
                                         'Afzender (organisatie)',
                                         domain=[('email', '!=', False)],
                                         )

    @api.onchange('email_from_company')
    def _onchange_email_from_company(self):
        for rec in self:
            rec.email_from = rec.email_from_company.email_formatted
            rec.reply_to = rec.email_from_company.email_formatted
