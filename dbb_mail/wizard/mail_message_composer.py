# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
import re

from logging import getLogger

_logger = getLogger(__name__)


class MailComposer(models.TransientModel):
    _inherit = 'mail.compose.message'

    email_from_company = fields.Many2one('res.company',
                                         'Afzender (organisatie)',
                                         domain=lambda self: self._get_from_company_domain(),
                                         )

    @api.model
    def _get_from_company_domain(self):
        # Get the current user's allowed companies
        allowed_company_ids = self._context.get('allowed_company_ids')
        if not allowed_company_ids:
            allowed_company_ids = [self.env.user.company_id.id]

        # Return the domain combining both conditions
        return [('email', '!=', False), ('id', 'in', allowed_company_ids)]

    @api.onchange('email_from_company')
    def _onchange_email_from_company(self):
        for rec in self:
            if not rec.email_from_company:
                continue

            if rec.composition_mode == 'mass_mail':
                template_id = self.env['mail.template'].browse(40)  # 40 = standaard mail-template voor groep (met volledige opmaak)
                rec.mass_mailing_name = rec.subject or '-'
            else:
                template_id = self.env['mail.template'].browse(28)  # 28 = standaard mail-template met alleen aanhef

            if rec.template_id != template_id:
                # keep quoted-content
                current_body = rec.body
                current_subject = rec.subject
                current_partner_ids = rec.partner_ids
                rec.template_id = template_id

                if current_body:
                    rec.body = '%s %s' % (rec.body, current_body)
                if current_subject and rec.wizard_mode in ["quote", "forward"]:
                    rec.subject = current_subject
                if current_partner_ids:
                    rec.partner_ids = current_partner_ids

            rec.record_company_id = rec.email_from_company
            rec.email_from = rec.email_from_company.email_formatted
            rec.reply_to = rec.email_from_company.email_formatted

    @api.onchange('subject')
    def _onchange_subject(self):
        for rec in self:
            if rec.subject == '-' or rec.subject == 'Re: -':
                rec.subject = False
                continue

            if rec.composition_mode == 'mass_mail' and rec.subject:
                rec.mass_mailing_name = rec.subject

    def _action_send_mail(self, auto_commit=False):
        # _logger.info('context _action_send_mail %s' % self.env.context)
        # _logger.info('email_from_company = %s' % self.email_from_company)

        # check if it's from mass_mail, and if so, set email_from_company from there
        if not self.email_from_company and 'post_convert_links' in self.env.context and 'mass_mailing_id' in self.env.context['post_convert_links']:
            mailing_id = self.env['mailing.mailing'].browse(self.env.context['post_convert_links']['mass_mailing_id'])
            # _logger.info('found mass mailing: %s, with email_from_company %s -> attach it to current mail.compose.message' % (mailing_id, mailing_id.email_from_company))
            self.email_from_company = mailing_id.email_from_company

        if 'email_from_company_id' in self.env.context:
            _logger.info('get email_from_company_id from context: %s' % self.env.context['email_from_company_id'])
            self.email_from_company = self.env['res.company'].browse(self.env.context['email_from_company_id'])

        # Validate email_from_company
        if not (self.email_from_company or self.subtype_is_log):
            raise ValidationError("Afzender (organisatie) is niet gekozen!")

        # Set author to current user, but sender/reply_to to company
        self.author_id = self.env['res.users'].browse(self.env.uid).partner_id
        self.email_from = self.email_from_company.email_formatted
        self.reply_to = self.email_from_company.email_formatted

        # Set company for logo's
        if self.email_from_company:
            _logger.info('with email_from_company - send via company: %s' % self.email_from_company)
            res = super(MailComposer, self.with_company(self.email_from_company))._action_send_mail(auto_commit=auto_commit)
            return res

        # _logger.info('no email_from_company, send via company: %s' % self.env.company)
        return super()._action_send_mail(auto_commit=auto_commit)

    def _set_value_from_template(self, template_fname, composer_fname=False):
        """
        This method is called when a template is applied in composer.
        Here we want to set company-data immediately, so user can see it in preview.
        """
        res = super()._set_value_from_template(template_fname, composer_fname)

        # apply company-data
        if template_fname == 'body_html' and composer_fname == 'body':
            # _logger.info('base64 = %s' % self.email_from_company.logo_web.decode('utf-8'))
            res = res.format(
                COMPANY_LOGO='data:image/png;base64,%s' % self.email_from_company.logo_web.decode('utf-8'),
                COMPANY_NAME=self.email_from_company.name,
                COMPANY_NAME_LOWER=self.email_from_company.name.lower(),
                COMPANY_STREET=self.email_from_company.street,
                COMPANY_ZIP=self.email_from_company.zip,
                COMPANY_CITY=self.email_from_company.city,
                COMPANY_PHONE=self.email_from_company.phone,
                COMPANY_EMAIL=self.email_from_company.email,
                COMPANY_WEBSITE=self.email_from_company.website,
                ALG_OPENINGSTIJDEN=self.env['res.company'].browse(1).x_dbb_openingstijden.replace('\n', '<br/>'),
                ALG_TELEFOONTIJDEN=self.env['res.company'].browse(1).x_dbb_telefoontijden,
            )

            self[composer_fname] = res

        # _logger.info('res2 = %s' % res)
        return res

    # region Default email_from on quote/forward

    @api.model
    def default_get(self, fields_list):
        result = super().default_get(fields_list)
        wizard_mode = result.get("wizard_mode") or self._context.get("default_wizard_mode")
        if not wizard_mode:
            return result

        parent_id = result.get("parent_id")
        if parent_id and wizard_mode in ["quote", "forward"]:
            parent = self.env["mail.message"].browse(parent_id)
            result.update(
                email_from_company=self.get_company_by_email(parent.email_from, parent.reply_to)
            )
        return result

    def get_company_by_email(self, email_from, reply_to):
        # Functie om het emailadres te extraheren als het in < > staat
        def extract_email(email_str):
            match = re.search(r'<(.+?)>', email_str)
            return match.group(1) if match else email_str.strip()

        # Probeer eerst reply_to
        if reply_to:
            reply_to_email = extract_email(reply_to)
            company = self.env['res.company'].search([('email', '=', reply_to_email)], limit=1)
            if company:
                return company

        # Probeer daarna email_from als er geen match is gevonden
        if email_from:
            email_from_email = extract_email(email_from)
            company = self.env['res.company'].search([('email', '=', email_from_email)], limit=1)
            if company:
                return company

        return None

    # endregion


class DocumentsRequestWizard(models.TransientModel):
    _inherit = 'documents.request_wizard'

    email_from_company = fields.Many2one('res.company',
                                         'Afzender (organisatie)',
                                         domain=lambda self: self._get_from_company_domain(),
                                         required=True,
                                         )

    @api.model
    def _get_from_company_domain(self):
        # Get the current user's allowed companies
        allowed_company_ids = self._context.get('allowed_company_ids')
        if not allowed_company_ids:
            allowed_company_ids = [self.env.user.company_id.id]

        # Return the domain combining both conditions
        return [('email', '!=', False), ('id', 'in', allowed_company_ids)]

    def request_document(self):
        _logger.info('context request_document %s' % self.env.context)
        _logger.info('request_document email_from_company = %s' % self.email_from_company)
        return super(DocumentsRequestWizard, self.with_context(email_from_company_id=self.email_from_company.id)).request_document()

