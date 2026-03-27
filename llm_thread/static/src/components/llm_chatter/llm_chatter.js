/** @odoo-module **/

import { Chatter } from "@mail/components/chatter/chatter";
import { consumePendingOpenInChatter } from "@llm_thread/client_actions/open_chatter_action";
import { onMounted } from "@odoo/owl";
import { patch } from "@web/core/utils/patch";

patch(Chatter.prototype, "llm_thread.Chatter", {
  /**
   * @override
   */
  setup() {
    this._super(...arguments);

    onMounted(() => {
      this._checkPendingAIChatOpen();
    });
  },

  /**
   * Check for pending AI chat open request from client action.
   * Uses sessionStorage to persist state across page navigation.
   */
  async _checkPendingAIChatOpen() {
    const chatter = this.chatter;
    if (!chatter || !chatter.thread) {
      return;
    }

    const pending = consumePendingOpenInChatter(
      chatter.thread.model,
      chatter.thread.id
    );

    if (!pending) {
      return;
    }

    console.log("[LLM] Found pending AI chat open request:", pending);

    try {
      const messaging = chatter.messaging;

      // Ensure llmChat exists
      if (!messaging.llmChat) {
        messaging.update({ llmChat: { isInitThreadHandled: false } });
      }

      // Find the thread (should exist since backend created it)
      let thread = messaging.models.Thread.findFromIdentifyingData({
        id: pending.threadId,
        model: "llm.thread",
      });

      if (!thread) {
        // Thread doesn't exist in frontend yet, reload threads for this record
        const domain = [
          ["model", "=", pending.model],
          ["res_id", "=", pending.resId],
        ];
        await messaging.llmChat.loadThreads([], domain);

        // Try to find it again
        thread = messaging.models.Thread.findFromIdentifyingData({
          id: pending.threadId,
          model: "llm.thread",
        });
      }

      if (!thread) {
        throw new Error(
          "Could not load the conversation thread. Please try again."
        );
      }

      // Open the thread using the unified pattern
      await thread.openLLMThread({ focus: true });

      // Auto-trigger generation if requested
      if (pending.autoGenerate) {
        const llmChat = messaging.llmChat;
        if (llmChat?.llmChatView?.composer) {
          await llmChat.llmChatView.composer.startGeneration();
        }
      }
    } catch (error) {
      console.error("[LLM] Error opening AI chat from pending state:", error);
      chatter.messaging.notify({
        title: "Error Opening AI Chat",
        message: error.message || "An unexpected error occurred",
        type: "danger",
      });
    }
  },
});
