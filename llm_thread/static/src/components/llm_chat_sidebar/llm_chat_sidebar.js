/** @odoo-module **/

import { registerMessagingComponent } from "@mail/utils/messaging_component";
import { useModels } from "@mail/component_hooks/use_models";
const { Component } = owl;

export class LLMChatSidebar extends Component {
  setup() {
    useModels();
    super.setup();
  }

  /**
   * @returns {LLMChatView}
   */
  get llmChatView() {
    return this.props.record;
  }

  /**
   * Handle backdrop click to close sidebar on mobile
   */
  _onBackdropClick() {
    if (this.llmChatView.isSmall) {
      this.llmChatView.update({ isThreadListVisible: false });
    }
  }

  /**
   * Toggle sidebar collapsed state (desktop only)
   */
  _onClickToggleSidebar() {
    this.llmChatView.toggleSidebar();
  }

  /**
   * Handle click on New Chat button
   */
  async _onClickNewChat() {
    const llmChat = this.llmChatView.llmChat;

    // If in chatter mode, create thread for the record
    if (llmChat.isChatterMode) {
      // Don't pass name - let backend generate it from record display_name
      const thread = await llmChat.createThread({
        relatedThreadModel: llmChat.relatedThreadModel,
        relatedThreadId: llmChat.relatedThreadId,
      });

      if (thread) {
        llmChat.update({ activeThread: thread });

        // Close sidebar on mobile/aside
        if (this.llmChatView.isSmall) {
          this.llmChatView.update({ isThreadListVisible: false });
        }
      }
    } else {
      // Standalone mode - existing behavior
      await llmChat.createNewThread();
      if (this.llmChatView.isSmall) {
        this.llmChatView.update({ isThreadListVisible: false });
      }
    }
  }
}

Object.assign(LLMChatSidebar, {
  props: { record: Object },
  template: "llm_thread.LLMChatSidebar",
});

registerMessagingComponent(LLMChatSidebar);
