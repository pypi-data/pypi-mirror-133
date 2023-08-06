from pydantic import Field
from decimal import Decimal
from pydantic_schemaorg.QuantitativeValue import QuantitativeValue
from typing import List, Optional, Union
from pydantic_schemaorg.BedDetails import BedDetails
from pydantic_schemaorg.BedType import BedType
from pydantic_schemaorg.Accommodation import Accommodation


class Suite(Accommodation):
    """A suite in a hotel or other public accommodation, denotes a class of luxury accommodations,"
     "the key feature of which is multiple rooms (Source: Wikipedia, the free encyclopedia,"
     "see <a href=\"http://en.wikipedia.org/wiki/Suite_(hotel)\">http://en.wikipedia.org/wiki/Suite_(hotel)</a>)."
     "<br /><br /> See also the <a href=\"/docs/hotels.html\">dedicated document on the"
     "use of schema.org for marking up hotels and other forms of accommodations</a>.

    See https://schema.org/Suite.

    """
    type_: str = Field("Suite", const=True, alias='@type')
    numberOfRooms: Optional[Union[List[Union[Decimal, QuantitativeValue, str]], Union[Decimal, QuantitativeValue, str]]] = Field(
        None,
        description="The number of rooms (excluding bathrooms and closets) of the accommodation or lodging"
     "business. Typical unit code(s): ROM for room or C62 for no unit. The type of room can be"
     "put in the unitText property of the QuantitativeValue.",
    )
    bed: Optional[Union[List[Union[str, BedDetails, BedType]], Union[str, BedDetails, BedType]]] = Field(
        None,
        description="The type of bed or beds included in the accommodation. For the single case of just one bed"
     "of a certain type, you use bed directly with a text. If you want to indicate the quantity"
     "of a certain kind of bed, use an instance of BedDetails. For more detailed information,"
     "use the amenityFeature property.",
    )
    occupancy: Optional[Union[List[Union[QuantitativeValue, str]], Union[QuantitativeValue, str]]] = Field(
        None,
        description="The allowed total occupancy for the accommodation in persons (including infants etc)."
     "For individual accommodations, this is not necessarily the legal maximum but defines"
     "the permitted usage as per the contractual agreement (e.g. a double room used by a single"
     "person). Typical unit code(s): C62 for person",
    )
    

Suite.update_forward_refs()
