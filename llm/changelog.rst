16.0.1.4.2 (2026-01-07)
~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] LLM Manager role now auto-implied for admin users (base.group_system)
* [IMP] Removed manual user assignment in favor of group implication

16.0.1.4.1 (2025-11-17)
~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Fixed wizard_id not being set on llm.fetch.models.line records
* [IMP] Refactored model fetching: moved logic from wizard default_get() to provider action_fetch_models()
* [IMP] Moved _determine_model_use() from wizard to provider for better extensibility
* [REM] Removed wizard write() override workaround
* [ADD] Comprehensive docstrings with extension pattern examples
* [ADD] Documented standard capability names and priority order

16.0.1.1.0 (2025-03-06)
~~~~~~~~~~~~~~~~~~~~~~~

* [ADD] Tool support framework in base LLM models
* [IMP] Enhanced provider interface to support tool execution
* [IMP] Updated model handling for function calling capabilities

16.0.1.0.0 (2025-01-02)
~~~~~~~~~~~~~~~~~~~~~~~

* [INIT] Initial release of the module
