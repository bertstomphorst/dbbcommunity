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
from odoo import _
from odoo.exceptions import UserError
from odoo.tests import common


class TestResConfigSettings(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.res_config_settings = cls.env["res.config.settings"].create({})

    def test_open_app_store_update_notifier_cron_with_existing_cron(self):
        """Test the open_app_store_update_notifier_cron method with an existing cron."""
        cron_id = self.env.ref(
            "cetmix_app_store_update_notifier.module_versions_check_and_notifi"
        ).id
        result = self.res_config_settings.open_app_store_update_notifier_cron()
        self.assertEqual(
            result["res_id"], cron_id, msg="the action should return with cron_id"
        )

    def test_open_app_store_update_notifier_cron_with_non_existing_cron(self):
        """Test the open_app_store_update_notifier_cron method with a non-existing cron.

        This test checks if the method raises a UserError when trying to open
        a non-existing cron.
        """
        self.env.ref(
            "cetmix_app_store_update_notifier.module_versions_check_and_notifi"
        ).unlink()
        with self.assertRaises(UserError) as context:
            self.res_config_settings.open_app_store_update_notifier_cron()
        self.assertEqual(
            str(context.exception),
            _("Cron action not found"),
            msg="UserError exception should be raised",
        )
