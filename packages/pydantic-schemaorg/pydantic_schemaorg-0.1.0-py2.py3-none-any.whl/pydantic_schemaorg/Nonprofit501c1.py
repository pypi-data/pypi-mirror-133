from pydantic import Field
from pydantic_schemaorg.USNonprofitType import USNonprofitType


class Nonprofit501c1(USNonprofitType):
    """Nonprofit501c1: Non-profit type referring to Corporations Organized Under Act of"
     "Congress, including Federal Credit Unions and National Farm Loan Associations.

    See https://schema.org/Nonprofit501c1.

    """
    type_: str = Field("Nonprofit501c1", const=True, alias='@type')
    

Nonprofit501c1.update_forward_refs()
