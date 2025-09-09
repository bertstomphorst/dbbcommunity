/* @odoo-module */

import {Message} from "@mail/core/common/message_model";
import {Record} from "@mail/core/common/record";
import {patch} from "@web/core/utils/patch";

patch(Message.prototype, {
    get isEmail() {
        return this.type === "email";
    },

    get getNotifyIconClass() {
        if (this.isEmail) return "fa fa-inbox";
        if (this.messageSendMode === "email") return "fa fa-at";
        if (this.messageSendMode === "odoo") return "fa fa-envelope-o";
        return false;
    },

    cx_edit_message: false,
    displayDocumentLink: false,
    partnerCc: Record.many("Persona"),
    partnerBcc: Record.many("Persona"),
    messageSendMode: Record.attr(),
    originalToEmail: Record.attr(),
    originalCcEmail: Record.attr(),
});
