/* @odoo-module */

import {Message} from "@mail/core/common/message";
import {_t} from "@web/core/l10n/translation";
import {parseEmail} from "@mail/js/utils";
import {patch} from "@web/core/utils/patch";

patch(Message.prototype, {
    get mailMessageType() {
        const types = ["email", "email_outgoing", "comment"];
        return types.indexOf(this.message.type) >= 0;
    },

    get messageIsNotChannel() {
        return (
            this.message &&
            !this.deletable &&
            this.mailMessageType &&
            this.message.originThread.model !== "discuss.channel"
        );
    },

    get IsAuthored() {
        return this.message.author;
    },

    openRecord() {
        if (this.message.displayDocumentLink) {
            const thread = this.message.originThread;
            this.action.doAction({
                type: "ir.actions.act_window",
                res_model: thread.model,
                res_id: thread.id,
                views: [[false, "form"]],
                target: "current",
            });
        } else {
            super.openRecord(...arguments);
        }
    },

    get isPreviewMessage() {
        return this.message.id === this.props.thread.previewMessageId;
    },

    refreshThreadMessage() {
        this.props.thread.isLoaded = false;
        this.threadService.fetchNewMessages(this.props.thread);
        this.threadService.fetchNewMessages(this.message.originThread);
        this.env.bus.trigger("reload-preview");
    },

    async openReplyAction(mode) {
        const context = await this.messageService.prepareReplyContext(
            this.message,
            mode
        );
        return this.env.services.action.doAction(
            {
                type: "ir.actions.act_window",
                res_model: "mail.compose.message",
                view_mode: "form",
                views: [[false, "form"]],
                target: "new",
                context: context,
            },
            {
                onClose: () => this.refreshThreadMessage(),
            }
        );
    },

    async openReplyForwardMessage() {
        return await this.openReplyAction("quote");
    },

    async openReplyQuoteMessage() {
        return await this.openReplyAction("forward");
    },

    async openMoveMessage() {
        this.action.doAction(
            {
                type: "ir.actions.act_window",
                res_model: "prt.message.move.wiz",
                view_mode: "form",
                views: [[false, "form"]],
                target: "new",
                context: {
                    thread_message_id: this.message.id,
                },
            },
            {
                onClose: () => this.refreshThreadMessage(),
            }
        );
    },

    async openEditMessage() {
        this.action.doAction(
            {
                type: "ir.actions.act_window",
                res_model: "cx.message.edit.wiz",
                view_mode: "form",
                views: [[false, "form"]],
                target: "new",
                context: {
                    active_ids: [this.message.id],
                },
            },
            {
                onClose: () => this.refreshThreadMessage(),
            }
        );
    },

    async openAssignAuthor() {
        const [name, email] =
            this.message.email_from && parseEmail(this.message.email_from);
        this.action.doAction(
            {
                name: _t("Assign Author"),
                type: "ir.actions.act_window",
                res_model: "cx.message.partner.assign.wiz",
                views: [[false, "form"]],
                target: "new",
                context: {
                    default_name: name,
                    default_email: email,
                    active_id: this.message.id,
                },
            },
            {
                onClose: () => this.refreshThreadMessage(),
            }
        );
    },
});
