/** @odoo-module **/
import { attr, one } from "@mail/model/model_field";
import { clear } from "@mail/model/model_field_command";
import { registerModel } from "@mail/model/model_core";

registerModel({
  name: "LLMChatView",
  lifecycleHooks: {
    _created() {
      this._updateLayoutState();
    },
  },
  recordMethods: {
    /**
     * Update layout state (isSmall, visibility, collapse)
     * Called on creation and when context changes
     * @private
     */
    _updateLayoutState() {
      const isSmall = this._isSmall();
      const isChatterMode = Boolean(this.llmChat.isChatterMode);

      this.update({
        // Set isSmall as stored value (not computed)
        isSmall: isSmall,
        // Thread list visibility:
        // - Desktop (!isSmall): always visible
        // - Mobile/Aside (isSmall): hidden by default, toggled by hamburger
        isThreadListVisible: !isSmall,
        // Desktop: collapse state (default collapsed in chatter, expanded standalone)
        isSidebarCollapsed: isChatterMode,
      });
    },

    /**
     * @private
     */
    _onLLMChatActiveThreadChanged() {
      this.env.services.router.pushState({
        action: this.llmChat.llmChatView.actionId,
        active_id: this.llmChat.activeId,
      });
    },

    /**
     * React to context changes (chatter mode changes)
     * @private
     */
    _onContextChanged() {
      this._updateLayoutState();
    },

    /**
     * Check if should use mobile/small layout
     * - On actual mobile devices (window < 768px)
     * - In chatter positioned on the side (narrow panel)
     *
     * @returns {Boolean}
     * @private
     */
    _isSmall() {
      const isActuallySmall = this.messaging.device.isSmall;

      // Only check chatter aside mode if we're actually in chatter mode
      // Otherwise, a background chatter can incorrectly trigger mobile layout
      let isChatterAside = false;
      if (this.llmChat.isChatterMode) {
        // When hasMessageListScrollAdjust is true, the chatter is on the form view's side
        const chatters = this.messaging.models.Chatter.all();
        isChatterAside = chatters.some(
          (chatter) => chatter.hasMessageListScrollAdjust
        );
      }

      return isActuallySmall || isChatterAside;
    },

    /**
     * Toggle sidebar collapsed state (desktop only)
     */
    toggleSidebar() {
      this.update({ isSidebarCollapsed: !this.isSidebarCollapsed });
    },
  },
  fields: {
    actionId: attr(),
    isThreadListVisible: attr({
      default: true,
    }),
    isSidebarCollapsed: attr({
      default: false,
    }),
    isSmall: attr({
      default: false,
    }),
    llmChat: one("LLMChat", {
      inverse: "llmChatView",
      required: true,
    }),
    isActive: attr({
      compute() {
        return Boolean(this.llmChat);
      },
    }),
    thread: one("Thread", {
      compute() {
        return this.llmChat.activeThread;
      },
    }),
    threadViewer: one("ThreadViewer", {
      compute() {
        if (!this.llmChat.activeThread) {
          return clear();
        }
        return {
          hasThreadView: true,
          thread: this.llmChat.activeThread,
          threadCache: this.llmChat.threadCache,
        };
      },
    }),
    threadView: one("ThreadView", {
      compute() {
        if (!this.threadViewer) {
          return clear();
        }
        return {
          threadViewer: this.threadViewer,
          messageListView: {},
          llmChatThreadHeaderView: {},
        };
      },
    }),
    composer: one("Composer", {
      compute() {
        if (!this.threadViewer) {
          return clear();
        }
        return { thread: this.threadViewer.thread };
      },
    }),
  },
  onChanges: [
    {
      dependencies: ["llmChat.activeThread"],
      methodName: "_onLLMChatActiveThreadChanged",
    },
    {
      dependencies: ["llmChat.isChatterMode", "llmChat.relatedThreadModel", "llmChat.relatedThreadId"],
      methodName: "_onContextChanged",
    },
  ],
});
