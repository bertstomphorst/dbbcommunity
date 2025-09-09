/* @odoo-module */

import {onMounted, onWillUpdateProps} from "@odoo/owl";
import {Chatter} from "@mail/core/web/chatter";

export class ChatterPreview extends Chatter {
    setup() {
        super.setup();
        onMounted(() => {
            this.changeThread(
                this.props.threadModel,
                this.props.threadId,
                this.props.webRecord
            );
            if (!this.env.chatter || (this.env.chatter && this.env.chatter.fetchData)) {
                if (this.env.chatter) {
                    this.env.chatter.fetchData = false;
                }
                this.state.thread.previewMessageId = this.props.previewMessageId;
                this.load(this.state.thread, ["messages"]);
            }
        });

        onWillUpdateProps((nextProps) => {
            if (
                this.props.threadId !== nextProps.threadId ||
                this.props.threadModel !== nextProps.threadModel
            ) {
                this.changeThread(
                    nextProps.threadModel,
                    nextProps.threadId,
                    nextProps.webRecord
                );
            }
            this.state.thread.previewMessageId = nextProps.previewMessageId;
            if (!this.env.chatter || (this.env.chatter && this.env.chatter.fetchData)) {
                if (this.env.chatter) {
                    this.env.chatter.fetchData = false;
                }
                this.load(this.state.thread, ["messages"]);
            }
        });
    }
}
ChatterPreview.template = "prt_mail_messages_pro.ChatterPreview";
ChatterPreview.props = [...ChatterPreview.props, "previewMessageId?"];
