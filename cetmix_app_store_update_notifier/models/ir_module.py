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
import requests

from odoo import models
from odoo.service.common import exp_version

from odoo.addons.base_import_module.models.ir_module import APPS_URL


class Module(models.Model):
    _inherit = "ir.module.module"

    def send_module_update_notification(self):
        """Checks for updates for installed modules and sends an email when found.

        Returns:
            bool: True if notifications were successfully sent, False otherwise.
        """
        ICPSudo = self.env["ir.config_parameter"].sudo()
        modules_update_notif = ICPSudo.get_param(
            "cetmix_app_store_update_notifier.modules_update_notif", False
        )
        template = self.env.ref(
            "cetmix_app_store_update_notifier.email_template_app_store_update",
            raise_if_not_found=False,
        )
        if not modules_update_notif or not template:
            return False
        modules_to_update_dict = self.get_modules_need_update()
        if not modules_to_update_dict:
            return False
        emails = [
            ICPSudo.get_param(
                "cetmix_app_store_update_notifier.modules_update_notification_email",
                False,
            )
        ]
        odoobot = self.env.ref("base.partner_root")
        email_values = {
            "email_to": ", ".join(emails),
            "author_id": odoobot.id,
        }
        if not template.email_from:
            email_values["email_from"] = odoobot.email_formatted
        template.sudo().send_mail(
            template.write_uid.id,
            force_send=True,
            email_values=email_values,
        )
        return True

    def check_app_store_updates(self, modules):
        """Check for updates in the app store for the given modules.

        Args:
            modules (dict): A dictionary of installed modules.

        Returns:
            dict: Information about the modules on the odoo server.
            Example:
            {
                'module.name': {
                    'id': 123,  # module ID
                    'name': 'example_module',  # module name
                    'version_local_running': '1.0.0',  # local version
                    'version_local_downloaded': '1.0.0',  # downloaded version
                    'version_remote': '1.2.0',  # version available in odoo app store
                    'todo': 'to_update',  # Indicates that an update is needed
                },
            }
        """
        # odoo apps server
        url = f"{APPS_URL}/apps/embed/update"
        payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "modules": modules,
                "version": exp_version(),
            },
        }
        response = requests.Session().post(url, json=payload).json()
        return response.get("result")

    def get_modules_need_update(self):
        """Find installed modules and get a dictionary of modules that need an update.

        Returns:
            dict: Modules that need an update.
            Example:
            {
                'module.name': {
                    'id': 123,  # module ID on the odoo server
                    'name': 'example_module',  # module name
                    'version_local_running': '1.0.0',  # local version
                    'version_local_downloaded': '1.0.0',  # downloaded version
                    'version_remote': '1.2.0',  # version available in odoo app store
                    'todo': 'to_update',  # Indicates that an update is needed
                    'display_name': 'Example Module',  # display name
                },
            }
        """
        # find the installed modules and prepare the dictionary
        # for the query on the server
        installed_modules = self.search_read(
            [("state", "=", "installed")],
            fields=[
                "name",
                "installed_version",
                "latest_version",
                "state",
                "display_name",
            ],
        )
        modules_dict = {record["name"]: record for record in installed_modules}

        # Check for updates
        modules_to_update_dict = self.check_app_store_updates(modules_dict)

        # Update modules_to_update_dict with display_name
        for module_name, module_info in modules_to_update_dict.items():
            installed_module_info = modules_dict.get(module_name, {})
            module_info["display_name"] = installed_module_info.get("display_name", "")
        return modules_to_update_dict
