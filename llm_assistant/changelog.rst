16.0.1.5.3 (2026-01-05)
~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Prevent duplicate get_prepend_messages() calls in generate_messages()

16.0.1.5.2 (2025-12-02)
~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Changed action_open_llm_assistant to return client action instead of bus notification
* [IMP] Improved reliability of AI chat opening on cloud deployments

16.0.1.5.1 (2025-11-21)
~~~~~~~~~~~~~~~~~~~~~~~

* [ADD] Added llm.assistant.action.mixin for reusable assistant action methods
* [IMP] Enhanced action_open_llm_assistant with force_new_thread parameter
* [IMP] Improved assistant-thread integration for better UX
* [IMP] Extended llm.thread model integration in assistants

16.0.1.0.1 (2025-04-04)
~~~~~~~~~~~~~~~~~~~~~~~

* [ADD] Added Assistant Creator assistant data record using OpenAI GPT-4o model
* [ADD] Created data directory structure for llm_assistant module

16.0.1.0.0 (2025-03-01)
~~~~~~~~~~~~~~~~~~~~~~~

* [ADD] Initial release of the LLM Assistant module
