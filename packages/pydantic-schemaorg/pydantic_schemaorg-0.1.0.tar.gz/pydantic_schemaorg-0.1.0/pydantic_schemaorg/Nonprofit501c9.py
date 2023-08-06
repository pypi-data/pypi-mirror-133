from pydantic import Field
from pydantic_schemaorg.USNonprofitType import USNonprofitType


class Nonprofit501c9(USNonprofitType):
    """Nonprofit501c9: Non-profit type referring to Voluntary Employee Beneficiary Associations.

    See https://schema.org/Nonprofit501c9.

    """
    type_: str = Field("Nonprofit501c9", const=True, alias='@type')
    

Nonprofit501c9.update_forward_refs()
