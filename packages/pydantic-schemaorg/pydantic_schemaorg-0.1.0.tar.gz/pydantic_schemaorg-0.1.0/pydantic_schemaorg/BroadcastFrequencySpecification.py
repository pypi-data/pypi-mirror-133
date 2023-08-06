from pydantic import Field
from pydantic_schemaorg.QualitativeValue import QualitativeValue
from typing import List, Optional, Any, Union
from decimal import Decimal
from pydantic_schemaorg.QuantitativeValue import QuantitativeValue
from pydantic_schemaorg.Intangible import Intangible


class BroadcastFrequencySpecification(Intangible):
    """The frequency in MHz and the modulation used for a particular BroadcastService.

    See https://schema.org/BroadcastFrequencySpecification.

    """
    type_: str = Field("BroadcastFrequencySpecification", const=True, alias='@type')
    broadcastSignalModulation: Optional[Union[List[Union[str, QualitativeValue]], Union[str, QualitativeValue]]] = Field(
        None,
        description="The modulation (e.g. FM, AM, etc) used by a particular broadcast service.",
    )
    broadcastFrequencyValue: Optional[Union[List[Union[Decimal, QuantitativeValue, str]], Union[Decimal, QuantitativeValue, str]]] = Field(
        None,
        description="The frequency in MHz for a particular broadcast.",
    )
    broadcastSubChannel: Optional[Union[List[str], str]] = Field(
        None,
        description="The subchannel used for the broadcast.",
    )
    

BroadcastFrequencySpecification.update_forward_refs()
