from pydantic import Field
from pydantic_schemaorg.TherapeuticProcedure import TherapeuticProcedure


class PsychologicalTreatment(TherapeuticProcedure):
    """A process of care relying upon counseling, dialogue and communication aimed at improving"
     "a mental health condition without use of drugs.

    See https://schema.org/PsychologicalTreatment.

    """
    type_: str = Field("PsychologicalTreatment", const=True, alias='@type')
    

PsychologicalTreatment.update_forward_refs()
