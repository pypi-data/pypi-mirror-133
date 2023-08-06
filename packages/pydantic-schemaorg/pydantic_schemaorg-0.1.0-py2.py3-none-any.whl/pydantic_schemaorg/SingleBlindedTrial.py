from pydantic import Field
from pydantic_schemaorg.MedicalTrialDesign import MedicalTrialDesign


class SingleBlindedTrial(MedicalTrialDesign):
    """A trial design in which the researcher knows which treatment the patient was randomly"
     "assigned to but the patient does not.

    See https://schema.org/SingleBlindedTrial.

    """
    type_: str = Field("SingleBlindedTrial", const=True, alias='@type')
    

SingleBlindedTrial.update_forward_refs()
