from pydantic import Field
from pydantic_schemaorg.AnatomicalStructure import AnatomicalStructure
from typing import List, Optional, Any, Union
from pydantic_schemaorg.MedicalCondition import MedicalCondition
from pydantic_schemaorg.MedicalTherapy import MedicalTherapy
from pydantic_schemaorg.MedicalEntity import MedicalEntity


class AnatomicalSystem(MedicalEntity):
    """An anatomical system is a group of anatomical structures that work together to perform"
     "a certain task. Anatomical systems, such as organ systems, are one organizing principle"
     "of anatomy, and can includes circulatory, digestive, endocrine, integumentary, immune,"
     "lymphatic, muscular, nervous, reproductive, respiratory, skeletal, urinary, vestibular,"
     "and other systems.

    See https://schema.org/AnatomicalSystem.

    """
    type_: str = Field("AnatomicalSystem", const=True, alias='@type')
    comprisedOf: Optional[Union[List[Union[AnatomicalStructure, 'AnatomicalSystem', str]], Union[AnatomicalStructure, 'AnatomicalSystem', str]]] = Field(
        None,
        description="Specifying something physically contained by something else. Typically used here"
     "for the underlying anatomical structures, such as organs, that comprise the anatomical"
     "system.",
    )
    relatedCondition: Optional[Union[List[Union[MedicalCondition, str]], Union[MedicalCondition, str]]] = Field(
        None,
        description="A medical condition associated with this anatomy.",
    )
    relatedStructure: Optional[Union[List[Union[AnatomicalStructure, str]], Union[AnatomicalStructure, str]]] = Field(
        None,
        description="Related anatomical structure(s) that are not part of the system but relate or connect"
     "to it, such as vascular bundles associated with an organ system.",
    )
    relatedTherapy: Optional[Union[List[Union[MedicalTherapy, str]], Union[MedicalTherapy, str]]] = Field(
        None,
        description="A medical therapy related to this anatomy.",
    )
    associatedPathophysiology: Optional[Union[List[str], str]] = Field(
        None,
        description="If applicable, a description of the pathophysiology associated with the anatomical"
     "system, including potential abnormal changes in the mechanical, physical, and biochemical"
     "functions of the system.",
    )
    

AnatomicalSystem.update_forward_refs()
