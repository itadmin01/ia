/** @odoo-module **/

import { attr, one } from "@mail/model/model_field";
import { clear } from "@mail/model/model_field_command";
import { registerPatch } from "@mail/model/model_core";

registerPatch({
  name: "Chatter",
  fields: {
    is_chatting_with_llm: attr({
      compute() {
        // Derived from llmChat state, not stored locally
        const llmChat = this.messaging.llmChat;
        if (!llmChat || !llmChat.activeThread || !this.thread) {
          return false;
        }
        // True if active LLM thread is for this chatter's record
        return (
          llmChat.activeThread.relatedThreadModel === this.thread.model &&
          llmChat.activeThread.relatedThreadId === this.thread.id
        );
      },
    }),
    llmChatThread: one("Thread", {
      compute() {
        if (!this.is_chatting_with_llm || !this.llmChatThreadView) {
          return clear();
        }
        return this.llmChatThreadView.thread;
      },
    }),
    llmChatThreadView: one("ThreadView", {
      compute() {
        if (!this.is_chatting_with_llm || !this.thread) {
          return clear();
        }
        const llmChat = this.messaging.llmChat;
        if (!llmChat || !llmChat.activeThread || !llmChat.llmChatView) {
          return clear();
        }
        return {
          threadViewer: llmChat.llmChatView.threadViewer,
          messageListView: {},
          llmChatThreadHeaderView: {},
        };
      },
    }),
  },
  recordMethods: {
    /**
     * @override
     */
    onClickSendMessage(ev) {
      if (this.is_chatting_with_llm) {
        this.toggleLLMChat();
      }
      this._super(ev);
    },

    /**
     * @override
     */
    onClickLogNote(ev) {
      if (this.is_chatting_with_llm) {
        this.toggleLLMChat();
      }
      this._super(ev);
    },

    /**
     * @override
     */
    onClickScheduleActivity(ev) {
      if (this.is_chatting_with_llm) {
        this.toggleLLMChat();
      }
      this._super(ev);
    },

    /**
     * @override
     */
    onClickButtonAddAttachments(ev) {
      if (this.is_chatting_with_llm) {
        this.toggleLLMChat();
      }
      this._super(ev);
    },

    /**
     * @override
     */
    onClickButtonToggleAttachments(ev) {
      if (this.is_chatting_with_llm) {
        this.toggleLLMChat();
      }
      this._super(ev);
    },

    /**
     * Toggles LLM chat mode, initializing LLMChat and selecting/creating a thread.
     */
    async toggleLLMChat() {
      if (!this.thread) return;

      const messaging = this.messaging;
      const llmChat = messaging.llmChat;

      if (this.is_chatting_with_llm) {
        // Close: Clear active thread and context
        if (llmChat) {
          llmChat.update({
            activeThread: clear(),
            relatedThreadModel: clear(),
            relatedThreadId: clear(),
          });
        }
      } else {
        // Open: Find/create thread for this record
        try {
          if (!llmChat) {
            messaging.update({ llmChat: { isInitThreadHandled: false } });
          }

          // EnsureThread handles context update, change detection, and loading threads
          const thread = await messaging.llmChat.ensureThread({
            relatedThreadModel: this.thread.model,
            relatedThreadId: this.thread.id,
          });

          if (!thread) {
            throw new Error("Failed to ensure thread");
          }

          // Use unified API to open thread
          await thread.openLLMThread();
        } catch (error) {
          messaging.notify({
            title: "Failed to Start AI Chat",
            message: error.message || "An error occurred",
            type: "danger",
          });
        }
      }
    },
  },
});
