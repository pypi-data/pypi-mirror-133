from pydantic import Field
from pydantic_schemaorg.BodyMeasurementTypeEnumeration import BodyMeasurementTypeEnumeration


class BodyMeasurementWaist(BodyMeasurementTypeEnumeration):
    """Girth of natural waistline (between hip bones and lower ribs). Used, for example, to"
     "fit pants.

    See https://schema.org/BodyMeasurementWaist.

    """
    type_: str = Field("BodyMeasurementWaist", const=True, alias='@type')
    

BodyMeasurementWaist.update_forward_refs()
