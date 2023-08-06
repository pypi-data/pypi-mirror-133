from pydantic import Field
from decimal import Decimal
from pydantic_schemaorg.QuantitativeValue import QuantitativeValue
from typing import List, Optional, Union
from pydantic_schemaorg.ListItem import ListItem


class HowToItem(ListItem):
    """An item used as either a tool or supply when performing the instructions for how to to achieve"
     "a result.

    See https://schema.org/HowToItem.

    """
    type_: str = Field("HowToItem", const=True, alias='@type')
    requiredQuantity: Optional[Union[List[Union[Decimal, str, QuantitativeValue]], Union[Decimal, str, QuantitativeValue]]] = Field(
        None,
        description="The required quantity of the item(s).",
    )
    

HowToItem.update_forward_refs()
