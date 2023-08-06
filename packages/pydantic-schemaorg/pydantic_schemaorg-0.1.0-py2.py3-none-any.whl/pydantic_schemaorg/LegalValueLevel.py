from pydantic import Field
from pydantic_schemaorg.Enumeration import Enumeration


class LegalValueLevel(Enumeration):
    """A list of possible levels for the legal validity of a legislation.

    See https://schema.org/LegalValueLevel.

    """
    type_: str = Field("LegalValueLevel", const=True, alias='@type')
    

LegalValueLevel.update_forward_refs()
