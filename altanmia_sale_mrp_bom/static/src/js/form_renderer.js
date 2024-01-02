/** @odoo-module **/

import { getMessagingComponent } from "@mail/utils/messaging_component";

import FormRenderer from 'web.FormRenderer';
import { ComponentWrapper } from 'web.OwlCompatibility';

class ChatterContainerWrapperComponent extends ComponentWrapper {}

/**
 * Include the FormRenderer to instantiate the chatter area containing (a
 * subset of) the mail widgets (mail_thread, mail_followers and mail_activity).
 */
FormRenderer.include({

    /**
     * @override
     */
    _renderNode(node) {
        if (node.tag === 'div' && node.attrs.class === 'op_chatter') {
            console.info("build the chatter");
            return this._makeChatterContainerTarget();
        }
        return this._super(...arguments);
    },
});
