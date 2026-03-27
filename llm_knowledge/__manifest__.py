{
    "name": "LLM Knowledge",
    "summary": "Retrieval Augmented Generation for LLM with Document Resource Management",
    "description": """
        Implements Retrieval Augmented Generation (chunking and embedding) for the LLM module.
        
        This module consolidates the functionality of both llm_resource and llm_knowledge modules,
        providing a comprehensive solution for document resource management and RAG processing.

        Features:
        - Base document resource model
        - Resource retrieval interfaces (HTTP, etc.)
        - Resource parsing interfaces (PDF, HTML, etc.)
        - Document collections for RAG
        - Document chunking pipeline
        - Document embedding integration
        - Vector search using various stores (pgvector, chroma, qdrant)
        - PDF processing and text extraction
    """,
    "category": "Technical",
    "version": "16.0.1.1.0",
    "depends": ["llm", "llm_store"],
    "external_dependencies": {
        "python": ["requests", "markdownify", "PyMuPDF", "numpy"],
    },
    "author": "Apexive Solutions LLC",
    "website": "https://github.com/apexive/odoo-llm",
    "data": [
        # Security must come first
        "security/ir.model.access.csv",
        # Data / Actions
        "data/server_actions.xml",
        # Views for models
        "views/llm_resource_views.xml",  # Consolidated llm.resource views
        "views/llm_knowledge_collection_views.xml",
        "views/llm_knowledge_chunk_views.xml",
        # Wizard Views
        "wizards/create_rag_resource_wizard_views.xml",
        "wizards/upload_resource_wizard_views.xml",
        # Menus must come last
        "views/llm_resource_menu.xml",
        "views/menu.xml",
    ],
    "images": [
        "static/description/banner.jpeg",
    ],
    "license": "LGPL-3",
    "installable": True,
    "application": False,
    "auto_install": False,
}
