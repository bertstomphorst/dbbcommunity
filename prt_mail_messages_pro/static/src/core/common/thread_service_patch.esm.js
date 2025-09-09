/* @odoo-module */

import {ThreadService} from "@mail/core/common/thread_service";

import {patch} from "@web/core/utils/patch";

patch(ThreadService.prototype, {
    getFetchParams(thread) {
        const data = super.getFetchParams(thread);
        if (thread.type === "chatter" && thread.previewMessageId) {
            return {
                ...data,
                action_id: this.action.currentController.action.id,
                force_message_id: thread.previewMessageId,
            };
        }
        return data;
    },
});
