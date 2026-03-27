/** @odoo-module **/

import { clear } from "@mail/model/model_field_command";
import { registerPatch } from "@mail/model/model_core";

registerPatch({
  name: "MessagingNotificationHandler",
  recordMethods: {
    /**
     * @override
     * @private
     * @param {Object} message
     */
    _handleNotification(message) {
      if (message.type === "llm.thread/delete") {
        return this._handleLLMThreadsDelete(message);
      }
      if (message.type === "llm.thread/open_in_chatter") {
        return this._handleLLMThreadOpenInChatter(message);
      }
      super._handleNotification(message);
    },

    _handleLLMThreadsDelete(message) {
      const ids = message.payload.ids;
      for (const id of ids) {
        this._handleLLMThreadDelete(id);
      }
    },

    /**
     * @private
     * @param {Number} id
     */
    _handleLLMThreadDelete(id) {
      const thread = this.messaging.models.Thread.findFromIdentifyingData({
        id,
        model: "llm.thread",
      });
      if (thread) {
        const llmChat = thread.llmChat;
        if (llmChat) {
          const isActiveThread =
            llmChat.activeThread && llmChat.activeThread.id === thread.id;
          if (isActiveThread) {
            const composer = llmChat.llmChatView?.composer;
            if (composer && composer.isStreaming) {
              composer._closeEventSource();
            }
          }
          const updatedData = {
            threads: llmChat.threads.filter((t) => t.id !== thread.id),
          };
          if (isActiveThread) {
            updatedData.activeThread = clear();
          }
          llmChat.update(updatedData);
        }
        thread.delete();
      }
    },

    /**
     * Handle opening an LLM thread in the chatter
     * Triggered when backend action_open_llm_assistant sends notification
     * @private
     * @param {Object} message
     * @param {Number} message.payload.thread_id - ID of llm.thread to open
     * @param {String} message.payload.model - Model name of related document
     * @param {Number} message.payload.res_id - ID of related document
     */
    async _handleLLMThreadOpenInChatter(message) {
      const { thread_id, model, res_id } = message.payload;

      // Validate payload
      if (!thread_id) {
        return;
      }

      try {
        // Ensure llmChat exists
        if (!this.messaging.llmChat) {
          this.messaging.update({ llmChat: { isInitThreadHandled: false } });
        }

        // Find the thread (might already be in memory)
        let thread = this.messaging.models.Thread.findFromIdentifyingData({
          id: thread_id,
          model: "llm.thread",
        });

        if (!thread) {
          // Thread doesn't exist in frontend yet, reload threads
          // If we have record context, filter by it
          const domain = [];
          if (model && res_id) {
            domain.push(["model", "=", model]);
            domain.push(["res_id", "=", res_id]);
          }
          await this.messaging.llmChat.loadThreads([], domain);

          // Now find the thread (should exist after loading)
          thread = this.messaging.models.Thread.findFromIdentifyingData({
            id: thread_id,
            model: "llm.thread",
          });
        }

        if (!thread) {
          throw new Error("Could not load the conversation thread. Please try again.");
        }

        // Use the unified Odoo pattern to open the thread
        await thread.openLLMThread({ focus: true });

        // Auto-trigger generation (if needed)
        const llmChat = this.messaging.llmChat;
        if (llmChat?.llmChatView?.composer) {
          await llmChat.llmChatView.composer.startGeneration();
        }
      } catch (error) {
        console.error("Error opening LLM thread in chatter:", error);
        this.messaging.notify({
          title: "Error Opening AI Chat",
          message: error.message || "An unexpected error occurred",
          type: "danger",
        });
      }
    },
  },
});
