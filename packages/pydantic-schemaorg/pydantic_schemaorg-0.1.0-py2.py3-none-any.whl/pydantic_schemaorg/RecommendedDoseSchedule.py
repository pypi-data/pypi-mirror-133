from pydantic import Field
from pydantic_schemaorg.DoseSchedule import DoseSchedule


class RecommendedDoseSchedule(DoseSchedule):
    """A recommended dosing schedule for a drug or supplement as prescribed or recommended"
     "by an authority or by the drug/supplement's manufacturer. Capture the recommending"
     "authority in the recognizingAuthority property of MedicalEntity.

    See https://schema.org/RecommendedDoseSchedule.

    """
    type_: str = Field("RecommendedDoseSchedule", const=True, alias='@type')
    

RecommendedDoseSchedule.update_forward_refs()
