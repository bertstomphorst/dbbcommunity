import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class MailMessage(models.Model):
    _inherit = "mail.message"

    # region register mail_server incoming

    fetchmail_server_id = fields.Many2one('fetchmail.server',
                                          string="Mail Server", help="The mail server used for this incoming message.")

    # endregion
