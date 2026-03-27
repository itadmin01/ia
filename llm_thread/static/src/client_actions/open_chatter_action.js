/** @odoo-module **/

import { registry } from "@web/core/registry";

const SESSION_STORAGE_KEY = "llm_pending_open_in_chatter";

/**
 * Client action to open AI chat in a record's chatter.
 * This bypasses the unreliable bus notification system by:
 * 1. Storing pending state in sessionStorage (survives navigation)
 * 2. Navigating to the record's form view
 * 3. The Chatter model checks sessionStorage on update and opens AI chat
 *
 * @param {Object} env - The component environment
 * @param {Object} action - The action definition
 * @param {Object} action.params - Action parameters
 * @param {Number} action.params.thread_id - ID of the llm.thread to open
 * @param {String} action.params.model - Model name of the related record
 * @param {Number} action.params.res_id - ID of the related record
 */
async function openChatterAction(env, action) {
  const { thread_id, model, res_id } = action.params || {};

  if (!thread_id || !model || !res_id) {
    console.error(
      "[LLM] open_chatter_action: Missing required params",
      action.params
    );
    return;
  }

  // Store pending state in sessionStorage (survives page navigation)
  const pendingState = {
    threadId: thread_id,
    model: model,
    resId: res_id,
    autoGenerate: true,
    timestamp: Date.now(),
  };

  try {
    sessionStorage.setItem(SESSION_STORAGE_KEY, JSON.stringify(pendingState));
  } catch (e) {
    console.error("[LLM] Failed to store pending state in sessionStorage:", e);
  }

  // Navigate to the record's form view
  return env.services.action.doAction({
    type: "ir.actions.act_window",
    res_model: model,
    res_id: res_id,
    views: [[false, "form"]],
    target: "current",
  });
}

// Register the client action
registry.category("actions").add("llm_open_chatter", openChatterAction);

/**
 * Get pending open in chatter state from sessionStorage.
 *
 * @returns {Object|null} The pending state or null if not found/expired
 */
export function getPendingOpenInChatter() {
  try {
    const data = sessionStorage.getItem(SESSION_STORAGE_KEY);
    if (!data) return null;

    const state = JSON.parse(data);

    // Expire after 30 seconds to prevent stale state
    if (Date.now() - state.timestamp > 30000) {
      sessionStorage.removeItem(SESSION_STORAGE_KEY);
      return null;
    }

    return state;
  } catch (e) {
    console.error("[LLM] Failed to get pending state from sessionStorage:", e);
    return null;
  }
}

export function consumePendingOpenInChatter(model, resId) {
  const pending = getPendingOpenInChatter();
  if (!pending) return null;

  // Only consume if it matches the current record
  if (pending.model === model && pending.resId === resId) {
    sessionStorage.removeItem(SESSION_STORAGE_KEY);
    return pending;
  }

  return null;
}

export function clearPendingOpenInChatter() {
  sessionStorage.removeItem(SESSION_STORAGE_KEY);
}
