from pydantic import Field
from pydantic_schemaorg.PhysicalActivityCategory import PhysicalActivityCategory


class StrengthTraining(PhysicalActivityCategory):
    """Physical activity that is engaged in to improve muscle and bone strength. Also referred"
     "to as resistance training.

    See https://schema.org/StrengthTraining.

    """
    type_: str = Field("StrengthTraining", const=True, alias='@type')
    

StrengthTraining.update_forward_refs()
