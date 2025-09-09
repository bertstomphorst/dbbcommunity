# -*- coding: utf-8 -*-

from odoo import _, api, fields, models


class IrAttachment(models.Model):
    _inherit = "ir.attachment"

    sc_model_id = fields.Many2one('ir.model',
                                    string='Model',
                                    compute='_compute_model_id',
                                    store=True,
                                    )

    @api.depends('res_model')
    def _compute_model_id(self):
        for rec in self:
            rec.sc_model_id = self.env['ir.model']._get(rec.res_model).id

    sc_reference = fields.Char('Reference',
                                 compute='_compute_reference')

    @api.depends('res_model', 'res_id')
    def _compute_reference(self):
        for rec in self:
            rec.sc_reference = "%s,%s" % (rec.res_model, rec.res_id)

    def action_open_document(self):
        """ Opens the related record based on the model and ID """
        self.ensure_one()
        return {
            'name': _('Record voor %s', self.res_name),
            'res_id': self.res_id,
            'res_model': self.res_model,
            'target': 'current',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
        }
