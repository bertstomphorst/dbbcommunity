/** @odoo-module **/

import {ListRecordPreview} from "@prt_mail_messages_pro/core/web/list_record_preview.esm";
import {MailMessageUpdateListRenderer} from "@prt_mail_messages/views/list/mail_message_list_renderer.esm";

export class MailMessagePreviewListRenderer extends MailMessageUpdateListRenderer {
    setup() {
        super.setup();
    }
    async onCellClicked(record, column, ev) {
        if (!this.props.previewMode) {
            return super.onCellClicked(record, column, ev);
        }
        this.env.bus.trigger("open-record", record);
    }
}
MailMessagePreviewListRenderer.template = "prt_mail_messages_pro.MessageListRenderer";
MailMessagePreviewListRenderer.components = {
    ...MailMessagePreviewListRenderer.components,
    ListRecordPreview,
};
MailMessagePreviewListRenderer.props = [
    ...MailMessagePreviewListRenderer.props,
    "previewMode",
];
