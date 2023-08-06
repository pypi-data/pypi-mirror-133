from pydantic import Field
from pydantic_schemaorg.MedicalBusiness import MedicalBusiness
from pydantic_schemaorg.MedicalSpecialty import MedicalSpecialty


class Psychiatric(MedicalBusiness, MedicalSpecialty):
    """A specific branch of medical science that is concerned with the study, treatment, and"
     "prevention of mental illness, using both medical and psychological therapies.

    See https://schema.org/Psychiatric.

    """
    type_: str = Field("Psychiatric", const=True, alias='@type')
    

Psychiatric.update_forward_refs()
