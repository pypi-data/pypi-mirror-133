from pydantic import Field
from pydantic_schemaorg.ReturnFeesEnumeration import ReturnFeesEnumeration


class ReturnShippingFees(ReturnFeesEnumeration):
    """Specifies that the customer must pay the return shipping costs when returning a product

    See https://schema.org/ReturnShippingFees.

    """
    type_: str = Field("ReturnShippingFees", const=True, alias='@type')
    

ReturnShippingFees.update_forward_refs()
