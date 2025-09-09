/* @odoo-module */

import {MessageService} from "@mail/core/common/message_service";

import {patch} from "@web/core/utils/patch";

patch(MessageService.prototype, {
    /** @override **/
    async delete(message) {
        await this.orm.call("mail.message", "unlink_pro", [[message.id]]);
    },

    async prepareReplyContext(message, mode) {
        return await this.orm.call(
            "mail.message",
            "reply_prep_context",
            [[message.id]],
            {
                context: {wizard_mode: mode},
            }
        );
    },
});
