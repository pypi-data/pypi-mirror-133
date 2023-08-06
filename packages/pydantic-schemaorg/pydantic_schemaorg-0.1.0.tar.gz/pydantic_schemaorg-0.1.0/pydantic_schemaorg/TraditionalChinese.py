from pydantic import Field
from pydantic_schemaorg.MedicineSystem import MedicineSystem


class TraditionalChinese(MedicineSystem):
    """A system of medicine based on common theoretical concepts that originated in China and"
     "evolved over thousands of years, that uses herbs, acupuncture, exercise, massage,"
     "dietary therapy, and other methods to treat a wide range of conditions.

    See https://schema.org/TraditionalChinese.

    """
    type_: str = Field("TraditionalChinese", const=True, alias='@type')
    

TraditionalChinese.update_forward_refs()
