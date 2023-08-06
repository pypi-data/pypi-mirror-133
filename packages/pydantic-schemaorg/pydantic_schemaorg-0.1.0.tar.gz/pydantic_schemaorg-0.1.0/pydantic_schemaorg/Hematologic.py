from pydantic import Field
from pydantic_schemaorg.MedicalSpecialty import MedicalSpecialty


class Hematologic(MedicalSpecialty):
    """A specific branch of medical science that pertains to diagnosis and treatment of disorders"
     "of blood and blood producing organs.

    See https://schema.org/Hematologic.

    """
    type_: str = Field("Hematologic", const=True, alias='@type')
    

Hematologic.update_forward_refs()
