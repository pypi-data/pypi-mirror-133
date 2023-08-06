from pydantic import Field
from pydantic_schemaorg.USNonprofitType import USNonprofitType


class Nonprofit501c26(USNonprofitType):
    """Nonprofit501c26: Non-profit type referring to State-Sponsored Organizations Providing"
     "Health Coverage for High-Risk Individuals.

    See https://schema.org/Nonprofit501c26.

    """
    type_: str = Field("Nonprofit501c26", const=True, alias='@type')
    

Nonprofit501c26.update_forward_refs()
