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
{
    "name": "New Module Version Notifications",
    "summary": "Notify about new module versions available in App Store",
    "version": "17.0.1.0.0",
    "category": "Maintenance",
    "website": "https://cetmix.com",
    "author": "Cetmix",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "images": ["static/description/banner.png"],
    "depends": [
        "digest",
    ],
    "data": [
        "data/email_template.xml",
        "data/ir_cron_data.xml",
        "views/res_config_settings_view.xml",
    ],
}
