from typing import Any

from .base import GrantTypeBase as GrantTypeBase

log: Any

class ImplicitGrant(GrantTypeBase):
    response_types: Any
    grant_allows_refresh_token: bool
    def create_authorization_response(self, request, token_handler): ...
    def create_token_response(self, request, token_handler): ...
    def validate_authorization_request(self, request): ...
    def validate_token_request(self, request): ...
