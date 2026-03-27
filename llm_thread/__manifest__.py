{
    "name": "Easy AI Chat",
    "summary": "Simple AI Chat for Odoo",
    "description": """
Easy AI Chat for Odoo
=====================
A user-friendly module that brings AI-powered chat to your Odoo environment. Integrate with multiple AI providers, manage real-time conversations, and enhance workflows with multimodal support.

Key Features:
- Multiple AI Providers: OpenAI, Anthropic, Grok, Ollama, DeepSeek, and more
- Real-Time Chat: Instant AI conversations integrated with Odoo's mail system
- Multimodal Support: Go beyond text with advanced AI models
- Full Odoo Integration: Link chats to any Odoo record for context
- Tool Integration: Enable AI to execute custom tools and functions
- Function Calling: Select specific tools for each thread to enhance AI capabilities
- Optimized Performance: Efficient role-based message handling for better performance

Recent Updates:
- Refactored to use stored llm_role field for maximum efficiency
- Improved performance with direct field filtering and comparison
- Better integration with LLM base module's stored role field
- Enhanced database performance with proper indexing on llm_role field

Getting Started:
1. Install this module and the "LLM Integration Base" dependency
2. Configure your AI provider API keys
3. Fetch available models with one click
4. Start chatting from anywhere in Odoo

Use cases include customer support automation, data analysis, training assistance, custom AI workflows, and automated tool execution for your business.

Contact: support@apexive.com
    """,
    "category": "Productivity, Discuss",
    "version": "16.0.1.3.2",
    "depends": ["base", "mail", "web", "llm", "llm_tool"],
    "author": "Apexive Solutions LLC",
    "website": "https://github.com/apexive/odoo-llm",
    "external_dependencies": {"python": ["emoji", "markdown2"]},
    "data": [
        "security/llm_thread_security.xml",
        "security/ir.model.access.csv",
        "views/llm_thread_views.xml",
        "views/menu.xml",
    ],
    "assets": {
        "web.assets_backend": [
            # Client Actions (must be loaded before models that depend on them)
            "llm_thread/static/src/client_actions/open_chatter_action.js",
            # Models
            "llm_thread/static/src/models/main.js",
            "llm_thread/static/src/models/messaging.js",
            "llm_thread/static/src/models/llm_chat.js",
            "llm_thread/static/src/models/llm_chat_view.js",
            "llm_thread/static/src/models/thread.js",
            "llm_thread/static/src/models/composer.js",
            "llm_thread/static/src/models/composer_view.js",
            "llm_thread/static/src/models/llm_model.js",
            "llm_thread/static/src/models/llm_provider.js",
            "llm_thread/static/src/models/thread_view.js",
            "llm_thread/static/src/models/llm_chat_thread_header_view.js",
            "llm_thread/static/src/models/chatter.js",
            "llm_thread/static/src/models/llm_tool.js",
            "llm_thread/static/src/models/message.js",
            "llm_thread/static/src/models/message_action.js",
            "llm_thread/static/src/models/message_action_list.js",
            "llm_thread/static/src/models/message_action_view.js",
            "llm_thread/static/src/models/messaging_notification_handler.js",
            # Components
            "llm_thread/static/src/components/llm_chat/llm_chat.js",
            "llm_thread/static/src/components/llm_chat/llm_chat.xml",
            "llm_thread/static/src/components/llm_chat_thread_list/llm_chat_thread_list.js",
            "llm_thread/static/src/components/llm_chat_thread_list/llm_chat_thread_list.xml",
            "llm_thread/static/src/components/llm_chat_thread/llm_chat_thread.js",
            "llm_thread/static/src/components/llm_chat_thread/llm_chat_thread.scss",
            "llm_thread/static/src/components/llm_chat_thread/llm_chat_thread.xml",
            "llm_thread/static/src/components/llm_chat_container/llm_chat_container.js",
            "llm_thread/static/src/components/llm_chat_container/llm_chat_container.xml",
            "llm_thread/static/src/components/llm_chat_container/llm_chat_container.scss",
            "llm_thread/static/src/components/llm_chat_sidebar/llm_chat_sidebar.js",
            "llm_thread/static/src/components/llm_chat_sidebar/llm_chat_sidebar.xml",
            "llm_thread/static/src/components/llm_chat_sidebar/llm_chat_sidebar.scss",
            "llm_thread/static/src/components/llm_chat_composer/llm_chat_composer.js",
            "llm_thread/static/src/components/llm_chat_composer/llm_chat_composer.xml",
            "llm_thread/static/src/components/llm_chat_composer/llm_chat_composer.scss",
            "llm_thread/static/src/components/llm_chat_composer_text_input/llm_chat_composer_text_input.js",
            "llm_thread/static/src/components/llm_chat_composer_text_input/llm_chat_composer_text_input.xml",
            "llm_thread/static/src/components/llm_chat_composer_text_input/llm_chat_composer_text_input.scss",
            "llm_thread/static/src/components/llm_chat_message_list/llm_chat_message_list.js",
            "llm_thread/static/src/components/llm_chat_message_list/llm_chat_message_list.xml",
            "llm_thread/static/src/components/llm_chat_thread_header/llm_chat_thread_header.js",
            "llm_thread/static/src/components/llm_chat_thread_header/llm_chat_thread_header.xml",
            "llm_thread/static/src/components/llm_chat_thread_header/llm_chat_thread_header.scss",
            "llm_thread/static/src/components/llm_chatter_topbar/llm_chatter_topbar.xml",
            "llm_thread/static/src/components/llm_chatter_topbar/llm_chat_topbar.scss",
            "llm_thread/static/src/components/llm_chatter/llm_chatter.js",
            "llm_thread/static/src/components/llm_chatter/llm_chatter.xml",
            "llm_thread/static/src/components/message/message.xml",
            "llm_thread/static/src/components/message/message.scss",
            # Streaming indicator component
            "llm_thread/static/src/components/llm_streaming_indicator/llm_streaming_indicator.js",
            "llm_thread/static/src/components/llm_streaming_indicator/llm_streaming_indicator.xml",
            # LLMChatThreadRelatedRecord Component
            "llm_thread/static/src/components/llm_chat_thread_related_record/llm_chat_thread_related_record.js",
            "llm_thread/static/src/components/llm_chat_thread_related_record/llm_chat_thread_related_record.xml",
            "llm_thread/static/src/components/llm_chat_thread_related_record/llm_chat_thread_related_record.scss",
            # Client Actions
            "llm_thread/static/src/llm_chat_client_action.js",
            # Styles
            (
                "after",
                "web/static/src/scss/pre_variables.scss",
                "llm_thread/static/src/components/llm_chat/llm_chat.scss",
            ),
            (
                "after",
                "web/static/src/scss/pre_variables.scss",
                "llm_thread/static/src/components/llm_chat_thread_list/llm_chat_thread_list.scss",
            ),
        ],
    },
    "images": [
        "static/description/banner.jpeg",
    ],
    "license": "LGPL-3",
    "installable": True,
    "application": True,
    "auto_install": False,
}
