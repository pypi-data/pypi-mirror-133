from pydantic import Field
from pydantic_schemaorg.MedicalCondition import MedicalCondition
from typing import List, Optional, Union
from pydantic_schemaorg.Drug import Drug
from pydantic_schemaorg.MedicalAudience import MedicalAudience
from pydantic_schemaorg.Person import Person


class Patient(MedicalAudience, Person):
    """A patient is any person recipient of health care services.

    See https://schema.org/Patient.

    """
    type_: str = Field("Patient", const=True, alias='@type')
    diagnosis: Optional[Union[List[Union[MedicalCondition, str]], Union[MedicalCondition, str]]] = Field(
        None,
        description="One or more alternative conditions considered in the differential diagnosis process"
     "as output of a diagnosis process.",
    )
    healthCondition: Optional[Union[List[Union[MedicalCondition, str]], Union[MedicalCondition, str]]] = Field(
        None,
        description="Specifying the health condition(s) of a patient, medical study, or other target audience.",
    )
    drug: Optional[Union[List[Union[Drug, str]], Union[Drug, str]]] = Field(
        None,
        description="Specifying a drug or medicine used in a medication procedure.",
    )
    

Patient.update_forward_refs()
