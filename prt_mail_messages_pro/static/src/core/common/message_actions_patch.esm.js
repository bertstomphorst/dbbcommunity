/* @odoo-module */

import {_t} from "@web/core/l10n/translation";
import {messageActionsRegistry} from "@mail/core/common/message_actions";

messageActionsRegistry
    .add("msg-quote", {
        condition: (component) => component.mailMessageType,
        onClick: (component) => component.openReplyForwardMessage(),
        icon: "fa-quote-left",
        title: _t("Quote"),
        sequence: 50,
    })
    .add("msg-forward", {
        condition: (component) => component.mailMessageType,
        onClick: (component) => component.openReplyQuoteMessage(),
        icon: "fa-copy",
        title: _t("Forward"),
        sequence: 60,
    })
    .add("msg-move", {
        condition: (component) => component.mailMessageType,
        onClick: (component) => component.openMoveMessage(),
        icon: "fa-arrow-right",
        title: _t("Move"),
        sequence: 70,
    })
    .add("msg-delete", {
        condition: (component) => component.messageIsNotChannel,
        onClick: (component) => component.onClickDelete(),
        icon: "fa-trash",
        title: _t("Delete"),
        sequence: 90,
    })
    .add("msg-edit", {
        condition: (component) => component.messageIsNotChannel,
        onClick: (component) => component.openEditMessage(),
        icon: "fa-pencil",
        title: _t("Edit"),
        sequence: 80,
    })
    .add("msg-assign", {
        condition: (component) => !component.IsAuthored,
        onClick: (component) => component.openAssignAuthor(),
        icon: "fa-user-plus",
        title: _t("Assign"),
        sequence: 65,
    });
