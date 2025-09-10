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
import unittest.mock

from odoo.modules.module import get_manifest
from odoo.tests import HttpCase

from ..models.ir_module import Module


class TestAppStoreUpdateNotifier(HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.module_obj = cls.env["ir.module.module"]
        cls.installed_modules = cls.module_obj.search([("state", "=", "installed")])
        # change version for one installed module
        cls.test_module = cls.installed_modules[0]
        cls.test_module_manifest = get_manifest(cls.test_module.name)
        cls.current_version = cls.test_module_manifest["version"]
        # increase version by 1
        cls.new_version = cls.current_version[:-1] + str(
            int(cls.current_version[-1]) + 1
        )

        cls.uninstalled_modules = cls.module_obj.search([("state", "=", "uninstalled")])
        cls.test_uninstall_module = cls.uninstalled_modules[0]

        # To verify that Mocked function will receive a properly processed dictionary
        cls.modules = None

        cls.res_config = cls.env["res.config.settings"]

        cls.template_description = "New Odoo module updates are available for "

    def _set_notification_settings(
        self, modules_update_notif, modules_update_notification_email
    ):
        """Set notification settings for module updates.

        :param modules_update_notif(bool): indicating whether module update
        notifications are enabled.
        :param modules_update_notification_email(str): Email address to
        receive module update notifications.

        :return: The result of executing the record creation operation.
        """
        return self.res_config.create(
            {
                "modules_update_notif": modules_update_notif,
                "modules_update_notification_email": modules_update_notification_email,
            }
        ).execute()

    def check_app_store_updates_mock(self, modules):
        """Mocked method for testing the check_app_store_updates functionality.

        This method imitates the response from the Odoo Apps server
        when checking for module updates

        Args:
            modules (dict): Dictionary containing installed modules.

        Returns:
            dict: A mocked result.
        """
        self.modules = modules
        result = {
            self.test_module.name: {
                "name": self.test_module.name,
                "version_local_running": self.current_version,
                "version_local_downloaded": self.current_version,
                "version_remote": self.new_version,
            },
        }
        return result

    def test_get_modules_need_update(self):
        """Test the get_modules_need_update method.

        This test checks if the method correctly identifies modules that need an update.
        """
        # Mocking the check_app_store_updates method
        # of the Module class for testing purposes
        with unittest.mock.patch.object(
            Module, "check_app_store_updates", self.check_app_store_updates_mock
        ):
            # Call the method and check if the test modules is returned
            updated_modules = self.module_obj.get_modules_need_update()
            self.assertIn(
                self.test_module.name, updated_modules, msg="Module must be in the list"
            )
            self.assertNotIn(
                self.test_uninstall_module.name,
                updated_modules,
                msg="Module must not be in the list",
            )
            self.assertEqual(
                len(updated_modules), 1, msg="only one record must be in the dictionary"
            )
            key, value = next(iter(updated_modules.items()))
            self.assertEqual(
                self.test_module.name, key, msg="Key must match the test module name"
            )

            # Check that Mocked function has received the correct dictionary
            installed_modules = self.installed_modules.read(
                fields=[
                    "name",
                    "installed_version",
                    "latest_version",
                    "state",
                    "display_name",
                ],
            )
            modules_dict = {record["name"]: record for record in installed_modules}
            self.assertEqual(
                modules_dict,
                self.modules,
                msg="Mocked function must receive the correct dictionary",
            )

    def test_send_module_update_notification_enabled_notif(self):
        """Test send_module_update_notification method when notifications are enabled.

        This test checks if the method sends an email when there are module updates,
        notifications are enabled, and the email template is available.
        """
        recipients_emails = "test@mail.com, mail@test.com"
        # Mocking configuration parameters
        self._set_notification_settings(True, recipients_emails)
        mail_obj = self.env["mail.mail"]

        template = self.env.ref(
            "cetmix_app_store_update_notifier.email_template_app_store_update"
        )
        # We need disable it to find our email in mail_obj
        template.auto_delete = False

        ir_module = self.env["ir.model"]._get("ir.module.module")
        # check exist mail.mail records
        mail = mail_obj.search([("model", "=", ir_module.model)])
        self.assertFalse(mail, msg="Message must not existing")

        with unittest.mock.patch.object(
            Module, "check_app_store_updates", self.check_app_store_updates_mock
        ):
            # Call the method and check if the email created
            self.module_obj.get_modules_need_update()
            self.module_obj.send_module_update_notification()
            mail = mail_obj.search([("model", "=", ir_module.model)])
            base_url = self.env["ir.config_parameter"].sudo().get_param("web.base.url")
            mail_description = self.template_description + base_url
            self.assertEqual(
                ir_module.model,
                mail.model,
                msg="Email from our model must created",
            )
            self.assertEqual(
                mail_description,
                mail.description,
                msg="Correct email description",
            )
            self.assertIn(
                recipients_emails,
                mail.email_to,
                msg="all recipients emails must be added",
            )
            self.assertIn(
                self.test_module.display_name,
                mail.body_html,
                msg="Display name must be present in the email",
            )
            self.assertIn(
                self.test_module.name,
                mail.body_html,
                msg="Name of the test module must be present in the email",
            )
            self.assertIn(
                self.test_module.latest_version,
                mail.body_html,
                msg="Current version must be present in the email",
            )
            self.assertIn(
                self.test_module.installed_version,
                mail.body_html,
                msg="New version must be present in the email",
            )

    def test_send_module_update_notification_disabled_notif(self):
        """Test send_module_update_notification method when notifications are disabled.

        This test checks if the method returns False when notifications are disabled.
        """
        recipients_emails = "test@mail.com, mail@test.com"
        # Mocking configuration parameters
        self._set_notification_settings(False, recipients_emails)
        self.assertFalse(
            self.module_obj.send_module_update_notification(),
            msg="function must return False",
        )
