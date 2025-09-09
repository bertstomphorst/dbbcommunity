# -*- coding: utf-8 -*-

from odoo import fields, models, api


@api.model
def _lang_get(self):
    return self.env['res.lang'].get_installed()


class Project(models.Model):
    _inherit = 'project.project'

    related_partner_ids = fields.Many2many('res.partner',
                                           'project_project_res_partner_rel',
                                           'project_id',
                                           'partner_id',
                                           string='Related contacts',
                                           )
    related_partner_category_ids = fields.Many2many('res.partner.category',
                                                    'project_project_res_partner_category_rel',
                                                    'project_id',
                                                    'category_id',
                                                    string='Related contacts tags'
                                                    )

    def get_all_related_partner_ids(self):
        result = set()
        result.update(self.related_partner_ids.ids)
        result.update(self.related_partner_category_ids.partner_ids.ids)
        return result

