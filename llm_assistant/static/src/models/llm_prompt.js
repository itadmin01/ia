/** @odoo-module **/

import { attr, many } from "@mail/model/model_field";
import { registerModel } from "@mail/model/model_core";

registerModel({
  name: "LLMPrompt",
  fields: {
    id: attr({
      identifying: true,
    }),
    name: attr(),
    inputSchemaJson: attr({
      default: "{}",
    }),
    /**
     * Assistants using this prompt
     */
    assistants: many("LLMAssistant", {
      inverse: "llmPrompt",
    }),
  },
});
