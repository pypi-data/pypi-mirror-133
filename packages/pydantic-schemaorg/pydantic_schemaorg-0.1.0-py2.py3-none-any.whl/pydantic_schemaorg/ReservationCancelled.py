from pydantic import Field
from pydantic_schemaorg.ReservationStatusType import ReservationStatusType


class ReservationCancelled(ReservationStatusType):
    """The status for a previously confirmed reservation that is now cancelled.

    See https://schema.org/ReservationCancelled.

    """
    type_: str = Field("ReservationCancelled", const=True, alias='@type')
    

ReservationCancelled.update_forward_refs()
