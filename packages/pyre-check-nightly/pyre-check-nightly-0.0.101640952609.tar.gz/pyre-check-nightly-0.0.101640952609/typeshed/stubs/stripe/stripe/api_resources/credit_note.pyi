from typing import Any

from stripe import api_requestor as api_requestor
from stripe.api_resources.abstract import (
    CreateableAPIResource as CreateableAPIResource,
    ListableAPIResource as ListableAPIResource,
    UpdateableAPIResource as UpdateableAPIResource,
    custom_method as custom_method,
)

class CreditNote(CreateableAPIResource, ListableAPIResource, UpdateableAPIResource):
    OBJECT_NAME: str
    def void_credit_note(self, idempotency_key: Any | None = ..., **params): ...
    @classmethod
    def preview(cls, api_key: Any | None = ..., stripe_version: Any | None = ..., stripe_account: Any | None = ..., **params): ...
