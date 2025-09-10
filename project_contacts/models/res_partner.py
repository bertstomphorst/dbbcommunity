# -*- coding: utf-8 -*-

from odoo import fields, models, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    related_project_count = fields.Integer('Related projects', compute='_compute_related_project_ids')
    related_project_ids_union = fields.One2many('project.project', compute='_compute_related_project_ids')
    related_project_ids = fields.Many2many('project.project',
                                           'project_project_res_partner_rel',
                                           'partner_id',
                                           'project_id',
                                           string='Related Projects'
                                           )

    def _compute_related_project_ids(self):
        for partner in self:
            partner.related_project_count = len(partner.related_project_ids) + len(partner.category_id.related_project_ids)
            partner.related_project_ids_union = partner.related_project_ids | partner.category_id.related_project_ids

    def action_view_project_related(self):
        self.ensure_one()
        return {
            'res_model': 'project.project',
            'type': 'ir.actions.act_window',
            'name': _("Related projects for %s", self.name),
            'domain': [('id', 'in', self.related_project_ids_union.ids)],
            'view_mode': 'tree,form',
        }


class ResPartnerCategory(models.Model):
    _inherit = 'res.partner.category'

    related_project_ids = fields.Many2many('project.project',
                                           'project_project_res_partner_category_rel',
                                           'category_id',
                                           'project_id',
                                           string='Related Projects'
                                           )
