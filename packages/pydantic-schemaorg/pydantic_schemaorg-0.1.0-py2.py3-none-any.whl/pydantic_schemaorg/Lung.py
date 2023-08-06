from pydantic import Field
from pydantic_schemaorg.PhysicalExam import PhysicalExam


class Lung(PhysicalExam):
    """Lung and respiratory system clinical examination.

    See https://schema.org/Lung.

    """
    type_: str = Field("Lung", const=True, alias='@type')
    

Lung.update_forward_refs()
