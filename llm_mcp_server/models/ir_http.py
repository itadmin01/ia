"""
Odoo 16.0 Backport: Bearer Token Authentication

This module backports the _auth_method_bearer from Odoo 18.0 to Odoo 16.0,
enabling Bearer token authentication for API endpoints.

Original implementation from Odoo 18.0:
odoo/addons/base/models/ir_http.py lines 204-243
"""

import logging
import re

import werkzeug.exceptions

from odoo import models
from odoo.exceptions import AccessDenied
from odoo.http import request

_logger = logging.getLogger(__name__)


class IrHttp(models.AbstractModel):
    _inherit = "ir.http"

    @classmethod
    def _auth_method_bearer(cls):
        """
        Bearer token authentication method for Odoo 16.0.

        This method authenticates requests using Bearer tokens from the Authorization header.
        It's a backport of the Odoo 18.0 implementation adapted for Odoo 16.0 compatibility.

        Authentication Flow:
        1. Extract Bearer token from Authorization header
        2. Validate token against res.users.apikeys
        3. Update request environment with authenticated user
        4. Fallback to session-based authentication if no token provided

        Raises:
            werkzeug.exceptions.Unauthorized: If authentication fails
            AccessDenied: If session user doesn't match API key user or missing Sec-headers
        """
        headers = request.httprequest.headers

        def get_http_authorization_bearer_token():
            """
            Extract Bearer token from Authorization header.

            Returns:
                str: The bearer token if found, None otherwise
            """
            # werkzeug<2.3 doesn't expose `authorization.token` (for bearer authentication)
            # check header directly
            header = headers.get("Authorization")
            if header:
                # Use case-insensitive regex to match "Bearer <token>"
                match = re.match(r"^bearer\s+(.+)$", header, re.IGNORECASE)
                if match:
                    return match.group(1)
            return None

        def check_sec_headers():
            """
            Protection against CSRF attacks.

            Modern browsers automatically add Sec- headers that we can check to
            protect against CSRF attacks.

            See: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Sec-Fetch-User

            Returns:
                bool: True if all required security headers are valid, False otherwise
            """
            return (
                headers.get("Sec-Fetch-Dest") == "document"
                and headers.get("Sec-Fetch-Mode") == "navigate"
                and headers.get("Sec-Fetch-Site") in ("none", "same-origin")
                and headers.get("Sec-Fetch-User") == "?1"
            )

        # Try to authenticate with Bearer token first
        token = get_http_authorization_bearer_token()
        if token:
            # 'rpc' scope does not really exist, we basically require a global key (scope NULL)
            uid = request.env["res.users.apikeys"]._check_credentials(
                scope="rpc", key=token
            )
            if not uid:
                # Odoo 16.0 doesn't have werkzeug.datastructures.WWWAuthenticate
                # Use simpler approach compatible with werkzeug 0.16.x
                raise werkzeug.exceptions.Unauthorized(
                    description="Invalid apikey",
                    www_authenticate='Bearer realm="Odoo API"',
                )
            if request.env.uid and request.env.uid != uid:
                raise AccessDenied("Session user does not match the used apikey")
            request.update_env(user=uid)
        elif not request.env.uid:
            # No bearer token and no session user
            raise werkzeug.exceptions.Unauthorized(
                description='User not authenticated, use the "Authorization" header',
                www_authenticate='Bearer realm="Odoo API"',
            )
        elif not check_sec_headers():
            # Session user exists but no bearer token and missing Sec-headers
            # This protects against CSRF attacks in interactive (browser) usage
            raise AccessDenied(
                'Missing "Authorization" or Sec-headers for interactive usage'
            )

        # If we have a session user and proper Sec-headers, validate the session
        cls._auth_method_user()
