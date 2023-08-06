from typing import List, Optional, Union

from pydantic import Field

from pydantic_schemaorg.MedicalContraindication import MedicalContraindication
from pydantic_schemaorg.MedicalEntity import MedicalEntity
from pydantic_schemaorg.TherapeuticProcedure import TherapeuticProcedure


class MedicalTherapy(TherapeuticProcedure):
    """Any medical intervention designed to prevent, treat, and cure human diseases and medical"
     "conditions, including both curative and palliative therapies. Medical therapies"
     "are typically processes of care relying upon pharmacotherapy, behavioral therapy,"
     "supportive therapy (with fluid or nutrition for example), or detoxification (e.g."
     "hemodialysis) aimed at improving or preventing a health condition.

    See https://schema.org/MedicalTherapy.

    """
    type_: str = Field("MedicalTherapy", const=True, alias='@type')
    duplicateTherapy: Optional[Union[List[Union['MedicalTherapy', str]], Union['MedicalTherapy', str]]] = Field(
        None,
        description="A therapy that duplicates or overlaps this one.",
    )
    seriousAdverseOutcome: Optional[Union[List[Union[MedicalEntity, str]], Union[MedicalEntity, str]]] = Field(
        None,
        description="A possible serious complication and/or serious side effect of this therapy. Serious"
                    "adverse outcomes include those that are life-threatening; result in death, disability,"
                    "or permanent damage; require hospitalization or prolong existing hospitalization;"
                    "cause congenital anomalies or birth defects; or jeopardize the patient and may require"
                    "medical or surgical intervention to prevent one of the outcomes in this definition.",
    )
    contraindication: Optional[
        Union[List[Union[str, MedicalContraindication]], Union[str, MedicalContraindication]]] = Field(
        None,
        description="A contraindication for this therapy.",
    )


MedicalTherapy.update_forward_refs()
