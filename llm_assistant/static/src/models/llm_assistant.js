/** @odoo-module **/

import { attr, many, one } from "@mail/model/model_field";
import { registerModel } from "@mail/model/model_core";

/**
 * Model for LLM Assistant
 */
registerModel({
  name: "LLMAssistant",
  fields: {
    id: attr({
      identifying: true,
    }),
    name: attr(),
    /**
     * Threads associated with this assistant
     */
    threads: many("Thread", {
      inverse: "llmAssistant",
    }),
    /**
     * The prompt associated with this assistant
     */
    llmPrompt: one("LLMPrompt", {
      inverse: "assistants",
    }),
    /**
     * Prompt ID (used for loading from server)
     */
    promptId: attr(),
    defaultValues: attr(),
    evaluatedDefaultValues: attr(),
  },
});
