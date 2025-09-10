# -*- coding: utf-8 -*-
import uuid
import base64
import logging

from collections import defaultdict
from odoo import api, Command, fields, models, _
from odoo.addons.base.models.res_partner import _tz_get
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class Attendee(models.Model):
    _inherit = 'calendar.attendee'

    def _should_notify_attendee(self):
        """ override base Utility method that determines if the attendee should be notified. """
        self.ensure_one()
        # return self.partner_id != self.env.user.partner_id
        return super()._should_notify_attendee() or self.partner_id == self.env.user.partner_id  # we want to notify current user also
