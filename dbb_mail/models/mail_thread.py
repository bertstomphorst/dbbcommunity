# -*- coding: utf-8 -*-

from odoo import models, api


class MailThread(models.AbstractModel):
    _inherit = 'mail.thread'

    def _notify_get_classified_recipients_iterator(
            self, message, recipients_data, msg_vals=False,
            model_description=False, force_email_company=False, force_email_lang=False,  # rendering
            subtitles=None):

        # set force_email_company to current company
        # (from sending single e-mail, this one is not set so it seems to become a bit random)
        if not force_email_company:
            force_email_company = self.env.company

        return super()._notify_get_classified_recipients_iterator(message, recipients_data, msg_vals, model_description, force_email_company, force_email_lang, subtitles)

    def _message_subscribe(self, partner_ids=None, subtype_ids=None, customer_ids=None):
        # disable subscription of followers completely
        return True

    # region register mail_server incoming

    @api.model
    def message_process(self, model, message, custom_values=None, save_original=False, strip_attachments=False, thread_id=None):
        # Verwerk de e-mail zoals gebruikelijk
        result = super(MailThread, self).message_process(model, message, custom_values, save_original, strip_attachments, thread_id)

        # Vind het aangemaakte mail.message record en voeg de mailserver toe
        mail_message = self.env['mail.message'].search([('message_id', '=', message.get('Message-Id'))], limit=1)
        if mail_message and 'default_fetchmail_server_id' in self.env.context:
            mail_message.fetchmail_server_id = self.env.context['default_fetchmail_server_id']

        return result

    # endregion
