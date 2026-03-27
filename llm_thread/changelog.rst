16.0.1.3.2 (2025-12-02)
~~~~~~~~~~~~~~~~~~~~~~~

* [ADD] Added client action (llm_open_chatter) to open AI chat in record's chatter
* [IMP] Replaced unreliable bus notification with client action pattern for cloud deployments
* [ADD] Added sessionStorage-based pending state for cross-navigation communication
* [ADD] Added checkPendingAIChatOpen method to Chatter model for auto-opening AI chat

16.0.1.3.1 (2025-11-21)
~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Fixed chatter aside detection for Odoo 16.0 using hasMessageListScrollAdjust
* [FIX] Fixed context leakage between chatter and standalone LLM chat modes
* [FIX] Fixed layout reactivity when switching between chatter and standalone contexts
* [IMP] Unified thread naming with backend-generated names using record display_name
* [IMP] Added unique ID suffix to standalone thread names (e.g., "New Chat #123")
* [IMP] Unified isSmall detection across all components using llmChatView.isSmall
* [IMP] Made layout state reactive with _onContextChanged() handler
* [REMOVE] Removed hardcoded name generation from frontend components
* [REMOVE] Removed duplicate isSmall getters from individual components

16.0.1.3.0 (2025-01-04)
~~~~~~~~~~~~~~~~~~~~~~~

* [BREAKING] Refactored to use stored llm_role field for maximum efficiency
* [PERF] Added computed stored llm_role field for instant role lookups
* [PERF] Optimized message queries using direct field filtering instead of batch methods
* [PERF] Improved frontend performance with direct field comparison instead of computed properties
* [PERF] Enhanced database performance with proper indexing on llm_role field
* [IMP] Simplified message_post API with llm_role parameter instead of subtype_xmlid
* [IMP] Updated JavaScript models to use direct field access for role checking
* [IMP] Streamlined message template rendering with direct field conditionals
* [IMP] Simplified message action visibility logic with direct role comparison
* [MIGRATION] Added migration script to compute llm_role for existing messages
* [REMOVE] Removed complex role checking computed properties (replaced with direct field access)
* [OPT] Leveraged database indexing for improved query performance on llm_role field

16.0.1.2.0 (2025-01-04)
~~~~~~~~~~~~~~~~~~~~~~~

* [BREAKING] Refactored to use LLM base module message subtypes instead of separate llm_mail_message_subtypes module
* [MIGRATION] Added migration script to convert existing message subtypes to new format
* [REMOVE] Removed dependency on llm_mail_message_subtypes module
* [IMP] Simplified subtype handling by using direct XML IDs from llm base module
* [OPT] Optimized XML ID resolution using _xmlid_to_res_id instead of env.ref

16.0.1.1.1 (2025-04-09)
~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Update method names to be consistent

16.0.1.1.0 (2025-03-06)
~~~~~~~~~~~~~~~~~~~~~~~

* [ADD] Tool integration in chat interface - Support for displaying tool executions and results
* [IMP] Enhanced UI for tool messages with cog icon and argument display
* [IMP] Updated chat components to handle tool-related message types

16.0.1.0.0 (2025-01-02)
~~~~~~~~~~~~~~~~~~~~~~~

* [INIT] Initial release of the module
