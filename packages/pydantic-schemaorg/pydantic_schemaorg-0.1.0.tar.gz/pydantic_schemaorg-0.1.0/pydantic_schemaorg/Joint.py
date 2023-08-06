from pydantic import Field
from pydantic_schemaorg.MedicalEntity import MedicalEntity
from typing import List, Optional, Any, Union
from pydantic_schemaorg.AnatomicalStructure import AnatomicalStructure


class Joint(AnatomicalStructure):
    """The anatomical location at which two or more bones make contact.

    See https://schema.org/Joint.

    """
    type_: str = Field("Joint", const=True, alias='@type')
    functionalClass: Optional[Union[List[Union[str, MedicalEntity]], Union[str, MedicalEntity]]] = Field(
        None,
        description="The degree of mobility the joint allows.",
    )
    structuralClass: Optional[Union[List[str], str]] = Field(
        None,
        description="The name given to how bone physically connects to each other.",
    )
    biomechnicalClass: Optional[Union[List[str], str]] = Field(
        None,
        description="The biomechanical properties of the bone.",
    )
    

Joint.update_forward_refs()
