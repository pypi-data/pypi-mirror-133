from pydantic import Field
from pydantic_schemaorg.Reservation import Reservation
from typing import List, Optional, Union


class ReservationPackage(Reservation):
    """A group of multiple reservations with common values for all sub-reservations.

    See https://schema.org/ReservationPackage.

    """
    type_: str = Field("ReservationPackage", const=True, alias='@type')
    subReservation: Optional[Union[List[Union[Reservation, str]], Union[Reservation, str]]] = Field(
        None,
        description="The individual reservations included in the package. Typically a repeated property.",
    )
    

ReservationPackage.update_forward_refs()
