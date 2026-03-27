"""
MCP Protocol Types - Custom implementation for Python 3.9+ compatibility.

This module provides type definitions that mirror the official mcp.types module,
allowing the llm_mcp_server to work without the mcp package dependency
(which requires Python 3.10+).

All types are compliant with the MCP specification.
Based on: https://github.com/modelcontextprotocol/python-sdk/blob/main/src/mcp/types.py
"""
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, ConfigDict, Field

# JSON-RPC 2.0 Error Codes (standard spec)
PARSE_ERROR = -32700
INVALID_REQUEST = -32600
METHOD_NOT_FOUND = -32601
INVALID_PARAMS = -32602
INTERNAL_ERROR = -32603


# Content Types
class TextContent(BaseModel):
    """Text content in tool results."""

    type: str = "text"
    text: str
    annotations: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(extra="allow")


# Tool Types
class ToolAnnotations(BaseModel):
    """
    Additional properties describing a Tool to clients.

    NOTE: all properties in ToolAnnotations are **hints**.
    They are not guaranteed to provide a faithful description of
    tool behavior (including descriptive properties like `title`).
    """

    title: Optional[str] = None
    readOnlyHint: Optional[bool] = None
    destructiveHint: Optional[bool] = None
    idempotentHint: Optional[bool] = None
    openWorldHint: Optional[bool] = None

    model_config = ConfigDict(extra="allow")


class Tool(BaseModel):
    """Definition for a tool the client can call."""

    name: str
    title: Optional[str] = None
    description: Optional[str] = None
    inputSchema: Dict[str, Any] = Field(default_factory=dict)
    outputSchema: Optional[Dict[str, Any]] = None
    annotations: Optional[ToolAnnotations] = None

    model_config = ConfigDict(extra="allow")


class ListToolsResult(BaseModel):
    """The server's response to a tools/list request from the client."""

    tools: List[Tool]
    nextCursor: Optional[str] = None

    model_config = ConfigDict(extra="allow")


class CallToolResult(BaseModel):
    """The server's response to a tool call."""

    content: List[TextContent]
    structuredContent: Optional[Dict[str, Any]] = None
    isError: bool = False

    model_config = ConfigDict(extra="allow")


# Server Types
class Implementation(BaseModel):
    """Describes the name and version of an MCP implementation."""

    name: str
    version: str
    title: Optional[str] = None

    model_config = ConfigDict(extra="allow")


class ToolsCapability(BaseModel):
    """Capability for tools operations."""

    listChanged: Optional[bool] = None

    model_config = ConfigDict(extra="allow")


class ServerCapabilities(BaseModel):
    """Capabilities that a server may support."""

    experimental: Optional[Dict[str, Dict[str, Any]]] = None
    logging: Optional[Dict[str, Any]] = None
    prompts: Optional[Dict[str, Any]] = None
    resources: Optional[Dict[str, Any]] = None
    tools: Optional[ToolsCapability] = None
    completions: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(extra="allow")


class InitializeResult(BaseModel):
    """After receiving an initialize request from the client, the server sends this."""

    protocolVersion: Union[str, int]
    capabilities: ServerCapabilities
    serverInfo: Implementation
    instructions: Optional[str] = None

    model_config = ConfigDict(extra="allow")
