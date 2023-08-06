from pydantic import Field
from pydantic_schemaorg.AnatomicalStructure import AnatomicalStructure
from typing import List, Optional, Union
from pydantic_schemaorg.Vessel import Vessel


class Artery(Vessel):
    """A type of blood vessel that specifically carries blood away from the heart.

    See https://schema.org/Artery.

    """
    type_: str = Field("Artery", const=True, alias='@type')
    supplyTo: Optional[Union[List[Union[AnatomicalStructure, str]], Union[AnatomicalStructure, str]]] = Field(
        None,
        description="The area to which the artery supplies blood.",
    )
    arterialBranch: Optional[Union[List[Union[AnatomicalStructure, str]], Union[AnatomicalStructure, str]]] = Field(
        None,
        description="The branches that comprise the arterial structure.",
    )
    

Artery.update_forward_refs()
