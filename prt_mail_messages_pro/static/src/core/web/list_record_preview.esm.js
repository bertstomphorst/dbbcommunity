/** @odoo-module **/

import {Component, useState} from "@odoo/owl";
import {useBus, useService} from "@web/core/utils/hooks";
import {ChatterPreview} from "./chatter_preview.esm";
import {session} from "@web/session";

export class ListRecordPreview extends Component {
    setup() {
        this.threadService = useService("mail.thread");
        this.state = useState({
            threadId: false,
            threadModel: false,
            previewMessageId: false,
        });
        useBus(this.env.bus, "reload-preview", ({detail}) => {
            if (detail !== null) {
                const {threadId, threadModel, messageId} = detail;
                if (messageId === this.state.previewMessageId) {
                    const thread = this.threadService.getThread(threadModel, threadId);
                    thread.previewMessageId = messageId;
                    this.state.threadId = threadId;
                    this.state.threadModel = threadModel;
                    this.state.previewMessageId = messageId;
                }
            }
        });
        useBus(this.env.bus, "open-record", ({detail}) => {
            session.web_action.force_message_id = detail.resId;
            const thread = this.threadService.getThread(
                detail.data.model,
                detail.data.res_id
            );
            thread.previewMessageId = this.state.previewMessageId;
            this.setThreadData(detail.data.res_id, detail.data.model, detail.resId);
        });
        useBus(this.env.bus, "clear-chatter", () => {
            this.setThreadData();
        });
    }

    setThreadData(threadId, threadModel, previewId) {
        this.state.previewMessageId = previewId || false;
        this.state.threadId = threadId || false;
        this.state.threadModel = threadModel || false;
    }

    get className() {
        return this.props.isDisplay ? "" : "d-none";
    }
}

ListRecordPreview.template = `prt_mail_messages_pro.ListRecordPreview`;
ListRecordPreview.components = {
    ChatterPreview,
};
ListRecordPreview.props = ["isDisplay?"];
