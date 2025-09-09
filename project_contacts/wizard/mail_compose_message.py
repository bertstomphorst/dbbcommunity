# -*- coding: utf-8 -*-

from odoo import models, api


class MailComposeMessage(models.TransientModel):
    _inherit = 'mail.compose.message'

    @api.model
    def default_get(self, fields):
        result = super().default_get(fields)
        context = dict(self._context)

        if context.get('default_model') and context.get('default_res_ids'):
            model = context.get('default_model')
            res_ids = context.get('default_res_ids')
            partner_ids = set()

            if model == 'project.project':
                for res_id in res_ids:
                    record = self.env[model].browse(res_id)
                    partner_ids.update(record.get_all_related_partner_ids())
            elif model == 'project.task':
                for res_id in res_ids:
                    record = self.env[model].browse(res_id)
                    partner_ids.update(record.project_id.get_all_related_partner_ids())

            # update partner_ids when needed
            if len(partner_ids) > 0:
                result['partner_ids'] = [(6, 0, partner_ids)]

        return result
