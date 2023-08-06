from pydantic import StrictBool, Field
from typing import List, Optional, Union
from pydantic_schemaorg.Intangible import Intangible


class HealthPlanNetwork(Intangible):
    """A US-style health insurance plan network.

    See https://schema.org/HealthPlanNetwork.

    """
    type_: str = Field("HealthPlanNetwork", const=True, alias='@type')
    healthPlanNetworkTier: Optional[Union[List[str], str]] = Field(
        None,
        description="The tier(s) for this network.",
    )
    healthPlanNetworkId: Optional[Union[List[str], str]] = Field(
        None,
        description="Name or unique ID of network. (Networks are often reused across different insurance"
     "plans).",
    )
    healthPlanCostSharing: Optional[Union[List[Union[StrictBool, str]], Union[StrictBool, str]]] = Field(
        None,
        description="Whether The costs to the patient for services under this network or formulary.",
    )
    

HealthPlanNetwork.update_forward_refs()
