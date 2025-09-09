###################################################################################
#
#    Copyright (C) 2020 Cetmix OÜ
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as
#   published by the Free Software Foundation, either version 3 of the
#   License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###################################################################################

# Copyright (C) 2023 Cetmix OÜ
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0).

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    modules_update_notif = fields.Boolean(
        string="Modules Update Notifications",
        config_parameter="cetmix_app_store_update_notifier.modules_update_notif",
    )

    modules_update_notification_email = fields.Char(
        string="Notify on email",
        help="Using a plain email address to send notifications.",
        config_parameter="cetmix_app_store_update_notifier.modules_update_notification_email",
    )

    @api.constrains("modules_update_notification_email")
    def _check_notifications_email_address(self):
        """Checks for the presence of the email address for notification"""
        if self.modules_update_notif and not self.modules_update_notification_email:
            raise ValidationError(
                _(
                    "Module update notifications are enabled, please add an email"
                    " address or disable notifications to save the settings."
                )
            )

    def open_app_store_update_notifier_cron(self):
        """Opens the configured cron action related to app store updates."""
        cron = self.env.ref(
            "cetmix_app_store_update_notifier.module_versions_check_and_notifi",
            raise_if_not_found=False,
        )
        if not cron:
            raise UserError(_("Cron action not found"))
        return {
            "type": "ir.actions.act_window",
            "name": _("Cron Action"),
            "view_mode": "form",
            "res_id": cron.id,
            "res_model": "ir.cron",
        }

    def open_app_store_update_notifier_template(self):
        """Opens the configured template related to app store updates."""
        template = self.env.ref(
            "cetmix_app_store_update_notifier.email_template_app_store_update",
            raise_if_not_found=False,
        )
        if not template:
            raise UserError(_("Template was not found"))
        return {
            "type": "ir.actions.act_window",
            "name": _("Template open Action"),
            "view_mode": "form",
            "res_id": template.id,
            "res_model": "mail.template",
        }
