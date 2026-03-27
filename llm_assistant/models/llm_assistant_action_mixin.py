import logging

from odoo import models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class LLMAssistantActionMixin(models.AbstractModel):
    """
    Mixin to add AI assistant action functionality to any model.
    Provides generic methods to open LLM chat with specific assistants.

    Usage:
        class MyModel(models.Model):
            _inherit = ['my.model', 'llm.assistant.action.mixin']

            def action_my_ai_button(self):
                # Simple usage
                return self.action_open_llm_assistant('my_assistant_code')

            def action_my_ai_button_with_logic(self):
                # With custom logic before/after
                self.ensure_some_field_is_set()
                result = self.action_open_llm_assistant('my_assistant_code')
                self.log_ai_usage()
                return result
    """

    _name = "llm.assistant.action.mixin"
    _description = "LLM Assistant Action Mixin"

    def action_open_llm_assistant(
        self, assistant_code=None, force_new_thread=False, **kwargs
    ):
        """
        Generic method to open AI assistant for current record.
        Creates/finds thread, sets assistant, and returns client action to open chat.

        Args:
            assistant_code: Code of the assistant to use (e.g., 'invoice_analyzer')
                           If not provided, tries to get from context
            force_new_thread: If True, always create new thread (ignore existing)
            **kwargs: Additional parameters for extensibility in overrides

        Returns:
            dict: Client action to navigate to record and open AI chat

        Raises:
            UserError: If no provider/model found or assistant code missing

        Usage:
            Simple usage:
                def action_process_with_ai(self):
                    return self.action_open_llm_assistant('my_assistant')

            With custom logic before/after:
                def action_process_with_ai(self):
                    self.ensure_ready_for_processing()
                    result = self.action_open_llm_assistant('my_assistant')
                    self.log_ai_usage()
                    return result

            Override with custom parameters:
                def action_open_llm_assistant(self, assistant_code=None, force_new_thread=False,
                                             custom_field=None, **kwargs):
                    if custom_field:
                        self.process_custom_field(custom_field)
                    return super().action_open_llm_assistant(
                        assistant_code=assistant_code,
                        force_new_thread=force_new_thread,
                        **kwargs
                    )
        """
        self.ensure_one()

        # Get assistant code from parameter or context
        if not assistant_code:
            assistant_code = self.env.context.get("assistant_code")

        if not assistant_code:
            raise UserError(
                "No assistant code provided. Please specify assistant_code parameter or context."
            )

        # Find existing thread or create new one
        thread = self._find_or_create_llm_thread(force_new=force_new_thread)

        # Find and set assistant
        self._set_assistant_on_thread(thread, assistant_code)

        # Return client action to open AI chat in chatter
        # This bypasses the bus notification system which can be unreliable on cloud deployments
        return {
            "type": "ir.actions.client",
            "tag": "llm_open_chatter",
            "params": {
                "thread_id": thread.id,
                "model": self._name,
                "res_id": self.id,
            },
        }

    def _find_or_create_llm_thread(self, force_new=False):
        """
        Find existing thread for this record or create a new one.

        Args:
            force_new: If True, always create new thread (ignore existing)

        Returns:
            llm.thread: The thread record
        """
        if not force_new:
            thread = self.env["llm.thread"].search(
                [("model", "=", self._name), ("res_id", "=", self.id)], limit=1
            )
            if thread:
                return thread

        # Find default chat model or fallback to first available
        default_model = self.env["llm.model"].search(
            [
                ("model_use", "in", ["chat", "multimodal"]),
                ("default", "=", True),
                ("active", "=", True),
            ],
            limit=1,
        )

        if not default_model:
            # Fallback: Get first provider and its first chat model
            provider = self.env["llm.provider"].search([("active", "=", True)], limit=1)
            if not provider:
                raise UserError(
                    "No active LLM provider found. Please configure a provider first."
                )

            default_model = self.env["llm.model"].search(
                [
                    ("provider_id", "=", provider.id),
                    ("model_use", "in", ["chat", "multimodal"]),
                    ("active", "=", True),
                ],
                limit=1,
            )

        if not default_model:
            raise UserError(
                "No active chat model found. Please configure a model first."
            )

        # Create new thread
        thread = self.env["llm.thread"].create(
            {
                "name": f"AI Chat - {self._name} #{self.id}",
                "model": self._name,
                "res_id": self.id,
                "provider_id": default_model.provider_id.id,
                "model_id": default_model.id,
            }
        )

        return thread

    def _set_assistant_on_thread(self, thread, assistant_code):
        """
        Find assistant by code and set it on the thread.

        Args:
            thread: llm.thread record
            assistant_code: Code of the assistant to find
        """
        assistant = self.env["llm.assistant"].search(
            [("code", "=", assistant_code)], limit=1
        )

        if not assistant:
            raise UserError(f"Assistant with code '{assistant_code}' not found!")

        if not thread.assistant_id:
            thread.set_assistant(assistant.id)
