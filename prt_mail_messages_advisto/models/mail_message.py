import logging

from odoo import fields, models, api

_logger = logging.getLogger(__name__)


class MailMessage(models.Model):
    _inherit = "mail.message"

    def _search_shared_inbox(self, operator, operand):
        """ Override base, and search only for items that are not from a user in current database """
        if operator == "=" and operand:
            return [
                "|",
                ("author_id", "=", False),
                ("author_id", "not in", [user.partner_id.id for user in self.env['res.users'].search([])]),
            ]
        return [("author_id", "!=", False)]

    # region split body on quote

    def get_body_without_quote(self):
        self.ensure_one()

        quote_index = self.body.find("<blockquote")
        if quote_index > 0:
            return self.body[:quote_index]

        return self.body

    def get_body_quote(self):
        self.ensure_one()

        quote_index = self.body.find("<blockquote")
        if quote_index > 0:
            return self.body[quote_index:]

        return False

    # endregion

    # region Message read-status

    is_read = fields.Boolean('Is read')

    def _compute_needaction(self):
        super(MailMessage, self)._compute_needaction()

        for message in self:
            if not message.is_read:
                message.needaction = True

    @api.model
    def _search_needaction(self, operator, operand):
        domain = super()._search_needaction(operator, operand)

        is_read = False if operator == '=' and operand else True
        domain = ['|'] + domain + [('is_read', '=', is_read)]
        return domain

    def set_message_done(self):
        self.write({'is_read': True})

        super().set_message_done()

    # endregion
