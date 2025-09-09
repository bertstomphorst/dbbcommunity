# -*- coding: utf-8 -*-

from odoo import _, api, fields, models


class MailMessage(models.Model):
    _inherit = "mail.message"

    sc_model_id = fields.Many2one('ir.model',
                                  string='Model ',
                                  compute='_compute_model_id',
                                  store=True,
                                  )
    sc_reference = fields.Char('Reference', compute='_compute_reference')
    sc_message_type = fields.Char('Message type', compute='_compute_message_type')
    sc_email_to = fields.Text('E-mail to', compute='_compute_message_to')
    sc_author_name = fields.Char('Author name', compute='_compute_author_name')

    @api.depends('model')
    def _compute_model_id(self):
        for rec in self:
            rec.sc_model_id = self.env['ir.model']._get(rec.model).id

    @api.depends('model', 'res_id')
    def _compute_reference(self):
        for rec in self:
            rec.sc_reference = "%s,%s" % (rec.model, rec.res_id)

    @api.depends('message_type')
    def _compute_message_type(self):
        for rec in self:
            if rec.message_type == 'email':
                rec.sc_message_type = _('E-mail incoming')
            elif rec.message_type == 'email_outgoing' or rec.partner_ids:
                rec.sc_message_type = _('E-mail outgoing')
            elif rec.message_type == 'comment':
                rec.sc_message_type = _('Note')
            else:
                rec.sc_message_type = _('Unknown')

    @api.depends('partner_ids', 'model')
    def _compute_message_to(self):
        for rec in self:
            if rec.partner_ids:
                rec.sc_email_to = '; '.join(filter(None, rec.partner_ids.mapped('email_formatted')))
            elif rec.model == 'res.partner':
                rec.sc_email_to = self.env[rec.model].browse(rec.res_id).email_formatted
            else:
                rec.sc_email_to = False

    def _compute_author_name(self):
        for rec in self:
            rec.sc_author_name = rec.author_id.name
