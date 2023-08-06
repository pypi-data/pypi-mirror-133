from pydantic import Field
from pydantic_schemaorg.QuantitativeValue import QuantitativeValue
from typing import List, Optional, Union
from pydantic_schemaorg.MonetaryAmount import MonetaryAmount
from pydantic_schemaorg.Duration import Duration
from pydantic_schemaorg.CreativeWork import CreativeWork
from pydantic_schemaorg.HowToStep import HowToStep
from pydantic_schemaorg.HowToSection import HowToSection
from pydantic_schemaorg.HowToTool import HowToTool
from pydantic_schemaorg.ItemList import ItemList
from pydantic_schemaorg.HowToSupply import HowToSupply


class HowTo(CreativeWork):
    """Instructions that explain how to achieve a result by performing a sequence of steps.

    See https://schema.org/HowTo.

    """
    type_: str = Field("HowTo", const=True, alias='@type')
    yield_: Optional[Union[List[Union[str, QuantitativeValue]], Union[str, QuantitativeValue]]] = Field(
        None,alias="yield",
        description="The quantity that results by performing instructions. For example, a paper airplane,"
     "10 personalized candles.",
    )
    estimatedCost: Optional[Union[List[Union[str, MonetaryAmount]], Union[str, MonetaryAmount]]] = Field(
        None,
        description="The estimated cost of the supply or supplies consumed when performing instructions.",
    )
    prepTime: Optional[Union[List[Union[Duration, str]], Union[Duration, str]]] = Field(
        None,
        description="The length of time it takes to prepare the items to be used in instructions or a direction,"
     "in [ISO 8601 duration format](http://en.wikipedia.org/wiki/ISO_8601).",
    )
    step: Optional[Union[List[Union[str, CreativeWork, HowToStep, HowToSection]], Union[str, CreativeWork, HowToStep, HowToSection]]] = Field(
        None,
        description="A single step item (as HowToStep, text, document, video, etc.) or a HowToSection.",
    )
    totalTime: Optional[Union[List[Union[Duration, str]], Union[Duration, str]]] = Field(
        None,
        description="The total time required to perform instructions or a direction (including time to prepare"
     "the supplies), in [ISO 8601 duration format](http://en.wikipedia.org/wiki/ISO_8601).",
    )
    performTime: Optional[Union[List[Union[Duration, str]], Union[Duration, str]]] = Field(
        None,
        description="The length of time it takes to perform instructions or a direction (not including time"
     "to prepare the supplies), in [ISO 8601 duration format](http://en.wikipedia.org/wiki/ISO_8601).",
    )
    tool: Optional[Union[List[Union[str, HowToTool]], Union[str, HowToTool]]] = Field(
        None,
        description="A sub property of instrument. An object used (but not consumed) when performing instructions"
     "or a direction.",
    )
    steps: Optional[Union[List[Union[str, ItemList, CreativeWork]], Union[str, ItemList, CreativeWork]]] = Field(
        None,
        description="A single step item (as HowToStep, text, document, video, etc.) or a HowToSection (originally"
     "misnamed 'steps'; 'step' is preferred).",
    )
    supply: Optional[Union[List[Union[str, HowToSupply]], Union[str, HowToSupply]]] = Field(
        None,
        description="A sub-property of instrument. A supply consumed when performing instructions or a direction.",
    )
    

HowTo.update_forward_refs()
